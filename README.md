# AI-Powered Phishing & Malicious URL Detector

A full-stack web application that uses Machine Learning to detect and classify potentially malicious or phishing URLs in real-time. Built to demonstrate practical applications of AI in cybersecurity.

## Features
- **Real-time Analysis**: Instantly checks URLs and returns a safety classification.
- **Confidence Scoring**: Provides a percentage confidence level for each prediction.
- **Feature Extraction**: Automatically analyzes URL characteristics (length, special characters, protocol, etc.).
- **Modern UI**: Clean, responsive React frontend.

## Tech Stack
- **Machine Learning**: Python, Scikit-Learn, Pandas
- **Backend**: FastAPI, Uvicorn
- **Frontend**: React.js, Vite
- **Deployment**: *(To be added)*

## Project Structure
```text
ai-phishing-detector/
├── backend/        # FastAPI server and feature extraction logic
├── frontend/       # React application
├── model/          # Jupyter notebooks and trained .pkl model files
└── README.md


## Installation & Setup

1. Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py

2. Frontend Setup
```bash
cd frontend
npm install
npm run dev

