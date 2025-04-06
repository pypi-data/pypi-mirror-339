"""NOAA GFS (Global Forecast System) Data Downloader

This module provides functionality to download specific elements from NOAA's GFS
(Global Forecast System) data stored in public S3 buckets. It supports efficient
partial downloads by using idx files to locate and download only the required
data elements.

Key Features:
    - Selective download of specific variables and levels
    - Efficient byte-range requests for partial file downloads
    - Performance monitoring and logging
    - Object-oriented idx file parsing and querying
    - Type-safe data structures using dataclasses

Example:
    >>> from hinox.utils.collector.gfs import download_gfs_data
    >>> elements = [
    ...     {"name": "TMP", "level": "2 m above ground"},
    ...     {"name": "UGRD", "level": "10 m above ground"}
    ... ]
    >>> result = download_gfs_data(
    ...     date_str="20250326",
    ...     cycle_str="00",
    ...     forecast_hour="000",
    ...     elements=elements,
    ...     output_path="gfs_data.grib2"
    ... )
    >>> if result.success:
    ...     print(f"Downloaded {result.file_size_mb:.2f}MB")

Notes:
    - GFS data is available from NOAA's public S3 bucket: noaa-gfs-bdp-pds
    - Data updates can be monitored via SNS: arn:aws:sns:us-east-1:123901341784:NewGFSObject
    - File naming format: gfs.YYYYMMDD/HH/atmos/gfs.tHHz.pgrb2.0p25.fHHH
    - Supported forecast cycles: 00, 06, 12, 18
    - Forecast hours range: 000-384
"""

import os
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple

import boto3
from botocore import UNSIGNED
from botocore.config import Config
from loguru import logger


@dataclass
class GFSDownloadResult:
    """Result of GFS data download operation

    Attributes:
        success (bool): Whether the download was successful
        date (str): The date of the GFS data in format "YYYYMMDD"
        cycle (str): The cycle hour in format "HH"
        forecast_hour (int): The forecast hour (0-384)
        elements (List[Dict]): List of downloaded elements with their levels
        file_format (str): Format of the downloaded file, defaults to "grib2"
        file_path (Optional[str]): Path where the file was saved
        file_size_mb (Optional[float]): Size of the downloaded file in MB
        download_time_s (Optional[float]): Total download time in seconds
        download_speed_mbs (Optional[float]): Average download speed in MB/s
        error_message (Optional[str]): Error message if download failed
    """

    success: bool
    date: str
    cycle: str
    forecast_hour: int
    elements: List[Dict]
    file_format: str = "grib2"
    file_path: Optional[str] = None
    file_size_mb: Optional[float] = None
    download_time_s: Optional[float] = None
    download_speed_mbs: Optional[float] = None
    error_message: Optional[str] = None


@dataclass
class GribElement:
    """Represents a single element in a GRIB2 file

    Attributes:
        variable (str): Variable name (e.g., "TMP", "UGRD")
        level (str): Level description (e.g., "2 m above ground")
        start_byte (int): Start byte position in the grib2 file
        end_byte (int): End byte position in the grib2 file
    """

    variable: str
    level: str
    start_byte: int
    end_byte: int


class GribIdx:
    """Parser and query interface for GRIB2 idx files

    This class provides functionality to parse GRIB2 idx files and query specific
    elements within them. It maintains an internal mapping of variables and levels
    to their byte ranges in the corresponding GRIB2 file.

    Attributes:
        elements (List[GribElement]): List of all elements found in the idx file
    """

    def __init__(self, idx_content: str):
        """Initialize GribIdx with idx file content

        Args:
            idx_content (str): Content of the idx file as string
        """
        self.elements = self._parse_idx_content(idx_content)

    def _parse_idx_content(self, idx_content: str) -> List[GribElement]:
        """Parse idx file content into GribElement objects

        Args:
            idx_content (str): Content of the idx file

        Returns:
            List[GribElement]: List of parsed elements
        """
        elements = []
        lines = idx_content.split("\n")

        for i, line in enumerate(lines):
            if not line.strip():
                continue

            parts = line.strip().split(":")
            if len(parts) >= 6:
                start_byte = int(parts[1])
                variable = parts[3]
                level = parts[4]

                # Get end byte from next line
                end_byte = None
                if i < len(lines) - 1:
                    next_line = lines[i + 1]
                    if next_line.strip():
                        next_parts = next_line.strip().split(":")
                        if len(next_parts) >= 2:
                            end_byte = int(next_parts[1])

                if end_byte is not None:
                    elements.append(
                        GribElement(
                            variable=variable,
                            level=level,
                            start_byte=start_byte,
                            end_byte=end_byte,
                        )
                    )

        return elements

    def find_elements(self, target_elements: List[Dict]) -> List[GribElement]:
        """Find specified elements in the idx file

        Args:
            target_elements (List[Dict]): List of elements to find, each containing:
                - name (str): Variable name to find
                - level (str): Level description to find

        Returns:
            List[GribElement]: List of matched elements with their byte ranges

        Example:
            >>> idx = GribIdx(idx_content)
            >>> elements = idx.find_elements([
            ...     {"name": "TMP", "level": "2 m above ground"}
            ... ])
            >>> print(elements[0].variable)
            'TMP'
        """
        result = []
        for target in target_elements:
            for elem in self.elements:
                if elem.variable == target["name"] and elem.level == target["level"]:
                    logger.info(f"Found match: {elem.variable} @ {elem.level}")
                    result.append(elem)
        return result

    def get_byte_ranges(self, target_elements: List[Dict]) -> List[Tuple[int, int]]:
        """Get byte ranges for specified elements

        Args:
            target_elements (List[Dict]): List of elements to find

        Returns:
            List[Tuple[int, int]]: List of (start_byte, end_byte) tuples
        """
        elements = self.find_elements(target_elements)
        return [(elem.start_byte, elem.end_byte) for elem in elements]


