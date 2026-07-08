"""
Test script to demonstrate the hybrid scoring model
"""

# Example Job Description
job_description = """
Senior Python Developer - 5+ years experience required

We are looking for an experienced Python developer to join our team.

Required Skills:
- 5+ years of Python development experience
- Strong experience with Django or Flask frameworks
- Experience with AWS cloud services
- Knowledge of Docker and Kubernetes
- Proficiency in SQL databases (PostgreSQL, MySQL)
- Experience with REST API development
- Git version control
- Agile/Scrum methodology

Nice to have:
- React or Angular frontend experience
- CI/CD pipeline experience
- Machine learning knowledge
- Redis or Elasticsearch experience

Responsibilities:
- Design and develop scalable web applications
- Write clean, maintainable code
- Collaborate with cross-functional teams
- Participate in code reviews
"""

# Example Resume 1 - Excellent Match
resume_1 = """
John Doe
Senior Software Engineer

EXPERIENCE:
Software Engineer at Tech Corp (2018 - Present) - 6 years
- Developed scalable web applications using Python and Django
- Implemented REST APIs serving 1M+ requests daily
- Deployed applications on AWS using Docker and Kubernetes
- Worked with PostgreSQL and Redis for data storage
- Implemented CI/CD pipelines using Jenkins and Git
- Collaborated in Agile/Scrum environment

SKILLS:
- Languages: Python, JavaScript, SQL
- Frameworks: Django, Flask, React
- Cloud: AWS (EC2, S3, RDS, Lambda)
- DevOps: Docker, Kubernetes, Jenkins, Git
- Databases: PostgreSQL, MySQL, Redis
- Other: REST API, Microservices, Agile, Scrum

EDUCATION:
BS Computer Science, State University
"""

# Example Resume 2 - Moderate Match
resume_2 = """
Jane Smith
Full Stack Developer

EXPERIENCE:
Developer at StartupXYZ (2021 - Present) - 3 years
- Built web applications using Python and Flask
- Developed frontend interfaces with React
- Worked with MySQL databases
- Used Git for version control

SKILLS:
- Python, JavaScript, HTML, CSS
- Flask, React, Node.js
- MySQL, MongoDB
- Git, GitHub

EDUCATION:
BS Information Technology
"""

# Example Resume 3 - Poor Match
resume_3 = """
Bob Johnson
Java Developer

EXPERIENCE:
Java Developer at Enterprise Inc (2015 - Present) - 8 years
- Developed enterprise applications using Java and Spring
- Worked with Oracle databases
- Implemented SOAP web services
- Used SVN for version control

SKILLS:
- Java, Spring, Hibernate
- Oracle, SQL Server
- SOAP, XML
- Maven, Ant

EDUCATION:
MS Computer Science
"""

print("=" * 80)
print("HYBRID SCORING MODEL - TEST EXAMPLES")
print("=" * 80)
print("\nJob Description Summary:")
print("- Position: Senior Python Developer")
print("- Required Experience: 5+ years")
print("- Key Technologies: Python, Django/Flask, AWS, Docker, Kubernetes, PostgreSQL")
print("\n" + "=" * 80)

print("\n\nEXPECTED RESULTS:")
print("\n1. Resume 1 (John Doe) - EXCELLENT FIT")
print("   - Has 6 years experience (matches 5+ requirement)")
print("   - Strong keyword matches: Python, Django, AWS, Docker, Kubernetes, PostgreSQL, etc.")
print("   - High semantic similarity (same domain and technologies)")
print("   - Expected score: 0.15+ (Excellent Fit)")

print("\n2. Resume 2 (Jane Smith) - POTENTIAL/GOOD FIT")
print("   - Has 3 years experience (below 5+ requirement)")
print("   - Moderate keyword matches: Python, Flask, MySQL, Git")
print("   - Missing: AWS, Docker, Kubernetes, PostgreSQL")
print("   - Expected score: 0.05-0.14 (Potential to Good Fit)")

print("\n3. Resume 3 (Bob Johnson) - NOT FIT")
print("   - Has 8 years experience (good) but in Java, not Python")
print("   - Very few keyword matches (no Python, no modern cloud tools)")
print("   - Low semantic similarity (different tech stack)")
print("   - Expected score: <0.05 (Not Fit)")

print("\n" + "=" * 80)
print("\nSCORE BREAKDOWN EXPLANATION:")
print("=" * 80)
print("\nEach resume receives 4 component scores:")
print("  1. TF-IDF (40% weight) - Overall text similarity")
print("  2. Keywords (30% weight) - Exact skill matches")
print("  3. Semantic (20% weight) - Conceptual similarity")
print("  4. Experience (10% weight) - Years of experience match")
print("\nFinal Score = (TF-IDF × 0.4) + (Keywords × 0.3) + (Semantic × 0.2) + (Experience × 0.1)")
print("\n" + "=" * 80)
print("\nTo test this with actual scoring:")
print("1. Upload these resumes to the application")
print("2. Submit the job description")
print("3. Check the console output for detailed score breakdowns")
print("4. Verify the API response includes all scoring components")
print("=" * 80)
