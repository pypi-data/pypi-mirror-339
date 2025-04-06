import click
import json
import os
import sys
import threading
from concurrent.futures import as_completed, FIRST_COMPLETED, ThreadPoolExecutor, wait
from nomad_media_cli.commands.admin.asset_upload.upload_assets import upload_assets
from nomad_media_cli.commands.common.asset.delete_asset import delete_asset
from nomad_media_cli.commands.common.asset.download_assets import download_assets
from nomad_media_cli.commands.common.asset.get_asset_details import get_asset_details
from nomad_media_cli.commands.common.asset.list_assets import list_assets
from nomad_media_cli.helpers.capture_click_output import capture_click_output
from nomad_media_cli.helpers.utils import initialize_sdk
from nomad_media_cli.helpers.get_id_from_url import get_id_from_url
@click.command()
@click.option("--id", help="The ID of the Asset folder to be synced.")
@click.option("--url", help="The Nomad URL of the Asset folder to be synced (bucket::object-key).")
@click.option("--object-key", help="Object-key of the Asset folder to be synced. This option assumes the default bucket that was previously set with the `set-bucket` command.")
@click.option("--sync-direction", required=True, type=click.Choice(["local-to-nomad", "nomad-to-local"]), help="Direction of the sync.")
@click.option("--source", required=True, help="Source path for the sync.")
@click.option("--threads", default=4, type=click.INT, help="Number of threads to use for the sync.")
@click.option("--include-empty-folders", is_flag=True, help="Include empty folders in the sync.")
@click.pass_context
def sync_assets(ctx, id, url, object_key, sync_direction, source, threads, include_empty_folders):
    """Sync assets between Nomad and local storage."""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    if not id and not url and not object_key:
        click.echo(json.dumps({"error": "Please provide an id, url, or object-key."}))
        sys.exit(1)

    if url or object_key:
        id = get_id_from_url(ctx, url, object_key, nomad_sdk)

    response = nomad_sdk.get_asset(id)
    if not response:
        click.echo(json.dumps({"error": f"Asset folder not found: {id}."}))
        sys.exit(1)

    if response["assetType"] != 1:
        click.echo(json.dumps({"error": "Asset must be a folder."}))
        sys.exit(1)

    # Checks if the path is a directory
    if not os.path.isdir(source):
        click.echo(json.dumps({"error": "Source path must be a directory."}))
        sys.exit(1)
        
    differences = check_dir_structure(ctx, id, response["objectKey"], source, sync_direction, threads, include_empty_folders)

    def check_differences(differences, sync_direction):
        for dif_key, difference_info in differences.items():
            try:
                if not "missing" in difference_info:
                    for key, value in difference_info.items():
                        def get_files(file_dict, files, path = ""):
                            if all(isinstance(val, str) for val in file_dict["value"].values()):
                                file_dict["value"]["path"] = path + file_dict["key"]
                                files[file_dict["key"]] = file_dict["value"]

                            elif isinstance(file_dict["value"], dict):
                                for key, value in file_dict["value"].items():
                                    get_files({ "key": key, "value": value }, files, path + file_dict["key"] + "/")
                        files = {}
                        get_files({"key": key, "value": value}, files, dif_key + "/")
                        check_differences(files, sync_direction)    
                    continue          


                if sync_direction == "local-to-nomad":
                    if difference_info["missing"] == "nomad":
                        file_path = os.path.join(source, difference_info["path"])
                        capture_click_output(ctx, upload_assets, id=id, source=file_path, recursive=True)
                    else:
                        capture_click_output(ctx, delete_asset, id=difference_info["id"])
                elif sync_direction == "nomad-to-local":
                    if difference_info["missing"] == "local":
                        asset_info = capture_click_output(ctx, get_asset_details, id=difference_info["id"])
                        if asset_info["properties"]["statusName"] == "Error":
                            continue

                        file_path = f"{source}/{difference_info["path"]}"
                        file_path = file_path.rsplit("/", 1)[0]
                        capture_click_output(ctx, download_assets, id=difference_info["id"], destination=file_path, include_empty_folders=include_empty_folders, recursive=True)
                    else:
                        file_path = os.path.join(source, difference_info["path"])
                        if os.path.isdir(file_path):
                            os.rmdir(file_path)
                        else:
                            os.remove(file_path)
            except Exception as e:
                click.echo(json.dumps({"error": f"Error processing differences: {e}"}))
                sys.exit(1)
                
    if differences:
        check_differences(differences, sync_direction)
    else:
        click.echo("No differences found.")

