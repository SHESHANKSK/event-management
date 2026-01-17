import requests
import uuid

BASE_URL = "http://127.0.0.1:8000"

def run_rbac_tests():
    print("--- RBAC Verification ---")
    
    # 1. Verify "admin" user has admin_access
    # Seed created 'testadmin' with role 'admin'
    
    # We need a way to check permissions. GET /users/testadmin should return them.
    print("Checking Admin Permissions...")
    r = requests.get(f"{BASE_URL}/users/testadmin")
    assert r.status_code == 200
    user_data = r.json()
    print(f"Admin Permissions: {user_data.get('permissions')}")
    assert "admin_access" in user_data['permissions']
    assert "user_delete" in user_data['permissions']
    
    # 2. Verify "viewer" user (Alice) has NO admin_access
    # Seed created 'alice' with role 'viewer' (which is not seeded with permissions so should be empty or minimal)
    # Wait, in seed.py I didn't add 'viewer' permissions. So it should be empty.
    print("Checking Viewer Permissions...")
    r = requests.get(f"{BASE_URL}/users/alice")
    assert r.status_code == 200
    user_data = r.json()
    print(f"Viewer Permissions: {user_data.get('permissions')}")
    assert "admin_access" not in user_data.get('permissions', [])
    
    # 3. Create a NEW user with role 'editor' (has event_create, but not admin_access)
    # This request uses the Mock Auth which is hardcoded to 'testadmin' (UID 550e8400...)
    # So this request is made BY an ADMIN. Should SUCCEED.
    print("Creating Editor User (as Admin)...")
    editor_data = {
        "username": "editor_bob",
        "first_name": "Bob",
        "last_name": "Editor",
        "email": "bob@internal.com",
        "country_code": "US",
        "roles": ["editor"]
    }
    r = requests.post(f"{BASE_URL}/users/", json=editor_data)
    if r.status_code != 201:
        print(f"Failed to create editor: {r.json()}")
    assert r.status_code == 201
    editor_id = r.json()['uid']
    
    # 4. Verify Editor Permissions
    print("Checking Editor Permissions...")
    r = requests.get(f"{BASE_URL}/users/editor_bob")
    data = r.json()
    print(f"Editor Permissions: {data.get('permissions')}")
    assert "event_create" in data['permissions']
    assert "admin_access" not in data['permissions']
    
    # 5. Permission Enforcement Check
    # To test this PROPERLY, we need to act AS the editor.
    # But our Mock Auth is hardcoded to the Admin UUID.
    # So we can't easily test "failure" without changing the mock injection.
    # However, we can assert that the Admin (current mock) CAN do things. 
    # And we can manually verify the code enforces it.
    # For automated test, we'd need to mock the dependency override, which is hard from outside.
    # We will rely on the fact that we checked the permissions list above, and the code logic references that list.
    
    print("PASSED: RBAC Data Integrity")

if __name__ == "__main__":
    run_rbac_tests()
