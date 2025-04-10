import os
import subprocess
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

import boto3
from botocore.exceptions import ClientError


def rclone_copy(
    source_dir: str,
    destination: str,
    dry_run: bool = False,
    transfers: int = 4,
    extra_args: Optional[List[str]] = None,
    verbose: bool = True,
) -> bool:
    """
    Upload a directory to a remote bucket using `rclone copy`.

    Args:
        source_dir (str): Path to local directory to upload.
        destination (str): Remote destination, e.g., 's3:my-bucket/path'.
        dry_run (bool): If True, performs a dry run without uploading.
        transfers (int): Number of parallel transfers.
        extra_args (Optional[List[str]]): Additional rclone flags.
        verbose (bool): If True, prints command and output live.

    Returns:
        bool: True if upload succeeded, False otherwise.
    """
    command = [
        "rclone",
        "copy",
        source_dir,
        destination,
        f"--transfers={transfers}",
        "--progress",
    ]

    if dry_run:
        command.append("--dry-run")
    if extra_args:
        command.extend(extra_args)

    if verbose:
        print("Running command:", " ".join(command))

    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )

        if not process.stdout:
            raise Exception("No output from rclone")

        for line in process.stdout:
            if verbose:
                print(line.strip())

        return process.wait() == 0

    except Exception as e:
        print(f"Error during rclone copy: {e}")
        return False


def find_latest_checkpoint(training_dir: str) -> Optional[str]:
    """
    Finds the checkpoint directory with the highest step number in a Hugging Face
    training output directory.

    Args:
        training_dir (str): The path to the training output directory.

    Returns:
        Optional[str]: The path to the latest checkpoint directory, or None if
                       no checkpoint directories are found or the directory
                       doesn't exist.
    """
    latest_step = -1
    latest_checkpoint_dir = None

    if not os.path.isdir(training_dir):
        print(f"Error: Directory not found: {training_dir}")
        return None

    for item in os.listdir(training_dir):
        item_path = os.path.join(training_dir, item)
        if os.path.isdir(item_path) and item.startswith("checkpoint-"):
            try:
                step_str = item.split("-")[-1]
                if step_str.isdigit():
                    step = int(step_str)
                    if step > latest_step:
                        latest_step = step
                        latest_checkpoint_dir = item_path
            except (ValueError, IndexError):
                # Ignore items that don't match the expected pattern
                continue

    return latest_checkpoint_dir


def _parse_s3_path(path: str) -> Tuple[Optional[str], Optional[str]]:
    """Parses an S3 path (s3://bucket/prefix) into bucket and prefix."""
    parsed = urlparse(path)
    if parsed.scheme != "s3":
        return None, None
    bucket = parsed.netloc
    prefix = parsed.path.lstrip("/")
    return bucket, prefix


