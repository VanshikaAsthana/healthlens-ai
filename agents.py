import ollama

def compression_agent(data):
    profile = f"""
Age: {data['age']}
Gender: {data['gender']}
BMI: {round(data['bmi'],2)}
Sleep (hours): {data['sleep']}
Steps: {data['steps']}
Medical history: {data['history']}
Symptoms: {data['symptoms']}
"""
    return profile.strip()

def symptom_analysis_agent(symptoms, history, sleep, steps, gender):
    prompt = f"""
    You are a health coach, not a doctor.
    Identify ONLY the 2-3 most likely common causes.
    
    Each cause must be exactly 2 short sentences.
    Use simple language.
    Do NOT exceed 2-3 causes.

    Format exactly like this:
    - Name of Cause: sentence one. sentence two.
   
    User data:
    Gender: {gender}
    Symptoms: {symptoms}
    Medical history: {history}
    Sleep: {sleep} hours
    Steps: {steps}
    """

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.05, "num_predict": 100}
    )

    return response["message"]["content"].strip()




def risk_agent(bmi, sleep, steps, symptoms,history,gender):
    numeric_risks = []

    if bmi >= 25:
        numeric_risks.append(
            "Overweight risk: BMI is above the healthy range, which can increase fatigue and long-term health concerns."
        )

    if sleep < 6:
        numeric_risks.append(
            "Sleep deprivation: Low sleep duration can cause dizziness, headaches, and reduced concentration."
        )

    if steps < 3000:
        numeric_risks.append(
            "Low physical activity: Limited daily movement may affect energy levels and overall fitness."
        )

    symptom_analysis = symptom_analysis_agent(symptoms, history, sleep, steps, gender)



    return numeric_risks, symptom_analysis




def recommendation_agent(profile, numeric_risks,history):
    prompt = f"""
    Based only on these risks and history:
    {numeric_risks,history}

    Give exactly 3 short recommendations.
    Each recommendation must be one line.
    Use correct terms like "Sleep deprivation" not "Sleeplessness".
    Do not add explanations or headings.
    """

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.2, "num_predict": 100}
    )

    return response["message"]["content"].strip()