def download_bytes(
    s3_client,
    bucket: str,
    key: str,
    start_byte: int,
    end_byte: int,
    quiet: bool = False,
) -> bytes:
    """Download data for specified byte range from S3

    This function downloads a specific byte range from an S3 object and logs the
    download performance metrics including size, time, and speed.

    Args:
        s3_client: Boto3 S3 client instance
        bucket (str): S3 bucket name
        key (str): S3 object key (path to the file in the bucket)
        start_byte (int): Starting byte position (inclusive)
        end_byte (int): Ending byte position (exclusive)
        quiet (bool, optional): If True, suppress all log output. Defaults to False

    Returns:
        bytes: The downloaded data within the specified byte range

    Raises:
        botocore.exceptions.ClientError: If there's an error accessing the S3 object
        ValueError: If start_byte is greater than or equal to end_byte
    """
    chunk_size = end_byte - start_byte
    start_time = time.time()

    response = s3_client.get_object(
        Bucket=bucket, Key=key, Range=f"bytes={start_byte}-{end_byte - 1}"
    )
    data = response["Body"].read()

    end_time = time.time()
    duration = end_time - start_time
    speed_mbps = (chunk_size / 1024 / 1024) / duration if duration > 0 else 0

    if not quiet:
        logger.info(
            f"Download completed: {chunk_size / 1024 / 1024:.2f}MB, Time: {duration:.2f}s, Speed: {speed_mbps:.2f}MB/s"
        )

    return data