def _list_s3_objects(
    s3_client: Any, bucket: str, prefix: Optional[str], verbose: bool = True
) -> Dict[str, Dict[str, Any]]:
    """Lists objects in an S3 prefix."""
    objects: Dict[str, Dict[str, Any]] = {}
    paginator = s3_client.get_paginator("list_objects_v2")
    list_prefix = (
        prefix if prefix else ""
    )  # Use empty string if prefix is None for listing
    if verbose:
        print(f"Listing objects in s3://{bucket}/{list_prefix}...")

    operation_parameters = {"Bucket": bucket}
    # Only add Prefix parameter if it's non-empty
    if list_prefix:
        operation_parameters["Prefix"] = list_prefix

    try:
        page_iterator = paginator.paginate(**operation_parameters)
        for page in page_iterator:
            if "Contents" in page:
                for obj in page["Contents"]:
                    # Ignore zero-byte objects ending in '/' (S3 console folders)
                    if obj["Key"].endswith("/") and obj["Size"] == 0:
                        continue

                    # Determine key relative to the *prefix* for comparison
                    # If prefix is None or empty, relative key is the full key.
                    relative_key: Optional[str] = None
                    if prefix and obj["Key"].startswith(prefix):
                        # Ensure trailing slash consistency if prefix has one
                        prefix_adjusted = (
                            prefix if prefix.endswith("/") else prefix + "/"
                        )
                        # Handle exact match of prefix as a file
                        if obj["Key"] == prefix:
                            relative_key = os.path.basename(obj["Key"])
                        # Handle keys within the prefix "directory"
                        elif obj["Key"].startswith(prefix_adjusted):
                            relative_key = obj["Key"][len(prefix_adjusted) :]
                        # This case should technically not be needed if prefix is used correctly in listing
                        # but handle defensively if object key *is* the prefix itself (without trailing slash)
                        elif obj["Key"] == prefix.rstrip("/"):
                            relative_key = os.path.basename(obj["Key"])
                        # else: # Should not happen if prefix filter works correctly
                        #    print(f"Warning: Unexpected key {obj['Key']} found for prefix {prefix}")
                        #    relative_key = obj["Key"] # Fallback
                    elif not prefix:
                        # If no prefix specified, the relative key is the full key
                        relative_key = obj["Key"]
                    # else: obj["Key"] does not start with prefix - ignore (shouldn't happen with Prefix param)

                    # Skip if relative key is empty or None (e.g., prefix itself listed, or unexpected case)
                    if not relative_key:
                        continue

                    # Ensure LastModified is timezone-aware
                    last_modified = obj["LastModified"]
                    if last_modified.tzinfo is None:
                        last_modified = last_modified.replace(tzinfo=timezone.utc)

                    objects[relative_key] = {
                        "path": f"s3://{bucket}/{obj['Key']}",  # Store full path for reference
                        "key": obj["Key"],  # Store full S3 key
                        "size": obj["Size"],
                        "mtime": last_modified,
                        "type": "s3",
                    }
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchBucket":
            print(f"Error: Bucket '{bucket}' not found.")
        # Allow sync *to* a non-existent prefix (will just upload all)
        elif e.response["Error"]["Code"] == "NoSuchKey" and prefix:
            if verbose:
                print(f"Prefix s3://{bucket}/{prefix} not found (treating as empty).")
        else:
            print(f"Error listing S3 objects: {e}")
        # Return empty dict on error that prevents listing (like NoSuchBucket)
        if e.response["Error"]["Code"] == "NoSuchBucket":
            return {}
    except Exception as e:
        print(f"An unexpected error occurred listing S3 objects: {e}")
        return {}  # Return empty on unexpected error

    if verbose:
        print(f"Found {len(objects)} objects in S3.")
    return objects


def _list_local_files(
    local_dir: str, verbose: bool = True
) -> Dict[str, Dict[str, Any]]:
    """Lists files in a local directory."""
    if not os.path.isdir(local_dir):
        # Check if it's a file path instead of a dir
        if os.path.isfile(local_dir):
            print(
                f"Warning: Source {local_dir} is a file, not a directory. Syncing single file."
            )
            try:
                local_size = os.path.getsize(local_dir)
                local_mtime_ts = os.path.getmtime(local_dir)
                local_mtime = datetime.fromtimestamp(local_mtime_ts, tz=timezone.utc)
                file_name = os.path.basename(local_dir)
                return {
                    file_name: {
                        "path": local_dir,
                        "size": local_size,
                        "mtime": local_mtime,
                        "type": "local",
                    }
                }
            except OSError as e:
                print(f"Error accessing source file {local_dir}: {e}")
                return {}
        else:
            print(f"Warning: Local path not found: {local_dir} (treating as empty).")
            return {}

    files: Dict[str, Dict[str, Any]] = {}
    if verbose:
        print(f"Scanning local directory: {local_dir}...")
    for root, _, file_list in os.walk(local_dir):
        for file_name in file_list:
            local_path = os.path.join(root, file_name)
            try:
                # Use '/' for relative key consistency
                relative_path = os.path.relpath(local_path, local_dir).replace(
                    "\\", "/"
                )
                # relative_path will be '.' if local_dir points to a file, handled above.

                local_size = os.path.getsize(local_path)
                local_mtime_ts = os.path.getmtime(local_path)
                local_mtime = datetime.fromtimestamp(local_mtime_ts, tz=timezone.utc)

                files[relative_path] = {
                    "path": local_path,
                    "size": local_size,
                    "mtime": local_mtime,
                    "type": "local",
                }
            except OSError as e:
                print(f"Warning: Could not get metadata for {local_path}: {e}")
            except Exception as e:
                print(f"Warning: Unexpected error processing {local_path}: {e}")

    if verbose:
        print(f"Found {len(files)} files locally.")
    return files


