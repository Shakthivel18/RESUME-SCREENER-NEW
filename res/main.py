# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import time
import pandas as pd
import random
import string
import json
# from tqdm import tqdm # Removing tqdm as we aren't loading large CSV anymore
import utils 
from domain_manager import domain_bp
from interview_api import interview_bp

app = Flask(__name__, static_folder='templates')
CORS(app)

# Register blueprints
app.register_blueprint(domain_bp)
app.register_blueprint(interview_bp)
from analytics_api import analytics_bp
app.register_blueprint(analytics_bp)
from status_api import status_bp
app.register_blueprint(status_bp)

UPLOAD_FOLDER = 'uploads/resumes'
PROCESSED_FOLDER = 'uploads/processed_text'
REFERENCES_FILE = 'candidate_data/references.json'
# CSV_PATH = 'resume/Resume.csv' # Disabled

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs('candidate_data', exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# --- CSV Dataset Disabled ---
# We are now strictly using files in UPLOAD_FOLDER / PROCESSED_FOLDER
print("Running in Uploads-Only Mode.")

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

@app.route('/config')
def serve_config():
    return app.send_static_file('config.html')

@app.route('/i')
def ii():
    return app.send_static_file('profile.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend', path)

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    candidate_id = filename.replace('.txt', '')
    ref_id = "REF-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    try:
        raw_text = utils.extract_text_from_file(filepath)
        if raw_text:
            text_filename = filename + ".txt"
            text_path = os.path.join(app.config['PROCESSED_FOLDER'], text_filename)
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(raw_text)
            print(f"Text extracted and saved for: {filename}")
        else:
            print(f"Warning: No text extracted from {filename}")
            
    except Exception as e:
        print(f"Error processing file {filename}: {e}")

    # Save reference mapping
    try:
        refs = {}
        if os.path.exists(REFERENCES_FILE):
            with open(REFERENCES_FILE, 'r') as f:
                refs = json.load(f)
        refs[ref_id] = {"id": candidate_id, "name": candidate_id, "timestamp": time.time()}
        with open(REFERENCES_FILE, 'w') as f:
            json.dump(refs, f, indent=2)
    except Exception as e:
        print(f"Error saving reference ID: {e}")

    # Also embed ref_id into the candidate's status file
    try:
        status_file = f'candidate_data/{candidate_id}_status.json'
        status_data = {'candidate_id': candidate_id, 'current_status': 'new', 'history': [], 'notes': [], 'tags': []}
        if os.path.exists(status_file):
            with open(status_file, 'r') as f:
                status_data = json.load(f)
        status_data['ref_id'] = ref_id
        with open(status_file, 'w') as f:
            json.dump(status_data, f, indent=2)
    except Exception as e:
        print(f"Error embedding ref_id in status: {e}")

    return jsonify({
        "message": f"File '{filename}' uploaded and processed successfully!",
        "filename": filename,
        "filepath": filepath,
        "reference_id": ref_id
    }), 200

@app.route('/api/backfill-refs', methods=['GET'])
def backfill_refs():
    """Assign reference IDs to all existing resumes that don't have one yet"""
    try:
        refs = {}
        if os.path.exists(REFERENCES_FILE):
            with open(REFERENCES_FILE, 'r') as f:
                refs = json.load(f)

        # Build set of candidate_ids already in refs
        already_have = {v.get('id') for v in refs.values()}
        assigned = []

        processed_dir = app.config['PROCESSED_FOLDER']
        if os.path.exists(processed_dir):
            for text_file in os.listdir(processed_dir):
                if not text_file.endswith('.txt'):
                    continue
                candidate_id = text_file.replace('.txt', '')
                if candidate_id in already_have:
                    continue
                new_ref = "REF-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
                refs[new_ref] = {"id": candidate_id, "name": candidate_id, "timestamp": time.time()}
                already_have.add(candidate_id)

                # Write into status file
                status_file = f'candidate_data/{candidate_id}_status.json'
                status_data = {'candidate_id': candidate_id, 'current_status': 'new', 'history': [], 'notes': [], 'tags': []}
                if os.path.exists(status_file):
                    try:
                        with open(status_file, 'r') as f:
                            status_data = json.load(f)
                    except:
                        pass
                if not status_data.get('ref_id'):
                    status_data['ref_id'] = new_ref
                    with open(status_file, 'w') as f:
                        json.dump(status_data, f, indent=2)
                assigned.append({"candidate_id": candidate_id, "ref_id": new_ref})

        with open(REFERENCES_FILE, 'w') as f:
            json.dump(refs, f, indent=2)

        return jsonify({"success": True, "assigned": len(assigned), "details": assigned}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/candidate/login', methods=['POST'])
def candidate_login():
    """Candidate login using Reference ID"""
    try:
        data = request.get_json() or {}
        ref_id = data.get('reference_id', '').strip().upper()
        
        if not ref_id:
            return jsonify({'success': False, 'error': 'Reference ID is required'}), 400
            
        if os.path.exists(REFERENCES_FILE):
            with open(REFERENCES_FILE, 'r') as f:
                refs = json.load(f)
                if ref_id in refs:
                    return jsonify({
                        'success': True,
                        'candidate': refs[ref_id]
                    }), 200
                    
        return jsonify({'success': False, 'error': 'Invalid Reference ID'}), 404
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get-resume/<resume_id>', methods=['GET'])
def get_resume(resume_id):
    """Get resume content by ID"""
    try:
        # Try to find the resume text file
        processed_dir = app.config['PROCESSED_FOLDER']
        text_file = os.path.join(processed_dir, f"{resume_id}.txt")
        
        if os.path.exists(text_file):
            with open(text_file, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({
                "success": True,
                "id": resume_id,
                "content": content
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Resume not found"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


def get_all_resumes():
    """Returns only currently uploaded files."""
    # 1. Start with empty list (CSV Disabled)
    all_resumes = []
    
    # 2. Add Uploaded Files
    processed_dir = app.config['PROCESSED_FOLDER']
    if os.path.exists(processed_dir):
        for text_file in os.listdir(processed_dir):
            if text_file.endswith(".txt"):
                original_name = text_file.replace(".txt", "")
                with open(os.path.join(processed_dir, text_file), 'r', encoding='utf-8') as f:
                    content = f.read()
                
                all_resumes.append({
                    "id": original_name,
                    "name": original_name,
                    "text": content,
                    "source": "upload"
                })
    return all_resumes

@app.route('/api/match-resumes', methods=['POST'])
def match_resumes():
    data = request.get_json()
    if not data or 'job_description' not in data:
        return jsonify({"message": "Invalid request: 'job_description' missing"}), 400

    job_description = data['job_description']
    job_title = data.get('job_title', None)
    
    # If job_title not explicit, try to extract from first line of JD
    if not job_title and job_description:
        first_line = job_description.split('\n')[0].strip()
        if len(first_line) < 100:
            job_title = first_line
    
    # Get combined data
    resume_data_list = get_all_resumes()
    
    if not resume_data_list:
        return jsonify({
            "message": "No resumes found to match.",
            "job_description_received": job_description,
            "matched_resumes": []
        }), 200

    try:
        # NOTE: Calculating TF-IDF on 60k+ docs can take time.
        # Ideally we'd limit this or cache the vectorizer.
        # For this demo, we'll slice the list if it's too huge, or let it run.
        # Let's cap at 5000 for performance unless user requested ALL.
        # Python handles 5000 relatively fast. 60k might take 10-20s.
        
        # Using subset for responsiveness
        # matched_results = utils.calculate_match_scores(job_description, resume_data_list[:5000], job_title) 
        matched_results = utils.calculate_match_scores(job_description, resume_data_list, job_title)
        
        # Clean up output
        final_results = []
        
        print("\n" + "="*50)
        print(f"TOP 10 MATCHES for Job Description")
        print("="*50)
        
        for i, res in enumerate(matched_results):
            score = res.get("score", 0)
            status = res.get("status", "Not Fit")
            name = res.get("name", "Unknown")
            score_breakdown = res.get("score_breakdown", {})
            
            # Print top 10 to terminal with detailed breakdown
            if i < 10:
                print(f"\n{i+1}. [{score:.4f}] {name}")
                print(f"   Status: {status}")
                
                # Show domain info if available (advanced scoring)
                if 'jd_domain' in res:
                    print(f"   JD Domain: {res['jd_domain']} | Resume Domain: {res['resume_domain']}")
                    domain_match = "✓ Match" if res.get('domain_match', False) else "✗ Mismatch"
                    print(f"   Domain Match: {domain_match}")
                
                # Score breakdown
                if 'domain' in score_breakdown:
                    # Advanced scoring with 6 components
                    print(f"   Scores: TF-IDF={score_breakdown.get('tfidf', 0):.3f} | "
                          f"Keywords={score_breakdown.get('keyword', 0):.3f} | "
                          f"Semantic={score_breakdown.get('semantic', 0):.3f}")
                    print(f"           Experience={score_breakdown.get('experience', 0):.3f} | "
                          f"Domain={score_breakdown.get('domain', 0):.3f} | "
                          f"Education={score_breakdown.get('education', 0):.3f}")
                else:
                    # Basic hybrid scoring with 4 components
                    print(f"   Scores: TF-IDF={score_breakdown.get('tfidf', 0):.3f} | "
                          f"Keywords={score_breakdown.get('keyword', 0):.3f} | "
                          f"Semantic={score_breakdown.get('semantic', 0):.3f} | "
                          f"Experience={score_breakdown.get('experience', 0):.3f}")
                
                # Keywords and experience
                keyword_match_pct = res.get('keyword_match_percent', 0) * 100 if 'keyword_match_percent' in res else 0
                print(f"   Keywords: {res.get('matched_keywords', 0)}/{res.get('total_keywords', 0)} "
                      f"({keyword_match_pct:.1f}% match)")
                print(f"   Experience: {res.get('experience_years', 0)} years "
                      f"(Required: {res.get('required_experience', 'N/A')})")
                
                # Interview recommendation if available
                if 'should_interview' in res:
                    interview_status = "✓ RECOMMEND" if res['should_interview'] else "✗ Do not recommend"
                    print(f"   Interview: {interview_status}")

            # Build API response
            result_data = {
                "id": res["id"],
                "name": res["name"],
                "score": score,
                "status": status,
                "source": res.get("source", "upload"),
                "score_breakdown": score_breakdown,
                "matched_keywords": res.get("matched_keywords", 0),
                "total_keywords": res.get("total_keywords", 0),
                "experience_years": res.get("experience_years", 0)
            }
            
            # Add advanced scoring fields if available
            if 'category' in res:
                result_data['category'] = res['category']
            if 'should_interview' in res:
                result_data['should_interview'] = res['should_interview']
            if 'keyword_match_percent' in res:
                result_data['keyword_match_percent'] = res['keyword_match_percent']
            if 'required_experience' in res:
                result_data['required_experience'] = res['required_experience']
            if 'jd_domain' in res:
                result_data['jd_domain'] = res['jd_domain']
                result_data['resume_domain'] = res['resume_domain']
                result_data['domain_match'] = res['domain_match']
            
            final_results.append(result_data)
            
            # --- PERSISTENCE: Save scores to status JSON ---
            try:
                import json
                os.makedirs('candidate_data', exist_ok=True)
                candidate_id = res['id']
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
                
                # Update with latest analysis results
                status_data['score'] = score
                status_data['experience_years'] = res.get('experience_years', 0)
                status_data['jd_domain'] = res.get('jd_domain', '')
                status_data['name'] = res.get('name', candidate_id) # ensure name is saved
                
                # Auto-shortlist if score is exceptionally high (optional/demo)
                if score >= 85 and status_data.get('current_status') == 'new':
                    status_data['current_status'] = 'shortlisted'
                    status_data['history'].append({
                        'from_status': 'new',
                        'to_status': 'shortlisted',
                        'timestamp': time.strftime("%Y-%m-%dT%H:%M:%S"),
                        'user': 'system',
                        'note': 'Auto-shortlisted by high diagnostic score'
                    })
                
                with open(status_file, 'w') as f:
                    json.dump(status_data, f, indent=2)
            except Exception as e:
                print(f"Failed to persist score for {res['id']}: {e}")
            # ----------------------------------------------
            
        print("="*50 + "\n")
            
        return jsonify({
            "message": "Matching process completed successfully!",
            "matched_resumes": final_results[:100] # Return top 100 to avoid browser crash
        }), 200
        
    except Exception as e:
        print(f"Matching error: {e}")
        return jsonify({"message": "Error during matching process."}), 500

@app.route('/api/get-resume/<resume_id>', methods=['GET'])
def get_resume_content(resume_id):
    """Fetches resume content by ID from either CSV or File."""
    print(f"INFO: Fetching content for resume_id: {resume_id}")
    try:
        # 2. Check File System
        processed_dir = app.config['PROCESSED_FOLDER']
        
        # Exact match attempt
        possible_name = resume_id + ".txt"
        file_path = os.path.join(processed_dir, possible_name)
        
        if os.path.exists(file_path):
             with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                print(f"INFO: Found file content, length: {len(content)}")
                return jsonify({"content": content, "name": resume_id})
        
        print(f"WARNING: File not found at {file_path}")
        return jsonify({"content": "Resume content file not found on server.", "name": "Unknown"}), 404

    except Exception as e:
        print(f"ERROR: Loading resume {resume_id}: {e}")
        return jsonify({"content": f"Error loading resume: {e}", "name": "Error"}), 500

@app.route('/api/matched-resumes', methods=['GET'])
def get_matched_resumes():
    return jsonify([]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
