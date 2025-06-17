# runner.py

# import sys

# if len(sys.argv) < 2:
#     print("No Python code provided.")
#     sys.exit(1)

# code_str = sys.argv[1]

# try:
#     exec(code_str)
# except Exception as e:
#     print(f"Error executing code: {e}")

import requests
import json
from datetime import datetime

# Define the search parameters
search_terms = ["H. pylori", "acne vulgaris"]
start_date_range = ("2018-01-01", "2018-05-31")

# Construct the API endpoint
base_url = "https://clinicaltrials.gov/api/v2/studies"

# Define the query parameters
params = {
    "query.cond": " AND ".join(search_terms),
    "fields": "NCTId,BriefTitle,StartDate,EnrollmentCount,Condition,StudyType",
    "format": "json",
    "pageSize": 100
}

# Send the GET request to ClinicalTrials.gov
response = requests.get(base_url, params=params)

# Check for successful response
if response.status_code != 200:
    print(f"Failed to fetch data: {response.status_code}")
    print(response.text)
    exit(1)

# Parse the JSON response
data = response.json()
print(data)
# Save raw results to a local JSON file for debugging (optional)
with open("step1_raw_response.json", "w") as f:
    json.dump(data, f, indent=2)

# Extract study records
studies = data.get("studies", [])

print(f"Found {len(studies)} candidate studies.")
print("\nSample Output:")
for study in studies[:3]:  # Display first 3 for preview
    print(json.dumps(study, indent=2))