def s3_sync(
    source: str,
    destination: str,
    delete: bool = False,
    dry_run: bool = False,
    verbose: bool = True,
) -> None:
    """
    Synchronizes files between a source and a destination, which can be
    local paths or S3 paths (e.g., 's3://my-bucket/my-prefix').

    Compares file sizes and modification times. Copies files from source
    to destination if they are missing, larger, or newer in the source.
    Optionally deletes files from the destination if they are not present
    in the source.

    Args:
        source (str): The source path (local directory/file or s3://...).
        destination (str): The destination path (local directory or s3://...).
        delete (bool): If True, delete extraneous files from the destination.
        dry_run (bool): If True, print actions without performing them.
        verbose (bool): If True, print actions being taken.
    """
    s3_client = boto3.client("s3")
    mtime_tolerance = timedelta(
        seconds=2
    )  # S3 mtime might not have sub-second precision

    src_bucket, src_prefix = _parse_s3_path(source)
    dest_bucket, dest_prefix = _parse_s3_path(destination)

    source_items: Dict[str, Dict[str, Any]] = {}
    dest_items: Dict[str, Dict[str, Any]] = {}
    sync_direction = ""
    is_single_file_sync = False

    # Determine sync direction and list items
    if src_bucket is None and dest_bucket is not None:
        sync_direction = "upload"
        source_items = _list_local_files(source, verbose)
        dest_items = _list_s3_objects(s3_client, dest_bucket, dest_prefix, verbose)
        # Check if source exists (either dir or file)
        if not os.path.exists(source):
            print(f"Error: Source path {source} not found.")
            return
        is_single_file_sync = os.path.isfile(source)
        # Destination prefix defaults to empty if not specified
        if dest_prefix is None:
            dest_prefix = ""

    elif src_bucket is not None and dest_bucket is None:
        sync_direction = "download"
        source_items = _list_s3_objects(s3_client, src_bucket, src_prefix, verbose)
        # For download, destination MUST be a directory (or created as one)
        # If destination exists and is a file, it's an error.
        if os.path.exists(destination) and not os.path.isdir(destination):
            print(
                f"Error: Local destination '{destination}' exists but is not a directory."
            )
            return

        dest_items = _list_local_files(destination, verbose)

        # Ensure destination directory exists for downloads
        if not dry_run:
            os.makedirs(destination, exist_ok=True)
        elif not os.path.isdir(destination) and verbose:
            print(f"Dry run: Would create local directory {destination}")

    elif src_bucket is None and dest_bucket is None:
        print(
            "Error: Both source and destination are local paths. Use standard file copy tools."
        )
        return
    elif src_bucket is not None and dest_bucket is not None:
        print(
            "Error: S3 to S3 sync not implemented. Use AWS CLI or S3 Batch Operations."
        )
        return
    else:
        # This case should not be reachable given the above checks
        print("Error: Invalid source or destination path combination.")
        return

    actions_to_perform: List[Dict[str, Any]] = []

    # --- Compare items ---
    # Use source keys as the primary loop iterator
    source_keys = set(source_items.keys())
    dest_keys = set(dest_items.keys())

    for rel_key in source_keys:
        src_item = source_items[rel_key]
        dest_item = dest_items.get(rel_key)
        reason = ""

        if dest_item is None:
            reason = "does not exist in destination"
        else:
            # Compare metadata (size and mtime)
            if src_item["size"] != dest_item["size"]:
                reason = (
                    f"size differs (src: {src_item['size']}, dest: {dest_item['size']})"
                )
            # Sync if source is newer (outside tolerance)
            elif src_item["mtime"] > (dest_item["mtime"] + mtime_tolerance):
                reason = f"is newer in source (src: {src_item['mtime']}, dest: {dest_item['mtime']})"

        if reason:
            action_type = "upload" if sync_direction == "upload" else "download"
            # Determine the final destination key/path
            dest_full_path_or_key: Optional[str] = None
            if sync_direction == "upload":
                # If uploading single file, dest key is prefix + filename
                # If uploading dir, dest key is prefix + relative key
                # Ensure dest_prefix is treated as empty string if None
                current_dest_prefix = dest_prefix or ""
                final_dest_key = (
                    rel_key
                    if is_single_file_sync
                    else os.path.join(current_dest_prefix, rel_key).replace("\\", "/")
                )
                # Ensure we don't create keys like 's3://bucket//key' if prefix was empty
                if not current_dest_prefix and final_dest_key.startswith("/"):
                    final_dest_key = final_dest_key.lstrip("/")
                dest_full_path_or_key = f"s3://{dest_bucket}/{final_dest_key}"
            else:  # download
                dest_full_path_or_key = os.path.join(
                    destination, rel_key.replace("/", os.sep)
                )

            actions_to_perform.append(
                {
                    "action": action_type,
                    "relative_key": rel_key,
                    "source_path": src_item["path"],  # Local path or S3 URI
                    "source_mtime": src_item.get("mtime"),
                    "dest_full_path_or_key": dest_full_path_or_key,
                    # Store details needed for specific actions
                    "dest_bucket": dest_bucket,
                    "dest_prefix": dest_prefix,
                    "s3_key_full_src": src_item.get("key")
                    if sync_direction == "download"
                    else None,
                    "source_bucket": src_bucket,
                    "reason": reason,
                }
            )

    # Identify items for deletion in destination
    if delete:
        keys_to_delete = dest_keys - source_keys
        for rel_key in keys_to_delete:
            dest_item = dest_items[rel_key]
            action_type = "delete_s3" if sync_direction == "upload" else "delete_local"
            actions_to_perform.append(
                {
                    "action": action_type,
                    "relative_key": rel_key,
                    "path_to_delete": dest_item["path"],  # Full S3 URI or local path
                    "s3_key_full_dest": dest_item.get("key")
                    if sync_direction == "upload"
                    else None,  # Needed for delete_s3
                    "dest_bucket": dest_bucket,  # Needed for delete_s3
                    "reason": "does not exist in source",
                }
            )

    # --- Execute Actions ---
    uploads_done = downloads_done = deletions_done = 0
    s3_deletions_batch: List[Dict[str, str]] = []

    if not actions_to_perform:
        print("Source and destination are already synchronized.")
        # Still check if source/dest actually exist if nothing to do
        if sync_direction == "upload" and not os.path.exists(source):
            print(f"Note: Source path {source} does not exist.")
        # Add check for S3 source existence if needed via head_bucket or similar
        return

    for action in actions_to_perform:
        rel_key = action["relative_key"]
        reason = action["reason"]
        dest_full_path_or_key = action["dest_full_path_or_key"]

        if action["action"] == "upload":
            local_path = action["source_path"]
            # Ensure dest_full_path_or_key is valid before parsing
            if not isinstance(dest_full_path_or_key, str):
                print(
                    f"ERROR: Invalid destination path calculated for upload: {dest_full_path_or_key}"
                )
                continue
            # Extract final key from the pre-calculated dest_full_path_or_key
            _, upload_key = _parse_s3_path(dest_full_path_or_key)
            target_bucket = action["dest_bucket"]

            if verbose:
                print(f"Upload: {local_path} to {dest_full_path_or_key} ({reason})")
            if not dry_run:
                if target_bucket and upload_key is not None:
                    try:
                        s3_client.upload_file(local_path, target_bucket, upload_key)
                        uploads_done += 1
                    except ClientError as e:
                        print(f"ERROR uploading {local_path}: {e}")
                    except Exception as e:
                        print(f"ERROR uploading {local_path}: {e}")
                else:
                    print(
                        f"ERROR: Invalid S3 target for upload: bucket={target_bucket}, key={upload_key}"
                    )

        elif action["action"] == "download":
            s3_key_full = action["s3_key_full_src"]
            local_path = dest_full_path_or_key  # This is the local destination path
            source_bucket_dl = action["source_bucket"]

            if verbose:
                print(f"Download: {action['source_path']} to {local_path} ({reason})")
            # Ensure local_path is valid before proceeding
            if not isinstance(local_path, str):
                print(
                    f"ERROR: Invalid local destination path calculated for download: {local_path}"
                )
                continue
            if not dry_run:
                if source_bucket_dl and s3_key_full and local_path:
                    try:
                        local_file_dir = os.path.dirname(local_path)
                        os.makedirs(local_file_dir, exist_ok=True)
                        s3_client.download_file(
                            source_bucket_dl, s3_key_full, local_path
                        )
                        downloads_done += 1
                    except ClientError as e:
                        print(f"ERROR downloading {s3_key_full}: {e}")
                    except OSError as e:
                        print(
                            f"ERROR creating directory or writing file {local_path}: {e}"
                        )
                    except Exception as e:
                        print(f"ERROR downloading {s3_key_full}: {e}")
                else:
                    print(
                        f"ERROR: Invalid parameters for download: bucket={source_bucket_dl}, key={s3_key_full}, local={local_path}"
                    )

        elif action["action"] == "delete_s3":
            s3_key_to_delete = action["s3_key_full_dest"]
            target_bucket_del = action["dest_bucket"]
            if target_bucket_del and s3_key_to_delete:
                if verbose:
                    print(f"Delete S3: {action['path_to_delete']} ({reason})")
                # Check type before appending to batch
                if isinstance(s3_key_to_delete, str):
                    s3_deletions_batch.append({"Key": s3_key_to_delete})
                else:
                    print(f"ERROR: Invalid S3 key for deletion: {s3_key_to_delete}")
            else:
                print(
                    f"ERROR: Invalid S3 target for deletion: bucket={target_bucket_del}, key={s3_key_to_delete}"
                )

        elif action["action"] == "delete_local":
            local_path_to_delete = action["path_to_delete"]
            if verbose:
                print(f"Delete Local: {local_path_to_delete} ({reason})")
            if not dry_run:
                try:
                    os.remove(local_path_to_delete)
                    deletions_done += 1
                    # TODO: Optionally clean up empty directories?
                except OSError as e:
                    print(f"ERROR deleting local file {local_path_to_delete}: {e}")

    # Process S3 deletions in batches
    if s3_deletions_batch:
        # Get the target bucket from the first deletion action (should be consistent)
        target_bucket_del_batch = next(
            (
                a["dest_bucket"]
                for a in actions_to_perform
                if a["action"] == "delete_s3"
            ),
            None,
        )
        if not dry_run and target_bucket_del_batch:
            deleted_count_batch = 0
            for i in range(0, len(s3_deletions_batch), 1000):
                batch = s3_deletions_batch[i : i + 1000]
                delete_payload = {"Objects": batch, "Quiet": False}  # Get errors back
                try:
                    response = s3_client.delete_objects(
                        Bucket=target_bucket_del_batch, Delete=delete_payload
                    )
                    # Increment count based on successful deletions reported (if not Quiet) or assume success if Quiet
                    deleted_count_batch += len(
                        batch
                    )  # Assume success unless errors reported
                    if "Deleted" in response:
                        pass  # Counted optimistically above
                        # deleted_count_batch += len(response['Deleted'])
                    if "Errors" in response and response["Errors"]:
                        deleted_count_batch -= len(
                            response["Errors"]
                        )  # Adjust count for errors
                        for error in response["Errors"]:
                            print(
                                f"ERROR deleting S3 object {error['Key']}: {error['Code']} - {error['Message']}"
                            )
                except ClientError as e:
                    print(f"ERROR deleting S3 objects batch: {e}")
                    deleted_count_batch = 0  # Assume batch failed
                except Exception as e:
                    print(f"ERROR deleting S3 objects batch: {e}")
                    deleted_count_batch = 0  # Assume batch failed
            deletions_done += deleted_count_batch
        elif target_bucket_del_batch:  # dry_run is True
            deletions_done = len(
                s3_deletions_batch
            )  # Report planned deletions for dry run
        else:
            print("Warning: Could not determine target bucket for S3 deletion batch.")

    # --- Summary ---
    if dry_run:
        upload_count = sum(1 for a in actions_to_perform if a["action"] == "upload")
        download_count = sum(1 for a in actions_to_perform if a["action"] == "download")
        # Deletion count for dry run is based on the batch prepared
        delete_s3_count = len(s3_deletions_batch)
        delete_local_count = sum(
            1 for a in actions_to_perform if a["action"] == "delete_local"
        )
        print("\n--- DRY RUN SUMMARY ---")
        if sync_direction == "upload":
            print(f"Would upload: {upload_count} file(s)")
            if delete:
                print(f"Would delete from S3: {delete_s3_count} object(s)")
        elif sync_direction == "download":
            print(f"Would download: {download_count} file(s)")
            if delete:
                print(f"Would delete locally: {delete_local_count} file(s)")
        print("--- END DRY RUN ---")
    else:
        if sync_direction == "upload":
            print(
                f"Sync completed. Uploaded: {uploads_done} file(s). Deleted from S3: {deletions_done if delete else 0} object(s)."
            )
        elif sync_direction == "download":
            print(
                f"Sync completed. Downloaded: {downloads_done} file(s). Deleted locally: {deletions_done if delete else 0} file(s)."
            )


