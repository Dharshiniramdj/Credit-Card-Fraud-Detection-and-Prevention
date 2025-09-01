# 🔐 Fraud Detection Streamlit App

This project is a **real-time credit card fraud prevention and prediction system** built with Streamlit, scikit-learn, and Twilio.

## 📂 Project Structure
```
fraud_detection_app/
│
├── data/
│   └── creditcard.csv        # dataset
│
├── models/
│   └── fraud_rf_model.pkl    # trained RandomForest model
│
├── logs/
│   ├── customers.json        # customer records
│   └── transaction_log.json  # transactions & alerts
│
├── app/
│   └── streamlit_customer_fraud_app.py   # main Streamlit app
│
├── requirements.txt          # Python dependencies
└── README.md                 # project documentation
```

## 🚀 How to Run
1. Navigate to project folder:
   ```bash
   cd fraud_detection_app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app/streamlit_customer_fraud_app.py
   ```

Open `http://localhost:8501` in your browser to use the app.