def get_total_asset_list(ctx, dir_id, threads):
    page_offset = 0
    dir_assets = []
    lock = threading.Lock()
    stop_event = threading.Event()
    
    def get_assets(dir_id, page_offset):
        for i in range(3):
            list_assets_result = capture_click_output(ctx, list_assets, id=dir_id, page_size=100, page_offset=page_offset, recursive=True)
            if list_assets_result and "items" in list_assets_result:
                return list_assets_result["items"]
        else:
            raise Exception("Failed to retrieve assets after 3 attempts.")
    try:
        first_result = get_assets(dir_id, page_offset)
        if len(first_result) < 100:
            return first_result
        dir_assets.extend(first_result["items"])
        page_offset += 1        

        with ThreadPoolExecutor(max_workers=threads) as executor:
            while not stop_event.is_set():
                futures = []
                current_offset = page_offset
                for i in range(threads):
                    futures.append(executor.submit(get_assets, dir_id, current_offset + i))
                
                batch_results = []
                for future in as_completed(futures):
                    try:
                        items = future.result()
                        batch_results.append(items)
                    except Exception as e:
                        click.echo(json.dumps({"error": f"Error retrieving assets: {e}"}))
                        stop_event.set()
                        break
                    
                with lock:
                    for items in batch_results:
                        dir_assets.extend(items)

                if any(len(items) == 0 for items in batch_results):
                    stop_event.set()
                    break

                page_offset += threads

        return dir_assets
    except Exception as e:
        return(e)

def check_dir_structure(ctx, id, nom_path, path, sync_direction, threads, include_empty_folders):
    try:
        nomad_structure = get_nomad_structure(ctx, id, nom_path, threads)
        local_structure = get_local_structure(path)
    except Exception as e:
        click.echo(json.dumps({"error": f"Error checking directory structure: {e}"}))
        sys.exit(1)

    return compare_structs(nomad_structure["sub_dirs"], local_structure["sub_dirs"], sync_direction, include_empty_folders)
    
import os

def compare_structs(nomad_struct, local_struct, sync_direction, include_emtpy_folders, current_path=""):
    differences = {}

    # Combine both structures into a single dictionary for easy lookup
    nomad_lookup = {item["name"]: item for item in nomad_struct}
    local_lookup = {item["name"]: item for item in local_struct}

    # Get all unique keys from both structures
    all_keys = set(nomad_lookup.keys()).union(set(local_lookup.keys()))

    for key in all_keys:
        asset_path = os.path.join(current_path, key) if current_path else key

        nomad_asset = nomad_lookup.get(key)
        local_asset = local_lookup.get(key)

        # Check if the asset is missing in either structure
        if not nomad_asset:
            if not include_emtpy_folders and len(local_asset.get("sub_dirs", [])) == 0:
                continue
            differences[key] = {"missing": "nomad", "path": asset_path}
        elif not local_asset:
            differences[key] = {
                "missing": "local",
                "path": asset_path,
                "id": nomad_asset.get("id"),
                "file_type": nomad_asset.get("file_type")
            }
        else:
            # If both assets exist, check if they are directories and compare their subdirectories
            if nomad_asset.get("sub_dirs") or local_asset.get("sub_dirs"):
                nested_diff = compare_structs(
                    nomad_asset.get("sub_dirs", []),
                    local_asset.get("sub_dirs", []),
                    sync_direction,
                    asset_path
                )
                if nested_diff:
                    differences[key] = nested_diff

    return differences


def get_nomad_structure(ctx, asset_id, path, threads):
    assets = get_total_asset_list(ctx, asset_id, threads)
    
    root_asset_name = path.strip("/").split("/")[-1]
    root = {"id": asset_id, "name": root_asset_name, "file_type": "Folder", "sub_dirs": []}
    
    def add_asset_to_structure(structure, parts, asset):
        try:
            if not parts or parts[0] == "":
                return

            current_part = parts[0]
            remaining_parts = parts[1:]

            sub_dir = next((d for d in structure["sub_dirs"] if d["name"] == current_part), None)
            if not sub_dir:
                sub_dir = {"id": None, "name": current_part, "file_type": asset["assetTypeDisplay"], "sub_dirs": []}
                structure["sub_dirs"].append(sub_dir)

            if not remaining_parts:
                sub_dir.update({
                    "id": asset["id"]
                })
            else:
                add_asset_to_structure(sub_dir, remaining_parts, asset)
        except Exception as e:
            click.echo(json.dumps({"error": f"Error adding asset to structure: {e}"}))
            raise e
    
    # Process each asset
    try:
        for asset in assets:
            # Split the asset's URL into parts relative to the root path
            display_path = asset["displayPath"]
            if len(display_path.split(path)) < 2:
                continue
            relative_path = display_path.split(path, 1)[1].lstrip("/")
            parts = relative_path.split("/")

            # Add the asset to the structure
            add_asset_to_structure(root, parts, asset)

        return root
    except Exception as e:
        click.echo(json.dumps({"error": f"Error processing assets: {e}"}))
        raise e

def get_local_structure(path):
    structure = {"name": os.path.basename(path), "sub_dirs": []}
    path = os.path.abspath(path)

    for root, dirs, files in os.walk(path):
        rel_path = os.path.relpath(root, path)
        
        if rel_path == ".":
            current_level = structure
        else:
            current_level = structure
            parts = rel_path.split(os.sep)
            for part in parts:
                for sub_dir in current_level["sub_dirs"]:
                    if sub_dir["name"] == part:
                        current_level = sub_dir
                        break
        
        for dir_name in dirs:
            sub_dir = {"name": dir_name, "sub_dirs": []}
            current_level["sub_dirs"].append(sub_dir)
        
        for file_name in files:
            file_entry = {"name": file_name, "sub_dirs": []}
            current_level["sub_dirs"].append(file_entry)
    
    return structure