import streamlit as st
import pandas as pd
import numpy as np
import os
import base64
import requests
from datetime import datetime
import db
import auth

# Set page config
st.set_page_config(
    page_title="Smart Healthcare Management System (SHMS)",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper for base64 background encoding
def get_base64_image(image_path):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    except Exception:
        pass
    return ""

# Initialize Session States
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'full_name' not in st.session_state:
    st.session_state.full_name = None
if 'role' not in st.session_state:
    st.session_state.role = None
if 'menu' not in st.session_state:
    st.session_state.menu = "📊 Clinical Dashboard"

# Get base64 string for global stethoscope background dynamically and absolutely
db_dir = os.path.dirname(os.path.abspath(__file__))
bg_path = os.path.join(db_dir, "login_stethoscope_bg.jpg")
bg_base64 = get_base64_image(bg_path)

# Custom CSS for Premium Design & Google Material Icons Integration
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<style>
    html, body, [class*="css"] {{
        font-family: 'Outfit', sans-serif;
    }}
    
    /* Custom Cursor Styles */
    button, [role="button"], a, select, input[type="submit"] {{
        cursor: pointer !important;
    }}
    
    /* Striped Design on the Edges of the Application */
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: repeating-linear-gradient(
            -45deg,
            #0f766e,
            #0f766e 12px,
            #0d9488 12px,
            #0d9488 24px
        );
        z-index: 999999;
    }}
    
    [data-testid="stSidebar"]::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        width: 5px;
        background: repeating-linear-gradient(
            45deg,
            #0f766e,
            #0f766e 12px,
            #0d9488 12px,
            #0d9488 24px
        );
        z-index: 99999;
    }}
    
    /* Global Stethoscope Watermark Background across ALL pages using theme-aware color-mix */
    [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(
            color-mix(in srgb, var(--background-color) 92%, transparent), 
            color-mix(in srgb, var(--background-color) 96%, transparent)
        ), url("data:image/jpg;base64,{bg_base64}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    
    [data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0) !important;
    }}
    
    /* Premium Sidebar Styling using color-mix */
    [data-testid="stSidebar"] {{
        background: color-mix(in srgb, var(--background-color) 93%, transparent) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border-right: 1px solid color-mix(in srgb, var(--text-color) 12%, transparent) !important;
    }}
    
    /* Premium Boxed Options in the Navigation */
    [data-testid="stSidebar"] button {{
        text-align: left !important;
        justify-content: flex-start !important;
        border-radius: 8px !important;
        padding: 12px 18px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        margin-bottom: 8px !important;
        display: flex !important;
        width: 100% !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
    }}
    
    /* Active Navigation Option Box (Primary Blue-Teal) */
    [data-testid="stSidebar"] button[kind="primary"] {{
        background-color: #0f766e !important;
        color: white !important;
        border: 1px solid #115e59 !important;
        box-shadow: 0 4px 12px rgba(15, 118, 110, 0.25) !important;
    }}
    
    /* Inactive Navigation Option Box (Theme-contrast background) */
    [data-testid="stSidebar"] button[kind="secondary"] {{
        background-color: color-mix(in srgb, var(--background-color) 80%, transparent) !important;
        color: var(--text-color) !important;
        border: 1px solid color-mix(in srgb, var(--text-color) 12%, transparent) !important;
    }}
    
    [data-testid="stSidebar"] button:hover {{
        transform: translateX(6px) !important;
        background-color: rgba(13, 148, 136, 0.1) !important;
        border-color: #0d9488 !important;
        color: #0d9488 !important;
    }}
    
    /* Opposing backgrounds: Card elements have distinct contrasting shades */
    .card-panel {{
        background: color-mix(in srgb, var(--background-color) 85%, transparent) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid color-mix(in srgb, var(--text-color) 12%, transparent) !important;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        margin-bottom: 24px;
        color: var(--text-color) !important;
    }}
    
    .main-title-banner {{
        background: linear-gradient(135deg, #0f766e 0%, #115e59 100%);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        color: white;
        box-shadow: 0 10px 25px rgba(15, 118, 110, 0.2);
        display: flex;
        align-items: center;
        gap: 20px;
    }}
    .main-title-banner .logo-icon {{
        font-size: 3.5rem;
        color: #2dd4bf;
    }}
    .main-title-banner h1 {{
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(135deg, #2dd4bf 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    
    .metric-card {{
        background: color-mix(in srgb, var(--background-color) 85%, transparent) !important;
        backdrop-filter: blur(8px) !important;
        border: 1px solid color-mix(in srgb, var(--text-color) 12%, transparent) !important;
        border-radius: 12px;
        padding: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s;
        color: var(--text-color) !important;
    }}
    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }}
    .metric-card .icon {{
        font-size: 2.8rem;
        color: #0f766e;
    }}
    .pathway-step {{
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 14px;
        background: color-mix(in srgb, var(--background-color) 85%, transparent);
        border: 1px solid color-mix(in srgb, var(--text-color) 12%, transparent);
        border-radius: 8px;
        font-weight: 500;
        color: var(--text-color) !important;
    }}
    .pathway-step.active {{
        background: rgba(15, 118, 110, 0.1);
        border-color: #0f766e;
        color: #0f766e !important;
    }}
    .pathway-step.completed {{
        background: rgba(16, 185, 129, 0.1);
        border-color: #10b981;
        color: #10b981 !important;
    }}
</style>
""", unsafe_allow_html=True)

# 1. LOGIN SCREEN - CENTERED GLASSMORPHIC CARD WITH STETHOSCOPE
if not st.session_state.logged_in:
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(
            color-mix(in srgb, var(--background-color) 82%, transparent), 
            color-mix(in srgb, var(--background-color) 90%, transparent)
        ), url("data:image/jpg;base64,{bg_base64}") !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    
    /* Center the Form Card */
    div[data-testid="stForm"] {{
        background: color-mix(in srgb, var(--background-color) 82%, transparent) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border: 1px solid color-mix(in srgb, var(--text-color) 15%, transparent) !important;
        border-radius: 16px !important;
        padding: 40px !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3) !important;
        max-width: 480px !important;
        margin: 80px auto 0 auto !important;
        color: var(--text-color) !important;
    }}
    
    div[data-testid="stForm"] label {{
        color: var(--text-color) !important;
        font-weight: 600 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Render Centered Login Header
    cols = st.columns([1, 2, 1])
    with cols[1]:
        st.markdown("""
        <div style="text-align: center; margin-top: 40px; margin-bottom: -40px;">
            <span class="material-icons" style="font-size: 5.5rem; color: #0f766e;">local_hospital</span>
            <h1 style="margin: 10px 0; font-weight: 700; font-size: 2.3rem;">Smart Healthcare</h1>
            <p style="color: grey; margin: 0; font-size: 1.05rem;">Hospital Management & Pathway Portal</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", value="", placeholder="Enter clinical username")
            password = st.text_input("Password", type="password", placeholder="Enter security password")
            submit = st.form_submit_button("Sign In")
            
            if submit:
                if username and password:
                    success, msg = auth.login(username, password)
                    if success:
                        st.success("Login Successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Please fill in all fields.")
                    
        st.markdown(f"""
        <div style="text-align: center; margin-top: 30px; font-size: 0.85rem; color: color-mix(in srgb, var(--text-color) 60%, transparent);">
            <b>Default Seeding Credentials:</b><br/>
            Admin: <code>ADMIN</code> / <code>ADMIN</code><br/>
            Clinician: <code>Sindiri</code> / <code>Aryan@AS_1622</code>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# 2. LOGGED IN LAYOUT
st.markdown(f"""
<div class="main-title-banner">
    <span class="material-icons logo-icon">healing</span>
    <div>
        <h1>Smart Healthcare Management System</h1>
        <p style="margin: 0; opacity: 0.85;">Hospital Information & Clinical Pathway Engine | Connected: {st.session_state.full_name} ({st.session_state.role})</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation (Slide buttons)
with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding-bottom: 15px;">
        <span class="material-icons" style="font-size: 3.5rem; color: #0f766e;">account_circle</span>
        <h4 style="margin: 5px 0 0 0; color: var(--text-color);">{st.session_state.full_name}</h4>
        <span style="font-size: 0.8rem; background: rgba(15, 118, 110, 0.1); color: #0f766e; padding: 2px 8px; border-radius: 12px; font-weight: 600;">{st.session_state.role}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"<p style='font-weight:600; color:color-mix(in srgb, var(--text-color) 50%, transparent); font-size:0.8rem; text-transform:uppercase;'>Navigation Menu</p>", unsafe_allow_html=True)
    
    # Custom vertical button list
    menu_items = [
        "📊 Clinical Dashboard",
        "👤 Patient Registration",
        "🔄 Clinical Pathways",
        "📝 EHR & Lab Records",
        "💳 Billing & Pharmacy",
        "⚙️ Control & Audit Logs"
    ]
    
    for item in menu_items:
        is_active = st.session_state.menu == item
        btn_type = "primary" if is_active else "secondary"
        if st.sidebar.button(item, key=f"nav_{item}", use_container_width=True, type=btn_type):
            st.session_state.menu = item
            st.rerun()
            
    st.markdown("---")
    if st.sidebar.button("🚪 Sign Out", use_container_width=True):
        auth.logout()
        st.rerun()

menu = st.session_state.menu

# Helpers to call FastAPI AI Services with Fallbacks
def call_symptom_checker(symptoms):
    try:
        r = requests.post("http://127.0.0.1:8000/ai/symptom-checker", json={"symptoms": symptoms}, timeout=2)
        if r.status_code == 200:
            return r.json()["predictions"]
    except Exception:
        pass
    # Offline fallback logic
    s = [sm.lower() for sm in symptoms]
    if any(item in s for item in ["chest pain", "shortness of breath"]):
        return [{"disease": "Angina / Coronary Heart Disease", "probability": 0.80, "severity": "High", "department": "Cardiology", "recommendation": "Urgent Cardiology consult and ECG."}]
    return [{"disease": "Viral Infection / Common Flu", "probability": 0.70, "severity": "Low", "department": "General Medicine", "recommendation": "Hydration and symptomatic rest."}]

# ----------------- MENU: DASHBOARD -----------------
if menu == "📊 Clinical Dashboard":
    st.header("Operational Overview Dashboard")
    
    # Run DB count queries
    patients_count = db.execute_query("SELECT count(*) as cnt FROM patients", fetch=True)[0]['cnt']
    pathways_count = db.execute_query("SELECT count(*) as cnt FROM clinical_pathways WHERE status = 'Active'", fetch=True)[0]['cnt']
    depts_count = db.execute_query("SELECT count(*) as cnt FROM departments", fetch=True)[0]['cnt']
    appointments_count = db.execute_query("SELECT count(*) as cnt FROM appointments WHERE status = 'Scheduled'", fetch=True)[0]['cnt']
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div>
                <h5 style="margin: 0; color: color-mix(in srgb, var(--text-color) 60%, transparent);">Registered Patients</h5>
                <h2 style="margin: 5px 0 0 0; font-weight: 700;">{patients_count}</h2>
            </div>
            <span class="material-icons icon">people</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div>
                <h5 style="margin: 0; color: color-mix(in srgb, var(--text-color) 60%, transparent);">Active Pathways</h5>
                <h2 style="margin: 5px 0 0 0; font-weight: 700; color: #10b981;">{pathways_count}</h2>
            </div>
            <span class="material-icons icon" style="color: #10b981;">swap_calls</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div>
                <h5 style="margin: 0; color: color-mix(in srgb, var(--text-color) 60%, transparent);">Medical Departments</h5>
                <h2 style="margin: 5px 0 0 0; font-weight: 700;">{depts_count}</h2>
            </div>
            <span class="material-icons icon" style="color: #f59e0b;">local_pharmacy</span>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div>
                <h5 style="margin: 0; color: color-mix(in srgb, var(--text-color) 60%, transparent);">Appointments Scheduled</h5>
                <h2 style="margin: 5px 0 0 0; font-weight: 700;">{appointments_count}</h2>
            </div>
            <span class="material-icons icon" style="color: #e879f9;">calendar_month</span>
        </div>
        """, unsafe_allow_html=True)

    # Show active pathways list
    st.subheader("Active Patient Pathways Status")
    query = """
        SELECT p.patient_id, u.full_name, cp.pathway_id, cp.current_stage, cp.symptoms, cp.created_at 
        FROM clinical_pathways cp
        JOIN patients p ON cp.patient_id = p.patient_id
        JOIN users u ON p.user_id = u.user_id
        WHERE cp.status = 'Active'
        ORDER BY cp.created_at DESC
    """
    pathways = db.execute_query(query, fetch=True)
    
    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    if pathways:
        pathways_df = pd.DataFrame(pathways)
        pathways_df.columns = ["Patient ID", "Patient Name", "Pathway ID", "Current Stage", "Presented Symptoms", "Admission Date"]
        st.dataframe(pathways_df, use_container_width=True)
    else:
        st.info("No active patient pathways currently tracking.")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- MENU: PATIENT REGISTRATION -----------------
elif menu == "👤 Patient Registration":
    st.header("Patient Registration and Records")
    
    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    with st.form("patient_registration_form"):
        st.subheader("New Patient Account Details")
        full_name = st.text_input("Patient Name")
        email = st.text_input("Email Address")
        dob = st.date_input("Date of Birth", min_value=datetime(1920, 1, 1))
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        emergency_contact = st.text_input("Emergency Contact Number")
        
        submit_btn = st.form_submit_button("Register Patient")
        
        if submit_btn:
            if full_name and email:
                # Generate unique username
                username = email.split('@')[0] + "_" + str(np.random.randint(100, 999))
                # Insert user
                role_query = "SELECT role_id FROM roles WHERE name = 'Patient'"
                role_id = db.execute_query(role_query, fetch=True)[0]['role_id']
                
                user_id = db.execute_query("""
                    INSERT INTO users (full_name, username, email, password_hash, role_id, status)
                    VALUES (%s, %s, %s, 'hashed_patient_pass', %s, 'Active')
                """, (full_name, username, email, role_id), commit=True)
                
                # Insert patient details
                db.execute_query("""
                    INSERT INTO patients (user_id, gender, dob, blood_group, emergency_contact)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, gender, dob.strftime("%Y-%m-%d"), blood_group, emergency_contact), commit=True)
                
                auth.log_audit(st.session_state.user_id, "PATIENT_REGISTER", "Patients", f"Registered new patient {full_name} (Username: {username})")
                st.success(f"Patient {full_name} registered successfully! Default login generated: Username: {username}")
            else:
                st.error("Please fill in the Patient Name and Email fields.")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- MENU: CLINICAL PATHWAYS -----------------
