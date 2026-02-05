# HealthLens AI 🩺

## Personal Health Coach powered by LLMs & Context Compression

HealthLens AI is an AI-powered personal health analysis system that collects user health data and generates meaningful insights, risk analysis, and personalized recommendations. The project uses local Large Language Models (Ollama) to deliver efficient, cost-effective AI reasoning.

## 🚀 Features

Collects health inputs: age, gender, BMI, sleep, steps, medical history, and symptoms

Compresses user health context using ScaleDown API

Generates AI-driven health summaries and insights using Ollama (local LLM)

Detects potential health risks and explains them in natural language

Provides personalized lifestyle and wellness recommendations

Visualizes health metrics using charts

Fully local inference (no paid OpenAI API required)

## 🧠 Architecture Overview
User Input
   ↓
ScaleDown Context Compression
   ↓
Local LLM (Ollama: Phi-3 / Llama-3)
   ↓
Risk Analysis + Recommendations
   ↓
Streamlit UI (Health Report)

## 🛠️ Tech Stack

Python

Streamlit – frontend UI

Ollama – local LLM inference

ScaleDown API – context compression

Matplotlib – data visualization

Requests – API communication

## 📁 Project Structure
HealthMonitoringAgent/
│
├── app.py              # Streamlit application
├── agents.py           # AI agents (compression, risk, recommendation)
├── assets/
│   ├── background.jpg
│   ├── header.png
│   └── health2.png
└── README.md

## ⚙️ Installation & Setup
1️⃣ Install dependencies
pip install streamlit matplotlib requests ollama

2️⃣ Install & run Ollama

Download Ollama from: https://ollama.com

Start a local model:

ollama run phi3
# or
ollama run llama3


⚠️ Keep Ollama running in the background.

3️⃣ Run the application
streamlit run app.py

## 📊 Example Output

Compressed health profile

Detected health risks

AI symptom analysis

Personalized health recommendations

Visual BMI, sleep, and activity metrics

## 🎯 Why This Project Stands Out

Uses LLMs responsibly with context compression

Works offline using local AI models

Reduces token cost and latency

Modular AI agent design

Competition-ready and scalable

## ⚠️ Disclaimer

This project is intended for educational and research purposes only.
It does not provide medical diagnoses or replace professional medical advice.

## 👩‍💻 Author

Vanshika Asthana
AI / ML Enthusiast | Student Developer

## ⭐ Future Enhancements

PDF report export

Multi-language support

Wearable device integration

Long-term health tracking

Model switching UI (Phi-3 / Llama-3)
