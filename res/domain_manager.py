"""
Domain Management System
Provides API endpoints for managing job domains
"""

from flask import Blueprint, request, jsonify
import json
import os
import config
import importlib

domain_bp = Blueprint('domains', __name__)

DOMAINS_FILE = 'custom_domains.json'

# Backup original built-in domains to allow clean deletion reload
_BUILTIN_DOMAINS = config.DOMAINS.copy()

def load_custom_domains():
    """Load custom domains from JSON file"""
    if os.path.exists(DOMAINS_FILE):
        try:
            with open(DOMAINS_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_custom_domains(domains):
    """Save custom domains to JSON file"""
    with open(DOMAINS_FILE, 'w') as f:
        json.dump(domains, f, indent=2)

def merge_domains():
    """Merge built-in and custom domains"""
    custom = load_custom_domains()
    all_domains = config.DOMAINS.copy()
    all_domains.update(custom)
    return all_domains

@domain_bp.route('/api/domains', methods=['GET'])
def get_domains():
    """Get all domains (built-in + custom)"""
    try:
        all_domains = merge_domains()
        
        # Format for frontend
        domains_list = []
        for key, value in all_domains.items():
            domains_list.append({
                'id': key,
                'name': value['name'],
                'keywords_count': len(value.get('keywords', [])),
                'required_skills_count': len(value.get('required_skills', [])),
                'is_custom': key not in config.DOMAINS
            })
        
        return jsonify({
            'success': True,
            'domains': domains_list,
            'total': len(domains_list)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@domain_bp.route('/api/domains/<domain_id>', methods=['GET'])
def get_domain_details(domain_id):
    """Get detailed information about a specific domain"""
    try:
        all_domains = merge_domains()
        
        if domain_id not in all_domains:
            return jsonify({'success': False, 'error': 'Domain not found'}), 404
        
        domain = all_domains[domain_id]
        
        # Get template if available
        from domain_templates import get_domain_template
        template = get_domain_template(domain_id)
        
        return jsonify({
            'success': True,
            'domain': {
                'id': domain_id,
                'name': domain['name'],
                'keywords': domain.get('keywords', []),
                'required_skills': domain.get('required_skills', []),
                'nice_to_have': domain.get('nice_to_have', []),
                'is_custom': domain_id not in config.DOMAINS,
                'template': template
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@domain_bp.route('/api/domains', methods=['POST'])
def create_domain():
    """Create a new custom domain"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('id'):
            return jsonify({'success': False, 'error': 'Domain ID is required'}), 400
        if not data.get('name'):
            return jsonify({'success': False, 'error': 'Domain name is required'}), 400
        if not data.get('keywords') or not isinstance(data['keywords'], list):
            return jsonify({'success': False, 'error': 'Keywords list is required'}), 400
        
        domain_id = data['id'].upper().replace(' ', '_')
        
        # Check if domain already exists
        all_domains = merge_domains()
        if domain_id in all_domains:
            return jsonify({'success': False, 'error': 'Domain ID already exists'}), 400
        
        # Create new domain
        new_domain = {
            'name': data['name'],
            'keywords': [kw.lower().strip() for kw in data['keywords'] if kw.strip()],
            'required_skills': [skill.lower().strip() for skill in data.get('required_skills', []) if skill.strip()],
            'nice_to_have': [skill.lower().strip() for skill in data.get('nice_to_have', []) if skill.strip()]
        }
        
        # Load existing custom domains
        custom_domains = load_custom_domains()
        custom_domains[domain_id] = new_domain
        
        # Save to file
        save_custom_domains(custom_domains)
        
        # Reload config to include new domain
        reload_domains()
        
        return jsonify({
            'success': True,
            'message': 'Domain created successfully',
            'domain': {
                'id': domain_id,
                **new_domain
            }
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@domain_bp.route('/api/domains/<domain_id>', methods=['PUT'])
def update_domain(domain_id):
    """Update an existing custom domain"""
    try:
        custom_domains = load_custom_domains()
        
        # Only allow updating custom domains
        if domain_id not in custom_domains:
            return jsonify({'success': False, 'error': 'Can only update custom domains'}), 400
        
        data = request.get_json()
        
        # Update domain
        if 'name' in data:
            custom_domains[domain_id]['name'] = data['name']
        if 'keywords' in data:
            custom_domains[domain_id]['keywords'] = [kw.lower().strip() for kw in data['keywords'] if kw.strip()]
        if 'required_skills' in data:
            custom_domains[domain_id]['required_skills'] = [skill.lower().strip() for skill in data['required_skills'] if skill.strip()]
        if 'nice_to_have' in data:
            custom_domains[domain_id]['nice_to_have'] = [skill.lower().strip() for skill in data['nice_to_have'] if skill.strip()]
        
        # Save changes
        save_custom_domains(custom_domains)
        reload_domains()
        
        return jsonify({
            'success': True,
            'message': 'Domain updated successfully',
            'domain': {
                'id': domain_id,
                **custom_domains[domain_id]
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@domain_bp.route('/api/domains/<domain_id>', methods=['DELETE'])
def delete_domain(domain_id):
    """Delete a custom domain"""
    try:
        custom_domains = load_custom_domains()
        
        # Only allow deleting custom domains
        if domain_id not in custom_domains:
            return jsonify({'success': False, 'error': 'Can only delete custom domains'}), 400
        
        # Delete domain
        del custom_domains[domain_id]
        
        # Save changes
        save_custom_domains(custom_domains)
        reload_domains()
        
        return jsonify({
            'success': True,
            'message': 'Domain deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def reload_domains():
    """Reload domains in config module"""
    try:
        # Reset config.DOMAINS to built-ins first to clear deleted custom domains
        config.DOMAINS.clear()
        config.DOMAINS.update(_BUILTIN_DOMAINS)
        
        # Merge custom domains into config.DOMAINS
        custom_domains = load_custom_domains()
        
        # Update the config module's DOMAINS
        for domain_id, domain_data in custom_domains.items():
            config.DOMAINS[domain_id] = domain_data
        
        # Also reload advanced_scorer if it exists
        try:
            import advanced_scorer
            importlib.reload(advanced_scorer)
        except Exception:
            pass
            
    except Exception as e:
        print(f"Error reloading domains: {e}")

# Initialize: Load custom domains on startup
reload_domains()
