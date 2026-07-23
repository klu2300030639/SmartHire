import mysql.connector
from mysql.connector import pooling
import sqlite3
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

_connection_pool = None
DB_TYPE = "mysql"  # Can be "mysql" or "sqlite"

def get_connection_config():
    try:
        if "DB_HOST" in st.secrets:
            return {
                "host": st.secrets.get("DB_HOST"),
                "port": int(st.secrets.get("DB_PORT", 3306)),
                "database": st.secrets.get("DB_DATABASE", "HealthcareDB"),
                "user": st.secrets.get("DB_USER", "root"),
                "password": st.secrets.get("DB_PASSWORD", "")
            }
        elif "db" in st.secrets:
            return {
                "host": st.secrets.db.get("host", "localhost"),
                "port": int(st.secrets.db.get("port", 3306)),
                "database": st.secrets.db.get("database", "HealthcareDB"),
                "user": st.secrets.db.get("username", "root"),
                "password": st.secrets.db.get("password", "root")
            }
    except Exception:
        pass
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", 3306)),
        "database": os.getenv("DB_DATABASE", "HealthcareDB"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "root")
    }

def init_sqlite_db(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 1. DEPARTMENTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        department_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT
    )
    """)
    
    # 2. ROLES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roles (
        role_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT
    )
    """)
    
    # 3. PERMISSIONS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS permissions (
        permission_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT
    )
    """)
    
    # 4. USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role_id INTEGER,
        status TEXT DEFAULT 'Active' NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE SET NULL
    )
    """)
    
    # 5. USER ROLES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_roles (
        user_id INTEGER,
        role_id INTEGER,
        PRIMARY KEY (user_id, role_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE
    )
    """)
    
    # 6. PATIENTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        gender TEXT,
        dob DATE,
        blood_group TEXT,
        emergency_contact TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
    )
    """)
    
    # 7. DOCTORS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        department_id INTEGER,
        specialization TEXT,
        license_number TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
        FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE SET NULL
    )
    """)
    
    # 8. NURSES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nurses (
        nurse_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        department_id INTEGER,
        license_number TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
        FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE SET NULL
    )
    """)
    
    # 9. APPOINTMENTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        appointment_date DATETIME NOT NULL,
        status TEXT DEFAULT 'Scheduled' NOT NULL,
        reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
        FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
    )
    """)
    
    # 10. CLINICAL PATHWAYS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clinical_pathways (
        pathway_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        assigned_doctor_id INTEGER,
        current_stage TEXT DEFAULT 'Registration' NOT NULL,
        symptoms TEXT,
        diagnosis TEXT,
        treatment_plan TEXT,
        status TEXT DEFAULT 'Active' NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
        FOREIGN KEY (assigned_doctor_id) REFERENCES doctors(doctor_id) ON DELETE SET NULL
    )
    """)
    
    # 11. EHR RECORDS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ehr_records (
        ehr_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        recorded_by_user_id INTEGER,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
        FOREIGN KEY (recorded_by_user_id) REFERENCES users(user_id) ON DELETE SET NULL
    )
    """)
    
    # 12. VITALS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vitals (
        vital_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ehr_id INTEGER,
        patient_id INTEGER,
        blood_pressure TEXT,
        pulse_rate INTEGER,
        temperature DECIMAL(4,1),
        weight_kg DECIMAL(5,2),
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ehr_id) REFERENCES ehr_records(ehr_id) ON DELETE CASCADE,
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
    )
    """)
    
    # 13. PRESCRIPTIONS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prescriptions (
        prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
        pathway_id INTEGER,
        doctor_id INTEGER,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (pathway_id) REFERENCES clinical_pathways(pathway_id) ON DELETE CASCADE,
        FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE SET NULL
    )
    """)
    
    # 14. MEDICINES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        medicine_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        code TEXT UNIQUE NOT NULL,
        description TEXT
    )
    """)
    
    # 15. PHARMACY INVENTORY
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pharmacy_inventory (
        inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_id INTEGER,
        quantity INTEGER DEFAULT 0 NOT NULL,
        unit_price DECIMAL(10,2) NOT NULL,
        expiry_date DATE,
        FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id) ON DELETE CASCADE
    )
    """)
    
    # 16. LABORATORY TESTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS laboratory_tests (
        test_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        code TEXT UNIQUE NOT NULL,
        cost DECIMAL(10,2) NOT NULL
    )
    """)
    
    # 17. LABORATORY RESULTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS laboratory_results (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        pathway_id INTEGER,
        test_id INTEGER,
        technician_id INTEGER,
        result_value TEXT,
        status TEXT DEFAULT 'Pending' NOT NULL,
        performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (pathway_id) REFERENCES clinical_pathways(pathway_id) ON DELETE CASCADE,
        FOREIGN KEY (test_id) REFERENCES laboratory_tests(test_id) ON DELETE CASCADE,
        FOREIGN KEY (technician_id) REFERENCES users(user_id) ON DELETE SET NULL
    )
    """)
    
    # 18. ADMISSIONS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admissions (
        admission_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        admitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        discharged_at TIMESTAMP NULL,
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
    )
    """)
    
    # 19. WARDS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wards (
        ward_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        type TEXT NOT NULL,
        capacity INTEGER NOT NULL
    )
    """)
    
    # 20. BEDS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS beds (
        bed_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ward_id INTEGER,
        bed_number TEXT NOT NULL,
        status TEXT DEFAULT 'Available' NOT NULL,
        FOREIGN KEY (ward_id) REFERENCES wards(ward_id) ON DELETE CASCADE
    )
    """)
    
    # 21. BILLS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bills (
        bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
        pathway_id INTEGER,
        total_amount DECIMAL(10,2) DEFAULT 0.00 NOT NULL,
        discount DECIMAL(10,2) DEFAULT 0.00 NOT NULL,
        insurance_claimed DECIMAL(10,2) DEFAULT 0.00 NOT NULL,
        status TEXT DEFAULT 'Unpaid' NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (pathway_id) REFERENCES clinical_pathways(pathway_id) ON DELETE CASCADE
    )
    """)
    
    # 22. PAYMENTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_id INTEGER,
        amount DECIMAL(10,2) NOT NULL,
        method TEXT NOT NULL,
        status TEXT DEFAULT 'Success' NOT NULL,
        paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (bill_id) REFERENCES bills(bill_id) ON DELETE CASCADE
    )
    """)
    
    # 23. INSURANCE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS insurance (
        insurance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        provider TEXT NOT NULL,
        policy_number TEXT NOT NULL,
        coverage_details TEXT,
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
    )
    """)
    
    # 24. NOTIFICATIONS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT NOT NULL,
        type TEXT NOT NULL,
        status TEXT DEFAULT 'Unread' NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )
    """)
    
    # 25. ACTIVITY LOGS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_logs (
        activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT NOT NULL,
        ip_address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
    )
    """)
    
    # 26. AUDIT LOGS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT NOT NULL,
        module TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
    )
    """)
    
    # 27. LOGIN HISTORY
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login_history (
        login_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        logout_time TIMESTAMP NULL,
        login_status TEXT NOT NULL,
        ip_address TEXT,
        device_name TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
    )
    """)
    
    # 28. SETTINGS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
        setting_key TEXT UNIQUE NOT NULL,
        setting_value TEXT NOT NULL
    )
    """)
    
    # Seed Settings
    cursor.execute("SELECT setting_id FROM settings")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO settings (setting_key, setting_value) VALUES ('theme', 'light')")
        cursor.execute("INSERT INTO settings (setting_key, setting_value) VALUES ('max_login_attempts', '5')")
        cursor.execute("INSERT INTO settings (setting_key, setting_value) VALUES ('session_timeout_minutes', '30')")
        
    # Seed Departments
    cursor.execute("SELECT department_id FROM departments")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO departments (name, description) VALUES ('Emergency', 'Immediate treatment of acute illness and trauma')")
        cursor.execute("INSERT INTO departments (name, description) VALUES ('Cardiology', 'Heart and blood vessel treatments')")
        cursor.execute("INSERT INTO departments (name, description) VALUES ('Pediatrics', 'Medical care for children and infants')")
        cursor.execute("INSERT INTO departments (name, description) VALUES ('General Medicine', 'Primary care and internal medicine')")
        
    # Seed Roles
    cursor.execute("SELECT role_id FROM roles")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO roles (name, description) VALUES ('Admin', 'System and Hospital Administrator')")
        cursor.execute("INSERT INTO roles (name, description) VALUES ('Doctor', 'Medical Practitioner')")
        cursor.execute("INSERT INTO roles (name, description) VALUES ('Nurse', 'Clinical Nursing Staff')")
        cursor.execute("INSERT INTO roles (name, description) VALUES ('Receptionist', 'Front Desk Registration Officer')")
        cursor.execute("INSERT INTO roles (name, description) VALUES ('Pharmacist', 'Pharmacy Inventory & Dispensing Agent')")
        cursor.execute("INSERT INTO roles (name, description) VALUES ('Patient', 'Healthcare Consumer / Client')")
        
    # Fetch Admin Role ID
    cursor.execute("SELECT role_id FROM roles WHERE name = 'Admin'")
    admin_role_id = cursor.fetchone()[0]
    
    # Seed Admin User (username: ADMIN, password: ADMIN)
    cursor.execute("SELECT user_id FROM users WHERE username = 'ADMIN'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO users (full_name, username, email, password_hash, role_id, status)
            VALUES ('System Administrator', 'ADMIN', 'admin@shms.com', '$2b$10$aTdvtkOadKHMNjT5brkqmeOLF8CKLdYinhmzHd.XN9omRNklr2hva', ?, 'Active')
        """, (admin_role_id,))
        
    # Seed Sindiri User (username: Sindiri, password: Aryan@AS_1622)
    cursor.execute("SELECT user_id FROM users WHERE username = 'Sindiri'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO users (full_name, username, email, password_hash, role_id, status)
            VALUES ('Aryan Sindiri', 'Sindiri', 'aryansindiri115714@gmail.com', '$2b$10$g4izTwI0z7zsuhABJQ.ypeqy6MhtjQ5/gU1gYEaCFgJKORNmkVoKG', ?, 'Active')
        """, (admin_role_id,))
        
    # Seed Aryan User (username: Aryan, password: ADMIN)
    cursor.execute("SELECT user_id FROM users WHERE username = 'Aryan'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO users (full_name, username, email, password_hash, role_id, status)
            VALUES ('Sindiri Aryan', 'Aryan', 'aryansindiri9876@gmail.com', '$2b$10$aTvNsqJzjwPJSAD78.X0..IcBpwBejYABcSOd6v8XgZfxxvxSD0DK', ?, 'Active')
        """, (admin_role_id,))
        
    conn.commit()
    cursor.close()

def get_pool():
    global _connection_pool, DB_TYPE
    if DB_TYPE == "sqlite":
        return None
    if _connection_pool is None:
        try:
            config = get_connection_config()
            is_cloud = os.path.exists('/mount/src') or os.getenv("STREAMLIT_SHARING_AUTHOR_KEY") is not None
            if is_cloud and config.get("host") in ("localhost", "127.0.0.1"):
                DB_TYPE = "sqlite"
                return None
            _connection_pool = pooling.MySQLConnectionPool(
                pool_name="shms_pool",
                pool_size=5,
                pool_reset_session=True,
                **config
            )
        except Exception:
            DB_TYPE = "sqlite"
            return None
    return _connection_pool

def get_connection():
    global DB_TYPE
    if DB_TYPE == "sqlite":
        conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), "healthcare.db"), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        init_sqlite_db(conn)
        return conn
    try:
        pool = get_pool()
        if DB_TYPE == "sqlite":
            return get_connection()
        conn = pool.get_connection()
    except Exception:
        try:
            config = get_connection_config()
            conn = mysql.connector.connect(**config)
        except Exception:
            DB_TYPE = "sqlite"
            return get_connection()
    return conn

def execute_query(query, params=None, fetch=False, commit=False):
    global DB_TYPE
    conn = get_connection()
    result = None
    
    if DB_TYPE == "sqlite":
        query = query.replace("%s", "?")
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or ())
            if commit:
                conn.commit()
                result = cursor.lastrowid if query.strip().upper().startswith("INSERT") else cursor.rowcount
            elif fetch:
                rows = cursor.fetchall()
                result = [dict(row) for row in rows]
        except Exception as e:
            if commit:
                conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    else:
        cursor = conn.cursor(dictionary=True, buffered=True)
        try:
            cursor.execute(query, params or ())
            if commit:
                conn.commit()
                result = cursor.lastrowid if query.strip().upper().startswith("INSERT") else cursor.rowcount
            elif fetch:
                result = cursor.fetchall()
        except Exception as e:
            if commit:
                conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
            
    return result

def check_db_connection():
    try:
        conn = get_connection()
        conn.close()
        return True
    except Exception:
        return False
