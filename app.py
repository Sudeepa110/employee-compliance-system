import streamlit as st
import pandas as pd
import joblib
import json
from datetime import datetime
import hashlib

# Load model
model = joblib.load("compliance_model.pkl")
st.success("✅ Model loaded successfully!")

# Load blockchain
try:
    with open("compliance_blockchain.json", "r") as f:
        blockchain_data = json.load(f)
except FileNotFoundError:
    blockchain_data = []

# Blockchain functions
def compute_hash(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def create_block(data, previous_hash):
    block = {
        'index': len(blockchain_data) + 1,
        'timestamp': datetime.now().timestamp(),
        'data': data,
        'previous_hash': previous_hash,
        'hash': ''
    }
    block['hash'] = compute_hash(block)
    return block

def add_to_blockchain(data):
    prev_hash = blockchain_data[-1]['hash'] if blockchain_data else '0'
    block = create_block(data, prev_hash)
    blockchain_data.append(block)
    with open("compliance_blockchain.json", "w") as f:
        json.dump(blockchain_data, f, indent=2)

# Streamlit UI
st.title("📊 Employee Policy Compliance Predictor")

with st.form("compliance_form"):
    working_days = st.number_input("Working Days", min_value=0, max_value=31)
    target_sales = st.number_input("Target Sales", min_value=0)
    actual_sales = st.number_input("Actual Sales", min_value=0)
    cust_sat = st.slider("Customer Satisfaction Score", 1, 5)
    month = st.selectbox("Month", list(range(1, 13)))

    # Derived flags
    low_working_days = working_days < 20
    target_not_met = actual_sales < target_sales
    low_cust_sat = cust_sat < 3

    submitted = st.form_submit_button("Predict Compliance")

    if submitted:
        # ⚠️ Order must match training
        input_data = pd.DataFrame([[
            working_days,
            target_sales,
            actual_sales,
            cust_sat,
            low_working_days,
            target_not_met,
            low_cust_sat,
            month
        ]], columns=[
            "Working_Days",
            "Target_Sales",
            "Actual_Sales",
            "Customer_Satisfaction_Score",
            "Low_Working_Days",
            "Target_Not_Met",
            "Low_Customer_Satisfaction",
            "Month"
        ])

        # Make prediction
        prediction = model.predict(input_data)[0]
        result = "✅ Compliant" if prediction == 1 else "❌ Non-Compliant"
        st.subheader("Prediction Result:")
        st.info(result)

        # Add to blockchain
        record = input_data.iloc[0].to_dict()
        record['Prediction'] = result
        add_to_blockchain(record)

        st.success("📦 Record added to blockchain!")

# Show Blockchain
st.markdown("---")
st.subheader("🔗 Blockchain Ledger (Last 3 Blocks)")
for block in blockchain_data[-3:]:
    st.json(block)
