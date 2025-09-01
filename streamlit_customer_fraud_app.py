import streamlit as st
import json
import os
import datetime
import re
from twilio.rest import Client
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# -----------------------------
# Data & Model Load
# -----------------------------
# Load Dataset (ALWAYS)
df = pd.read_csv(r"C:\Users\rjana\OneDrive\Desktop\ml_cap\creditcard.csv")

model_file = "fraud_rf_model.pkl"

if not os.path.exists(model_file):
    # Train & Save Model (No Warning)
    X = df.drop(columns=["Class"])
    y = df["Class"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    with open(model_file, "wb") as f:
        pickle.dump(model, f)
    
    st.toast("✅ Model trained and saved successfully!")
else:
    with open(model_file, "rb") as f:
        model = pickle.load(f)



CUSTOMER_FILE = "customers.json"
LOG_FILE = "transaction_log.json"

# -----------------------------
# Utility Functions
# -----------------------------
def load_customers():
    if os.path.exists(CUSTOMER_FILE):
        with open(CUSTOMER_FILE, 'r') as file:
            return json.load(file)
    return []

def save_customers(customers):
    with open(CUSTOMER_FILE, 'w') as file:
        json.dump(customers, file, indent=2)

def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as file:
            return json.load(file)
    return []

def save_log(entry):
    logs = load_logs()
    logs.append(entry)
    with open(LOG_FILE, 'w') as file:
        json.dump(logs, file, indent=2)

def validate_phone_number(number):
    return re.match(r'^\+\d{10,15}$', number) is not None

def send_sms_alert(phone_number, customer_name, amount):
    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

        if not validate_phone_number(phone_number):
            raise ValueError("Invalid phone number format. Use international format like +12345678901")

        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"🚨 Alert for {customer_name}: A suspicious transaction of ${amount} was detected.",
            from_=twilio_number,
            to=phone_number
        )
        st.success("📢 SMS sent successfully!")
    except Exception as e:
        st.error(f"❌ Failed to send SMS: {e}")

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Fraud Prevention & Prediction", page_icon="🔐", layout="centered")
st.title("🔐 Real-Time Credit Card Fraud Prevention & Prediction")

menu = st.sidebar.selectbox("Navigate", ["Home", "View Customers", "Add Customer",
                                         "Make Transaction", "Alert Log", "Fraud Prediction"])
customers = load_customers()

# -----------------------------
# Home Screen with Visual Graphs
# -----------------------------
if menu == "Home":
    st.subheader("🏠 Dashboard & Insights")
    st.markdown("""
    #### 🔐 Cybersecurity Tips
    - Never share your OTP or PIN.
    - Use strong and unique passwords.
    - Avoid using public Wi-Fi for transactions.
    - Enable SMS alerts for all transactions.
    - Regularly review bank statements.
    """)



    # Transaction Amount Distribution by Class
    fig2, ax2 = plt.subplots()
    sns.boxplot(x='Class', y='Amount', data=df, ax=ax2)
    ax2.set_title("Transaction Amount by Class")
    st.pyplot(fig2)


# -----------------------------
# View Customers
# -----------------------------
elif menu == "View Customers":
    st.subheader("📋 Customer List")
    if customers:
        st.table(customers)
        to_delete = st.selectbox("Select a customer to delete", [c['Name'] for c in customers])
        if st.button("🗑 Delete"):
            customers = [c for c in customers if c['Name'] != to_delete]
            save_customers(customers)
            st.success(f"Customer '{to_delete}' has been deleted.")
    else:
        st.info("No customers found.")

# -----------------------------
# Add New Customer
# -----------------------------
elif menu == "Add Customer":
    st.subheader("➕ Add New Customer")
    if len(customers) >= 15:
        st.warning("Cannot add more than 15 customers.")
    else:
        with st.form("add_customer_form"):
            name = st.text_input("Name")
            sex = st.selectbox("Sex", ["Male", "Female", "Other"])
            age = st.number_input("Age", min_value=1, max_value=100)
            dob = st.date_input(
                                "Date of Birth",
                                value=datetime.date(2000, 1, 1),  # Default selected date
                                min_value=datetime.date(1900, 1, 1),  # Earliest allowed date
                                max_value=datetime.date.today()       # Latest allowed date
                            )
            credit = st.text_input("Credit")
            email = st.text_input("Email")
            phone = st.text_input("Phone (+1234567890)")
            submitted = st.form_submit_button("Save")
            if submitted:
                if not all([name, sex, age, dob, credit, email, phone]):
                    st.error("All fields are required.")
                else:
                    customers.append({
                        "Name": name, "Sex": sex, "Age": age, "DOB": str(dob),
                        "credit": credit, "Email": email, "Phone": phone
                    })
                    save_customers(customers)
                    st.success("Customer added successfully!")

# -----------------------------
# Make Transaction
# -----------------------------
elif menu == "Make Transaction":
    st.subheader("💳 Transaction Entry")
    if customers:
        name = st.selectbox("Select Customer", [c['Name'] for c in customers])
        amount = st.number_input("Transaction Amount ($)", min_value=0.0)
        if st.button("Submit Transaction"):
            customer = next((c for c in customers if c['Name'] == name), None)
            if not customer:
                st.error("Customer not found.")
            else:
                limit = 5000
                alert_needed = amount > 25000 or amount > (limit * 5)
                log = {
                    "Name": name,
                    "Amount": amount,
                    "Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Alert": "Yes" if alert_needed else "No"
                }
                save_log(log)
                if alert_needed:
                    send_sms_alert(customer['Phone'], name, amount)
                    st.warning(f"⚠ Suspicious transaction detected! SMS sent to {customer['Phone']}")
                else:
                    st.success("Transaction processed successfully.")
    else:
        st.info("No customers to make a transaction with.")

# -----------------------------
# View Alert Logs
# -----------------------------
elif menu == "Alert Log":
    st.subheader("📊 Alert Logs")
    logs = load_logs()
    if logs:
        st.dataframe(logs)
    else:
        st.info("No transactions logged yet.")

# -----------------------------
# Fraud Prediction Page
# -----------------------------
elif menu == "Fraud Prediction":
    st.subheader("🔎 Predict Fraudulent Transaction")
    input_data = []
    for feature in df.drop(columns=['Class']).columns:
        val = st.number_input(f"Enter value for {feature}", value=0.0)
        input_data.append(val)

    if st.button("Predict Fraud"):
        prediction = model.predict([input_data])[0]
        st.success(f"Prediction: {'Fraudulent Transaction' if prediction == 1 else 'Normal Transaction'}")
