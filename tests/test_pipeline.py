import unittest
import os
import pandas as pd
from src.preprocessing import clean_text, extract_email, extract_phone, extract_skills, parse_resume
from src.classifier import predict_category, CLASSIFIER_PATH
from src.recommender import get_job_recommendations, analyze_skill_gap
from src.clustering import cluster_jobs_pipeline

class TestSmartHirePipeline(unittest.TestCase):
    
    def setUp(self):
        # Create a dummy resume text
        self.sample_resume = """
        John Doe
        Email: john.doe@example.com | Phone: +91 98765 43210
        Location: Bangalore
        
        Summary:
        Data Scientist with 3 years of experience. Experienced in Python, SQL, and Machine Learning.
        
        Skills:
        Python, Machine Learning, SQL, Git, Tableau.
        
        Education:
        B.Tech in Computer Science from IIT.
        """
        
        # Ensure we have model files generated
        if not os.path.exists(CLASSIFIER_PATH):
            from src.classifier import train_classifier
            train_classifier()
            
    def test_text_cleaning(self):
        text = "Hello World! This is a test with email@test.com and python coding."
        cleaned = clean_text(text)
        self.assertIn("hello", cleaned)
        self.assertIn("world", cleaned)
        self.assertNotIn("email@test.com", cleaned)
        self.assertNotIn("this", cleaned)
        self.assertIn("python", cleaned)
        self.assertIn("coding", cleaned)

    def test_metadata_extraction(self):
        email = extract_email(self.sample_resume)
        phone = extract_phone(self.sample_resume)
        self.assertEqual(email, "john.doe@example.com")
        self.assertIn("98765", phone)

    def test_skill_extraction(self):
        skills = extract_skills(self.sample_resume)
        self.assertIn("Python", skills)
        self.assertIn("Machine Learning", skills)
        self.assertIn("SQL", skills)
        self.assertIn("GIT", skills)
        self.assertIn("Tableau", skills)

    def test_resume_classification(self):
        category, probs = predict_category(self.sample_resume)
        self.assertEqual(category, "Data Science")
        self.assertIn("Data Science", probs)
        self.assertGreaterEqual(probs["Data Science"], 0.4)

    def test_skill_gap_analysis(self):
        resume_skills = ["Python", "SQL", "Git"]
        job_skills = ["Python", "Machine Learning", "SQL", "Scikit-Learn"]
        
        analysis = analyze_skill_gap(resume_skills, job_skills)
        self.assertIn("Python", analysis["matching_skills"])
        self.assertIn("Machine Learning", analysis["missing_skills"])
        self.assertIn("Scikit-Learn", analysis["missing_skills"])
        self.assertEqual(analysis["skill_match_rate"], 0.5)
        self.assertEqual(len(analysis["guidance"]), 2)

    def test_job_recommendation(self):
        jobs_df = pd.read_csv("data/raw_jobs.csv")
        recs = get_job_recommendations(self.sample_resume, jobs_df, top_n=3)
        
        self.assertEqual(len(recs), 3)
        self.assertGreaterEqual(recs[0]["compatibility_score"], recs[1]["compatibility_score"])
        self.assertTrue("compatibility_score" in recs[0])
        self.assertTrue("missing_skills" in recs[0])

    def test_job_clustering(self):
        clustered_df, themes = cluster_jobs_pipeline()
        self.assertIn("cluster", clustered_df.columns)
        self.assertEqual(len(themes), 6)
        self.assertTrue(0 in themes)
        self.assertTrue("display_name" in themes[0])

if __name__ == "__main__":
    unittest.main()
