import json
import os

import requests
from pathlib import Path
from dotenv import load_dotenv

# Pra usar as informações do .env
env_path = Path(__file__).resolve().parents[1] / "api" / "config" / ".env"
load_dotenv(env_path)

# Muda o base_dir para acessar corretamente a pasta test_cases
BASE_DIR = Path(__file__).resolve().parent
TEST_CASES_DIR = BASE_DIR / "test_cases"

API_BASE_URL=os.getenv("API_BASE_URL", "http://localhost:8000")

def load_test_case(filename: str) -> dict:
    file_path = TEST_CASES_DIR / filename
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f) 

def test_agent_endpoint_apple():
    test_case = load_test_case("apple_test.json")
    
    response = requests.post(
        f"{API_BASE_URL}/agent", json={"query": test_case["query"], "limit":3}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == test_case["expected_ticker"]
    assert "fundamental_analysis" in data
    assert "momentum_analysis" in data
    assert "sentiment_analysis" in data
    assert "final_recommendation" in data
    
def test_agent_endpoint_ibm():
    test_case = load_test_case("ibm_test.json")
    
    response = requests.post(
        f"{API_BASE_URL}/agent", json={"query": test_case["query"], "limit":3}
    )
    
    if response.status_code != 200:
        print(f"\nError response: {response.json()}")
        
    assert response.status_code == 200    
    data = response.json()
    
    assert data["ticker"] == test_case["expected_ticker"]
    # assert "fundamental_analysis" in data
    # assert "momentum_analysis" in data
    # assert "sentiment_analysis" in data
    # assert "final_recomendation" in data
    
def test_agent_endpoint_no_company():
    test_case = load_test_case("no_company_test.json")
    
    response = requests.post(
        f"{API_BASE_URL}/agent", json={"query": test_case["query"], "limit": 3}
    )
    
    assert response.status_code == 400
    
def test_agent_endpoint_natural_language():
    test_case = load_test_case("natural_language_test.json")
    
    response = requests.post(
        f"{API_BASE_URL}/agent", json={"query": test_case["query"], "limit": 3}
    )
    
    if response.status_code != 200:
        print(f"\nError response: {response.json()}")
        
    assert response.status_code == 200    
    data = response.json()
    assert data["ticker"] == test_case["expected_ticker"]
    assert data["final_recommendation"]["action"] in ["BUY", "HOLD", "SELL"]
    
    # rodar com pytest
    # pytest level2-integration-tests.py -v