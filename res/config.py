"""
Configuration file for resume screening system
Includes domain definitions, thresholds, and scoring weights
"""

# === DOMAIN DEFINITIONS ===
# Each domain has specific keywords, required skills, and weights

DOMAINS = {
    "SOFTWARE_ENGINEERING": {
        "name": "Software Engineering",
        "keywords": [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'scala',
            'react', 'angular', 'vue', 'node', 'express', 'django', 'flask', 'spring', 'asp.net',
            'git', 'github', 'gitlab', 'bitbucket', 'ci/cd', 'jenkins', 'travis',
            'rest api', 'graphql', 'microservices', 'monolith', 'api design',
            'sql', 'nosql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'agile', 'scrum', 'kanban', 'jira', 'confluence',
            'unit testing', 'integration testing', 'tdd', 'bdd', 'jest', 'pytest', 'junit',
            'oop', 'design patterns', 'solid', 'clean code', 'refactoring'
        ],
        "required_skills": ['programming', 'software development', 'coding'],
        "nice_to_have": ['open source', 'github contributions', 'technical blog']
    },
    
    "DATA_SCIENCE": {
        "name": "Data Science & Machine Learning",
        "keywords": [
            'python', 'r', 'julia', 'matlab',
            'machine learning', 'deep learning', 'ai', 'artificial intelligence',
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'xgboost', 'lightgbm',
            'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn', 'plotly',
            'nlp', 'natural language processing', 'computer vision', 'cv',
            'neural networks', 'cnn', 'rnn', 'lstm', 'transformer', 'bert', 'gpt',
            'data analysis', 'data visualization', 'statistical analysis',
            'jupyter', 'notebook', 'colab',
            'sql', 'spark', 'hadoop', 'hive', 'pig',
            'feature engineering', 'model deployment', 'mlops',
            'tableau', 'power bi', 'looker', 'data studio'
        ],
        "required_skills": ['statistics', 'data analysis', 'machine learning'],
        "nice_to_have": ['kaggle', 'research papers', 'publications']
    },
    
    "DEVOPS_CLOUD": {
        "name": "DevOps & Cloud Engineering",
        "keywords": [
            'aws', 'azure', 'gcp', 'google cloud', 'cloud computing',
            'docker', 'kubernetes', 'k8s', 'containers', 'containerization',
            'jenkins', 'gitlab ci', 'github actions', 'circleci', 'travis ci',
            'terraform', 'ansible', 'puppet', 'chef', 'cloudformation',
            'ci/cd', 'continuous integration', 'continuous deployment',
            'linux', 'unix', 'bash', 'shell scripting', 'powershell',
            'monitoring', 'prometheus', 'grafana', 'elk', 'splunk', 'datadog',
            'nginx', 'apache', 'load balancing', 'reverse proxy',
            'microservices', 'service mesh', 'istio', 'linkerd',
            'infrastructure as code', 'iac', 'gitops', 'argocd', 'flux'
        ],
        "required_skills": ['cloud platforms', 'automation', 'infrastructure'],
        "nice_to_have": ['aws certification', 'azure certification', 'kubernetes certification']
    },
    
    "FRONTEND_DEVELOPMENT": {
        "name": "Frontend Development",
        "keywords": [
            'html', 'css', 'javascript', 'typescript',
            'react', 'angular', 'vue', 'svelte', 'next.js', 'nuxt', 'gatsby',
            'redux', 'mobx', 'vuex', 'state management',
            'webpack', 'vite', 'rollup', 'parcel', 'esbuild',
            'sass', 'scss', 'less', 'styled-components', 'css-in-js',
            'tailwind', 'bootstrap', 'material-ui', 'ant design',
            'responsive design', 'mobile-first', 'progressive web app', 'pwa',
            'accessibility', 'wcag', 'aria', 'a11y',
            'performance optimization', 'lazy loading', 'code splitting',
            'testing', 'jest', 'cypress', 'playwright', 'selenium',
            'figma', 'sketch', 'adobe xd', 'ui/ux'
        ],
        "required_skills": ['html', 'css', 'javascript', 'frontend frameworks'],
        "nice_to_have": ['design skills', 'ui/ux knowledge', 'portfolio']
    },
    
    "BACKEND_DEVELOPMENT": {
        "name": "Backend Development",
        "keywords": [
            'python', 'java', 'node.js', 'go', 'rust', 'php', 'ruby', 'c#',
            'django', 'flask', 'fastapi', 'spring', 'express', 'nest.js', 'laravel', 'rails',
            'rest api', 'graphql', 'grpc', 'soap', 'api design',
            'sql', 'postgresql', 'mysql', 'oracle', 'sql server',
            'nosql', 'mongodb', 'cassandra', 'dynamodb', 'couchdb',
            'redis', 'memcached', 'caching', 'session management',
            'microservices', 'monolith', 'service-oriented architecture', 'soa',
            'message queues', 'rabbitmq', 'kafka', 'sqs', 'pub/sub',
            'authentication', 'authorization', 'oauth', 'jwt', 'saml',
            'database design', 'orm', 'sqlalchemy', 'hibernate', 'sequelize',
            'performance optimization', 'scalability', 'load balancing'
        ],
        "required_skills": ['backend frameworks', 'databases', 'api development'],
        "nice_to_have": ['system design', 'architecture', 'scalability experience']
    },
    
    "MOBILE_DEVELOPMENT": {
        "name": "Mobile Development",
        "keywords": [
            'ios', 'android', 'mobile', 'mobile development',
            'swift', 'objective-c', 'kotlin', 'java',
            'react native', 'flutter', 'xamarin', 'ionic', 'cordova',
            'xcode', 'android studio', 'mobile ui', 'mobile ux',
            'app store', 'google play', 'app deployment',
            'push notifications', 'firebase', 'mobile analytics',
            'offline storage', 'sqlite', 'realm', 'core data',
            'mobile testing', 'appium', 'espresso', 'xctest',
            'responsive design', 'adaptive layout', 'mobile-first',
            'performance optimization', 'battery optimization', 'memory management'
        ],
        "required_skills": ['mobile platforms', 'mobile frameworks', 'app development'],
        "nice_to_have": ['published apps', 'app store presence', 'user reviews']
    },
    
    "CYBERSECURITY": {
        "name": "Cybersecurity",
        "keywords": [
            'security', 'cybersecurity', 'information security', 'infosec',
            'penetration testing', 'ethical hacking', 'vulnerability assessment',
            'owasp', 'security audit', 'security compliance',
            'encryption', 'cryptography', 'ssl', 'tls', 'https',
            'firewall', 'ids', 'ips', 'intrusion detection', 'intrusion prevention',
            'siem', 'security information and event management',
            'incident response', 'forensics', 'malware analysis',
            'authentication', 'authorization', 'identity management', 'iam',
            'zero trust', 'network security', 'application security',
            'cloud security', 'aws security', 'azure security',
            'compliance', 'gdpr', 'hipaa', 'pci-dss', 'iso 27001',
            'burp suite', 'metasploit', 'nmap', 'wireshark', 'kali linux'
        ],
        "required_skills": ['security', 'risk assessment', 'security tools'],
        "nice_to_have": ['certifications', 'cissp', 'ceh', 'oscp', 'security clearance']
    },
    
    "UI_UX_DESIGN": {
        "name": "UI/UX Design",
        "keywords": [
            'ui design', 'ux design', 'user interface', 'user experience',
            'figma', 'sketch', 'adobe xd', 'invision', 'framer',
            'wireframing', 'prototyping', 'mockups', 'user flows',
            'user research', 'usability testing', 'a/b testing',
            'design systems', 'style guides', 'design tokens',
            'typography', 'color theory', 'visual hierarchy',
            'interaction design', 'motion design', 'animation',
            'responsive design', 'mobile design', 'web design',
            'accessibility', 'wcag', 'inclusive design',
            'design thinking', 'human-centered design', 'user-centered design',
            'adobe creative suite', 'photoshop', 'illustrator', 'after effects'
        ],
        "required_skills": ['design tools', 'user research', 'prototyping'],
        "nice_to_have": ['portfolio', 'case studies', 'design awards']
    },
    
    "PRODUCT_MANAGEMENT": {
        "name": "Product Management",
        "keywords": [
            'product management', 'product manager', 'product owner',
            'product strategy', 'product roadmap', 'product vision',
            'agile', 'scrum', 'kanban', 'sprint planning',
            'user stories', 'backlog management', 'prioritization',
            'stakeholder management', 'cross-functional teams',
            'market research', 'competitive analysis', 'user research',
            'kpis', 'metrics', 'analytics', 'data-driven decisions',
            'a/b testing', 'experimentation', 'feature flags',
            'go-to-market', 'product launch', 'product lifecycle',
            'wireframing', 'prototyping', 'mvp', 'minimum viable product',
            'jira', 'confluence', 'asana', 'trello', 'monday.com',
            'sql', 'data analysis', 'business intelligence'
        ],
        "required_skills": ['product strategy', 'stakeholder management', 'agile methodologies'],
        "nice_to_have": ['mba', 'technical background', 'startup experience']
    },
    
    "GENERAL_IT": {
        "name": "General IT",
        "keywords": [
            'information technology', 'it support', 'technical support',
            'windows', 'linux', 'macos', 'operating systems',
            'networking', 'tcp/ip', 'dns', 'dhcp', 'vpn',
            'active directory', 'ldap', 'user management',
            'troubleshooting', 'problem solving', 'debugging',
            'hardware', 'software', 'installation', 'configuration',
            'backup', 'disaster recovery', 'business continuity',
            'ticketing systems', 'help desk', 'service desk',
            'itil', 'itsm', 'it service management',
            'documentation', 'knowledge base', 'training'
        ],
        "required_skills": ['technical support', 'troubleshooting', 'it fundamentals'],
        "nice_to_have": ['certifications', 'comptia a+', 'network+', 'itil']
    }
}