def s3_check(s3_uri: str) -> bool:
    """
    Check if an object or prefix exists in an S3 bucket using an S3 URI.

    Args:
        s3_uri (str): The S3 URI (e.g., 's3://my-bucket/my-key' or 's3://my-bucket/my-prefix/').
                      Use a trailing '/' to check for a prefix/directory.

    Returns:
        bool: True if the object or prefix exists, False otherwise.
    """
    s3 = boto3.client("s3")
    bucket_name, s3_key = _parse_s3_path(s3_uri)

    if bucket_name is None or s3_key is None:
        # _parse_s3_path returns None, None if scheme is not 's3'
        print(f"Error: Invalid S3 URI format: {s3_uri}")
        return False

    is_prefix = s3_key.endswith("/")

    try:
        if is_prefix:
            # Check for prefix existence by listing objects
            # Handle the case where s3_key might be empty if URI is just s3://bucket/
            list_prefix = s3_key if s3_key else ""
            response = s3.list_objects_v2(
                Bucket=bucket_name, Prefix=list_prefix, MaxKeys=1
            )
            # Check if any objects OR common prefixes (folders) are returned for the prefix
            return "Contents" in response or "CommonPrefixes" in response
        else:
            # Check for object existence
            s3.head_object(Bucket=bucket_name, Key=s3_key)
            return True
    except ClientError as e:  # Catch boto3 ClientError first
        # If head_object returns 404 (NoSuchKey), the object doesn't exist
        # list_objects_v2 does not raise NoSuchKey for prefixes
        if e.response["Error"]["Code"] == "404":
            return False
        elif e.response["Error"]["Code"] == "NoSuchBucket":
            print(f"Error: Bucket '{bucket_name}' not found (from URI: {s3_uri}).")
            return False
        # Handle other potential errors like AccessDenied differently if needed
        print(f"Error checking {s3_uri}: {e}")
        return False
    # except s3.exceptions.NoSuchBucket: # This specific exception is less common with boto3 client
    #     print(f"Error: Bucket '{bucket_name}' not found (from URI: {s3_uri}).")
    #     return False
    except Exception as e:
        print(f"An unexpected error occurred checking {s3_uri}: {e}")
        return False


