import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_rbac():
    print("🧪 Testing RBAC Implementation...")
    
    # Test data
    users = {
        "admin": {"email": "admin@example.com", "password": "admin123"},
        "maintainer": {"email": "maintainer@example.com", "password": "maintainer123"},
        "reporter": {"email": "reporter@example.com", "password": "reporter123"}
    }
    
    tokens = {}
    
    # 1. Login all users
    print("\n1️⃣ Logging in users...")
    for role, credentials in users.items():
        response = requests.post(f"{BASE_URL}/auth/login", json=credentials)
        if response.status_code == 200:
            tokens[role] = response.json()["access_token"]
            print(f"✅ {role.upper()} logged in successfully")
        else:
            print(f"❌ {role.upper()} login failed: {response.text}")
            return
    
    # 2. Test issue creation (all roles should be able to create)
    print("\n2️⃣ Testing issue creation...")
    issue_data = {
        "title": "Test Issue",
        "description": "Test description",
        "severity": "MEDIUM",
        "priority": "MINOR",
        "tags": ["test", "rbac"]
    }
    
    created_issues = {}
    for role, token in tokens.items():
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/issues/", data=issue_data, headers=headers)
        if response.status_code == 200:
            created_issues[role] = response.json()
            print(f"✅ {role.upper()} created issue successfully")
        else:
            print(f"❌ {role.upper()} failed to create issue: {response.text}")
    
    # 3. Test issue listing (REPORTER should only see their own)
    print("\n3️⃣ Testing issue listing...")
    for role, token in tokens.items():
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/issues/", headers=headers)
        if response.status_code == 200:
            issues = response.json()
            if role == "reporter":
                if len(issues) == 1:
                    print(f"✅ {role.upper()} sees only their own issue ({len(issues)} issue)")
                else:
                    print(f"❌ {role.upper()} should see only 1 issue, but sees {len(issues)}")
            else:
                if len(issues) >= 3:
                    print(f"✅ {role.upper()} sees all issues ({len(issues)} issues)")
                else:
                    print(f"❌ {role.upper()} should see all issues, but sees {len(issues)}")
        else:
            print(f"❌ {role.upper()} failed to list issues: {response.text}")
    
    # 4. Test triage endpoint (only MAINTAINER and ADMIN)
    print("\n4️⃣ Testing triage endpoint...")
    if "maintainer" in created_issues:
        issue_id = created_issues["reporter"]["id"]
        triage_data = {
            "status": "TRIAGED",
            "tags": ["triaged", "urgent"]
        }
        
        # Test MAINTAINER can triage
        headers = {"Authorization": f"Bearer {tokens['maintainer']}"}
        response = requests.patch(f"{BASE_URL}/issues/{issue_id}/triage", json=triage_data, headers=headers)
        if response.status_code == 200:
            print("✅ MAINTAINER can triage issues")
        else:
            print(f"❌ MAINTAINER cannot triage: {response.text}")
        
        # Test ADMIN can triage
        headers = {"Authorization": f"Bearer {tokens['admin']}"}
        response = requests.patch(f"{BASE_URL}/issues/{issue_id}/triage", json=triage_data, headers=headers)
        if response.status_code == 200:
            print("✅ ADMIN can triage issues")
        else:
            print(f"❌ ADMIN cannot triage: {response.text}")
        
        # Test REPORTER cannot triage
        headers = {"Authorization": f"Bearer {tokens['reporter']}"}
        response = requests.patch(f"{BASE_URL}/issues/{issue_id}/triage", json=triage_data, headers=headers)
        if response.status_code == 403:
            print("✅ REPORTER correctly blocked from triage")
        else:
            print(f"❌ REPORTER should be blocked from triage: {response.status_code}")
    
    # 5. Test delete endpoint (only ADMIN)
    print("\n5️⃣ Testing delete endpoint...")
    if "reporter" in created_issues:
        issue_id = created_issues["reporter"]["id"]
        
        # Test ADMIN can delete
        headers = {"Authorization": f"Bearer {tokens['admin']}"}
        response = requests.delete(f"{BASE_URL}/issues/{issue_id}", headers=headers)
        if response.status_code == 204:
            print("✅ ADMIN can delete issues")
        else:
            print(f"❌ ADMIN cannot delete: {response.text}")
        
        # Test MAINTAINER cannot delete
        headers = {"Authorization": f"Bearer {tokens['maintainer']}"}
        response = requests.delete(f"{BASE_URL}/issues/{issue_id}", headers=headers)
        if response.status_code == 403:
            print("✅ MAINTAINER correctly blocked from delete")
        else:
            print(f"❌ MAINTAINER should be blocked from delete: {response.status_code}")
        
        # Test REPORTER cannot delete
        headers = {"Authorization": f"Bearer {tokens['reporter']}"}
        response = requests.delete(f"{BASE_URL}/issues/{issue_id}", headers=headers)
        if response.status_code == 403:
            print("✅ REPORTER correctly blocked from delete")
        else:
            print(f"❌ REPORTER should be blocked from delete: {response.status_code}")
    
    print("\n🎉 RBAC Testing Complete!")

if __name__ == "__main__":
    test_rbac() 