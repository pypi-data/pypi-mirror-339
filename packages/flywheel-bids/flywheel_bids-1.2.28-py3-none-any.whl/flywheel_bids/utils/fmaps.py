"""Utility functions for handling BIDS fieldmap files."""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

log = logging.getLogger(__name__)


def get_fmap_files(bids_dir: str) -> List[Tuple[str, str]]:
    """Find and pair .nii[.gz] and .json files in the fmap directory.

    Args:
        bids_dir: Path to BIDS directory containing fmap folder

    Returns:
        List of tuples containing paired (nifti_path, json_path)
    """
    # Find fmap directory in bids_dir
    fmap_dir = None
    bids_path = Path(bids_dir)

    # Search for any 'fmap' subfolder in the bids directory
    for path in bids_path.glob("**/fmap"):
        if path.is_dir():
            fmap_dir = path
            break

    if fmap_dir is None:
        log.warning(f"No fmap directory found in {bids_dir}")
        return []

    # Get all files in fmap directory
    nifti_files = []
    json_files = []

    for f in fmap_dir.iterdir():
        if f.suffix in [".nii", ".gz"]:
            nifti_files.append(f)
        elif f.suffix == ".json":
            json_files.append(f)

    # Pair matching files
    paired_files = []
    for nifti in nifti_files:
        base = nifti.with_suffix("")
        if base.suffix == ".nii":
            base = base.with_suffix("")
        json_file = base.with_suffix(".json")

        if json_file in json_files:
            paired_files.append((nifti, json_file))
        else:
            log.warning(f"No matching JSON file found for {nifti}")

    # Find unpaired files
    unpaired_nifti = [
        nifti
        for nifti in nifti_files
        if not any(pair[0] == nifti for pair in paired_files)
    ]
    unpaired_json = [
        json_file
        for json_file in json_files
        if not any(pair[1] == json_file for pair in paired_files)
    ]
    unpaired_files = unpaired_nifti + unpaired_json

    # Log the unpaired files
    if unpaired_files:
        log.warning(
            f"Unpaired files found in {fmap_dir}: {', '.join(str(f) for f in unpaired_files)}"
        )

    return paired_files, unpaired_files


def get_intended_for(json_path: str) -> Optional[List[str]]:
    """Extract IntendedFor field from fieldmap JSON sidecar.

    Args:
        json_path: Path to JSON sidecar file

    Returns:
        List of intended target files or None if not specified
    """
    try:
        with json_path.open() as f:
            data = json.load(f)

        intended = data.get("IntendedFor")
        if not intended:
            log.info(f"No IntendedFor field found in {json_path}")
            return None

        # Handle single string vs list
        if isinstance(intended, str):
            intended = [intended]

        return intended

    except Exception as e:
        log.error(f"Error reading {json_path}: {str(e)}")
        return None


def validate_intended_targets(
    bids_dir: str, intended_files: List[str]
) -> Dict[str, bool]:
    """Check if intended target files exist in the BIDS directory.

    Args:
        bids_dir: Path to BIDS directory
        intended_files: List of target file paths from IntendedFor

    Returns:
        Dict mapping file paths to existence boolean
    """
    results = {}
    for f in intended_files:
        # Handle paths with or without leading slash
        if f.startswith("/"):
            f = f[1:]
        full_path = Path(bids_dir) / f
        results[f] = full_path.exists()
        if not results[f]:
            log.warning(f"IntendedFor target not found: {f}")

    return results


def validate_fmap(bids_dir: str) -> Dict[str, Dict[str, bool]]:
    """Validate all fieldmap files and their intended targets.

    Args:
        bids_dir: Path to BIDS directory

    Returns:
        Dict mapping fmap files to their target validation results
    """
    validation = {}

    paired_files, _ = get_fmap_files(bids_dir)
    for nifti, json_path in paired_files:
        intended = get_intended_for(json_path)
        if intended:
            results = validate_intended_targets(bids_dir, intended)
            validation[nifti.name] = results
        else:
            validation[nifti.name] = {}

    return validation


def find_target_file(bids_dir: str, target: str) -> Optional[Path]:
    """Search for the target file in the BIDS directory.

    Args:
        bids_dir: Path to BIDS directory
        target: Target file path from IntendedFor

    Returns:
        Full path to the target file if found, otherwise None
    """
    bids_path = Path(bids_dir)
    target_path = bids_path / target

    if target_path.exists():
        return target_path

    # If not found, search for the file in the entire BIDS directory
    for path in bids_path.glob("**/" + target):
        if path.exists():
            return path

    return None


def remove_orphaned_fmaps(bids_dir: str) -> Dict[str, List[str]]:
    """Remove fieldmap files whose intended targets are missing or do not match.

    Args:
        bids_dir: Path to BIDS directory

    Returns:
        Dict mapping action ('removed', 'skipped') to list of removed file paths
    """
    log.debug("Checking for orphaned fieldmap files...")
    results = {"removed": [], "skipped": []}

    paired_files, unpaired_files = get_fmap_files(bids_dir)
    for f in unpaired_files:
        f.unlink()
        results["removed"].append(str(f))

    for nifti, json_path in paired_files:
        intended = get_intended_for(json_path)

        if not intended:
            # Delete if no IntendedFor field
            nifti.unlink()
            json_path.unlink()
            results["removed"].append(str(nifti))
            results["removed"].append(str(json_path))
            continue

        # Check if any intended targets exist and match the NIfTI file
        target_exists = False
        for target in intended:
            if find_target_file(bids_dir, target):
                target_exists = True
                break

        if not target_exists:
            # Remove both .nii and .json files if no targets exist or match
            try:
                nifti.unlink()
                json_path.unlink()
                results["removed"].append(str(nifti))
                results["removed"].append(str(json_path))
            except Exception as e:
                log.error(f"Failed to remove fmap files: {str(e)}")
                results["skipped"].append(str(nifti))
                results["skipped"].append(str(json_path))
        else:
            results["skipped"].append(str(nifti))
            results["skipped"].append(str(json_path))

    if results["removed"]:
        log.debug(f"Removed orphaned fmap files: {results['removed']}")
    return results
