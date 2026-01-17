import requests
import time
import subprocess
import sys
import os
import signal

def run_tests():
    base_url = "http://127.0.0.1:8000"
    
    # Wait for server
    time.sleep(5)
    
    print("Testing GET /")
    try:
        r = requests.get(base_url + "/")
        print(r.json())
        assert r.status_code == 200
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    print("\nTesting GET /users/me - EXPECTING 404 (Removed)")
    r = requests.get(base_url + "/users/me")
    print(r.status_code)
    assert r.status_code == 404

    print("\nTesting Create Event (POST /events)")
    event_data = {
        "event_name": "Q1 Planning",
        "event_description": "First quarter planning session",
        "event_date": "2026-02-01",
        "organizing_team": "Exec"
    }
    r = requests.post(base_url + "/events", json=event_data)
    print(r.status_code, r.json())
    assert r.status_code == 201
    event_id = r.json()['event_id']

    print("\nTesting Get Event")
    r = requests.get(base_url + f"/events/{event_id}")
    assert r.status_code == 200
    assert r.json()['event_status'] == "TODO"

    print("\nTesting Update Event (PUT /events)")
    update_data = {
        "event_status": "IN_PROGRESS"
    }
    r = requests.put(base_url + f"/events/{event_id}", json=update_data)
    print(r.status_code, r.json())
    assert r.status_code == 200
    assert r.json()['event_status'] == "IN_PROGRESS"



    print("\nTesting Cancel Event (DELETE /events)")
    r = requests.delete(base_url + f"/events/{event_id}")
    print(r.status_code, r.json())
    assert r.status_code == 200
    assert r.json()['event_status'] == "CANCELLED"

    print("\nALL TESTS PASSED")

if __name__ == "__main__":
    # Server is started externally
    run_tests()
