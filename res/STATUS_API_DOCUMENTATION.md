# Candidate Status Management API Documentation

## Overview
Complete API for managing candidate workflow status, notes, tags, and history tracking.

---

## Base URL
All endpoints are prefixed with the Flask application base URL (e.g., `http://localhost:5000`)

---

## Endpoints

### 1. Get Candidate Status
**GET** `/api/candidate/<candidate_id>/status`

Get the current status and metadata for a specific candidate.

**Response:**
```json
{
  "success": true,
  "status": {
    "candidate_id": "john_doe_resume",
    "current_status": "interviewed",
    "history": [...],
    "notes": [...],
    "tags": ["python", "senior"]
  }
}
```

---

### 2. Update Candidate Status
**PUT** `/api/candidate/<candidate_id>/status`

Update a candidate's status with optional note.

**Request Body:**
```json
{
  "status": "shortlisted",
  "note": "Great technical skills",
  "user": "admin"
}
```

**Valid Statuses:**
- `new`
- `reviewed`
- `interviewed`
- `shortlisted`
- `rejected`
- `hired`
- `on_hold`

**Response:**
```json
{
  "success": true,
  "status": {
    "candidate_id": "john_doe_resume",
    "current_status": "shortlisted",
    "history": [
      {
        "from_status": "interviewed",
        "to_status": "shortlisted",
        "timestamp": "2026-01-18T13:30:00",
        "user": "admin",
        "note": "Great technical skills"
      }
    ],
    "notes": [],
    "tags": []
  }
}
```

---

### 3. Add Candidate Note
**POST** `/api/candidate/<candidate_id>/notes`

Add a note/comment to a candidate.

**Request Body:**
```json
{
  "note": "Candidate has excellent communication skills",
  "user": "admin"
}
```

**Response:**
```json
{
  "success": true,
  "note": {
    "text": "Candidate has excellent communication skills",
    "timestamp": "2026-01-18T13:30:00",
    "user": "admin"
  }
}
```

---

### 4. Get Candidate Notes
**GET** `/api/candidate/<candidate_id>/notes`

Get all notes for a candidate.

**Response:**
```json
{
  "success": true,
  "candidate_id": "john_doe_resume",
  "notes": [
    {
      "text": "Candidate has excellent communication skills",
      "timestamp": "2026-01-18T13:30:00",
      "user": "admin"
    }
  ]
}
```

---

### 5. Delete Candidate Note
**DELETE** `/api/candidate/<candidate_id>/notes/<note_index>`

Delete a specific note by index.

**Response:**
```json
{
  "success": true,
  "deleted_note": {...},
  "remaining_notes": [...]
}
```

---

### 6. Update Candidate Tags
**PUT** `/api/candidate/<candidate_id>/tags`

Update tags for a candidate.

**Request Body:**
```json
{
  "tags": ["python", "senior", "remote"]
}
```

**Response:**
```json
{
  "success": true,
  "tags": ["python", "senior", "remote"]
}
```

---

### 7. Get Candidate History
**GET** `/api/candidate/<candidate_id>/history`

Get full status history, notes, and tags for a candidate.

**Response:**
```json
{
  "success": true,
  "candidate_id": "john_doe_resume",
  "current_status": "shortlisted",
  "history": [
    {
      "from_status": "new",
      "to_status": "reviewed",
      "timestamp": "2026-01-18T10:00:00",
      "user": "admin",
      "note": "Initial review"
    },
    {
      "from_status": "reviewed",
      "to_status": "interviewed",
      "timestamp": "2026-01-18T11:00:00",
      "user": "admin",
      "note": "Scheduled interview"
    }
  ],
  "notes": [...],
  "tags": [...]
}
```

---

### 8. Bulk Update Status
**POST** `/api/candidates/bulk-status`

Update status for multiple candidates at once.

**Request Body:**
```json
{
  "candidate_ids": ["john_doe_resume", "jane_smith_resume"],
  "status": "shortlisted",
  "note": "Bulk shortlisted for next round",
  "user": "admin"
}
```

**Response:**
```json
{
  "success": true,
  "updated": 2,
  "failed": 0,
  "updated_ids": ["john_doe_resume", "jane_smith_resume"],
  "failed_ids": []
}
```

---

### 9. Get Candidate Statistics
**GET** `/api/candidates/stats`

Get count of candidates by status.

**Response:**
```json
{
  "success": true,
  "stats": {
    "new": 5,
    "reviewed": 3,
    "interviewed": 2,
    "shortlisted": 4,
    "rejected": 1,
    "hired": 0,
    "on_hold": 0
  },
  "total": 15
}
```

---

### 10. Get All Candidate Statuses
**GET** `/api/candidates/all-statuses`

Get a list of all candidates with their current status.

**Response:**
```json
{
  "success": true,
  "candidates": [
    {
      "id": "john_doe_resume",
      "status": "shortlisted",
      "tags": ["python", "senior"],
      "notes_count": 2,
      "last_updated": "2026-01-18T13:30:00"
    }
  ],
  "total": 15
}
```

