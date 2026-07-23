import unittest
import os
import sys
import sqlite3

# Ensure db.py can be imported from the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import db

class TestHealthcareSystem(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Force SQLite database mode for testing
        db.DB_TYPE = "sqlite"
        # Reset database file to ensure clean state
        if os.path.exists("SmartHealthcare/healthcare.db"):
            try:
                os.remove("SmartHealthcare/healthcare.db")
            except PermissionError:
                pass
                
        # Initialize connection which will trigger table creation and seeding
        cls.conn = db.get_connection()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_database_creation(self):
        # Verify database file exists
        self.assertTrue(os.path.exists("SmartHealthcare/healthcare.db"))
        
        # Verify we can query SQLite master for the 28 tables
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = [
            "settings", "login_history", "audit_logs", "activity_logs", "notifications",
            "insurance", "payments", "bills", "beds", "wards", "admissions",
            "laboratory_results", "laboratory_tests", "pharmacy_inventory", "medicines",
            "prescriptions", "vitals", "ehr_records", "clinical_pathways", "appointments",
            "nurses", "doctors", "patients", "user_roles", "users", "permissions",
            "roles", "departments"
        ]
        
        for table in expected_tables:
            self.assertIn(table, tables, f"Table {table} is missing from database schema")

    def test_seed_departments(self):
        depts = db.execute_query("SELECT name FROM departments", fetch=True)
        dept_names = [d['name'] for d in depts]
        self.assertIn("Emergency", dept_names)
        self.assertIn("Cardiology", dept_names)
        self.assertIn("Pediatrics", dept_names)
        self.assertIn("General Medicine", dept_names)

    def test_seed_roles(self):
        roles = db.execute_query("SELECT name FROM roles", fetch=True)
        role_names = [r['name'] for r in roles]
        self.assertIn("Admin", role_names)
        self.assertIn("Doctor", role_names)
        self.assertIn("Patient", role_names)

    def test_seed_users(self):
        # Verify seeded Admin users
        users = db.execute_query("SELECT username, email FROM users", fetch=True)
        usernames = [u['username'] for u in users]
        self.assertIn("ADMIN", usernames)
        self.assertIn("Sindiri", usernames)
        self.assertIn("Aryan", usernames)

    def test_clinical_pathway_flow(self):
        # 1. Create a dummy user and patient
        user_id = db.execute_query("""
            INSERT INTO users (full_name, username, email, password_hash, status)
            VALUES ('Jane Doe', 'janedoe', 'jane@example.com', 'dummy_hash', 'Active')
        """, commit=True)
        
        patient_id = db.execute_query("""
            INSERT INTO patients (user_id, gender, dob, blood_group)
            VALUES (?, 'Female', '1995-05-15', 'O+')
        """, (user_id,), commit=True)
        
        # 2. Initialize clinical pathway for the patient
        pathway_id = db.execute_query("""
            INSERT INTO clinical_pathways (patient_id, current_stage, symptoms)
            VALUES (?, 'Triage', 'Mild chest pain and shortness of breath')
        """, (patient_id,), commit=True)
        
        # Verify initial stage
        pathway = db.execute_query("SELECT * FROM clinical_pathways WHERE pathway_id = ?", (pathway_id,), fetch=True)[0]
        self.assertEqual(pathway['current_stage'], 'Triage')
        
        # 3. Transition patient to Diagnosis stage
        db.execute_query("""
            UPDATE clinical_pathways 
            SET current_stage = 'Diagnosis', diagnosis = 'Rule out Angina'
            WHERE pathway_id = ?
        """, (pathway_id,), commit=True)
        
        # Verify updated stage and diagnosis
        updated_pathway = db.execute_query("SELECT * FROM clinical_pathways WHERE pathway_id = ?", (pathway_id,), fetch=True)[0]
        self.assertEqual(updated_pathway['current_stage'], 'Diagnosis')
        self.assertEqual(updated_pathway['diagnosis'], 'Rule out Angina')

if __name__ == "__main__":
    unittest.main()
