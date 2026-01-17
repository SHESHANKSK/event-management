import requests
import time
import uuid

def run_csv_tests():
    base_url = "http://127.0.0.1:8000"
    
    # Wait for server
    time.sleep(2)
    
    print("\n--- Testing CSV Upload ---")

    # 1. Create Event
    print("Creating Event...")
    event_data = {
        "event_name": "CSV Test Event",
        "event_date": "2025-12-31",
        "organizing_team": "QA",
        "event_status": "TODO"
    }
    r = requests.post(base_url + "/events", json=event_data)
    assert r.status_code == 201
    event_id = r.json()['event_id']

    # 2. Upload CSV
    # 2. Upload CSV
    print("Uploading CSV from oopat.csv...")
    try:
        with open(r"f:\event-management\oopat.csv", "rb") as f:
            files = {'file': ('oopat.csv', f, 'text/csv')}
            r = requests.post(base_url + f"/attendance/upload/{event_id}", files=files)
            
        print(r.status_code)
        if r.status_code != 200:
            print(r.json())
            
        assert r.status_code == 200
        records = r.json()
        print(f"Uploaded {len(records)} records.")
        
        # Verify Stats
        print("Verifying Event Stats...")
        r_event = requests.get(base_url + f"/events/{event_id}")
        assert r_event.status_code == 200
        event_details = r_event.json()
        print("Event Details:", event_details)
        
        assert event_details['participants_count'] == 45
        assert event_details['average_duration'] > 0
        
        print("PASS: CSV Upload & Stats Calculation")

    except FileNotFoundError:
        print("oopat.csv not found. Skipping test.")

    # 3. Test Invalid CSV (Wrong extension)
    print("Testing Invalid Extension...")
    files = {'file': ('test.txt', 'junk', 'text/plain')}
    r = requests.post(base_url + f"/attendance/upload/{event_id}", files=files)
    assert r.status_code == 400
    print("PASS: Extension Check")

    print("\nALL CSV TESTS PASSED")

if __name__ == "__main__":
    run_csv_tests()
