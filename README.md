# 🔐 Real-Time Credit Card Fraud Detection & Prevention  

## 📌 Overview  
This project implements a **real-time fraud detection system** using **Machine Learning (Random Forest Classifier)** and a **Streamlit web application**. The goal is to detect and prevent fraudulent credit card transactions while providing a secure customer management and alert system.  

Key highlights:  
- Machine Learning model trained on the **creditcard.csv** dataset  
- **Streamlit dashboard** for fraud prediction and customer management  
- **Transaction monitoring** with suspicious activity alerts  
- **Twilio API integration** for real-time SMS alerts  
- **Visualization tools** for fraud insights and data analysis  

---

## 🎯 Features  

✅ **Fraud Detection** – Predict fraudulent vs normal transactions  
✅ **Customer Management** – Add, view, and delete customers  
✅ **Transaction Monitoring** – Logs transactions with alerts for suspicious activity  
✅ **SMS Alerts** – Sends real-time notifications for high-risk transactions  
✅ **Data Insights** – Box plots and visualizations for fraud analysis  
✅ **Secure Credentials** – Twilio keys handled via environment variables  

---

## 🏗 Project Structure  

```
fraud_detection_app/
│
├── creditcard.csv          # dataset
│
├──  fraud_rf_model.pkl      # trained RandomForest model
│
├── logs/
│   ├── customers.json          # customer records
│   └── transaction_log.json    # transactions & alerts
│
├── streamlit_customer_fraud_app.py   # main Streamlit app
│
├── .env                        # environment variables (Twilio keys)
├── requirements.txt            # Python dependencies
└── README.md                   # documentation
```

---

## ⚙️ Installation  

1. **Clone Repository / Extract Files**  
```bash
git clone https://github.com/Dharshiniramdj/fraud_detection_app.git
cd fraud_detection_app
```

2. **Install Dependencies**  
```bash
pip install -r requirements.txt
```

3. **Set Up Environment Variables**  
Create a `.env` file inside the project root:  
```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

4. **Run the App**  
```bash
streamlit run app/streamlit_customer_fraud_app.py
```

---

## 📊 Dataset  
- Source: [Kaggle – Credit Card Fraud Detection Dataset](https://www.kaggle.com/mlg-ulb/creditcardfraud)  
- Features: 30 (including anonymized PCA-transformed features + Amount + Time)  
- Target:  
  - `0` → Normal transaction  
  - `1` → Fraudulent transaction  

---

## 🔎 How It Works  

1. Load dataset & train a **RandomForestClassifier**  
2. Input new transaction details → prediction (fraud or normal)  
3. Monitor transactions → suspicious activity flagged  
4. If risk detected → **SMS alert sent** via Twilio  
5. Dashboard provides **data insights & visualization**  

---

## 📈 Results  

- **Model Used**: Random Forest Classifier  
- **Accuracy**: ~99% on test set (with stratified sampling)  
- **Key Insight**: Fraudulent transactions typically have **lower amounts but unusual patterns**  

---

## 🚀 Future Enhancements  

- Deploy model on **cloud (AWS/GCP)** for scalability  
- Add **deep learning models (LSTM, Autoencoders)** for anomaly detection  
- Implement **role-based access** for admins and users  
- Enhance UI with **real-time transaction streaming**  

---

## 🧑‍💻 Author  

👩‍💻 **Dharshini**  
Capstone Project – *Machine Learning for Data Analysis (ITA0618)*  