# === SCORING WEIGHTS ===
# Weights for different components of the hybrid scoring algorithm

SCORING_WEIGHTS = {
    "tfidf": 0.15,              # TF-IDF cosine similarity
    "keyword": 0.25,            # Exact keyword matching
    "semantic": 0.15,           # Semantic similarity
    "experience": 0.10,         # Years of experience matching
    "domain": 0.10,             # Domain-specific scoring
    "education": 0.05,          # Education level matching
    "role_match": 0.20          # Job Title/Role matching
}

# === THRESHOLDS ===
# Score thresholds for different fit categories (0-100 Scale)

THRESHOLDS = {
    "excellent": 75.0,      # Excellent Fit: >= 75%
    "good": 60.0,           # Good Fit: 60% - 74%
    "potential": 40.0,      # Potential Fit: 40% - 59%
    "marginal": 20.0,       # Marginal Fit: 20% - 39%
    "reject": 0.0           # Not Fit: < 20%
}

# Minimum score to be considered for interview
MIN_INTERVIEW_SCORE = THRESHOLDS["potential"]  # 40.0

# Minimum keyword match percentage
MIN_KEYWORD_MATCH_PERCENT = 0.30  # At least 30% of required keywords

# === EXPERIENCE LEVELS ===
EXPERIENCE_LEVELS = {
    "entry": (0, 2),
    "junior": (2, 4),
    "mid": (4, 7),
    "senior": (7, 12),
    "lead": (12, 100)
}

