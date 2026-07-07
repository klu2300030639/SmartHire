import os
import random
import pandas as pd

# Define the domains and associated skills
DOMAINS = {
    "Software Engineering": [
        "Java", "Python", "C++", "Spring Boot", "REST APIs", "Microservices", "SQL", "Git", 
        "Docker", "Kubernetes", "System Design", "Multithreading", "PostgreSQL", "Redis", 
        "Maven", "Linux", "Hibernate", "AWS"
    ],
    "Data Science": [
        "Python", "R", "SQL", "Machine Learning", "Deep Learning", "Statistics", "Pandas", 
        "NumPy", "Scikit-learn", "PyTorch", "TensorFlow", "NLP", "Tableau", "Data Visualization",
        "Spark", "Hadoop", "Data Mining", "Jupyter"
    ],
    "Frontend Development": [
        "HTML5", "CSS3", "JavaScript", "TypeScript", "React", "Angular", "Vue.js", "Tailwind CSS", 
        "Sass", "UI/UX Design", "Bootstrap", "Webpack", "Responsive Design", "Redux", "Figma",
        "Jest", "GraphQL", "Next.js"
    ],
    "DevOps": [
        "AWS", "Azure", "GCP", "Linux", "Bash", "Docker", "Kubernetes", "Terraform", "Ansible", 
        "Jenkins", "CI/CD", "Prometheus", "Grafana", "Git", "Nginx", "Shell Scripting",
        "CloudFormation", "Terraform Cloud"
    ],
    "Product Management": [
        "Product Strategy", "Roadmap", "Agile", "Scrum", "Jira", "User Research", "Wireframing", 
        "Product Lifecycle", "SQL", "A/B Testing", "Market Analysis", "Cross-functional Leadership",
        "Confluence", "Data-driven Decisions", "KPI Tracking", "Customer Feedback"
    ],
    "Human Resources": [
        "Recruiting", "Talent Acquisition", "Employee Relations", "HR Policies", "Onboarding", 
        "ATS (Applicant Tracking Systems)", "Performance Management", "Payroll", "Compliance", "Sourcing", 
        "Interviewing", "Conflict Resolution", "FMLA", "HRIS", "Diversity & Inclusion"
    ]
}

NAMES = ["Aaditya", "Aarav", "Aryan", "Amit", "Anjali", "Bhavna", "Chaitanya", "Deepak", "Divya", "Ganesh", 
         "Ishaan", "Karan", "Kavita", "Manish", "Neha", "Nikhil", "Pooja", "Rahul", "Rohan", "Sanjay", 
         "Shreya", "Siddharth", "Sneha", "Vikram", "Yash", "James", "Emily", "Michael", "Sarah", "David"]
SURNAMES = ["Sharma", "Verma", "Gupta", "Patel", "Mehra", "Singh", "Joshi", "Kumar", "Iyer", "Nair", 
            "Reddy", "Rao", "Smith", "Johnson", "Brown", "Taylor", "Miller", "Wilson", "Davis", "Jones"]

EMAILS = ["gmail.com", "yahoo.com", "outlook.com", "techcorp.com", "innovate.io"]
UNIVERSITIES = [
    "Indian Institute of Technology (IIT)", "Birla Institute of Technology and Science (BITS)", 
    "National Institute of Technology (NIT)", "Delhi Technological University", 
    "Stanford University", "Massachusetts Institute of Technology (MIT)", 
    "University of California, Berkeley", "Carnegie Mellon University"
]
DEGREES = {
    "Software Engineering": ["B.Tech in Computer Science", "M.Tech in Software Engineering", "B.S. in Computer Science"],
    "Data Science": ["B.S. in Statistics", "M.S. in Data Science", "Ph.D. in Machine Learning", "B.Tech in Computer Science"],
    "Frontend Development": ["B.Tech in Information Technology", "B.S. in Computer Science", "Bachelor of Design (UI/UX)"],
    "DevOps": ["B.Tech in Computer Science", "B.S. in Information Technology", "M.S. in Cloud Computing"],
    "Product Management": ["MBA", "B.Tech in Computer Science & Engineering", "B.S. in Business Administration"],
    "Human Resources": ["MBA in HR", "Bachelor of Business Administration", "M.S. in Organizational Psychology"]
}

COMPANIES = ["Google", "Microsoft", "Amazon", "Meta", "Netflix", "TCS", "Infosys", "Wipro", "Accenture", 
             "StartUp Labs", "CloudNets", "DataSystems", "DesignStudio", "TalentForge", "FintechHub"]

JOB_TITLES = {
    "Software Engineering": [
        "Backend Developer", "Java Software Engineer", "Python Developer", "Full Stack Engineer", 
        "Senior Backend Engineer", "Lead Developer", "Software Engineer II", "Systems Architect"
    ],
    "Data Science": [
        "Data Scientist", "Machine Learning Engineer", "NLP Researcher", "Data Analyst", 
        "Senior Data Scientist", "AI Engineer", "Computer Vision Specialist", "Data Engineer"
    ],
    "Frontend Development": [
        "Frontend Developer", "React Engineer", "UI/UX Developer", "Web Designer", 
        "Senior Frontend Engineer", "UI Engineer", "Frontend Specialist", "Angular Developer"
    ],
    "DevOps": [
        "DevOps Engineer", "Site Reliability Engineer (SRE)", "Cloud Engineer", "Infrastructure Engineer", 
        "Senior DevOps Specialist", "Platform Engineer", "Kubernetes Administrator"
    ],
    "Product Management": [
        "Product Manager", "Associate Product Manager", "Senior Product Manager", "Technical Product Manager", 
        "Product Owner", "Director of Product", "Growth Product Manager"
    ],
    "Human Resources": [
        "HR Manager", "Talent Acquisition Specialist", "HR Generalist", "Technical Recruiter", 
        "HR Coordinator", "Head of People & Culture", "Employee Relations Specialist"
    ]
}

