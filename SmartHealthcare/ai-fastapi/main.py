from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import re

app = FastAPI(title="Smart Healthcare AI Microservice", version="1.0.0")

# 1. Models
class SymptomRequest(BaseModel):
    symptoms: List[str]

class RiskRequest(BaseModel):
    vitals: Dict[str, Any]
    history: List[str]

class ChatRequest(BaseModel):
    message: str
    session_id: str

# 2. Endpoints
@app.get("/health")
def health_check():
    return {"status": "Healthy", "module": "AI Services Microservice"}

@app.post("/ai/symptom-checker")
def symptom_checker(request: SymptomRequest):
    symptoms_lower = [s.lower().strip() for s in request.symptoms]
    matched_diseases = []
    
    # Simple Rule-based Disease mapping matching standard diagnostic indicators
    if any(s in symptoms_lower for s in ["chest pain", "shortness of breath", "heart palpitations"]):
        matched_diseases.append({
            "disease": "Coronary Artery Disease",
            "probability": 0.85,
            "severity": "High",
            "department": "Cardiology",
            "recommendation": "Consult a cardiologist immediately and schedule an ECG/Treadmill test."
        })
    if any(s in symptoms_lower for s in ["fever", "cough", "sore throat", "fatigue"]):
        matched_diseases.append({
            "disease": "Acute Respiratory Infection (Flu)",
            "probability": 0.75,
            "severity": "Medium",
            "department": "General Medicine",
            "recommendation": "Rest, stay hydrated, and take antipyretics. Consult a physician if fever exceeds 3 days."
        })
    if any(s in symptoms_lower for s in ["polydipsia", "polyuria", "increased hunger", "blurred vision"]):
        matched_diseases.append({
            "disease": "Diabetes Mellitus",
            "probability": 0.80,
            "severity": "Medium",
            "department": "Endocrinology",
            "recommendation": "Check fasting blood sugar and HbA1c levels. Limit carbohydrate intake."
        })
        
    if not matched_diseases:
        matched_diseases.append({
            "disease": "Undetermined Condition",
            "probability": 0.50,
            "severity": "Low",
            "department": "General Medicine",
            "recommendation": "Schedule a routine consultation with a general practitioner for physical examination."
        })
        
    return {"predictions": matched_diseases}

@app.post("/ai/disease-prediction")
def predict_disease_risk(request: RiskRequest):
    vitals = request.vitals
    history = request.history
    
    systolic = vitals.get("systolic_bp", 120)
    pulse = vitals.get("pulse_rate", 72)
    temp = vitals.get("temperature", 98.6)
    
    risk_factors = []
    cardio_risk = 0.10
    
    if systolic > 140:
        risk_factors.append("Hypertension detected")
        cardio_risk += 0.40
    if "Family history of heart disease" in history:
        risk_factors.append("Genetic cardiovascular predisposition")
        cardio_risk += 0.25
    if pulse > 100:
        risk_factors.append("Tachycardia detected")
        cardio_risk += 0.15
        
    return {
        "cardiovascular_risk_index": round(cardio_risk, 2),
        "identified_risks": risk_factors,
        "recommendation": "Refer to specialist if risk index exceeds 0.50."
    }

@app.post("/ai/prescription-assistant")
def suggest_prescriptions(disease_name: str):
    suggestions = {
        "Coronary Artery Disease": [
            {"medicine": "Aspirin 75mg", "dosage": "Once daily after food", "purpose": "Antiplatelet"},
            {"medicine": "Atorvastatin 20mg", "dosage": "Once daily at night", "purpose": "Cholesterol control"}
        ],
        "Acute Respiratory Infection (Flu)": [
            {"medicine": "Paracetamol 650mg", "dosage": "Three times daily as needed", "purpose": "Fever and pain"},
            {"medicine": "Amoxicillin 500mg", "dosage": "Three times daily for 5 days", "purpose": "Antibiotic (if secondary bacterial infection)"}
        ],
        "Diabetes Mellitus": [
            {"medicine": "Metformin 500mg", "dosage": "Twice daily with meals", "purpose": "Hypoglycemic agent"},
            {"medicine": "Glimepiride 1mg", "dosage": "Once daily before breakfast", "purpose": "Insulin secretagogue"}
        ]
    }
    
    recs = suggestions.get(disease_name, [
        {"medicine": "Multivitamin", "dosage": "Once daily", "purpose": "General recovery support"}
    ])
    return {"suggested_medicines": recs}

@app.post("/ai/ocr")
def process_report_ocr(file: UploadFile = File(...)):
    # Simulating OCR extraction on uploaded medical report
    filename = file.filename.lower()
    extracted_text = f"Parsed medical report content for file: {file.filename}\n"
    
    if "blood" in filename:
        extracted_text += "LAB REPORT SUMMARY:\nHb: 14.2 g/dL (Normal)\nWBC Count: 8500 cells/cu.mm (Normal)\nPlatelets: 2.5 Lakhs (Normal)\nGlucose Fasting: 110 mg/dL (Borderline)"
    elif "urine" in filename:
        extracted_text += "URINALYSIS REPORT:\nColor: Pale Yellow\npH: 6.0\nProtein: Nil\nSugar: Nil"
    else:
        extracted_text += "Generic medical record scan. No critical parameters flagged."
        
    return {"extracted_text": extracted_text}

@app.post("/ai/chatbot")
def consult_chatbot(request: ChatRequest):
    msg = request.message.lower()
    
    if "fever" in msg:
        reply = "For fever, monitor temperature regularly. Rest and hydration are critical. If it stays above 102F (38.9C) or lasts over 3 days, please schedule an appointment."
    elif "appointment" in msg:
        reply = "You can schedule appointments with our cardiologists or general medicine physicians directly from the App Dashboard."
    elif "cardiology" in msg:
        reply = "Our Cardiology department specializes in coronary treatments, heart health checks, and vital sign diagnostics."
    else:
        reply = "I am the SHMS Clinical Assistant. How can I help you track your symptoms, vitals, or departments today?"
        
    return {"reply": reply}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
