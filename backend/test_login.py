"""
Script de teste para verificar o formato da resposta da API de login
"""
import httpx
import os
from dotenv import load_dotenv
import json

load_dotenv()

url = "https://gateway.isolarcloud.com.hk/openapi/login"
headers = {
    "Content-Type": "application/json",
    "x-access-key": os.getenv("API_ACCESS_KEY"),
    "sys_code": "901"
}
data = {
    "appkey": os.getenv("API_APPKEY"),
    "user_account": os.getenv("USER_ACCOUNT"),
    "user_password": os.getenv("USER_PASSWORD"),
}

print("=" * 60)
print("Testing Login API")
print("=" * 60)
print(f"\nURL: {url}")
print(f"AppKey: {data['appkey'][:10]}...")
print(f"User: {data['user_account']}")
print(f"Access Key: {headers['x-access-key'][:10]}...")
print("\n" + "=" * 60)

try:
    response = httpx.post(url, json=data, headers=headers, timeout=30.0)
    response.raise_for_status()
    response_data = response.json()

    print("\n✅ Response received!")
    print("\nFull Response:")
    print(json.dumps(response_data, indent=2))

    print("\n" + "=" * 60)
    print("Response Analysis:")
    print("=" * 60)
    print(f"result_code: {response_data.get('result_code')}")
    print(f"result_msg: {response_data.get('result_msg')}")

    # Try to find token in different locations
    token = None
    if 'result_data' in response_data and isinstance(response_data['result_data'], dict):
        token = response_data['result_data'].get('token')
        print(f"\nToken location: response_data['result_data']['token']")
    elif 'token' in response_data:
        token = response_data.get('token')
        print(f"\nToken location: response_data['token']")

    if token:
        print(f"Token: {token[:50]}... (truncated)")
        print(f"Token length: {len(token)}")
    else:
        print("\n❌ No token found in response!")

except httpx.HTTPError as e:
    print(f"\n❌ HTTP Error: {e}")
except Exception as e:
    print(f"\n❌ Unexpected Error: {e}")