def generate_resume_text(name, email, phone, domain, skills, exp_years, degree, university):
    skill_str = ", ".join(skills)
    text = f"""
    {name}
    Email: {email} | Phone: {phone}
    Location: Bengaluru, India
    
    PROFESSIONAL SUMMARY
    Dedicated and detail-oriented professional with {exp_years} years of experience in {domain}. 
    Strong expertise in design, development, and implementation. Proven track record of delivering 
    high-quality systems and collaborating with cross-functional teams.
    
    EDUCATION
    {degree}
    {university}
    Graduated with Honors
    
    TECHNICAL SKILLS
    {skill_str}
    
    WORK EXPERIENCE
    Senior Consultant / Lead in {domain}
    {random.choice(COMPANIES)} | 2021 - Present
    - Designed and implemented key features for core product lines.
    - Led a team of developers/specialists to build scalable solutions.
    - Reduced system latency and improved process efficiency by 25%.
    - Applied {", ".join(skills[:3])} to solve critical business problems.
    
    Associate in {domain}
    {random.choice(COMPANIES)} | 2018 - 2021
    - Assisted in software, model, or process design under Agile methodologies.
    - Utilized {", ".join(skills[-3:])} for day-to-day tasks.
    - Conducted system tests, code reviews, and performance optimization.
    
    PROJECTS
    Automated System for {domain}
    - Developed an end-to-end automated framework using {skills[0] if skills else 'various technologies'}.
    - Integrated multiple modules resulting in 40% time savings.
    """
    return text.strip()

def generate_job_description(title, company, domain, required_skills, min_exp, location):
    skill_str = ", ".join(required_skills)
    text = f"""
    Job Title: {title}
    Company: {company}
    Location: {location}
    Department: {domain}
    
    ABOUT THE ROLE
    We are looking for a talented and motivated {title} to join our growing team. In this role, 
    you will design, build, and optimize solutions to push the boundaries of technology. You 
    will work closely with engineering, product, and business stakeholders.
    
    RESPONSIBILITIES
    - Develop, test, and maintain high-performance applications and services.
    - Write clean, maintainable, and efficient code/models.
    - Troubleshoot, debug, and upgrade existing systems.
    - Leverage technologies like {", ".join(required_skills[:3])} to build scalable systems.
    - Participate in code reviews, technical architecture planning, and agile standups.
    
    REQUIREMENTS
    - Minimum {min_exp} years of professional experience in {domain} or related fields.
    - Bachelor's or Master's degree in Computer Science, Business, or equivalent.
    - Strong proficiency in: {skill_str}.
    - Excellent problem-solving skills and communication.
    
    BENEFITS
    - Competitive salary and health benefits.
    - Flexible working hours and remote work options.
    - Continuous learning and career development opportunities.
    """
    return text.strip()

def create_datasets():
    resumes = []
    resume_id_counter = 1
    
    for domain, skill_list in DOMAINS.items():
        for _ in range(35):
            name = f"{random.choice(NAMES)} {random.choice(SURNAMES)}"
            email = f"{name.lower().replace(' ', '')}@{random.choice(EMAILS)}"
            phone = f"+91 {random.randint(70000, 99999)} {random.randint(10000, 99999)}"
            
            num_skills = random.randint(6, 10)
            skills = random.sample(skill_list, num_skills)
            
            if "Git" not in skills and random.random() > 0.5:
                skills.append("Git")
            if "SQL" not in skills and random.random() > 0.5:
                skills.append("SQL")
                
            exp_years = random.randint(1, 15)
            degree = random.choice(DEGREES[domain])
            university = random.choice(UNIVERSITIES)
            
            resume_text = generate_resume_text(name, email, phone, domain, skills, exp_years, degree, university)
            
            resumes.append({
                "resume_id": f"RES_{resume_id_counter:03d}",
                "name": name,
                "email": email,
                "phone": phone,
                "category": domain,
                "skills": ", ".join(skills),
                "experience_years": exp_years,
                "education": f"{degree} from {university}",
                "text": resume_text
            })
            resume_id_counter += 1
            
    df_resumes = pd.DataFrame(resumes)
    
    jobs = []
    job_id_counter = 1
    
    locations = ["Bengaluru, India", "Mumbai, India", "Hyderabad, India", "Remote, India", "Pune, India"]
    
    for domain, skill_list in DOMAINS.items():
        for _ in range(10):
            title = random.choice(JOB_TITLES[domain])
            company = random.choice(COMPANIES)
            location = random.choice(locations)
            min_exp = random.randint(2, 8)
            
            num_req_skills = random.randint(5, 8)
            required_skills = random.sample(skill_list, num_req_skills)
            
            job_desc_text = generate_job_description(title, company, domain, required_skills, min_exp, location)
            
            jobs.append({
                "job_id": f"JOB_{job_id_counter:03d}",
                "title": title,
                "company": company,
                "category": domain,
                "required_skills": ", ".join(required_skills),
                "min_experience": min_exp,
                "location": location,
                "description": job_desc_text
            })
            job_id_counter += 1
            
    df_jobs = pd.DataFrame(jobs)
    
    os.makedirs("data", exist_ok=True)
    df_resumes.to_csv("data/raw_resumes.csv", index=False)
    df_jobs.to_csv("data/raw_jobs.csv", index=False)
    print(f"Generated {len(df_resumes)} resumes and {len(df_jobs)} jobs.")

if __name__ == "__main__":
    create_datasets()
