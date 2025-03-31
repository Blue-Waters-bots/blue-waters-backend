import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
IAM_URL = "https://iam.cloud.ibm.com/identity/token"
WX_API_BASE_URL = "https://api.dataplatform.cloud.ibm.com"

def get_iam_token():
    """Fetch IBM Cloud IAM token using API key."""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "apikey": API_KEY,
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
    }
    response = requests.post(IAM_URL, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def list_agents():
    """List all agents in a Watsonx project."""
    token = get_iam_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    url = f"{WX_API_BASE_URL}/v2/agents?project_id={PROJECT_ID}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch agents: {str(e)}")

# Example usage
if __name__ == "__main__":
    try:
        agents = list_agents()
        print("Agents in project:")
        for agent in agents.get("resources", []):
            print(f"- ID: {agent['metadata']['guid']}, Name: {agent['entity']['name']}")
    except Exception as e:
        print(f"Error: {e}")