---

### 11. Get Candidates by Status
**GET** `/api/candidates/by-status/<status>`

Get all candidates with a specific status.

**Example:** `/api/candidates/by-status/shortlisted`

**Response:**
```json
{
  "success": true,
  "status": "shortlisted",
  "candidates": [
    {
      "id": "john_doe_resume",
      "status": "shortlisted",
      "tags": ["python", "senior"],
      "notes": [...],
      "history": [...]
    }
  ],
  "count": 4
}
```

---

### 12. Search Candidates
**POST** `/api/candidates/search`

Search candidates by ID, status, or tags.

**Request Body:**
```json
{
  "query": "john",
  "status": "shortlisted",
  "tags": ["python"]
}
```

**Response:**
```json
{
  "success": true,
  "candidates": [
    {
      "id": "john_doe_resume",
      "status": "shortlisted",
      "tags": ["python", "senior"],
      "notes_count": 2,
      "last_updated": "2026-01-18T13:30:00"
    }
  ],
  "count": 1
}
```

---

### 13. Get Valid Statuses
**GET** `/api/status/valid-statuses`

Get list of all valid status values.

**Response:**
```json
{
  "success": true,
  "statuses": ["new", "reviewed", "interviewed", "shortlisted", "rejected", "hired", "on_hold"]
}
```

---

### 14. Delete Candidate Data
**DELETE** `/api/candidate/<candidate_id>`

Delete all status data for a candidate (status, history, notes, tags).

**Response:**
```json
{
  "success": true,
  "message": "Deleted status data for john_doe_resume"
}
```

---

## Data Models

### Status Data Structure
```json
{
  "candidate_id": "string",
  "current_status": "string (one of VALID_STATUSES)",
  "history": [
    {
      "from_status": "string",
      "to_status": "string",
      "timestamp": "ISO 8601 datetime",
      "user": "string",
      "note": "string"
    }
  ],
  "notes": [
    {
      "text": "string",
      "timestamp": "ISO 8601 datetime",
      "user": "string"
    }
  ],
  "tags": ["string"]
}
```

---

## Error Responses

All endpoints return errors in this format:

```json
{
  "success": false,
  "error": "Error message description"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found (candidate doesn't exist)
- `500` - Internal Server Error

---

## Usage Examples

### JavaScript/Fetch

```javascript
// Get candidate status
const response = await fetch('/api/candidate/john_doe_resume/status');
const data = await response.json();

// Update status
await fetch('/api/candidate/john_doe_resume/status', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    status: 'shortlisted',
    note: 'Great candidate',
    user: 'admin'
  })
});

// Add note
await fetch('/api/candidate/john_doe_resume/notes', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    note: 'Follow up next week',
    user: 'admin'
  })
});

// Bulk update
await fetch('/api/candidates/bulk-status', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    candidate_ids: ['john_doe_resume', 'jane_smith_resume'],
    status: 'rejected',
    user: 'admin'
  })
});
```

---

## Storage

All candidate status data is stored in JSON files in the `candidate_data/` directory:
- Format: `{candidate_id}_status.json`
- Example: `john_doe_resume_status.json`

---

## Best Practices

1. **Always include user**: Track who made changes for audit trail
2. **Add notes on status changes**: Provide context for decisions
3. **Use tags for categorization**: Makes filtering easier
4. **Check valid statuses**: Use `/api/status/valid-statuses` endpoint
5. **Handle errors gracefully**: Check `success` field in responses

---

## Integration Tips

### Frontend Integration
```javascript
// Create a status management service
const StatusService = {
  async updateStatus(candidateId, status, note) {
    const response = await fetch(`/api/candidate/${candidateId}/status`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status, note, user: 'admin' })
    });
    return response.json();
  },
  
  async getStats() {
    const response = await fetch('/api/candidates/stats');
    return response.json();
  },
  
  async bulkUpdate(candidateIds, status) {
    const response = await fetch('/api/candidates/bulk-status', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ candidate_ids: candidateIds, status, user: 'admin' })
    });
    return response.json();
  }
};
```

---

## Testing

### Test with cURL

```bash
# Get status
curl http://localhost:5000/api/candidate/john_doe_resume/status

# Update status
curl -X PUT http://localhost:5000/api/candidate/john_doe_resume/status \
  -H "Content-Type: application/json" \
  -d '{"status":"shortlisted","note":"Great candidate","user":"admin"}'

# Get stats
curl http://localhost:5000/api/candidates/stats

# Bulk update
curl -X POST http://localhost:5000/api/candidates/bulk-status \
  -H "Content-Type: application/json" \
  -d '{"candidate_ids":["john_doe_resume"],"status":"hired","user":"admin"}'
```

---

## Changelog

### Version 1.0.0 (2026-01-18)
- Initial release
- 14 comprehensive endpoints
- Full CRUD operations for status, notes, and tags
- Bulk operations support
- Search and filter capabilities
- Statistics and analytics
