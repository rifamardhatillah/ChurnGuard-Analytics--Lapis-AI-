# 🛡️ ChurnGuard Analytics Dashboard

Dashboard Machine Learning berbasis Streamlit untuk membantu perusahaan menganalisis risiko churn pelanggan dan memahami sentimen pengguna melalui ulasan pelanggan.

Proyek ini menggabungkan model prediksi churn menggunakan XGBoost dan analisis sentimen berbasis Natural Language Processing (NLP) dalam satu platform interaktif yang mudah digunakan.

---

## 📌 Fitur Utama

### 📉 Churn Prediction Dashboard
- Prediksi churn pelanggan menggunakan algoritma XGBoost
- Perhitungan probabilitas churn (risk score)
- Klasifikasi pelanggan berdasarkan tingkat risiko
- Dashboard KPI interaktif
- Visualisasi data menggunakan Plotly
- Export laporan PDF

### 💬 Sentiment Analysis Dashboard
- Analisis sentimen ulasan pelanggan
- TF-IDF Vectorization
- Logistic Regression Classification
- Word Cloud Visualization
- Distribusi sentimen pelanggan
- Prediksi sentimen secara real-time

### 🔐 Authentication System
- Login dashboard
- Session management
- Multi-page navigation

---

## 🛠️ Teknologi yang Digunakan

- Python
- Streamlit
- XGBoost
- Scikit-Learn
- Logistic Regression
- TF-IDF
- Pandas
- NumPy
- Plotly
- WordCloud
- Joblib
- ReportLab

---

## 📂 Struktur Project

```text
ChurnGuard/
│
├── main.py
├── ChurnGuard.py
├── Sentiment_Analysis.py
│
├── models/
│   ├── churnguard_model.joblib
│   ├── encoder_nps.joblib
│   ├── encoder_plan.joblib
│   ├── forward_features.joblib
│   ├── model_metrics.joblib
│   ├── sentiment_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── churnguard_cleaned.csv
├── churnguard_predictions.csv
├── data_untuk_labeling_labeled.csv
├── ulasan_aplikasi.csv
│
└── .streamlit/
    └── config.toml
```

---

## 🚀 Cara Menjalankan

### 1. Clone Repository

```bash
git clone https://github.com/rifamardhatillah/ChurnGuard-Analytics.git
```

### 2. Install Dependency

```bash
pip install -r requirements.txt
```

### 3. Jalankan Dashboard

```bash
streamlit run main.py
```

---

## 🎯 Tujuan Proyek

Proyek ini dikembangkan untuk membantu perusahaan SaaS mengidentifikasi pelanggan yang berisiko churn lebih awal serta memahami opini pelanggan melalui analisis sentimen. Dengan memanfaatkan Machine Learning dan NLP, perusahaan dapat mengambil keputusan yang lebih tepat untuk meningkatkan retensi pelanggan.

---

## 👩‍💻 Pengembang

**Rifa Mardhatillah**

Mahasiswa D-IV Teknik Informatika  
Politeknik Negeri Jakarta

---

## 📚 Bidang Keilmuan

- Machine Learning
- Data Analytics
- Natural Language Processing (NLP)
- Customer Analytics
- Predictive Modeling
- Data Visualization
