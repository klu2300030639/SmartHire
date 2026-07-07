import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.preprocessing import clean_text, extract_skills
from src.classifier import predict_category

# Predefined courses/certifications for popular skills to provide career guidance
COURSE_RECOMMENDATIONS = {
    "Python": "Coursera: Python for Everybody Specialization or Harvard CS50P",
    "Java": "Udemy: Java Programming Masterclass or Oracle Certified Associate Java Programmer",
    "Spring Boot": "Baeldung: Learn Spring or Udemy Spring Boot Developer Course",
    "SQL": "Khan Academy: Intro to SQL or Stanford Online Databases",
    "Git": "GitHub Learning Lab or Udacity Git & GitHub Course",
    "Docker": "Docker Mastery on Udemy by Bret Fisher",
    "Kubernetes": "Linux Foundation: Certified Kubernetes Administrator (CKA)",
    "AWS": "AWS Certified Solutions Architect - Associate",
    "Azure": "Microsoft Certified: Azure Fundamentals (AZ-900)",
    "GCP": "Google Cloud Certified Associate Cloud Engineer",
    "Machine Learning": "Stanford/Coursera: Machine Learning Specialization by Andrew Ng",
    "Deep Learning": "deeplearning.ai: Deep Learning Specialization on Coursera",
    "PyTorch": "Udacity: Intro to Deep Learning with PyTorch or PyTorch official tutorials",
    "TensorFlow": "DeepLearning.AI TensorFlow Developer Professional Certificate",
    "NLP": "Coursera: Natural Language Processing Specialization by deeplearning.ai",
    "Pandas": "Kaggle Course: Pandas or DataCamp: Data Manipulation with Pandas",
    "NumPy": "Scientific Computing with Python on freeCodeCamp",
    "Scikit-learn": "Scikit-Learn Official User Guide or Udemy Machine Learning A-Z",
    "Tableau": "Tableau Desktop Specialist Certification or Coursera Data Visualization with Tableau",
    "React": "Epic React by Kent C. Dodds or Scrimba React Course",
    "Angular": "Udemy: Angular - The Complete Guide by Maximilian Schwarzmüller",
    "Vue.js": "Vue School: Vue.js 3 Fundamentals or Laracasts Vue Series",
    "TypeScript": "TypeScript Deep Dive online book or Udemy TypeScript course",
    "Tailwind CSS": "Tailwind Labs Official YouTube Course & Docs",
    "UI/UX Design": "Google UX Design Professional Certificate on Coursera",
    "Figma": "Figma Academy or Udemy Figma UI/UX Design course",
    "Terraform": "HashiCorp Certified: Terraform Associate",
    "Ansible": "Red Hat Certified Specialist in Ansible Automation",
    "Jenkins": "Jenkins Boot Camp on Udemy",
    "Agile": "PMI Agile Certified Practitioner (PMI-ACP) or Scrum Alliance CSPO",
    "Scrum": "Scrum Alliance: Certified ScrumMaster (CSM)",
    "Jira": "Atlassian University: Jira Fundamentals",
    "Recruiting": "LinkedIn Learning: Talent Acquisition & Recruiting Foundations",
    "ATS": "Capterra ATS training guides or Greenhouse/Lever tutorials",
}

def analyze_skill_gap(resume_skills, job_skills):
    """Compares resume skills with job required skills to find matches and gaps."""
    # Convert lists to sets (case-insensitive for robust matching)
    res_set = set([s.strip().lower() for s in resume_skills])
    job_set = set([s.strip().lower() for s in job_skills])
    
    # Original capitalization mapping for display
    res_map = {s.strip().lower(): s.strip() for s in resume_skills}
    job_map = {s.strip().lower(): s.strip() for s in job_skills}
    
    matching_set = res_set.intersection(job_set)
    missing_set = job_set.difference(res_set)
    
    # Get original casing back
    matching_skills = sorted([job_map[s] for s in matching_set])
    missing_skills = sorted([job_map[s] for s in missing_set])
    
    # Calculate match rate
    match_rate = len(matching_set) / len(job_set) if len(job_set) > 0 else 1.0
    
    # Generate recommendations for missing skills
    guidance = []
    for skill in missing_skills:
        skill_clean = skill.strip()
        rec_source = COURSE_RECOMMENDATIONS.get(skill_clean)
        if not rec_source:
            # Check case-insensitively
            for k, v in COURSE_RECOMMENDATIONS.items():
                if k.lower() == skill_clean.lower():
                    rec_source = v
                    break
        if rec_source:
            guidance.append(f"For **{skill}**: {rec_source}")
        else:
            guidance.append(f"For **{skill}**: Explore online tutorials (Udemy/Coursera/YouTube) and build a small project using {skill}.")
            
    return {
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "skill_match_rate": match_rate,
        "guidance": guidance
    }

def get_job_recommendations(resume_text, jobs_df, top_n=5):
    """Computes fit prediction scores and returns the top matching jobs."""
    if jobs_df.empty:
        return []
        
    cleaned_resume = clean_text(resume_text)
    cleaned_jobs = jobs_df['description'].apply(clean_text)
    
    # Vectorization
    vectorizer = TfidfVectorizer(max_features=2500, ngram_range=(1, 2))
    jobs_vectors = vectorizer.fit_transform(cleaned_jobs)
    resume_vector = vectorizer.transform([cleaned_resume])
    
    # Cosine Similarity
    cosine_sims = cosine_similarity(resume_vector, jobs_vectors)[0]
    
    resume_skills = extract_skills(resume_text)
    pred_category, prob_dict = predict_category(resume_text)
    
    recommendations = []
    
    for idx, row in jobs_df.iterrows():
        job_id = row['job_id']
        title = row['title']
        company = row['company']
        category = row['category']
        location = row['location']
        
        job_skills = [s.strip() for s in row['required_skills'].split(',')]
        gap_analysis = analyze_skill_gap(resume_skills, job_skills)
        skill_score = gap_analysis['skill_match_rate']
        
        cat_score = 1.0 if category == pred_category else 0.0
        text_score = cosine_sims[idx]
        
        # Compatibility Score (Weighted formula: 50% similarity, 30% skills, 20% category)
        compatibility_score = (text_score * 0.5 + skill_score * 0.3 + cat_score * 0.2) * 100
        
        recommendations.append({
            "job_id": job_id,
            "title": title,
            "company": company,
            "category": category,
            "location": location,
            "description": row['description'],
            "required_skills": row['required_skills'],
            "compatibility_score": round(compatibility_score, 1),
            "text_similarity_score": round(text_score * 100, 1),
            "skill_match_score": round(skill_score * 100, 1),
            "category_match_score": round(cat_score * 100, 1),
            "matching_skills": gap_analysis['matching_skills'],
            "missing_skills": gap_analysis['missing_skills'],
            "guidance": gap_analysis['guidance']
        })
        
    recommendations = sorted(recommendations, key=lambda x: x['compatibility_score'], reverse=True)
    return recommendations[:top_n]