elif menu == "🔄 Clinical Pathways":
    st.header("Clinical Workflow & Pathway Tracker")
    
    # 1. Fetch Patients
    patients = db.execute_query("""
        SELECT p.patient_id, u.full_name 
        FROM patients p 
        JOIN users u ON p.user_id = u.user_id
    """, fetch=True)
    
    if not patients:
        st.warning("Please register a patient first.")
    else:
        patient_options = {p['full_name']: p['patient_id'] for p in patients}
        selected_patient_name = st.selectbox("Select Patient to Manage Pathway:", list(patient_options.keys()))
        patient_id = patient_options[selected_patient_name]
        
        # Check active pathway
        active_pathway = db.execute_query("""
            SELECT * FROM clinical_pathways WHERE patient_id = %s AND status = 'Active'
        """, (patient_id,), fetch=True)
        
        if not active_pathway:
            st.markdown('<div class="card-panel">', unsafe_allow_html=True)
            st.info("No active clinical pathway found for this patient.")
            if st.button("Start New Pathway Flow"):
                # Initialize new pathway
                pathway_id = db.execute_query("""
                    INSERT INTO clinical_pathways (patient_id, current_stage, symptoms)
                    VALUES (%s, 'Triage', 'Patient admitted for diagnosis')
                """, (patient_id,), commit=True)
                st.success(f"Pathway flow initialized (ID: {pathway_id})! Patient placed in Triage.")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            pathway = active_pathway[0]
            pathway_id = pathway['pathway_id']
            current_stage = pathway['current_stage']
            
            # Show Visual Pathway Steps
            stages = ["Registration", "Triage", "Diagnosis", "Laboratory", "Treatment", "Pharmacy", "Billing", "Discharge"]
            cols = st.columns(len(stages))
            for idx, stage in enumerate(stages):
                with cols[idx]:
                    if stage == current_stage:
                        st.markdown(f'<div class="pathway-step active"><span class="material-icons" style="font-size:1.2rem;">rotate_right</span>{stage}</div>', unsafe_allow_html=True)
                    elif stages.index(current_stage) > idx:
                        st.markdown(f'<div class="pathway-step completed"><span class="material-icons" style="font-size:1.2rem;">check_circle</span>{stage}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="pathway-step"><span class="material-icons" style="font-size:1.2rem;">radio_button_unchecked</span>{stage}</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            col_info, col_action = st.columns([1, 1])
            with col_info:
                st.markdown('<div class="card-panel">', unsafe_allow_html=True)
                st.subheader("Current Stage Clinical Data")
                st.write(f"**Pathway ID:** {pathway_id}")
                st.write(f"**Current Stage:** `{current_stage}`")
                st.text_area("Reported Symptoms", value=pathway['symptoms'] or "", key="view_symptoms", disabled=True)
                st.text_area("Diagnosed Finding", value=pathway['diagnosis'] or "Pending evaluation", key="view_diagnosis", disabled=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col_action:
                st.markdown('<div class="card-panel">', unsafe_allow_html=True)
                st.subheader("Update Pathway Stage")
                next_stage_options = stages[stages.index(current_stage):]
                selected_next_stage = st.selectbox("Transition Patient to Stage:", next_stage_options)
                
                symptoms_input = st.text_area("Update Symptoms / Vital Notes:", value=pathway['symptoms'] or "")
                diagnosis_input = st.text_area("Clinical Diagnosis Findings:", value=pathway['diagnosis'] or "")
                
                # AI Symptom Checker Integration
                if st.button("Query AI Symptom Checker"):
                    if symptoms_input:
                        with st.spinner("Calling AI Symptom Checker microservice..."):
                            predictions = call_symptom_checker([symptoms_input])
                            for pred in predictions:
                                st.success(f"**AI Prediction:** {pred['disease']} ({int(pred['probability']*100)}% risk)")
                                st.info(f"**Recommendation:** {pred['recommendation']}")
                                st.write(f"**Referral Dept:** {pred['department']}")
                    else:
                        st.warning("Please type symptoms in the text area above to run the AI checker.")
                
                if st.button("Commit Pathway Transition"):
                    db.execute_query("""
                        UPDATE clinical_pathways 
                        SET current_stage = %s, symptoms = %s, diagnosis = %s
                        WHERE pathway_id = %s
                    """, (selected_next_stage, symptoms_input, diagnosis_input, pathway_id), commit=True)
                    
                    auth.log_audit(st.session_state.user_id, "PATHWAY_UPDATE", "ClinicalPathways", f"Updated pathway {pathway_id} to stage {selected_next_stage}")
                    st.success(f"Patient pathway committed successfully to stage: {selected_next_stage}")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# ----------------- MENU: EHR & LAB -----------------
elif menu == "📝 EHR & Lab Records":
    st.header("Electronic Health Records & Lab Orders")
    # Fetch active pathways
    active_pathways = db.execute_query("""
        SELECT cp.pathway_id, u.full_name 
        FROM clinical_pathways cp
        JOIN patients p ON cp.patient_id = p.patient_id
        JOIN users u ON p.user_id = u.user_id
        WHERE cp.status = 'Active'
    """, fetch=True)
    
    if not active_pathways:
        st.warning("No active patients currently undergoing clinical pathways.")
    else:
        pathway_options = {f"Pathway {p['pathway_id']} - {p['full_name']}": p['pathway_id'] for p in active_pathways}
        selected_pathway_lbl = st.selectbox("Select Patient Case:", list(pathway_options.keys()))
        pathway_id = pathway_options[selected_pathway_lbl]
        
        # Form to log vital signs
        st.markdown('<div class="card-panel">', unsafe_allow_html=True)
        st.subheader("Record Patient Vitals & Notes")
        with st.form("vitals_form"):
            bp = st.text_input("Blood Pressure (mmHg)", value="120/80")
            pulse = st.number_input("Pulse Rate (bpm)", min_value=30, max_value=220, value=72)
            temp = st.number_input("Temperature (°F)", min_value=90.0, max_value=110.0, value=98.6, step=0.1)
            notes = st.text_area("Clinical Notes & Symptoms details")
            
            submit_vitals = st.form_submit_button("Record EHR Vitals")
            
            if submit_vitals:
                # Insert EHR record
                patient_id = db.execute_query("SELECT patient_id FROM clinical_pathways WHERE pathway_id = %s", (pathway_id,), fetch=True)[0]['patient_id']
                ehr_id = db.execute_query("""
                    INSERT INTO ehr_records (patient_id, recorded_by_user_id, notes)
                    VALUES (%s, %s, %s)
                """, (patient_id, st.session_state.user_id, notes), commit=True)
                
                # Insert Vitals
                db.execute_query("""
                    INSERT INTO vitals (ehr_id, patient_id, blood_pressure, pulse_rate, temperature)
                    VALUES (%s, %s, %s, %s, %s)
                """, (ehr_id, patient_id, bp, pulse, temp), commit=True)
                
                auth.log_audit(st.session_state.user_id, "EHR_VITALS_RECORD", "EHR", f"Recorded vital signs for patient ID {patient_id}")
                st.success("Patient vitals and clinical notes successfully stored in electronic health records.")
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------- MENU: BILLING & PHARMACY -----------------
elif menu == "💳 Billing & Pharmacy":
    st.header("Financial Ledger & Pharmacy Invoices")
    
    bills = db.execute_query("""
        SELECT b.bill_id, u.full_name, b.total_amount, b.status, b.created_at 
        FROM bills b 
        JOIN clinical_pathways cp ON b.pathway_id = cp.pathway_id 
        JOIN patients p ON cp.patient_id = p.patient_id 
        JOIN users u ON p.user_id = u.user_id
    """, fetch=True)
    
    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    if not bills:
        st.info("No invoices currently registered in the hospital billing ledger.")
    else:
        bills_df = pd.DataFrame(bills)
        bills_df.columns = ["Invoice ID", "Patient Name", "Total Amount ($)", "Payment Status", "Billing Date"]
        st.dataframe(bills_df, use_container_width=True)
        
        # Payment form
        st.markdown("### Process Invoice Payment")
        invoice_options = {f"Invoice {b['bill_id']} - {b['full_name']} (${b['total_amount']})": b['bill_id'] for b in bills if b['status'] == 'Unpaid'}
        if not invoice_options:
            st.success("All invoices are settled.")
        else:
            selected_inv_lbl = st.selectbox("Select Invoice to Pay:", list(invoice_options.keys()))
            bill_id = invoice_options[selected_inv_lbl]
            payment_method = st.selectbox("Payment Method:", ["Credit Card", "Insurance Claim", "Cash", "Bank Transfer"])
            
            if st.button("Approve Payment"):
                # Update bill status
                db.execute_query("UPDATE bills SET status = 'Paid' WHERE bill_id = %s", (bill_id,), commit=True)
                
                # Fetch amount for log
                amount = db.execute_query("SELECT total_amount FROM bills WHERE bill_id = %s", (bill_id,), fetch=True)[0]['total_amount']
                # Insert payment record
                db.execute_query("""
                    INSERT INTO payments (bill_id, amount, method, status)
                    VALUES (%s, %s, %s, 'Success')
                """, (bill_id, amount, payment_method), commit=True)
                
                auth.log_audit(st.session_state.user_id, "BILL_PAYMENT", "Billing", f"Approved payment for bill ID {bill_id} via {payment_method}")
                st.success("Payment processed successfully! Bill status updated to Paid.")
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- MENU: SECURITY & AUDIT -----------------
elif menu == "⚙️ Control & Audit Logs":
    st.header("Hospital Security Control & Audit Logs")
    
    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    # Audit log panel
    st.subheader("System Access and Action Audit Trails")
    logs = db.execute_query("""
        SELECT a.log_id, u.username, a.action, a.module, a.description, a.created_at 
        FROM audit_logs a
        LEFT JOIN users u ON a.user_id = u.user_id 
        ORDER BY a.created_at DESC 
        LIMIT 50
    """, fetch=True)
    
    if logs:
        logs_df = pd.DataFrame(logs)
        logs_df.columns = ["Audit ID", "User", "Action Triggered", "System Module", "Details", "Timestamp"]
        st.dataframe(logs_df, use_container_width=True)
    else:
        st.info("No system audits recorded yet.")
    st.markdown('</div>', unsafe_allow_html=True)
