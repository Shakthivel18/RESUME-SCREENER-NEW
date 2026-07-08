"""
Candidate Status Management API
Handles candidate workflow status tracking and history
"""

from flask import Blueprint, request, jsonify
import os
import json
from datetime import datetime

status_bp = Blueprint('status', __name__)

# Status workflow
VALID_STATUSES = ['new', 'reviewed', 'interviewed', 'shortlisted', 'rejected', 'hired', 'on_hold', 'finalized']

def get_status_file(candidate_id):
    """Get the status file path for a candidate"""
    os.makedirs('candidate_data', exist_ok=True)
    return f'candidate_data/{candidate_id}_status.json'

def load_candidate_status(candidate_id):
    """Load candidate status data"""
    try:
        filepath = get_status_file(candidate_id)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return {
            'candidate_id': candidate_id,
            'current_status': 'new',
            'history': [],
            'notes': [],
            'tags': []
        }
    except Exception as e:
        print(f"Error loading status: {e}")
        return None

def save_candidate_status(candidate_id, status_data):
    """Save candidate status data"""
    try:
        filepath = get_status_file(candidate_id)
        with open(filepath, 'w') as f:
            json.dump(status_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving status: {e}")
        return False

@status_bp.route('/api/candidate/<candidate_id>/status', methods=['GET'])
def get_candidate_status(candidate_id):
    """Get candidate status"""
    status_data = load_candidate_status(candidate_id)
    if status_data:
        return jsonify({'success': True, 'status': status_data}), 200
    return jsonify({'success': False, 'error': 'Status not found'}), 404

@status_bp.route('/api/candidate/<candidate_id>/status', methods=['PUT'])
def update_candidate_status(candidate_id):
    """Update candidate status"""
    try:
        data = request.get_json() or {}
        new_status = data.get('status', '').lower()
        note = data.get('note', '')
        user = data.get('user', 'system')
        
        if new_status not in VALID_STATUSES:
            return jsonify({'success': False, 'error': f'Invalid status. Must be one of: {", ".join(VALID_STATUSES)}'}), 400
        
        # Load current status
        status_data = load_candidate_status(candidate_id)
        
        # Add to history
        history_entry = {
            'from_status': status_data['current_status'],
            'to_status': new_status,
            'timestamp': datetime.now().isoformat(),
            'user': user,
            'note': note
        }
        status_data['history'].append(history_entry)
        
        # Update current status
        status_data['current_status'] = new_status
        
        # Save
        if save_candidate_status(candidate_id, status_data):
            return jsonify({'success': True, 'status': status_data}), 200
        
        return jsonify({'success': False, 'error': 'Failed to save status'}), 500
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@status_bp.route('/api/candidate/<candidate_id>/recruiter-message', methods=['POST'])
def update_recruiter_message(candidate_id):
    """Update recruiter's message for the candidate"""
    try:
        data = request.get_json() or {}
        message = data.get('message', '')
        
        status_data = load_candidate_status(candidate_id)
        if not status_data:
            return jsonify({'success': False, 'error': 'Candidate not found'}), 404
            
        status_data['recruiter_message'] = message
        
        if save_candidate_status(candidate_id, status_data):
            return jsonify({'success': True, 'status': status_data}), 200
            
        return jsonify({'success': False, 'error': 'Failed to save message'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@status_bp.route('/api/candidate/<candidate_id>/notes', methods=['POST'])
def add_candidate_note(candidate_id):
    """Add a note to candidate"""
    try:
        data = request.get_json() or {}
        note_text = data.get('note', '')
        user = data.get('user', 'system')
        
        if not note_text:
            return jsonify({'success': False, 'error': 'Note text required'}), 400
        
        status_data = load_candidate_status(candidate_id)
        
        note_entry = {
            'text': note_text,
            'timestamp': datetime.now().isoformat(),
            'user': user
        }
        status_data['notes'].append(note_entry)
        
        if save_candidate_status(candidate_id, status_data):
            return jsonify({'success': True, 'note': note_entry}), 200
        
        return jsonify({'success': False, 'error': 'Failed to save note'}), 500
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@status_bp.route('/api/candidate/<candidate_id>/tags', methods=['PUT'])
def update_candidate_tags(candidate_id):
    """Update candidate tags"""
    try:
        data = request.get_json() or {}
        tags = data.get('tags', [])
        
        status_data = load_candidate_status(candidate_id)
        status_data['tags'] = tags
        
        if save_candidate_status(candidate_id, status_data):
            return jsonify({'success': True, 'tags': tags}), 200
        
        return jsonify({'success': False, 'error': 'Failed to save tags'}), 500
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@status_bp.route('/api/candidates/bulk-status', methods=['POST'])
def bulk_update_status():
    """Bulk update candidate statuses"""
    try:
        data = request.get_json() or {}
        candidate_ids = data.get('candidate_ids', [])
        new_status = data.get('status', '').lower()
        note = data.get('note', '')
        user = data.get('user', 'system')
        
        if new_status not in VALID_STATUSES:
            return jsonify({'success': False, 'error': f'Invalid status'}), 400
        
        updated = []
        failed = []
        
        for candidate_id in candidate_ids:
            try:
                status_data = load_candidate_status(candidate_id)
                
                history_entry = {
                    'from_status': status_data['current_status'],
                    'to_status': new_status,
                    'timestamp': datetime.now().isoformat(),
                    'user': user,
                    'note': note
                }
                status_data['history'].append(history_entry)
                status_data['current_status'] = new_status
                
                if save_candidate_status(candidate_id, status_data):
                    updated.append(candidate_id)
                else:
                    failed.append(candidate_id)
            except Exception as e:
                print(f"Error updating {candidate_id}: {e}")
                failed.append(candidate_id)
        
        return jsonify({
            'success': True,
            'updated': len(updated),
            'failed': len(failed),
            'updated_ids': updated,
            'failed_ids': failed
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@status_bp.route('/api/candidates/stats', methods=['GET'])
def get_candidate_stats():
    """Get candidate statistics by status"""
    try:
        stats = {status: 0 for status in VALID_STATUSES}
        total = 0
        
        if os.path.exists('candidate_data'):
            for filename in os.listdir('candidate_data'):
                if filename.endswith('_status.json'):
                    try:
                        with open(os.path.join('candidate_data', filename), 'r') as f:
                            data = json.load(f)
                            status = data.get('current_status', 'new')
                            if status in stats:
                                stats[status] += 1
                            total += 1
                    except:
                        continue
        
        return jsonify({
            'success': True,
            'stats': stats,
            'total': total
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@status_bp.route('/api/candidates/all-statuses', methods=['GET'])
def get_all_candidate_statuses():
    """Get all candidates with their statuses"""
    try:
        candidates = []
        
        if os.path.exists('candidate_data'):
            for filename in os.listdir('candidate_data'):
                if filename.endswith('_status.json'):
                    try:
                        candidate_id = filename.replace('_status.json', '')
                        with open(os.path.join('candidate_data', filename), 'r') as f:
                            data = json.load(f)
                            candidates.append({
                                'id': candidate_id,
                                'name': data.get('name', ''),
                                'score': data.get('score', 0),
                                'experience_years': data.get('experience_years', 0),
                                'jd_domain': data.get('jd_domain', ''),
                                'status': data.get('current_status', 'new'),
                                'ref_id': data.get('ref_id', ''),
                                'tags': data.get('tags', []),
                                'notes_count': len(data.get('notes', [])),
                                'last_updated': data.get('history', [{}])[-1].get('timestamp', '') if data.get('history') else ''
                            })
                    except Exception as e:
                        print(f"Error loading {filename}: {e}")
                        continue
        
        return jsonify({
            'success': True,
            'candidates': candidates,
            'total': len(candidates)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@status_bp.route('/api/candidate/<candidate_id>/clear', methods=['PUT'])
def clear_candidate(candidate_id):
    """Archive/Clear a candidate by setting their status to 'cleared'"""
    try:
        status_data = load_candidate_status(candidate_id)
        old_status = status_data['current_status']
        
        history_entry = {
            'from_status': old_status,
            'to_status': 'cleared',
            'timestamp': datetime.now().isoformat(),
            'user': 'recruiter',
            'note': 'Candidate archived/cleared from view'
        }
        
        status_data['history'].append(history_entry)
        status_data['current_status'] = 'cleared'
        
        if save_candidate_status(candidate_id, status_data):
            return jsonify({
                'success': True,
                'message': f'Candidate {candidate_id} cleared',
                'status': 'cleared'
            }), 200
            
        return jsonify({'success': False, 'error': 'Failed to clear candidate'}), 500
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@status_bp.route('/api/candidates/by-status/<status>', methods=['GET'])
def get_candidates_by_status(status):
    """Get all candidates with a specific status"""
    try:
        if status not in VALID_STATUSES:
            return jsonify({'success': False, 'error': 'Invalid status'}), 400
        
        candidates = []
        
        if os.path.exists('candidate_data'):
            for filename in os.listdir('candidate_data'):
                if filename.endswith('_status.json'):
                    try:
                        with open(os.path.join('candidate_data', filename), 'r') as f:
                            data = json.load(f)
                            if data.get('current_status') == status:
                                candidate_id = filename.replace('_status.json', '')
                                candidates.append({
                                    'id': candidate_id,
                                    'status': data.get('current_status'),
                                    'tags': data.get('tags', []),
                                    'notes': data.get('notes', []),
                                    'history': data.get('history', [])
                                })
                    except:
                        continue
        
        return jsonify({
            'success': True,
            'status': status,
            'candidates': candidates,
            'count': len(candidates)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@status_bp.route('/api/candidate/<candidate_id>/history', methods=['GET'])
def get_candidate_history(candidate_id):
    """Get full status history for a candidate"""
    try:
        status_data = load_candidate_status(candidate_id)
        if status_data:
            return jsonify({
                'success': True,
                'candidate_id': candidate_id,
                'current_status': status_data.get('current_status'),
                'history': status_data.get('history', []),
                'notes': status_data.get('notes', []),
                'tags': status_data.get('tags', [])
            }), 200
        
        return jsonify({'success': False, 'error': 'Candidate not found'}), 404
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@status_bp.route('/api/candidate/<candidate_id>/notes', methods=['GET'])
def get_candidate_notes(candidate_id):
    """Get all notes for a candidate"""
    try:
        status_data = load_candidate_status(candidate_id)
        if status_data:
            return jsonify({
                'success': True,
                'candidate_id': candidate_id,
                'notes': status_data.get('notes', [])
            }), 200
        
        return jsonify({'success': False, 'error': 'Candidate not found'}), 404
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@status_bp.route('/api/candidate/<candidate_id>/notes/<int:note_index>', methods=['DELETE'])
def delete_candidate_note(candidate_id, note_index):
    """Delete a specific note"""
    try:
        status_data = load_candidate_status(candidate_id)
        if not status_data:
            return jsonify({'success': False, 'error': 'Candidate not found'}), 404
        
        notes = status_data.get('notes', [])
        if note_index < 0 or note_index >= len(notes):
            return jsonify({'success': False, 'error': 'Invalid note index'}), 400
        
        deleted_note = notes.pop(note_index)
        status_data['notes'] = notes
        
        if save_candidate_status(candidate_id, status_data):
            return jsonify({
                'success': True,
                'deleted_note': deleted_note,
                'remaining_notes': notes
            }), 200
        
        return jsonify({'success': False, 'error': 'Failed to delete note'}), 500
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@status_bp.route('/api/candidate/<candidate_id>', methods=['DELETE'])
def delete_candidate_data(candidate_id):
    """Delete all status data for a candidate"""
    try:
        filepath = get_status_file(candidate_id)
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({
                'success': True,
                'message': f'Deleted status data for {candidate_id}'
            }), 200
        
        return jsonify({'success': False, 'error': 'Candidate not found'}), 404
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@status_bp.route('/api/status/valid-statuses', methods=['GET'])
def get_valid_statuses():
    """Get list of valid statuses"""
    return jsonify({
        'success': True,
        'statuses': VALID_STATUSES
    }), 200

@status_bp.route('/api/candidates/search', methods=['POST'])
def search_candidates():
    """Search candidates by various criteria"""
    try:
        data = request.get_json() or {}
        query = data.get('query', '').lower()
        status_filter = data.get('status')
        tags_filter = data.get('tags', [])
        
        candidates = []
        
        if os.path.exists('candidate_data'):
            for filename in os.listdir('candidate_data'):
                if filename.endswith('_status.json'):
                    try:
                        candidate_id = filename.replace('_status.json', '')
                        
                        # Check if candidate ID matches query
                        if query and query not in candidate_id.lower():
                            continue
                        
                        with open(os.path.join('candidate_data', filename), 'r') as f:
                            status_data = json.load(f)
                        
                        # Filter by status
                        if status_filter and status_data.get('current_status') != status_filter:
                            continue
                        
                        # Filter by tags
                        if tags_filter:
                            candidate_tags = status_data.get('tags', [])
                            if not any(tag in candidate_tags for tag in tags_filter):
                                continue
                        
                        candidates.append({
                            'id': candidate_id,
                            'status': status_data.get('current_status'),
                            'tags': status_data.get('tags', []),
                            'notes_count': len(status_data.get('notes', [])),
                            'last_updated': status_data.get('history', [{}])[-1].get('timestamp', '') if status_data.get('history') else ''
                        })
                    except:
                        continue
        
        return jsonify({
            'success': True,
            'candidates': candidates,
            'count': len(candidates)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@status_bp.route('/api/candidate/by-ref/<ref_id>', methods=['GET'])
def get_candidate_by_ref(ref_id):
    """Look up a candidate by their reference ID (for candidate-facing portal)"""
    try:
        refs_file = 'candidate_data/references.json'
        if not os.path.exists(refs_file):
            return jsonify({'success': False, 'error': 'Reference not found'}), 404

        with open(refs_file, 'r') as f:
            refs = json.load(f)

        ref_upper = ref_id.strip().upper()
        if ref_upper not in refs:
            return jsonify({'success': False, 'error': 'Invalid reference ID'}), 404

        record = refs[ref_upper]
        candidate_id = record.get('id', '')
        status_data = load_candidate_status(candidate_id)
        current_status = status_data.get('current_status', 'new') if status_data else 'new'
        is_finalized = current_status == 'finalized'

        return jsonify({
            'success': True,
            'ref_id': ref_upper,
            'candidate_id': candidate_id,
            'name': record.get('name', candidate_id),
            'finalized': is_finalized,
            'status': current_status,
            'recruiter_message': status_data.get('recruiter_message', '')
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@status_bp.route('/api/finalized-candidates', methods=['GET'])
def get_finalized_candidates():
    """Get all finalized candidates with their reference IDs"""
    try:
        refs_file = 'candidate_data/references.json'
        refs = {}
        if os.path.exists(refs_file):
            with open(refs_file, 'r') as f:
                refs = json.load(f)

        # Build reverse map: candidate_id -> ref_id
        rev = {v.get('id'): k for k, v in refs.items()}

        finalized = []
        if os.path.exists('candidate_data'):
            for filename in os.listdir('candidate_data'):
                if filename.endswith('_status.json'):
                    candidate_id = filename.replace('_status.json', '')
                    try:
                        with open(os.path.join('candidate_data', filename), 'r') as f:
                            data = json.load(f)
                        if data.get('current_status') == 'finalized':
                            ref_id = data.get('ref_id') or rev.get(candidate_id, 'N/A')
                            finalized.append({
                                'id': candidate_id,
                                'ref_id': ref_id,
                                'name': refs.get(ref_id, {}).get('name', candidate_id),
                                'finalized_at': next(
                                    (h['timestamp'] for h in reversed(data.get('history', []))
                                     if h.get('to_status') == 'finalized'), ''
                                )
                            })
                    except:
                        continue

        return jsonify({'success': True, 'candidates': finalized, 'count': len(finalized)}), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
