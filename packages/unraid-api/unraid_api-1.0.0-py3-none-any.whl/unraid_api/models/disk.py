"""Disk data models for unraid_api."""
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class DiskFsType(str, Enum):
    """Enum for disk filesystem types."""

    XFS = "xfs"
    BTRFS = "btrfs"
    VFAT = "vfat"
    ZFS = "zfs"


class DiskPartition(BaseModel):
    """Model for a disk partition."""

    number: int = Field(..., description="The partition number")
    name: str = Field(..., description="The partition name")
    fs_type: Optional[DiskFsType] = Field(None, alias="fsType", description="The filesystem type (xfs, btrfs, vfat, zfs)")
    mountpoint: Optional[str] = Field(None, description="The mount point")
    size: int = Field(..., description="The size of the partition in bytes")
    used: Optional[int] = Field(None, description="The used space in bytes")
    free: Optional[int] = Field(None, description="The free space in bytes")
    color: Optional[str] = Field(None, description="The color code for the partition")
    temp: Optional[int] = Field(None, description="The temperature of the partition in celsius")
    device_id: str = Field(..., alias="deviceId", description="The device identifier")
    is_array: bool = Field(..., alias="isArray", description="Whether the partition is part of the array")

    class Config:
        """Pydantic config."""

        populate_by_name = True


class SmartAttribute(BaseModel):
    """Model for a SMART attribute."""

    id: int = Field(..., description="The attribute ID")
    name: str = Field(..., description="The attribute name")
    value: int = Field(..., description="The attribute value")
    worst: int = Field(..., description="The worst value")
    threshold: int = Field(..., description="The threshold value")
    raw: str = Field(..., description="The raw value")
    status: str = Field(..., description="The attribute status")

    class Config:
        """Pydantic config."""

        populate_by_name = True


class SmartData(BaseModel):
    """Model for SMART data."""

    supported: bool = Field(..., description="Whether SMART is supported")
    enabled: bool = Field(..., description="Whether SMART is enabled")
    status: str = Field(..., description="The SMART status")
    temperature: Optional[int] = Field(None, description="The temperature in celsius")
    attributes: List[SmartAttribute] = Field(default_factory=list, description="The SMART attributes")

    class Config:
        """Pydantic config."""

        populate_by_name = True


class Disk(BaseModel):
    """Model for a disk."""

    id: str = Field(..., description="The disk ID")
    device: str = Field(..., description="The device path (e.g., '/dev/sda')")
    device_id: str = Field(..., alias="deviceId", description="The device identifier")
    device_node: str = Field(..., alias="deviceNode", description="The device node")
    name: str = Field(..., description="The disk name")
    partitions: List[DiskPartition] = Field(default_factory=list, description="The partitions on the disk")
    size: int = Field(..., description="The size of the disk in bytes")
    temp: Optional[int] = Field(None, description="The temperature of the disk in celsius")
    status: str = Field(..., description="The status of the disk")
    interface: Optional[str] = Field(None, description="The disk interface")
    model: Optional[str] = Field(None, description="The disk model")
    protocol: Optional[str] = Field(None, description="The disk protocol")
    rotation_rate: Optional[int] = Field(None, alias="rotationRate", description="The disk rotation rate in RPM")
    serial: Optional[str] = Field(None, description="The disk serial number")
    type: str = Field(..., description="The disk type")
    num_reads: int = Field(..., alias="numReads", description="Number of read operations")
    num_writes: int = Field(..., alias="numWrites", description="Number of write operations")
    num_errors: int = Field(..., alias="numErrors", description="Number of errors")
    color: Optional[str] = Field(None, description="The color code for the disk")
    rotational: bool = Field(..., description="Whether the disk is rotational (HDD vs SSD)")
    vendor: Optional[str] = Field(None, description="The disk vendor")
    spindown_status: Optional[str] = Field(None, alias="spindownStatus", description="The spindown status of the disk")
    last_spindown_time: Optional[int] = Field(None, alias="lastSpindownTime", description="The last spindown time of the disk")
    smart: Optional[SmartData] = Field(None, description="The SMART data for the disk")

    class Config:
        """Pydantic config."""

        populate_by_name = True