def s3_copy(
    source: str,
    destination: str,
    verbose: bool = True,
) -> None:
    """
    Copies files or directories between local paths and S3 URIs.

    Handles:
    - Local file to S3 object
    - Local directory to S3 prefix (recursive)
    - S3 object to local file
    - S3 prefix to local directory (recursive)

    Does NOT handle:
    - Local to Local (use shutil)
    - S3 to S3 (use AWS CLI or boto3 object copy)

    Args:
        source (str): The source path (local file/dir or s3://...).
        destination (str): The destination path (local file/dir or s3://...).
        verbose (bool): If True, print actions being taken.
    """
    s3_client = boto3.client("s3")
    src_bucket, src_prefix = _parse_s3_path(source)
    dest_bucket, dest_prefix = _parse_s3_path(destination)

    # --- Reject unsupported operations ---
    if src_bucket is None and dest_bucket is None:
        print(
            "Error: Both source and destination are local. Use 'shutil.copy' or 'shutil.copytree'."
        )
        return
    if src_bucket is not None and dest_bucket is not None:
        print(
            "Error: S3 to S3 copy not implemented. Use 'aws s3 cp' or boto3 'copy_object'."
        )
        return

    # --- Upload: Local to S3 ---
    if src_bucket is None and dest_bucket is not None:
        if not os.path.exists(source):
            print(f"Error: Local source path not found: {source}")
            return
        # Ensure dest_prefix is usable, default to empty string if None
        dest_prefix = dest_prefix or ""

        # Case 1: Source is a local file
        if os.path.isfile(source):
            # Determine final S3 key
            # If dest looks like a dir (ends /) or is empty, append filename
            if not dest_prefix or destination.endswith("/"):
                s3_key = os.path.join(dest_prefix, os.path.basename(source)).replace(
                    "\\", "/"
                )
            else:  # Treat dest as the exact key name
                s3_key = dest_prefix

            if verbose:
                print(f"Uploading {source} to s3://{dest_bucket}/{s3_key}")
            try:
                s3_client.upload_file(source, dest_bucket, s3_key)
                print("Upload complete.")
            except ClientError as e:
                print(f"ERROR uploading {source}: {e}")
            except Exception as e:
                print(f"ERROR uploading {source}: {e}")

        # Case 2: Source is a local directory
        elif os.path.isdir(source):
            if verbose:
                print(
                    f"Uploading directory {source}/* to s3://{dest_bucket}/{dest_prefix}/"
                )
            files_uploaded = 0
            files_failed = 0
            for root, _, files in os.walk(source):
                for file in files:
                    local_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_path, source)
                    s3_key = os.path.join(dest_prefix, relative_path).replace("\\", "/")
                    if verbose:
                        print(
                            f"  Uploading {local_path} to s3://{dest_bucket}/{s3_key}"
                        )
                    try:
                        s3_client.upload_file(local_path, dest_bucket, s3_key)
                        files_uploaded += 1
                    except ClientError as e:
                        print(f"  ERROR uploading {local_path}: {e}")
                        files_failed += 1
                    except Exception as e:
                        print(f"  ERROR uploading {local_path}: {e}")
                        files_failed += 1
            print(
                f"Directory upload complete. Files uploaded: {files_uploaded}, Failed: {files_failed}"
            )
        else:
            print(f"Error: Source {source} is neither a file nor a directory.")

    # --- Download: S3 to Local ---
    elif src_bucket is not None and dest_bucket is None:
        # Determine if source is likely a single object or a prefix
        is_prefix_download = False
        single_object_key = None

        # If source ends with '/', treat it as a prefix explicitly
        if source.endswith("/"):
            is_prefix_download = True
            src_prefix = src_prefix or ""  # Ensure not None
        else:
            # Try checking if the source key exists as a single object
            try:
                s3_client.head_object(Bucket=src_bucket, Key=src_prefix)
                single_object_key = src_prefix  # It exists as a single object
            except ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    # Object doesn't exist, assume it's a prefix for recursive download
                    is_prefix_download = True
                    src_prefix = src_prefix or ""  # Ensure not None
                elif e.response["Error"]["Code"] == "NoSuchBucket":
                    print(f"Error: Source bucket '{src_bucket}' not found.")
                    return
                else:
                    # Other error (e.g., permissions)
                    print(
                        f"Error checking S3 source object s3://{src_bucket}/{src_prefix}: {e}"
                    )
                    return
            except Exception as e:
                print(
                    f"Error checking S3 source object s3://{src_bucket}/{src_prefix}: {e}"
                )
                return

        # Case 1: Download single S3 object
        if single_object_key is not None:
            # Determine local destination path
            if os.path.isdir(destination) or destination.endswith(os.sep):
                # Download into the directory
                local_dest_path = os.path.join(
                    destination, os.path.basename(single_object_key)
                )
                # Create local directory if downloading into it and it doesn't exist
                os.makedirs(destination, exist_ok=True)
            else:
                # Download to the exact file path
                local_dest_path = destination
                # Ensure parent directory exists
                parent_dir = os.path.dirname(local_dest_path)
                if parent_dir:
                    os.makedirs(parent_dir, exist_ok=True)

            if verbose:
                print(
                    f"Downloading s3://{src_bucket}/{single_object_key} to {local_dest_path}"
                )
            try:
                s3_client.download_file(src_bucket, single_object_key, local_dest_path)
                print("Download complete.")
            except ClientError as e:
                print(f"ERROR downloading {single_object_key}: {e}")
            except OSError as e:
                print(
                    f"ERROR creating directory or writing file {local_dest_path}: {e}"
                )
            except Exception as e:
                print(f"ERROR downloading {single_object_key}: {e}")

        # Case 2: Download S3 prefix (recursive)
        elif is_prefix_download:
            # Ensure local destination is a directory
            if os.path.exists(destination) and not os.path.isdir(destination):
                print(
                    f"Error: Local destination '{destination}' exists but is not a directory for prefix download."
                )
                return
            os.makedirs(destination, exist_ok=True)

            if verbose:
                print(
                    f"Downloading prefix s3://{src_bucket}/{src_prefix}/* to {destination}/"
                )

            paginator = s3_client.get_paginator("list_objects_v2")
            files_downloaded = 0
            files_failed = 0
            operation_parameters = {"Bucket": src_bucket}
            if src_prefix:
                operation_parameters["Prefix"] = src_prefix

            try:
                page_iterator = paginator.paginate(**operation_parameters)
                found_objects = False
                for page in page_iterator:
                    if "Contents" in page:
                        found_objects = True
                        for obj in page["Contents"]:
                            s3_key = obj["Key"]
                            # Skip zero-byte directory markers if downloading a prefix
                            if s3_key.endswith("/") and obj["Size"] == 0:
                                continue

                            # Calculate relative path from the source prefix
                            if src_prefix and s3_key.startswith(src_prefix):
                                # Handle potential trailing slash inconsistency
                                prefix_adjusted = (
                                    src_prefix
                                    if src_prefix.endswith("/")
                                    else src_prefix + "/"
                                )
                                if s3_key.startswith(prefix_adjusted):
                                    relative_key = s3_key[len(prefix_adjusted) :]
                                # Handle the prefix itself if listed as an object (unlikely for prefix download)
                                elif s3_key == src_prefix.rstrip("/"):
                                    relative_key = os.path.basename(s3_key)
                                else:  # Should not happen
                                    relative_key = s3_key
                            elif not src_prefix:  # Downloading whole bucket essentially
                                relative_key = s3_key
                            else:  # Key doesn't start with prefix, should not happen
                                continue

                            # Skip if relative key is empty (e.g. prefix marker was somehow processed)
                            if not relative_key:
                                continue

                            local_dest_path = os.path.join(
                                destination, relative_key.replace("/", os.sep)
                            )
                            local_dest_dir = os.path.dirname(local_dest_path)

                            if verbose:
                                print(
                                    f"  Downloading s3://{src_bucket}/{s3_key} to {local_dest_path}"
                                )
                            try:
                                if local_dest_dir:
                                    os.makedirs(local_dest_dir, exist_ok=True)
                                s3_client.download_file(
                                    src_bucket, s3_key, local_dest_path
                                )
                                files_downloaded += 1
                            except ClientError as e:
                                print(f"  ERROR downloading {s3_key}: {e}")
                                files_failed += 1
                            except OSError as e:
                                print(
                                    f"  ERROR creating directory or writing file {local_dest_path}: {e}"
                                )
                                files_failed += 1
                            except Exception as e:
                                print(f"  ERROR downloading {s3_key}: {e}")
                                files_failed += 1

                if not found_objects:
                    print(
                        f"Warning: No objects found at source prefix s3://{src_bucket}/{src_prefix}"
                    )

                print(
                    f"Prefix download complete. Files downloaded: {files_downloaded}, Failed: {files_failed}"
                )

            except ClientError as e:
                if e.response["Error"]["Code"] == "NoSuchBucket":
                    print(f"Error: Source bucket '{src_bucket}' not found.")
                else:
                    print(
                        f"Error listing objects in s3://{src_bucket}/{src_prefix}: {e}"
                    )
            except Exception as e:
                print(f"Error listing objects in s3://{src_bucket}/{src_prefix}: {e}")

    else:  # Should not be reachable
        print("Error: Unknown copy operation type.")
