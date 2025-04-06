"""Array data models for unraid_api."""
from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field

from .disk import DiskFsType


class PoolDevice(BaseModel):
    """Model for a device in a cache pool."""

    id: str = Field(..., description="The device ID")
    device: str = Field(..., description="The device path (e.g., '/dev/sda')")
    name: str = Field(..., description="The device name")
    size: int = Field(..., description="The size of the device in bytes")
    status: str = Field(..., description="The status of the device")

    class Config:
        """Pydantic config."""

        populate_by_name = True


class CachePool(BaseModel):
    """Model for a cache pool."""

    name: str = Field(..., description="The name of the pool")
    size: int = Field(..., description="The size of the pool in bytes")
    free: int = Field(..., description="The free space in bytes")
    used: int = Field(..., description="The used space in bytes")
    devices: List[PoolDevice] = Field(default_factory=list, description="The devices in the pool")

    class Config:
        """Pydantic config."""

        populate_by_name = True


class ArrayDevice(BaseModel):
    """Model for a disk in the array."""

    name: str = Field(..., description="The name of the disk (e.g., 'disk1')")
    device: str = Field(..., description="The device path (e.g., '/dev/sda')")
    id: str = Field(..., description="The disk ID")
    size: int = Field(..., description="The size of the disk in bytes")
    temp: Optional[int] = Field(None, description="The temperature of the disk in celsius")
    num_reads: int = Field(..., alias="numReads", description="Number of read operations")
    num_writes: int = Field(..., alias="numWrites", description="Number of write operations")
    num_errors: int = Field(..., alias="numErrors", description="Number of errors")
    status: str = Field(..., description="The status of the disk")
    device_id: str = Field(..., alias="deviceId", description="The device identifier")
    fs_type: Optional[DiskFsType] = Field(None, alias="fsType", description="The filesystem type (xfs, btrfs, vfat, zfs)")
    spindown_status: Optional[str] = Field(None, alias="spindownStatus", description="The spindown status of the disk")
    last_spindown_time: Optional[int] = Field(None, alias="lastSpindownTime", description="The last spindown time of the disk")

    class Config:
        """Pydantic config."""

        populate_by_name = True


class BootDevice(BaseModel):
    """Model for the boot device."""

    id: str = Field(..., description="The device ID")
    device: str = Field(..., description="The device path (e.g., '/dev/sda')")
    name: str = Field(..., description="The device name")
    size: int = Field(..., description="The size of the device in bytes")
    status: str = Field(..., description="The status of the device")
    type: str = Field(..., description="The type of the device")

    class Config:
        """Pydantic config."""

        populate_by_name = True


class ArrayStatus(BaseModel):
    """Model for the array status."""

    name: str = Field(..., description="The name of the array")
    started: bool = Field(..., description="Whether the array is started")
    size: int = Field(..., description="The total size of the array in bytes")
    used: int = Field(..., description="The used space in bytes")
    free: int = Field(..., description="The free space in bytes")
    boot: Optional[BootDevice] = Field(None, description="The boot device")
    devices: List[ArrayDevice] = Field(..., description="The disks in the array")
    caches: List[ArrayDevice] = Field(default_factory=list, description="The cache disks in the array")
    pools: List[CachePool] = Field(default_factory=list, description="The cache pools in the array")
    md_resync_errs: int = Field(0, alias="mdResyncErrs", description="Number of resync errors")
    md_resync_action: Optional[str] = Field(None, alias="mdResyncAction", description="Current resync action")
    md_resync_pos: Optional[int] = Field(None, alias="mdResyncPos", description="Current resync position")
    md_resync_size: Optional[int] = Field(None, alias="mdResyncSize", description="Total resync size")
    md_resync_dt: Optional[str] = Field(None, alias="mdResyncDt", description="Resync date/time")
    protected: bool = Field(..., description="Whether the array is protected")
    status: str = Field(..., description="The status of the array")

    class Config:
        """Pydantic config."""

        populate_by_name = True


class ParityHistoryItem(BaseModel):
    """Model for a parity check history item."""

    duration: int = Field(..., description="Duration of the parity check in seconds")
    speed: int = Field(..., description="Speed of the parity check in bytes per second")
    status: str = Field(..., description="Status of the parity check")
    errors: int = Field(..., description="Number of errors found")
    date: datetime = Field(..., description="Date and time of the parity check")
    corrected: bool = Field(..., description="Whether errors were corrected")

    class Config:
        """Pydantic config."""

        populate_by_name = True


class MutationResponse(BaseModel):
    """Model for a mutation response."""

    success: bool = Field(..., description="Whether the mutation was successful")
    message: Optional[str] = Field(None, description="Any message from the server")

    class Config:
        """Pydantic config."""

        populate_by_name = True
