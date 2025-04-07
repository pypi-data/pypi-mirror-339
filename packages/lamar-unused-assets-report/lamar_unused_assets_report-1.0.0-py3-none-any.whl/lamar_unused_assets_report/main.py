import os
import argparse
import sys
import csv
import json
import requests
from pathlib import Path

API_URL = "https://cmsprod.lamar.edu/api/v1/read"
SUBSCRIBERS_API_URL = "https://cmsprod.lamar.edu/api/v1/listSubscribers"

def read_asset(asset_id, asset_type, headers):
    payload = {
        "authentication": {"apiKey": headers['Authorization'].split()[-1]},
        "identifier": {"type": asset_type, "id": asset_id}
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching asset {asset_id}: {e}", file=sys.stderr)
        return {}

def read_folder(folder_id, headers, csv_writer):
    payload = {
        "authentication": {"apiKey": headers['Authorization'].split()[-1]},
        "identifier": {"type": "folder", "id": folder_id}
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if "asset" in data and "folder" in data["asset"]:
            for child in data["asset"]["folder"].get("children", []):
                child_type = child.get("type")
                child_id = child.get("id")
                path = child.get("path", {}).get("path", "")
                if child_type == "folder":
                    read_folder(child_id, headers, csv_writer)
                else:
                    read_subscribers(child_type, child_id, path, headers, csv_writer)
    except Exception as e:
        print(f"Error fetching folder {folder_id}: {e}", file=sys.stderr)

def read_subscribers(asset_type, asset_id, asset_path, headers, csv_writer):
    payload = {
        "authentication": {"apiKey": headers['Authorization'].split()[-1]},
        "identifier": {"type": asset_type, "id": asset_id}
    }
    try:
        response = requests.post(SUBSCRIBERS_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if len(data.get('subscribers', [])) == 0:
            file_name = asset_path.split("/")[-1]
            asset_data = read_asset(asset_id, asset_type, headers)
            file_info = asset_data.get('asset', {}).get('file', {})
            name = file_info.get('name', '')
            lastModifiedDate = file_info.get('lastModifiedDate', '')
            createdBy = file_info.get('createdBy', '')
            cms_url = f"https://cmsprod.lamar.edu/entity/open.act?id={asset_id}&type=file"
            csv_writer.writerow([asset_id, file_name, asset_path, name, name, lastModifiedDate, createdBy, cms_url])
    except Exception as e:
        print(f"Error reading subscribers for {asset_id}: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Generate unused assets report from Lamar CMS")
    parser.add_argument("folder_id", help="The ID of the root folder to scan")
    parser.add_argument("--api-key", help="Lamar API key (or set LAMAR_API_KEY env variable)", default=os.getenv("LAMAR_API_KEY"))
    args = parser.parse_args()

    if not args.api_key:
        print("Error: API key must be provided via --api-key or LAMAR_API_KEY", file=sys.stderr)
        sys.exit(1)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {args.api_key}"
    }

    output_path = Path.home() / "Desktop" / "unused_assets_report.csv"
    with open(output_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["id", "file_name", "path", "title", "name", "lastModifiedDate", "createdBy", "cms_url"])
        read_folder(args.folder_id, headers, writer)

    print(f"Report saved to {output_path}")

if __name__ == "__main__":
    main()