import requests
import time
import uuid

def run_user_tests():
    base_url = "http://127.0.0.1:8000"
    
    # Wait for server
    time.sleep(2)
    
    print("\n--- Testing User CRUD ---")

    # 1. Test Get Current User (Fix Verification)
    print("Testing GET /users/{username}")
    r = requests.get(base_url + "/users/testadmin")
    print(r.status_code, r.json())
    assert r.status_code == 200
    me = r.json()
    assert me['username'] == 'testadmin'
    assert me['is_active'] == True
    print("PASS: /users/testadmin")

    # 2. Create User
    print("\nTesting Create User (POST /users)")
    new_user = {
        "username": "crudtest",
        "first_name": "Crud",
        "last_name": "Test",
        "email": "crud@test.com",
        "country_code": "US",
        "roles": ["editor"]
    }
    r = requests.post(base_url + "/users", json=new_user)
    print(r.status_code, r.json())
    assert r.status_code == 201
    user_id = r.json()['uid']
    print("PASS: Create User")

    # 3. Update User
    print("\nTesting Update User (PUT /users/{id})")
    update_data = {
        "first_name": "UpdatedName",
        "roles": ["editor", "admin"]
    }
    r = requests.put(base_url + f"/users/{user_id}", json=update_data)
    print(r.status_code, r.json())
    assert r.status_code == 200
    assert r.json()['first_name'] == "UpdatedName"
    assert "admin" in r.json()['roles']
    print("PASS: Update User")

    # 4. Soft Delete User
    print("\nTesting Delete User (DELETE /users/{id})")
    r = requests.delete(base_url + f"/users/{user_id}")
    print(r.status_code, r.json())
    assert r.status_code == 200
    assert r.json()['is_active'] == False
    print("PASS: Delete User (Soft Delete)")

    print("\nALL USER TESTS PASSED")

if __name__ == "__main__":
    run_user_tests()
