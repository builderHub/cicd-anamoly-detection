import os
import requests
import pandas as pd

# Jenkins Configuration
JENKINS_URL = "http://localhost:8080"
USER = "admin"
API_TOKEN = "119897c7b933dc85a0e750e3fd7f1876ed"

# API to list all jobs
JOBS_API = f"{JENKINS_URL}/api/json?tree=jobs[name,url]"

# Authenticate and fetch all jobs
response = requests.get(JOBS_API, auth=(USER, API_TOKEN))

if response.status_code == 200:
    jobs = response.json().get('jobs', [])
    
    all_build_data = []
    
    for job in jobs:
        job_name = job['name']
        job_url = job['url']
        builds_api = f"{job_url}/api/json?tree=builds[number,result,duration,timestamp,actions[totalCount,failCount]]&depth=1"
        
        build_response = requests.get(builds_api, auth=(USER, API_TOKEN))
        
        if build_response.status_code == 200:
            builds = build_response.json().get('builds', [])
            
            for build in builds:
                build_number = build.get("number")
                result = 1 if build.get("result") == "SUCCESS" else 0
                duration = build.get("duration") / 1000  # Convert to seconds
                test_data = next((action for action in build.get("actions", []) if "failCount" in action), {})
                fail_count = test_data.get("failCount", 0)
                total_tests = test_data.get("totalCount", 1)
                test_pass_rate = ((total_tests - fail_count) / total_tests) * 100 if total_tests > 0 else 100

                all_build_data.append([job_name, build_number, duration, fail_count, test_pass_rate, result])

    # Convert to DataFrame
    df = pd.DataFrame(all_build_data, columns=["job_name", "build_number", "build_duration", "previous_failures", "test_pass_rate", "build_status"])
    
    # Save dataset
    os.makedirs("resources", exist_ok=True)
    df.to_csv("resources/all_jenkins_builds.csv", index=False)
    
    print("✅ Jenkins build data for all jobs saved to all_jenkins_builds.csv")

else:
    print(f"❌ Failed to fetch job list from Jenkins. Status Code: {response.status_code}")

