import { useState } from 'react'


interface Patient {
  id: number;
  name: string;
  age: number;
  gender: string;
  bloodGroup: string;
  stage: string;
  symptoms: string;
  diagnosis: string;
}

function App() {
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [selectedPatientId, setSelectedPatientId] = useState<number>(1);
  const [symptomsInput, setSymptomsInput] = useState<string>('');
  const [aiPrediction, setAiPrediction] = useState<any>(null);
  const [loadingAI, setLoadingAI] = useState<boolean>(false);
  
  // Vitals State
  const [bp, setBp] = useState<string>('120/80');
  const [pulse, setPulse] = useState<number>(72);
  const [temp, setTemp] = useState<number>(98.6);
  const [vitalsLogged, setVitalsLogged] = useState<boolean>(false);

  // Mock Patients list matching Database schema initial load
  const [patients, setPatients] = useState<Patient[]>([
    { id: 1, name: 'Jane Doe', age: 34, gender: 'Female', bloodGroup: 'O+', stage: 'Triage', symptoms: 'Mild chest pain and shortness of breath', diagnosis: 'Pending evaluation' },
    { id: 2, name: 'John Smith', age: 45, gender: 'Male', bloodGroup: 'A-', stage: 'Diagnosis', symptoms: 'Chronic fever, fatigue, and dry cough', diagnosis: 'Acute viral bronchitis' },
    { id: 3, name: 'Robert Johnson', age: 58, gender: 'Male', bloodGroup: 'B+', stage: 'Treatment', symptoms: 'Polydipsia, polyuria, and blurred vision', diagnosis: 'Uncontrolled Type II Diabetes' }
  ]);

  const selectedPatient = patients.find(p => p.id === selectedPatientId) || patients[0];

  const stages = ["Registration", "Triage", "Diagnosis", "Laboratory", "Treatment", "Pharmacy", "Billing", "Discharge"];

  // Transition patient stage
  const handleTransition = (newStage: string) => {
    setPatients(prev => prev.map(p => {
      if (p.id === selectedPatientId) {
        return { ...p, stage: newStage };
      }
      return p;
    }));
  };

  // Run AI Symptom check simulation
  const handleAISymptomCheck = () => {
    if (!symptomsInput) return;
    setLoadingAI(true);
    setTimeout(() => {
      const input = symptomsInput.toLowerCase();
      let prediction = {
        disease: 'Undetermined Infection',
        probability: 0.50,
        severity: 'Low',
        department: 'General Medicine',
        recommendation: 'Rest, stay hydrated, and consult a general practitioner if symptoms persist.'
      };
      
      if (input.includes('chest') || input.includes('breath') || input.includes('heart')) {
        prediction = {
          disease: 'Coronary Artery Disease (Angina)',
          probability: 0.85,
          severity: 'High',
          department: 'Cardiology',
          recommendation: 'Immediate referral to cardiology department. Schedule ECG and Troponin blood tests.'
        };
      } else if (input.includes('fever') || input.includes('cough') || input.includes('throat')) {
        prediction = {
          disease: 'Acute Bronchial Infection (Flu)',
          probability: 0.75,
          severity: 'Medium',
          department: 'General Medicine',
          recommendation: 'Rest, paracetamol 650mg, and consult physician for auscultation check.'
        };
      } else if (input.includes('urine') || input.includes('hunger') || input.includes('thirst')) {
        prediction = {
          disease: 'Diabetes Mellitus Type II',
          probability: 0.80,
          severity: 'Medium',
          department: 'Endocrinology',
          recommendation: 'Order fasting blood glucose and HbA1c test. Limit simple carbohydrates.'
        };
      }
      setAiPrediction(prediction);
      setLoadingAI(false);
    }, 1000);
  };

  const handleLogVitals = (e: React.FormEvent) => {
    e.preventDefault();
    setVitalsLogged(true);
    setTimeout(() => setVitalsLogged(false), 3000);
  };

  return (
    <div className="dashboard-container" style={{ width: '100%' }}>
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <span className="material-icons">local_hospital</span>
          <span>SHMS HIMS Portal</span>
        </div>
        <ul className="sidebar-menu">
          <li 
            className={`menu-item ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('dashboard')}
          >
            <span className="material-icons">dashboard</span>
            <span>Clinical Dashboard</span>
          </li>
          <li 
            className={`menu-item ${activeTab === 'pathways' ? 'active' : ''}`}
            onClick={() => setActiveTab('pathways')}
          >
            <span className="material-icons">swap_calls</span>
            <span>Clinical Pathways</span>
          </li>
          <li 
            className={`menu-item ${activeTab === 'ehr' ? 'active' : ''}`}
            onClick={() => setActiveTab('ehr')}
          >
            <span className="material-icons">medical_services</span>
            <span>Medical Records</span>
          </li>
          <li 
            className={`menu-item ${activeTab === 'audit' ? 'active' : ''}`}
            onClick={() => setActiveTab('audit')}
          >
            <span className="material-icons">security</span>
            <span>Control & Audits</span>
          </li>
        </ul>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        {activeTab === 'dashboard' && (
          <div>
            <div className="page-header">
              <h1>Operational Clinical Dashboard</h1>
              <p>Real-time hospital statistics, active cases, and vital indicators.</p>
            </div>

            <div className="metrics-grid">
              <div className="card metric-card">
                <div className="metric-info">
                  <span style={{ color: 'grey', fontSize: '0.85rem' }}>Active Patient Pathways</span>
                  <h3>{patients.length}</h3>
                </div>
                <span className="material-icons metric-icon">timeline</span>
              </div>
              <div className="card metric-card">
                <div className="metric-info">
                  <span style={{ color: 'grey', fontSize: '0.85rem' }}>Doctors on Shift</span>
                  <h3>8</h3>
                </div>
                <span className="material-icons metric-icon" style={{ color: '#10b981' }}>badge</span>
              </div>
              <div className="card metric-card">
                <div className="metric-info">
                  <span style={{ color: 'grey', fontSize: '0.85rem' }}>Beds Available</span>
                  <h3>14 / 20</h3>
                </div>
                <span className="material-icons metric-icon" style={{ color: '#f59e0b' }}>meeting_room</span>
              </div>
              <div className="card metric-card">
                <div className="metric-info">
                  <span style={{ color: 'grey', fontSize: '0.85rem' }}>Pending Labs</span>
                  <h3>3</h3>
                </div>
                <span className="material-icons metric-icon" style={{ color: '#ef4444' }}>biotech</span>
              </div>
            </div>

            <div className="card" style={{ background: 'rgba(255, 255, 255, 0.85)', backdropFilter: 'blur(8px)' }}>
              <h2>Active Cases List</h2>
              <div className="table-container">
                <table className="hims-table">
                  <thead>
                    <tr>
                      <th>Patient ID</th>
                      <th>Name</th>
                      <th>Age/Gender</th>
                      <th>Blood Group</th>
                      <th>Presented Symptoms</th>
                      <th>Workflow Stage</th>
                    </tr>
                  </thead>
                  <tbody>
                    {patients.map(p => (
                      <tr key={p.id}>
                        <td>PAT_00{p.id}</td>
                        <td style={{ fontWeight: '600' }}>{p.name}</td>
                        <td>{p.age} / {p.gender}</td>
                        <td>{p.bloodGroup}</td>
                        <td>{p.symptoms}</td>
                        <td>
                          <span className="badge badge-stage">{p.stage}</span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'pathways' && (
          <div>
            <div className="page-header">
              <h1>Clinical Pathway Workflow Tracker</h1>
              <p>Manage, track, and update the patient care timeline.</p>
            </div>

            <div className="card" style={{ marginBottom: '24px', background: 'rgba(255, 255, 255, 0.85)', backdropFilter: 'blur(8px)' }}>
              <div className="form-group">
                <label>Select Case / Patient File:</label>
                <select 
                  className="form-control"
                  value={selectedPatientId}
                  onChange={(e) => {
                    setSelectedPatientId(Number(e.target.value));
                    setSymptomsInput('');
                    setAiPrediction(null);
                  }}
                >
                  {patients.map(p => (
                    <option key={p.id} value={p.id}>{p.name} (ID: PAT_00{p.id})</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Horizontal Workflow Stepper */}
            <div className="pathway-flow">
              {stages.map((stg, i) => {
                const isActive = stg === selectedPatient.stage;
                const isCompleted = stages.indexOf(selectedPatient.stage) > i;
                return (
                  <div 
                    key={stg} 
                    className={`flow-step ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}`}
                    style={{ background: 'rgba(255, 255, 255, 0.85)', backdropFilter: 'blur(8px)' }}
                  >
                    <span className="material-icons" style={{ fontSize: '1rem' }}>
                      {isCompleted ? 'check_circle' : isActive ? 'rotate_right' : 'radio_button_unchecked'}
                    </span>
                    <span>{stg}</span>
                  </div>
                );
              })}
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
              <div className="card" style={{ background: 'rgba(255, 255, 255, 0.85)', backdropFilter: 'blur(8px)' }}>
                <h2>Clinical Actions</h2>
                <div style={{ margin: '16px 0' }}>
                  <p><strong>Patient Name:</strong> {selectedPatient.name}</p>
                  <p><strong>Gender/Age:</strong> {selectedPatient.gender} / {selectedPatient.age} yrs</p>
                  <p><strong>Diagnosis:</strong> {selectedPatient.diagnosis}</p>
                </div>
                
                <div className="form-group">
                  <label>Update Pipeline Workflow Stage:</label>
                  <select 
                    className="form-control"
                    value={selectedPatient.stage}
                    onChange={(e) => handleTransition(e.target.value)}
                  >
                    {stages.map(stg => (
                      <option key={stg} value={stg}>{stg}</option>
                    ))}
                  </select>
                </div>
                
                <div className="form-group" style={{ marginTop: '20px' }}>
                  <label>Symptoms / Clinical Presentation Notes:</label>
                  <textarea 
                    className="form-control"
                    rows={4}
                    value={symptomsInput || selectedPatient.symptoms}
                    onChange={(e) => setSymptomsInput(e.target.value)}
                    placeholder="Enter presented clinical indicators to check diagnosis"
                  />
                </div>
              </div>

              <div className="card" style={{ background: 'rgba(255, 255, 255, 0.85)', backdropFilter: 'blur(8px)' }}>
                <h2>AI Clinical Decision Assistant</h2>
                <p style={{ color: 'grey', fontSize: '0.85rem' }}>
                  Query machine learning prediction models on symptoms notes.
                </p>
                
                <div style={{ marginTop: '20px' }}>
                  <button 
                    className="btn btn-primary"
                    onClick={handleAISymptomCheck}
                    disabled={loadingAI}
                  >
                    <span className="material-icons" style={{ fontSize: '1.2rem' }}>psychology</span>
                    {loadingAI ? 'Processing Vitals...' : 'Query AI Symptom Checker'}
                  </button>
                </div>

                {aiPrediction && (
                  <div className={`alert ${aiPrediction.severity === 'High' ? 'alert-danger' : 'alert-info'}`} style={{ marginTop: '24px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontWeight: '700' }}>
                      <span className="material-icons">warning</span>
                      <span>AI Predicted: {aiPrediction.disease} ({intToPct(aiPrediction.probability)})</span>
                    </div>
                    <p style={{ marginTop: '8px', fontSize: '0.9rem' }}>
                      <strong>Referral Department:</strong> {aiPrediction.department}<br/>
                      <strong>Recommendation:</strong> {aiPrediction.recommendation}
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'ehr' && (
          <div>
            <div className="page-header">
              <h1>Electronic Health Record (EHR) entry</h1>
              <p>Record, manage, and audit clinical patient health histories.</p>
            </div>

            <div className="card" style={{ maxWidth: '600px', margin: '0 auto', background: 'rgba(255, 255, 255, 0.85)', backdropFilter: 'blur(8px)' }}>
              <h2>Log Patient Vitals</h2>
              <form onSubmit={handleLogVitals} style={{ marginTop: '20px' }}>
                <div className="form-group">
                  <label>Blood Pressure (mmHg):</label>
                  <input 
                    type="text" 
                    className="form-control"
                    value={bp}
                    onChange={(e) => setBp(e.target.value)}
                  />
                </div>
                <div className="form-group">
                  <label>Pulse Rate (BPM):</label>
                  <input 
                    type="number" 
                    className="form-control"
                    value={pulse}
                    onChange={(e) => setPulse(Number(e.target.value))}
                  />
                </div>
                <div className="form-group">
                  <label>Temperature (°F):</label>
                  <input 
                    type="number" 
                    className="form-control"
                    step="0.1"
                    value={temp}
                    onChange={(e) => setTemp(Number(e.target.value))}
                  />
                </div>
                <button type="submit" className="btn btn-success" style={{ width: '100%', marginTop: '16px' }}>
                  <span className="material-icons">save</span>
                  Save Vitals to EHR
                </button>
              </form>

              {vitalsLogged && (
                <div className="alert alert-success" style={{ marginTop: '16px', textAlign: 'center' }}>
                  Vitals successfully updated in Patient EHR.
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'audit' && (
          <div>
            <div className="page-header">
              <h1>HIMS System Logs & Auditing</h1>
              <p>Secured activity audits and authentication logs.</p>
            </div>

            <div className="card" style={{ background: 'rgba(255, 255, 255, 0.85)', backdropFilter: 'blur(8px)' }}>
              <h2>Security Logs</h2>
              <div className="table-container">
                <table className="hims-table">
                  <thead>
                    <tr>
                      <th>Log ID</th>
                      <th>User</th>
                      <th>Action Module</th>
                      <th>Security Description</th>
                      <th>Timestamp</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>AUD_981</td>
                      <td>ADMIN</td>
                      <td>Authentication</td>
                      <td>Successful login from IP 192.168.1.45 (Device: ARYANSINDIRIS-D)</td>
                      <td>2026-07-23 12:30:11</td>
                    </tr>
                    <tr>
                      <td>AUD_982</td>
                      <td>Sindiri</td>
                      <td>ClinicalPathways</td>
                      <td>Transitioned pathway flow for Jane Doe to [Triage]</td>
                      <td>2026-07-23 12:34:25</td>
                    </tr>
                    <tr>
                      <td>AUD_983</td>
                      <td>Aryan</td>
                      <td>EHR</td>
                      <td>Logged clinical vitals (BP: 120/80, Pulse: 72) for Jane Doe</td>
                      <td>2026-07-23 12:38:09</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

function intToPct(val: number) {
  return `${Math.round(val * 100)}%`;
}

export default App
