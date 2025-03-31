
# Blue Waters Backend API

The backend for **Blue Waters Dashboard** provides real-time water quality analysis and health risk advisory using **IBM WatsonX AI**. This system helps industries, agriculture, and water utilities to monitor water quality parameters and receive automated alerts on water quality and health risks.

## Features
- **Real-time Water Quality Monitoring**
- **Health Risk Alerts** based on water quality data
- **AI-powered Advisory** using WatsonX for water quality and health risks
- **Data endpoints** for water sources, historical data, and quality predictions

## Technologies
- **FastAPI** for the backend
- **WatsonX** for AI-powered analysis
- **IBM Watson API** for authentication and querying models
- **Python 3.x** for backend logic

## Setup Instructions

### Prerequisites
- Python 3.7+
- Environment variables (`.env` file) with the following:
  - `WATSONX_API_KEY`: Your WatsonX API key
  - `WATSONX_PROJECT_ID`: Your WatsonX project ID
  - `WATSONX_URL`: The URL for WatsonX API
- Install required dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Environment Configuration
Create a `.env` file at the root of the project with the following values:

```env
WATSONX_API_KEY=your-watsonx-api-key
WATSONX_PROJECT_ID=your-watsonx-project-id
WATSONX_URL=https://api.dataplatform.cloud.ibm.com
```

### Running the Application

1. **Run the FastAPI Server**:
   ```bash
   uvicorn main:app --reload
   ```
   By default, the backend will be available at `http://127.0.0.1:8000`.

2. **API Documentation**:
   You can access the interactive API docs at `http://127.0.0.1:8000/docs`.

## API Endpoints

### 1. **Water Sources**
   - `GET /water-sources`: Fetch all water sources.
   - `GET /water-source/{source_id}`: Fetch a specific water source by ID.

### 2. **Water Quality Prediction**
   - `GET /quality-predictions/{source_id}`: Fetch quality prediction for a specific water source.

### 3. **Historical Data**
   - `GET /historical-data`: Fetch historical water data.

### 4. **Alerts**
   - `GET /alerts`: Fetch alerts for water quality and health risks.

### 5. **WatsonX Integration**
   - `GET /water-quality-agent`: AI-powered water quality advisory (use the `query` parameter for specific queries).
   - `GET /health-risk-agent`: AI-powered health risk advisory (use the `query` parameter for specific queries).

### Query Examples

#### Example 1: Water Quality Query
```http
GET /water-quality-agent?query=What is the risk of high levels of arsenic in the water?
```

#### Example 2: Health Risk Query
```http
GET /health-risk-agent?query=What are the health risks associated with high nitrate levels in water?
```

### WatsonX API Authentication
To interact with WatsonX, we authenticate using an API key. The following code demonstrates how the token is retrieved and used in the query process:

```python
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("WATSONX_API_KEY")
IAM_URL = "https://iam.cloud.ibm.com/identity/token"

def get_bearer_token():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={API_KEY}"
    
    response = requests.post(IAM_URL, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception("Failed to authenticate with WatsonX")

# Example query to WatsonX
def query_watsonx(prompt: str):
    token = get_bearer_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "model_id": "ibm/granite-3-8b-instruct",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    response = requests.post('https://api.dataplatform.cloud.ibm.com/ml/v1/text/chat', json=payload, headers=headers)
    return response.json()
```

## License

This project is licensed under the MIT License.

