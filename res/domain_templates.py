"""
Domain templates with predefined job descriptions
"""

DOMAIN_TEMPLATES = {
    "SOFTWARE_ENGINEERING": """Job Title: Senior Software Engineer

Requirements:
- 5+ years of experience in software development
- Expert knowledge of programming languages (Python, Java, JavaScript)
- Strong understanding of software design patterns and SOLID principles
- Experience with version control systems (Git, GitHub)
- Proficiency in agile methodologies and CI/CD practices
- Strong problem-solving and debugging skills
- Experience with REST APIs and microservices architecture
- Knowledge of databases (SQL and NoSQL)
- Excellent communication and teamwork abilities""",

    "DATA_SCIENCE": """Job Title: Senior Data Scientist

Requirements:
- 4+ years of experience in data science and machine learning
- Expert knowledge of Python and data science libraries (Pandas, NumPy, Scikit-learn)
- Strong understanding of machine learning algorithms and statistical modeling
- Experience with deep learning frameworks (TensorFlow, PyTorch)
- Proficiency in data visualization tools (Matplotlib, Seaborn, Tableau)
- Experience with big data technologies (Spark, Hadoop)
- Strong SQL skills and database knowledge
- Experience with feature engineering and model deployment
- Excellent analytical and problem-solving skills
- Master's degree in Computer Science, Statistics, or related field preferred""",

    "DEVOPS_CLOUD": """Job Title: Senior DevOps Engineer

Requirements:
- 5+ years of experience in DevOps and cloud infrastructure
- Expert knowledge of cloud platforms (AWS, Azure, or GCP)
- Strong experience with containerization (Docker, Kubernetes)
- Proficiency in infrastructure as code (Terraform, Ansible, CloudFormation)
- Experience with CI/CD pipelines (Jenkins, GitLab CI, GitHub Actions)
- Strong Linux/Unix administration skills
- Experience with monitoring and logging tools (Prometheus, Grafana, ELK)
- Knowledge of networking, security, and best practices
- Scripting skills (Bash, Python, PowerShell)
- Experience with microservices architecture""",

    "FRONTEND_DEVELOPMENT": """Job Title: Senior Frontend Developer

Requirements:
- 4+ years of experience in frontend development
- Expert knowledge of HTML5, CSS3, and JavaScript/TypeScript
- Strong experience with modern frameworks (React, Angular, or Vue.js)
- Proficiency in responsive design and mobile-first development
- Experience with state management (Redux, MobX, Vuex)
- Knowledge of build tools (Webpack, Vite, Rollup)
- Strong understanding of web performance optimization
- Experience with CSS preprocessors (Sass, Less) or CSS-in-JS
- Knowledge of accessibility standards (WCAG, ARIA)
- Experience with testing frameworks (Jest, Cypress, Playwright)
- Strong UI/UX sensibility and attention to detail""",

    "BACKEND_DEVELOPMENT": """Job Title: Senior Backend Developer

Requirements:
- 5+ years of experience in backend development
- Expert knowledge of server-side languages (Python, Java, Node.js, or Go)
- Strong experience with backend frameworks (Django, Flask, Spring, Express)
- Proficiency in database design and optimization (PostgreSQL, MySQL, MongoDB)
- Experience with REST API and GraphQL design
- Knowledge of microservices architecture and design patterns
- Experience with message queues (RabbitMQ, Kafka, Redis)
- Strong understanding of authentication and authorization (OAuth, JWT)
- Experience with caching strategies and performance optimization
- Knowledge of cloud services and deployment
- Strong problem-solving and scalability mindset""",

    "MOBILE_DEVELOPMENT": """Job Title: Senior Mobile Developer

Requirements:
- 4+ years of experience in mobile app development
- Expert knowledge of iOS (Swift) and/or Android (Kotlin/Java)
- Experience with cross-platform frameworks (React Native, Flutter) is a plus
- Strong understanding of mobile UI/UX design principles
- Proficiency in mobile app architecture patterns (MVVM, MVI, Clean Architecture)
- Experience with RESTful APIs and mobile backend integration
- Knowledge of mobile testing frameworks and best practices
- Experience with app store deployment (Apple App Store, Google Play)
- Understanding of mobile security and data protection
- Experience with push notifications and analytics
- Strong debugging and performance optimization skills""",

    "CYBERSECURITY": """Job Title: Senior Cybersecurity Engineer

Requirements:
- 5+ years of experience in cybersecurity and information security
- Expert knowledge of security frameworks and standards (OWASP, NIST, ISO 27001)
- Strong experience with penetration testing and vulnerability assessment
- Proficiency in security tools (Burp Suite, Metasploit, Nmap, Wireshark)
- Experience with SIEM systems and security monitoring
- Knowledge of encryption, cryptography, and PKI
- Strong understanding of network security and firewalls
- Experience with cloud security (AWS, Azure, GCP)
- Knowledge of compliance requirements (GDPR, HIPAA, PCI-DSS)
- Incident response and forensics experience
- Relevant certifications (CISSP, CEH, OSCP) preferred""",

    "UI_UX_DESIGN": """Job Title: Senior UI/UX Designer

Requirements:
- 4+ years of experience in UI/UX design
- Expert knowledge of design tools (Figma, Sketch, Adobe XD)
- Strong portfolio demonstrating user-centered design
- Experience with user research and usability testing
- Proficiency in wireframing, prototyping, and mockup creation
- Strong understanding of design systems and component libraries
- Knowledge of accessibility standards and inclusive design
- Experience with interaction design and micro-animations
- Understanding of responsive and mobile-first design
- Ability to collaborate with developers and stakeholders
- Strong visual design skills (typography, color theory, layout)
- Experience with design thinking and agile methodologies""",

    "PRODUCT_MANAGEMENT": """Job Title: Senior Product Manager

Requirements:
- 5+ years of experience in product management
- Strong understanding of product lifecycle and strategy
- Experience with agile methodologies (Scrum, Kanban)
- Proficiency in product management tools (Jira, Confluence, Asana)
- Strong stakeholder management and communication skills
- Experience with user research and data-driven decision making
- Knowledge of A/B testing and experimentation frameworks
- Understanding of technical concepts and ability to work with engineering teams
- Experience with roadmap planning and prioritization
- Strong analytical skills and metrics-driven approach
- Experience with go-to-market strategies
- MBA or technical background preferred""",

    "GENERAL_IT": """Job Title: IT Support Specialist

Requirements:
- 3+ years of experience in IT support and technical assistance
- Strong knowledge of Windows, Linux, and macOS operating systems
- Experience with networking fundamentals (TCP/IP, DNS, DHCP)
- Proficiency in Active Directory and user management
- Strong troubleshooting and problem-solving skills
- Experience with ticketing systems and help desk software
- Knowledge of hardware and software installation
- Understanding of backup and disaster recovery procedures
- Experience with ITIL or IT service management frameworks
- Strong customer service and communication skills
- Ability to work independently and in team environments
- Relevant certifications (CompTIA A+, Network+) preferred"""
}

def get_domain_template(domain_id):
    """Get the job description template for a domain"""
    return DOMAIN_TEMPLATES.get(domain_id, "")
