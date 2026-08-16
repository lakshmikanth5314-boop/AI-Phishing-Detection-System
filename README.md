# 🛡️ AI Phishing Detection System

An AI-powered web application that detects whether a website URL is **legitimate or potentially phishing** using machine learning.

## 🚀 Features

- 🔍 Analyze website URLs
- 🤖 Machine-learning-based phishing detection
- 🌐 Simple web interface
- ⚡ Fast prediction
- 📊 URL feature extraction
- 🔐 Helps users identify suspicious websites

## 🛠️ Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- Scikit-learn
- Pandas
- Machine Learning

## 📂 Project Structure

```text
AI-Phishing-Detection-System/
│
├── backend/
│   └── app/
│       ├── ml/
│       │   ├── feature_extraction.py
│       │   ├── phishing_dataset.csv
│       │   ├── phishing_model.pkl
│       │   └── train_model.py
│       │
│       ├── index.html
│       └── main.py
│
├── phishing_model.pkl
└── .gitignore
## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/lakshmikanth5314-boop/AI-Phishing-Detection-System.git
```

### 2. Open the project folder

```bash
cd AI-Phishing-Detection-System
```

### 3. Install required packages

```bash
pip install flask pandas scikit-learn joblib
```

### 4. Run the Flask application

```bash
python backend/app/main.py
```

### 5. Open in your browser

```text
http://127.0.0.1:5000
```
