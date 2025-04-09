# llama-backup

[![PyPI version](https://img.shields.io/pypi/v/llama_backup.svg)](https://pypi.org/project/llama_backup/)
[![License](https://img.shields.io/github/license/llamasearchai/llama-backup)](https://github.com/llamasearchai/llama-backup/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/llama_backup.svg)](https://pypi.org/project/llama_backup/)
[![CI Status](https://github.com/llamasearchai/llama-backup/actions/workflows/llamasearchai_ci.yml/badge.svg)](https://github.com/llamasearchai/llama-backup/actions/workflows/llamasearchai_ci.yml)

**Llama Backup (llama-backup)** is a utility within the LlamaSearch AI ecosystem designed for creating and managing backups. It likely handles backing up data to various storage backends with considerations for security like encryption.

## Key Features

- **Backup Management:** Core logic for creating, restoring, and managing backups (`core.py`, `main.py`).
- **Storage Backends:** Interfaces with different storage solutions (e.g., local disk, cloud storage) (`storage.py`).
- **Security Features:** Includes mechanisms for encryption and secure handling of backup data (`security.py`).
- **Command-Line Interface:** Provides CLI tools for initiating and managing backups (`cli.py`).
- **Configurable:** Allows specifying backup sources, destinations, schedules (potentially via integration), encryption keys, etc. (`config.py`).

## Installation

```bash
pip install llama-backup
# Or install directly from GitHub for the latest version:
# pip install git+https://github.com/llamasearchai/llama-backup.git
```

## Usage

### Command-Line Interface (CLI)

*(CLI usage examples for creating, listing, and restoring backups will be added here.)*

```bash
llama-backup create --source /path/to/data --destination s3://my-bucket/backups --encrypt
llama-backup list
llama-backup restore --backup-id <backup_id> --target /path/to/restore
```

### Python Client / Embedding

*(Python usage examples for programmatically managing backups will be added here.)*

```python
# Placeholder for Python client usage
# from llama_backup import BackupManager, BackupConfig

# config = BackupConfig.load("config.yaml")
# manager = BackupManager(config)

# # Create a backup
# backup_job = manager.create_backup(
#     source_path="/important/data",
#     options={'encryption_key': 'supersecret'}
# )
# print(f"Backup started: {backup_job.id}")

# # List backups
# backups = manager.list_backups()
# for b in backups:
#     print(f"ID: {b.id}, Timestamp: {b.timestamp}, Status: {b.status}")
```

## Architecture Overview

```mermaid
graph TD
    A[User / CLI (cli.py)] --> B{Core Backup Manager (core.py, main.py)};
    B -- Backup/Restore Request --> C{Storage Interface (storage.py)};
    C -- Read/Write --> D[(Storage Backend (Local, S3, etc.))];
    B -- Encryption/Decryption --> E{Security Module (security.py)};
    E -- Uses Keys --> F[(Key Store / Secrets Manager)];

    G[Configuration (config.py)] -- Configures --> B;
    G -- Configures --> C;
    G -- Configures --> E;

    style B fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#ccf,stroke:#333,stroke-width:1px
    style F fill:#ccf,stroke:#333,stroke-width:1px
```

1.  **Interface:** Users interact via the CLI or potentially a programmatic API.
2.  **Core Manager:** Orchestrates the backup or restore process based on configuration.
3.  **Storage Interface:** Handles communication with the chosen storage backend (local, cloud, etc.).
4.  **Security Module:** Manages encryption/decryption of backup data, potentially using external key management.
5.  **Configuration:** Defines source data, destination storage, encryption settings, etc.

## Configuration

*(Details on configuring backup sources, storage destinations (S3 buckets, local paths), encryption methods, keys, potential scheduling options, etc., will be added here.)*

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/llamasearchai/llama-backup.git
cd llama-backup

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

### Testing

```bash
pytest tests/
```

### Contributing

Contributions are welcome! Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) and submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
