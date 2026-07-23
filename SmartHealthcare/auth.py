import bcrypt
import streamlit as st
import socket
from datetime import datetime
import db

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_client_details():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address, hostname
    except Exception:
        return "127.0.0.1", "Unknown"

def login(username, password):
    # Query user details and role name
    query = """
        SELECT u.user_id, u.full_name, u.username, u.email, u.password_hash, u.status, r.name AS role_name 
        FROM users u 
        LEFT JOIN roles r ON u.role_id = r.role_id 
        WHERE u.username = %s
    """
    users = db.execute_query(query, (username,), fetch=True)
    ip_addr, device = get_client_details()
    
    if not users:
        log_audit(None, "LOGIN_FAILED", "Authentication", f"Failed login attempt for username: {username} (User not found)")
        return False, "Invalid username or password"
        
    user = users[0]
    
    if user['status'] != 'Active':
        log_audit(user['user_id'], "LOGIN_FAILED", "Authentication", f"Failed login attempt for {username} (Account suspended)")
        return False, f"Account is {user['status']}. Please contact administrator."
        
    if check_password(password, user['password_hash']):
        # Insert into login_history
        login_query = """
            INSERT INTO login_history (user_id, login_status, ip_address, device_name)
            VALUES (%s, 'Success', %s, %s)
        """
        login_id = db.execute_query(login_query, (user['user_id'], ip_addr, device), commit=True)
        
        # Log audit
        log_audit(user['user_id'], "LOGIN_SUCCESS", "Authentication", f"Logged in from {ip_addr} ({device})")
        
        # Save to streamlit session state
        st.session_state.logged_in = True
        st.session_state.user_id = user['user_id']
        st.session_state.username = user['username']
        st.session_state.full_name = user['full_name']
        st.session_state.role = user['role_name']
        st.session_state.login_id = login_id
        
        return True, "Login successful"
    else:
        # Log failed login history
        login_query = """
            INSERT INTO login_history (user_id, login_status, ip_address, device_name)
            VALUES (%s, 'Failed', %s, %s)
        """
        db.execute_query(login_query, (user['user_id'], ip_addr, device), commit=True)
        
        log_audit(user['user_id'], "LOGIN_FAILED", "Authentication", f"Failed password attempt for username: {username}")
        return False, "Invalid username or password"

def logout():
    if getattr(st.session_state, 'logged_in', False):
        user_id = st.session_state.get('user_id')
        login_id = st.session_state.get('login_id')
        
        if login_id:
            logout_query = "UPDATE login_history SET logout_time = %s WHERE login_id = %s"
            db.execute_query(logout_query, (datetime.now(), login_id), commit=True)
            
        log_audit(user_id, "LOGOUT", "Authentication", f"User {st.session_state.get('username')} logged out")
        
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.full_name = None
    st.session_state.role = None
    st.session_state.login_id = None

def log_audit(user_id, action, module, description):
    query = """
        INSERT INTO audit_logs (user_id, action, module, description)
        VALUES (%s, %s, %s, %s)
    """
    try:
        db.execute_query(query, (user_id, action, module, description), commit=True)
    except Exception as e:
        print(f"Failed to log audit: {e}")
