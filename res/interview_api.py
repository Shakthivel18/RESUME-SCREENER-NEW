"""
Interview API endpoints - Robust Implementation
"""

from flask import Blueprint, request, jsonify
import ai_interviewer
import utils
import os

interview_bp = Blueprint('interview', __name__)

@interview_bp.route('/api/interview/start', methods=['POST'])
def start_interview():
    """Start interview with safety checks"""
    try:
        data = request.get_json() or {}
        candidate_id = data.get('candidate_id')
        job_description = data.get('job_description', 'Standard technical role')
        domain = data.get('domain', 'SOFTWARE_ENGINEERING')
        
        print(f"INFO: API - Starting interview for candidate {candidate_id}")
        
        if not candidate_id:
            return jsonify({'success': False, 'error': 'Candidate ID required'}), 400
        
        # 1. Get Resume Text (Handle missing files gracefully)
        resume_text = "Resume text unavailable."
        try:
            extracted = utils.extract_text_from_file(f"uploads/processed_text/{candidate_id}")
            if extracted:
                resume_text = extracted
        except Exception as e:
            print(f"WARNING: Could not load resume text: {e}")
        
        # 2. Generate Questions (This is now guaranteed to return a list)
        questions = ai_interviewer.generate_interview_questions(
            resume_text, 
            job_description, 
            domain,
            num_questions=5  # Reduced count for speed/reliability, can increase later
        )
        
        # 3. Create Session
        session = {
            'candidate_id': candidate_id,
            'domain': domain,
            'questions': questions,
            'answers': [],
            'current_question': 0,
            'started_at': ai_interviewer.datetime.now().isoformat(),
            'status': 'in_progress',
            'job_context': job_description[:500] # Save context
        }
        
        return jsonify({'success': True, 'session': session}), 200
        
    except Exception as e:
        print(f"ERROR: API Start Interview Failed: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@interview_bp.route('/api/interview/answer', methods=['POST'])
def submit_answer():
    """Submit answer with timeout protection"""
    try:
        data = request.get_json() or {}
        candidate_id = data.get('candidate_id')
        question = data.get('question', '')
        answer = data.get('answer', '')
        
        if not candidate_id:
            return jsonify({'success': False, 'error': 'Candidate ID missing'}), 400

        # Background context
        resume_text = "Context unavailable"
        try:
             # Try to load resume context for better evaluation
             extracted = utils.extract_text_from_file(f"uploads/processed_text/{candidate_id}")
             if extracted:
                 resume_text = extracted
        except Exception as e:
            print(f"WARNING: Could not load resume text for evaluation: {e}")
        
        # Evaluate
        evaluation = ai_interviewer.evaluate_answer(question, answer, resume_text)
        
        return jsonify({
            'success': True,
            'evaluation': evaluation
        }), 200
        
    except Exception as e:
        print(f"ERROR: API Answer Failed: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@interview_bp.route('/api/interview/complete', methods=['POST'])
def complete_interview():
    """Complete and save session"""
    try:
        data = request.get_json() or {}
        candidate_id = data.get('candidate_id')
        session_data = data.get('session')
        
        if not candidate_id or not session_data:
            return jsonify({'success': False, 'error': 'Invalid data'}), 400
        
        # Calculate Score
        answers = session_data.get('answers', [])
        valid_scores = [a.get('evaluation', {}).get('score', 0) for a in answers if a.get('evaluation')]
        
        avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0
        
        # Update Session
        session_data['completed_at'] = ai_interviewer.datetime.now().isoformat()
        session_data['status'] = 'completed'
        session_data['overall_score'] = avg_score
        
        # Save
        filename = ai_interviewer.save_interview_session(candidate_id, session_data)
        
        # --- AUTO-UPDATE CANDIDATE STATUS ---
        try:
            import json
            os.makedirs('candidate_data', exist_ok=True)
            status_file = f'candidate_data/{candidate_id}_status.json'
            
            status_data = {
                'candidate_id': candidate_id,
                'current_status': 'new',
                'history': [],
                'notes': [],
                'tags': []
            }
            
            if os.path.exists(status_file):
                with open(status_file, 'r') as f:
                    status_data = json.load(f)
            
            # Update status if not already 'interviewed' or 'hired' etc.
            if status_data.get('current_status') not in ['interviewed', 'shortlisted', 'hired', 'rejected']:
                old_status = status_data.get('current_status')
                status_data['current_status'] = 'interviewed'
                status_data['history'].append({
                    'from_status': old_status,
                    'to_status': 'interviewed',
                    'timestamp': ai_interviewer.datetime.now().isoformat(),
                    'user': 'system',
                    'note': 'Interview completed successfully'
                })
                
                with open(status_file, 'w') as f:
                    json.dump(status_data, f, indent=2)
                print(f"INFO: Auto-updated status to 'interviewed' for {candidate_id}")
                
        except Exception as status_err:
            print(f"WARNING: Failed to auto-update status: {status_err}")
        # -----------------------------------
        
        return jsonify({
            'success': True, 
            'overall_score': avg_score,
            'filename': filename
        }), 200
        
    except Exception as e:
        print(f"ERROR: API Complete Failed: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
        
@interview_bp.route('/api/candidate/<candidate_id>/interview-latest', methods=['GET'])
def get_latest_interview(candidate_id):
    """Fetch the latest interview session for a candidate"""
    try:
        session = ai_interviewer.load_interview_session(candidate_id)
        if session:
            return jsonify({'success': True, 'session': session}), 200
        return jsonify({'success': False, 'error': 'No interview found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
