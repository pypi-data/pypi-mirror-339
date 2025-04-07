import os
import tempfile
import zipfile
from typing import List, Optional

import yaml


def load_config(key: Optional[str] = None, default: Optional[str] = None):
    config_dir = ".omega"
    config_file = os.path.join(config_dir, "config.yaml")

    # Default values
    config = {"platform_url": "https://platform.omegacloud.ai"}

    try:
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                data = yaml.safe_load(f)
                if data:
                    config.update(data)

    except (FileNotFoundError, yaml.YAMLError, OSError):
        pass

    if key:
        return config.get(key, default)
    else:
        return config


def save_config(config: dict):
    config_dir = ".omega"
    config_file = os.path.join(config_dir, "config.yaml")

    # Ensure directory exists
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        # Create .gitignore file in the config directory
        with open(os.path.join(config_dir, ".gitignore"), "w") as f:
            f.write("*\n")

    cfg = load_config()
    cfg.update(config)

    with open(config_file, "w") as f:
        yaml.dump(cfg, f)


def save_script(filename: str, content: List[str] = []):
    """Write content to a shell script file with proper permissions."""
    config_dir = ".omega"
    filepath = os.path.join(config_dir, filename)
    with open(filepath, "w") as f:
        f.write("#!/bin/bash\n\n")
        f.writelines(content)
    os.chmod(filepath, 0o755)  # Make the script executable


def load_script(filename: str) -> List[str]:
    config_dir = ".omega"
    filepath = os.path.join(config_dir, filename)
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r") as f:
            all_lines = f.readlines()
    except Exception as e:
        print(f"Error loading script {filename}: {e}")
        return []

    # Filter out empty lines and comments, strip whitespace
    lines = []
    for line in all_lines:
        line = line.strip()
        if line and not line.startswith("#"):
            lines.append(line)

    return lines


def create_zip_archive(
    include_paths: Optional[List[str]] = None,
    exclude_paths: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    archive_name: Optional[str] = None,
) -> str:
    """Create a zip archive with specified inclusion/exclusion rules.

    Args:
        include_paths: List of paths to include (if None, include everything)
        exclude_paths: List of paths to exclude
        exclude_patterns: List of glob patterns to exclude
        archive_name: Name of the archive (if None, a temporary name is generated)

    Returns:
        Path to the created zip archive
    """
    exclude_paths = exclude_paths or []
    exclude_patterns = exclude_patterns or [".git", ".venv"]

    if archive_name:
        zip_path = os.path.join(tempfile.gettempdir(), archive_name)
    else:
        tmp = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
        zip_path = tmp.name
        tmp.close()

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("."):
            # Skip excluded directories
            dirs[:] = [
                d
                for d in dirs
                if d not in exclude_patterns and os.path.join(root, d) not in exclude_paths
            ]

            # If include_paths is specified, only process those paths
            if include_paths and not any(
                root.startswith(f".{os.sep}{path}") or root == f".{os.sep}{path}"
                for path in include_paths
            ):
                continue

            # Skip excluded paths
            if any(root.startswith(f".{os.sep}{path}") for path in exclude_paths):
                continue

            for file in files:
                # Skip files matching exclude patterns
                if any(pattern in file for pattern in exclude_patterns):
                    continue

                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, ".")
                zipf.write(file_path, arcname)

    return zip_path