def download_gfs_data(
    init_dt: datetime,
    forecast_hour: int,
    elements: List[Dict],
    output_path: str,
    bucket: str = "noaa-gfs-bdp-pds",
    region: str = "us-east-1",
    quiet: bool = False,
) -> GFSDownloadResult:
    """Download GFS data for specified time and elements

    This function downloads selected elements from NOAA's GFS (Global Forecast System)
    data stored in a public S3 bucket. It first downloads an idx file to locate the
    byte ranges for requested elements, then downloads only the needed parts of the
    grib2 file. The function supports partial downloads of specific variables at
    specific levels, making it efficient for cases where only certain elements are needed.

    Args:
        init_dt (datetime): Datetime object for the initialization time (model start time)
        forecast_hour (int): Forecast hour (0-384)
        elements (List[Dict]): List of elements to download, each containing:
            - name (str): Variable name (e.g., "TMP", "UGRD")
            - level (str): Level description (e.g., "2 m above ground")
        output_path (str): Path where to save the downloaded grib2 file
        bucket (str, optional): S3 bucket name. Defaults to 'noaa-gfs-bdp-pds'
        region (str, optional): AWS region. Defaults to 'us-east-1'
        quiet (bool, optional): If True, suppress all log output. Defaults to False

    Returns:
        GFSDownloadResult: Download result containing success status and metadata
    """
    total_start_time = time.time()
    total_bytes = 0

    # Ensure datetime has timezone information
    if init_dt.tzinfo is None:
        init_dt = init_dt.replace(tzinfo=timezone.utc)
    else:
        # Convert to UTC for consistency
        init_dt = init_dt.astimezone(timezone.utc)

    # Extract date and cycle from datetime
    date_str = init_dt.strftime("%Y%m%d")
    cycle_str = init_dt.strftime("%H")

    result = GFSDownloadResult(
        success=False,
        date=date_str,
        cycle=cycle_str,
        forecast_hour=forecast_hour,
        elements=elements,
        file_path=output_path,
    )

    try:
        # Build file path
        grib_key = f"gfs.{date_str}/{cycle_str}/atmos/gfs.t{cycle_str}z.pgrb2.0p25.f{forecast_hour:03d}"
        idx_key = f"{grib_key}.idx"

        # Create S3 client with anonymous access
        s3_client = boto3.client(
            "s3",
            region_name=region,
            config=Config(signature_version=UNSIGNED, s3={"addressing_style": "path"}),
        )

        # Download and parse idx file
        if not quiet:
            logger.info(f"Downloading idx file: {idx_key}")
        response = s3_client.get_object(Bucket=bucket, Key=idx_key)
        idx_content = response["Body"].read().decode("utf-8")

        # Parse idx file and find elements
        grib_idx = GribIdx(idx_content)
        selected_elements = grib_idx.find_elements(elements)

        if not selected_elements:
            result.error_message = f"Specified elements not found: {elements}"
            if not quiet:
                logger.warning(result.error_message)
            return result

        # Get the byte ranges for all elements
        byte_ranges = grib_idx.get_byte_ranges(elements)

        # Sort byte ranges to ensure we download in order
        byte_ranges.sort(key=lambda x: x[0])

        # Merge overlapping ranges
        merged_ranges = []
        current_start, current_end = byte_ranges[0]

        for start, end in byte_ranges[1:]:
            if start <= current_end:
                current_end = max(current_end, end)
            else:
                merged_ranges.append((current_start, current_end))
                current_start, current_end = start, end
        merged_ranges.append((current_start, current_end))

        # Download and merge data
        if not quiet:
            logger.info(f"Starting data download: {grib_key}")
        merged_data = bytearray()

        for start_byte, end_byte in merged_ranges:
            if not quiet:
                logger.info(f"Downloading bytes {start_byte} to {end_byte}")
            chunk = download_bytes(
                s3_client, bucket, grib_key, start_byte, end_byte, quiet=quiet
            )
            merged_data.extend(chunk)
            total_bytes += len(chunk)

        # Save data
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
        except FileNotFoundError:
            pass

        with open(output_path, "wb") as f:
            f.write(merged_data)

        total_time = time.time() - total_start_time
        avg_speed_mbps = (
            (total_bytes / 1024 / 1024) / total_time if total_time > 0 else 0
        )

        # Update result with success and metadata
        result.success = True
        result.file_size_mb = total_bytes / 1024 / 1024
        result.download_time_s = total_time
        result.download_speed_mbs = avg_speed_mbps

        if not quiet:
            logger.success(
                f"Data saved to: {output_path}, Total size: {result.file_size_mb:.2f}MB, "
                f"Total time: {result.download_time_s:.2f}s, "
                f"Average speed: {result.download_speed_mbs:.2f}MB/s"
            )
        return result

    except Exception as e:
        error_msg = f"Error downloading data: {str(e)}"
        result.error_message = error_msg
        if not quiet:
            logger.error(error_msg)
        return result


if __name__ == "__main__":
    # Example usage
    elements = [
        {"name": "TMP", "level": "2 m above ground"},
        {"name": "UGRD", "level": "10 m above ground"},
        {"name": "VGRD", "level": "10 m above ground"},
    ]

    # Get previous day's UTC time
    utc_now = datetime.now(timezone.utc) - timedelta(days=1)
    # Set time to 00:00 UTC
    init_time = datetime(
        utc_now.year, utc_now.month, utc_now.day, 0, 0, tzinfo=timezone.utc
    )

    # Use fixed forecast hour
    forecast_hour = 3
    quiet = False  # 设置是否静默输出

    output_path = f"data/gfs_{init_time.strftime('%Y%m%d')}_{init_time.strftime('%H')}_{forecast_hour:03d}.grib2"
    if not quiet:
        logger.info(
            f"Starting GFS data download: {init_time.strftime('%Y%m%d')}_{init_time.strftime('%H')}z"
        )
    result = download_gfs_data(
        init_dt=init_time,
        forecast_hour=forecast_hour,
        elements=elements,
        output_path=output_path,
        quiet=quiet,
    )

    if not quiet:
        if result.success:
            logger.success(
                f"Download successful! File size: {result.file_size_mb:.2f}MB"
            )
        else:
            logger.error(f"Download failed: {result.error_message}")
