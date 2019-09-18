import pd
import csv
import json
import argparse
import os.path
import sys
from datetime import datetime, timedelta

parser = argparse.ArgumentParser()
parser.add_argument("pd_api_key", help="PagerDuty API key")
parser.add_argument("csv_output_file", help="CSV file to write to")
args = parser.parse_args()

if os.path.exists(args.csv_output_file):
    print(f"Oops, {args.csv_output_file} already exists... exiting.")
    sys.exit(1)

def ts_string(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")

since = ts_string(datetime.utcnow() - timedelta(days=30))

print(f"Getting incidents since {since}")
incidents = pd.fetch(
    api_key=args.pd_api_key, 
    endpoint="incidents", 
    params={
        "limit": 100,
        "since": since, 
        "statuses[]": ["triggered", "acknowledged", "resolved"],
        "include[]": ["first_trigger_log_entries"]
    }
)

print(f"Got {len(incidents)} incidents")

csv_data = []

for incident in incidents:
    incident_key = ""
    try:
        incident_key = incident['first_trigger_log_entry']['channel']['incident_key'] or ""
    except:
        pass

    geneos_path = ""
    try:
        geneos_path = incident['first_trigger_log_entry']['channel']['details']['Geneos Event Data']['_VARIABLEPATH']
    except:
        pass

    csv_data.append([
        incident['id'],
        incident['status'],
        incident['created_at'],
        incident['last_status_change_at'],
        geneos_path,
        incident_key
    ])

csv_headers = [
    "Incident ID",
    "Status",
    "Created At",
    "Last Update",
    "Geneos Path",
    "Incident Key"
]

with open(args.csv_output_file, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(csv_headers)
    writer.writerows(csv_data)