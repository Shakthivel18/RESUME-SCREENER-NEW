"""
Enterprise Analytics Engine
Aggregates recruitment data for executive dashboarding.
"""

from flask import Blueprint, jsonify
import os
import json
import glob

analytics_bp = Blueprint('analytics', __name__)

INTERVIEWS_DIR = 'interviews'
CANDIDATES_DIR = 'uploads/processed_text'

@analytics_bp.route('/api/analytics/stats', methods=['GET'])
def get_dashboard_stats():
    try:
        # Ensure directories exist
        os.makedirs(CANDIDATES_DIR, exist_ok=True)
        os.makedirs(INTERVIEWS_DIR, exist_ok=True)

        # 1. Pipeline Volume
        total_candidates = len(glob.glob(os.path.join(CANDIDATES_DIR, '*.txt')))
        
        # 2. Interview Metrics
        interview_files = glob.glob(os.path.join(INTERVIEWS_DIR, '*.json'))
        total_interviews = len(interview_files)
        
        scores = []
        domain_counts = {}
        pass_count = 0
        
        for fpath in interview_files:
            try:
                with open(fpath, 'r') as f:
                    data = json.load(f)
                    
                    # Score Processing
                    score = data.get('overall_score', 0)
                    scores.append(score)
                    if score >= 7.0: # Enterprise Threshold (7/10)
                        pass_count += 1
                        
                    # Domain Breakdown
                    domain = data.get('domain', 'Unknown')
                    domain_counts[domain] = domain_counts.get(domain, 0) + 1
                    
            except:
                continue
                
        avg_score = sum(scores) / len(scores) if scores else 0
        pass_rate = (pass_count / total_interviews * 100) if total_interviews else 0
        
        return jsonify({
            'success': True,
            'kpis': {
                'total_candidates': total_candidates,
                'interviews_conducted': total_interviews,
                'avg_technical_score': round(avg_score, 1),
                'pass_rate': round(pass_rate, 1)
            },
            'domain_distribution': domain_counts,
            'score_distribution': [len([s for s in scores if s < 5]), 
                                   len([s for s in scores if 5 <= s < 8]), 
                                   len([s for s in scores if s >= 8])]
        })
        
    except Exception as e:
        print(f"Analytics Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
