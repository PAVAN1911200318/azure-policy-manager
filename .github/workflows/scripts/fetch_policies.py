import requests
from bs4 import BeautifulSoup
import os
import re

BASE_URL = "https://learn.microsoft.com"
SAMPLES_PAGE = "https://learn.microsoft.com/en-us/azure/governance/policy/samples"

def fetch_initiatives():
    response = requests.get(SAMPLES_PAGE)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.select("a[href$='.json']")
    initiatives = {}

    for link in links:
        href = link['href']
        full_url = BASE_URL + href
        text = link.text.strip()

        # Extract Initiative Name (folder) and Policy Name (file)
        match = re.search(r'initiatives/(.+?)/(.+?\.json)', href)
        if match:
            initiative_name = match.group(1).replace('-', '_')
            policy_filename = match.group(2)
            initiatives.setdefault(initiative_name, []).append((policy_filename, full_url))

    return initiatives

def save_policies(initiatives):
    os.makedirs('azure_compliance_policies', exist_ok=True)

    for initiative, policies in initiatives.items():
        initiative_path = os.path.join("azure_compliance_policies", initiative)
        os.makedirs(initiative_path, exist_ok=True)

        for filename, url in policies:
            response = requests.get(url)
            file_path = os.path.join(initiative_path, filename)
            with open(file_path, 'w') as f:
                f.write(response.text)

def list_initiatives_and_policies(initiatives):
    print("\nAvailable Initiatives:\n")
    for i, (initiative, policies) in enumerate(initiatives.items(), start=1):
        print(f"{i}. {initiative}")
        for j, (filename, _) in enumerate(policies, start=1):
            print(f"    {j}. {filename}")

if __name__ == "__main__":
    initiatives = fetch_initiatives()
    list_initiatives_and_policies(initiatives)
    save_policies(initiatives)
    print("\n✅ All initiatives and policies downloaded successfully!")
