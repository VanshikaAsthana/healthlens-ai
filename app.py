import streamlit as st
import matplotlib.pyplot as plt
from agents import compression_agent, risk_agent, recommendation_agent
import base64

st.set_page_config(page_title="HealthLens AI", layout="centered")

# ---------- BACKGROUND ----------
def set_bg(image_file):
    with open(image_file, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{data}");
        background-size: cover;
        background-position: center;
    }}

    input, textarea {{
        background-color: white !important;
        color: black !important;
    }}

    div[data-baseweb="select"] > div {{
        background-color: white !important;
        color: black !important;
    }}

    .stButton>button {{
        background-color: #1f77b4;
        color: white;
        border-radius: 6px;
        padding: 10px 20px;
        font-size: 16px;
    }}
    </style>
    """, unsafe_allow_html=True)

set_bg("assets/background.png")

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "input"

# ---------- INPUT PAGE ----------
if st.session_state.page == "input":

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("assets/header.png", width=350)

    st.title("HealthLens AI")
    st.subheader("Enter your health details")

    age = st.number_input("Age", 1, 120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    weight = st.number_input("Weight (kg)", 1.0)
    height = st.number_input("Height (cm)", 50.0)
    sleep = st.number_input("Sleep hours per day", 0.0, 24.0)
    steps = st.number_input("Steps per day", 0)
    history = st.text_area("Medical History")
    symptoms = st.text_area("Current Symptoms")

    if st.button("Analyze Health"):
        bmi = weight / ((height / 100) ** 2)

        st.session_state.data = {
            "age": age,
            "gender": gender,
            "bmi": bmi,
            "sleep": sleep,
            "steps": steps,
            "history": history,
            "symptoms": symptoms
        }

        # clear old results
        st.session_state.results = None

        st.session_state.page = "results"
        st.rerun()


# ---------- RESULTS PAGE ----------
if st.session_state.page == "results":

    data = st.session_state.data

    # Run LLM only once (cache results)
    if "results" not in st.session_state or st.session_state.results is None:
        with st.spinner("Analyzing your health..."):
            profile = compression_agent(data)

            numeric_risks, symptom_analysis = risk_agent(
                data["bmi"],
                data["sleep"],
                data["steps"],
                data["symptoms"],
                data["history"],
                data["gender"]
            )

            recommendations = recommendation_agent(profile, numeric_risks,data['history'])

            st.session_state.results = {
                "profile": profile,
                "risks": numeric_risks,
                "symptoms": symptom_analysis,
                "recommendations": recommendations
            }

    # Load cached results (fast)
    profile = st.session_state.results["profile"]
    numeric_risks = st.session_state.results["risks"]
    symptom_analysis = st.session_state.results["symptoms"]
    recommendations = st.session_state.results["recommendations"]

    # Only health2 image
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("assets/health2.jpg", width=350)

    st.title("Health Report")

    st.subheader("Compressed Health Profile")
    st.write(f"Age: {data['age']}")
    st.write(f"Gender: {data['gender']}")
    st.write(f"BMI: {round(data['bmi'],2)}")
    st.write(f"Sleep (hours): {data['sleep']}")
    st.write(f"Steps: {data['steps']}")
    st.write(f"Medical history: {data['history']}")
    st.write(f"Symptoms: {data['symptoms']}")

    st.subheader("Detected Risks")
    for r in numeric_risks:
        st.write("•", r)

    st.subheader("AI Symptom Analysis")
    st.write(symptom_analysis)

    st.subheader("AI Recommendations")
    for line in recommendations.split("\n"):
        if line.strip():
            st.write("•", line)

    st.subheader("Health Metrics Visualization")

    metrics = ["BMI", "Sleep (hrs)", "Steps (x1000)"]
    values = [data["bmi"], data["sleep"], data["steps"]/1000]

    fig, ax = plt.subplots(figsize=(6,4))
    colors = ["#4e79a7", "#59a14f", "#f28e2b"]

    bars = ax.bar(metrics, values, color=colors)
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    for bar in bars:
        y = bar.get_height()
        ax.text(bar.get_x()+bar.get_width()/2, y+0.1, round(y,2), ha="center")

    st.pyplot(fig)

    if st.button("Go Back"):
        st.session_state.page = "input"
        st.session_state.results= None
        st.rerun()
    st.success("Health analysis completed successfully.")
    #ollama run llama3.1:8b
