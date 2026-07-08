"""
Test script for Candidate Status Management API
Tests all endpoints to ensure they're working correctly
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def print_result(test_name, response):
    """Print test result"""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        return data
    except:
        print(f"Response: {response.text}")
        return None

def test_api():
    """Run all API tests"""
    test_candidate_id = f"test_candidate_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    print(f"\n🚀 Starting API Tests")
    print(f"Test Candidate ID: {test_candidate_id}")
    
    # Test 1: Get valid statuses
    response = requests.get(f"{BASE_URL}/api/status/valid-statuses")
    data = print_result("Get Valid Statuses", response)
    
    # Test 2: Get candidate status (should create new)
    response = requests.get(f"{BASE_URL}/api/candidate/{test_candidate_id}/status")
    data = print_result("Get Candidate Status (New)", response)
    
    # Test 3: Update candidate status
    response = requests.put(
        f"{BASE_URL}/api/candidate/{test_candidate_id}/status",
        json={
            "status": "reviewed",
            "note": "Initial review completed",
            "user": "test_admin"
        }
    )
    data = print_result("Update Status to 'reviewed'", response)
    
    # Test 4: Add a note
    response = requests.post(
        f"{BASE_URL}/api/candidate/{test_candidate_id}/notes",
        json={
            "note": "Candidate has strong Python skills",
            "user": "test_admin"
        }
    )
    data = print_result("Add Note", response)
    
    # Test 5: Add another note
    response = requests.post(
        f"{BASE_URL}/api/candidate/{test_candidate_id}/notes",
        json={
            "note": "Good communication skills demonstrated",
            "user": "test_admin"
        }
    )
    data = print_result("Add Second Note", response)
    
    # Test 6: Get all notes
    response = requests.get(f"{BASE_URL}/api/candidate/{test_candidate_id}/notes")
    data = print_result("Get All Notes", response)
    
    # Test 7: Update tags
    response = requests.put(
        f"{BASE_URL}/api/candidate/{test_candidate_id}/tags",
        json={
            "tags": ["python", "senior", "remote"]
        }
    )
    data = print_result("Update Tags", response)
    
    # Test 8: Update status again
    response = requests.put(
        f"{BASE_URL}/api/candidate/{test_candidate_id}/status",
        json={
            "status": "interviewed",
            "note": "Technical interview completed",
            "user": "test_admin"
        }
    )
    data = print_result("Update Status to 'interviewed'", response)
    
    # Test 9: Get full history
    response = requests.get(f"{BASE_URL}/api/candidate/{test_candidate_id}/history")
    data = print_result("Get Full History", response)
    
    # Test 10: Get candidate stats
    response = requests.get(f"{BASE_URL}/api/candidates/stats")
    data = print_result("Get Candidate Statistics", response)
    
    # Test 11: Get all candidate statuses
    response = requests.get(f"{BASE_URL}/api/candidates/all-statuses")
    data = print_result("Get All Candidate Statuses", response)
    
    # Test 12: Get candidates by status
    response = requests.get(f"{BASE_URL}/api/candidates/by-status/interviewed")
    data = print_result("Get Candidates by Status (interviewed)", response)
    
    # Test 13: Search candidates
    response = requests.post(
        f"{BASE_URL}/api/candidates/search",
        json={
            "query": "test",
            "status": "interviewed",
            "tags": ["python"]
        }
    )
    data = print_result("Search Candidates", response)
    
    # Test 14: Bulk update (create another test candidate first)
    test_candidate_id_2 = f"test_candidate_2_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Create second candidate
    requests.put(
        f"{BASE_URL}/api/candidate/{test_candidate_id_2}/status",
        json={"status": "reviewed", "user": "test_admin"}
    )
    
    # Bulk update both
    response = requests.post(
        f"{BASE_URL}/api/candidates/bulk-status",
        json={
            "candidate_ids": [test_candidate_id, test_candidate_id_2],
            "status": "shortlisted",
            "note": "Bulk shortlisted for final round",
            "user": "test_admin"
        }
    )
    data = print_result("Bulk Update Status", response)
    
    # Test 15: Delete a note
    response = requests.delete(f"{BASE_URL}/api/candidate/{test_candidate_id}/notes/0")
    data = print_result("Delete First Note", response)
    
    # Test 16: Final status check
    response = requests.get(f"{BASE_URL}/api/candidate/{test_candidate_id}/status")
    data = print_result("Final Status Check", response)
    
    print(f"\n{'='*60}")
    print("✅ All tests completed!")
    print(f"\nTest candidates created:")
    print(f"  - {test_candidate_id}")
    print(f"  - {test_candidate_id_2}")
    print(f"\nTo clean up, you can delete them using:")
    print(f"  DELETE /api/candidate/{test_candidate_id}")
    print(f"  DELETE /api/candidate/{test_candidate_id_2}")
    
    # Optional: Clean up test data
    cleanup = input("\nDo you want to clean up test data? (y/n): ")
    if cleanup.lower() == 'y':
        response = requests.delete(f"{BASE_URL}/api/candidate/{test_candidate_id}")
        print(f"Deleted {test_candidate_id}: {response.json()}")
        
        response = requests.delete(f"{BASE_URL}/api/candidate/{test_candidate_id_2}")
        print(f"Deleted {test_candidate_id_2}: {response.json()}")
        
        print("✅ Cleanup completed!")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print("Make sure the Flask server is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