# === EDUCATION LEVELS ===
EDUCATION_KEYWORDS = {
    "phd": ["phd", "ph.d", "doctorate", "doctoral"],
    "masters": ["masters", "master's", "m.s", "m.tech", "mba", "m.b.a"],
    "bachelors": ["bachelors", "bachelor's", "b.s", "b.tech", "b.e", "undergraduate"],
    "associate": ["associate", "diploma", "certification"]
}

EDUCATION_SCORES = {
    "phd": 1.0,
    "masters": 0.8,
    "bachelors": 0.6,
    "associate": 0.4,
    "none": 0.2
}

# === ADVANCED SCORING PARAMETERS ===

# Boost multiplier for exact skill matches
EXACT_SKILL_BOOST = 1.2

# Penalty for missing critical skills
CRITICAL_SKILL_PENALTY = 0.15

# Recency bonus (for recent experience)
RECENCY_BONUS = 0.05

# Diversity bonus (for varied skill set)
DIVERSITY_BONUS = 0.03

# === FILTERING OPTIONS ===

# Enable/disable strict filtering
STRICT_FILTERING = False

# Require minimum years of experience
REQUIRE_MIN_EXPERIENCE = False

# Require specific education level
REQUIRE_EDUCATION = False

# Auto-reject below threshold
AUTO_REJECT_BELOW_THRESHOLD = True
