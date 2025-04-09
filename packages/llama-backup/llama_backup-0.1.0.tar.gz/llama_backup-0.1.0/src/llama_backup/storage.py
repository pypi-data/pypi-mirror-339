"""
Storage backend implementations for llama_backup.

This module provides the abstract StorageBackend class and concrete implementations
like FileSystemStorage.
"""

import json
import logging
import shutil
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass

# Import from missing file commented out
# from .backup import BackupMetadata, RetentionPolicy, StorageTier


# Dummy placeholders for missing imports from .backup
class StorageTier(Enum):
    HOT = "hot"
    COLD = "cold"
    ARCHIVE = "archive"


class RetentionPolicy(Enum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"


@dataclass
class BackupMetadata:
    chunk_id: str
    source_path: str
    created_at: datetime
    hash: str
    size_bytes: int
    storage_tier: StorageTier = StorageTier.HOT
    retention_policy: RetentionPolicy = RetentionPolicy.MEDIUM
    encryption_used: bool = False
    expires_at: Optional[datetime] = None
    tags: Optional[List[str]] = None
    # Add other fields as needed based on usage in this file


# Configure logging
logger = logging.getLogger("llama_backup.storage")


class StorageBackend(ABC):
    """Abstract base class for storage backends."""

    @abstractmethod
    def save_chunk(self, chunk_id: str, data: bytes, metadata: BackupMetadata) -> bool:
        """Save chunk data to storage."""
        pass

    @abstractmethod
    def get_chunk(self, chunk_id: str) -> Tuple[bytes, BackupMetadata]:
        """Retrieve chunk data from storage."""
        pass

    @abstractmethod
    def delete_chunk(self, chunk_id: str) -> bool:
        """Delete chunk from storage."""
        pass

    @abstractmethod
    def list_chunks(self, prefix: Optional[str] = None) -> List[str]:
        """List available chunks."""
        pass

    @abstractmethod
    def migrate_chunk(self, chunk_id: str, new_tier: StorageTier) -> bool:
        """Migrate chunk to a different storage tier."""
        pass


class FileSystemStorage(StorageBackend):
    """Storage backend that uses the local filesystem."""

    def __init__(self, base_path: str):
        """Initialize with the base storage path.

        Args:
            base_path: The base directory to store backup chunks
        """
        self.base_path = Path(base_path)
        self.metadata_path = self.base_path / "metadata"
        self.chunks_path = self.base_path / "chunks"

        # Create required directories
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.chunks_path.mkdir(parents=True, exist_ok=True)

        # Create tier directories
        for tier in StorageTier:
            (self.chunks_path / tier.value).mkdir(exist_ok=True)

    def save_chunk(self, chunk_id: str, data: bytes, metadata: BackupMetadata) -> bool:
        """Save a chunk to the filesystem.

        Args:
            chunk_id: Unique identifier for the chunk
            data: Binary data to save
            metadata: Metadata associated with the chunk

        Returns:
            bool: True if saved successfully
        """
        # Save chunk data
        chunk_path = self.chunks_path / metadata.storage_tier.value / chunk_id
        try:
            with open(chunk_path, "wb") as f:
                f.write(data)

            # Save metadata
            metadata_path = self.metadata_path / f"{chunk_id}.json"
            with open(metadata_path, "w") as f:
                # Convert dataclass to dict, handling datetime and enums
                meta_dict = {
                    k: (
                        v.isoformat()
                        if isinstance(v, datetime)
                        else (
                            v.value
                            if isinstance(v, StorageTier) or isinstance(v, RetentionPolicy)
                            else v
                        )
                    )
                    for k, v in metadata.__dict__.items()
                }
                json.dump(meta_dict, f, indent=2)

            return True
        except Exception as e:
            logger.error(f"Failed to save chunk {chunk_id}: {str(e)}")
            return False

    def get_chunk(self, chunk_id: str) -> Tuple[bytes, BackupMetadata]:
        """Retrieve a chunk from the filesystem.

        Args:
            chunk_id: ID of the chunk to retrieve

        Returns:
            Tuple containing the chunk data and metadata

        Raises:
            FileNotFoundError: If the chunk doesn't exist
        """
        # Find the chunk by checking all tier directories
        chunk_path = None
        for tier in StorageTier:
            temp_path = self.chunks_path / tier.value / chunk_id
            if temp_path.exists():
                chunk_path = temp_path
                break

        if not chunk_path:
            raise FileNotFoundError(f"Chunk {chunk_id} not found in any storage tier")

        # Read chunk data
        with open(chunk_path, "rb") as f:
            data = f.read()

        # Read metadata
        metadata_path = self.metadata_path / f"{chunk_id}.json"
        with open(metadata_path, "r") as f:
            meta_dict = json.load(f)

        # Convert dict back to BackupMetadata
        # Handle special types like datetime and enums
        meta_dict["created_at"] = datetime.fromisoformat(meta_dict["created_at"])
        if meta_dict.get("expires_at"):
            meta_dict["expires_at"] = datetime.fromisoformat(meta_dict["expires_at"])
        meta_dict["storage_tier"] = StorageTier(meta_dict["storage_tier"])
        meta_dict["retention_policy"] = RetentionPolicy(meta_dict["retention_policy"])

        metadata = BackupMetadata(**meta_dict)
        return data, metadata

    def delete_chunk(self, chunk_id: str) -> bool:
        """Delete a chunk from storage.

        Args:
            chunk_id: ID of the chunk to delete

        Returns:
            bool: True if deleted successfully
        """
        try:
            # Find and delete the chunk
            for tier in StorageTier:
                chunk_path = self.chunks_path / tier.value / chunk_id
                if chunk_path.exists():
                    chunk_path.unlink()
                    break

            # Delete metadata
            metadata_path = self.metadata_path / f"{chunk_id}.json"
            if metadata_path.exists():
                metadata_path.unlink()

            return True
        except Exception as e:
            logger.error(f"Failed to delete chunk {chunk_id}: {str(e)}")
            return False

    def list_chunks(self, prefix: Optional[str] = None) -> List[str]:
        """List all available chunks, optionally filtered by prefix.

        Args:
            prefix: Optional prefix to filter chunks

        Returns:
            List of chunk IDs
        """
        chunks = []
        for tier in StorageTier:
            tier_path = self.chunks_path / tier.value
            for chunk_file in tier_path.glob("*"):
                if not prefix or chunk_file.name.startswith(prefix):
                    chunks.append(chunk_file.name)
        return chunks

    def migrate_chunk(self, chunk_id: str, new_tier: StorageTier) -> bool:
        """Migrate a chunk to a new storage tier.

        Args:
            chunk_id: ID of the chunk to migrate
            new_tier: Target storage tier

        Returns:
            bool: True if migrated successfully
        """
        try:
            # Find the chunk
            current_path = None
            current_tier = None
            for tier in StorageTier:
                test_path = self.chunks_path / tier.value / chunk_id
                if test_path.exists():
                    current_path = test_path
                    current_tier = tier
                    break

            if not current_path:
                logger.error(f"Chunk {chunk_id} not found for migration")
                return False

            if current_tier == new_tier:
                logger.info(f"Chunk {chunk_id} already in tier {new_tier.value}")
                return True

            # Move the chunk to the new tier
            target_path = self.chunks_path / new_tier.value / chunk_id
            shutil.move(str(current_path), str(target_path))

            # Update metadata
            metadata_path = self.metadata_path / f"{chunk_id}.json"
            with open(metadata_path, "r") as f:
                meta_dict = json.load(f)

            meta_dict["storage_tier"] = new_tier.value

            with open(metadata_path, "w") as f:
                json.dump(meta_dict, f, indent=2)

            return True
        except Exception as e:
            logger.error(f"Failed to migrate chunk {chunk_id}: {str(e)}")
            return False
