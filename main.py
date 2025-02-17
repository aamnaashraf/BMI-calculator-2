import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configure page
st.set_page_config(
    page_title="Advanced BMI Calculator",
    page_icon="⚖️",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 18px;
        border-radius: 10px;
    }
    h1 {
        color: #1E90FF;
    }
    .stButton button {
        background-color: #1E90FF;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton button:hover {
        background-color: #0077B6;
    }
    .result-box {
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# App header
st.title("🚀 Advanced BMI Calculator")
st.markdown("---")

# Initialize session state for BMI history
if "bmi_history" not in st.session_state:
    st.session_state.bmi_history = []

# Input fields
with st.form("bmi_form"):
    st.subheader("Enter Your Details")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", 1, 120, 25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    with col2:
        weight = st.number_input("Weight (kg)", 1.0, 300.0, 70.0)
        height = st.number_input("Height (meters)", 0.5, 3.0, 1.75)

    submitted = st.form_submit_button("Calculate BMI")

# BMI Calculation
if submitted:
    bmi = weight / (height ** 2)
    
    # Adjust BMI based on age and gender
    if age < 18:
        bmi_adjusted = bmi * 1.1  # Teens have higher BMI ranges
    elif age > 60:
        bmi_adjusted = bmi * 0.9  # Elderly have lower BMI ranges
    else:
        bmi_adjusted = bmi

    if gender == "Female":
        bmi_adjusted *= 0.95  # Females generally have lower BMI ranges

    # Determine BMI category
    if bmi_adjusted < 18.5:
        category = "Underweight 🏋️"
        color = "#3498db"
        tips = [
            "Increase calorie intake with healthy foods like nuts, seeds, and avocados.",
            "Include protein-rich foods like eggs, fish, chicken, and legumes.",
            "Engage in strength training to build muscle mass.",
            "Eat smaller, frequent meals throughout the day.",
            "Consult a dietitian for a personalized meal plan."
        ]
    elif 18.5 <= bmi_adjusted < 25:
        category = "Healthy Weight ✅"
        color = "#2ecc71"
        tips = [
            "Maintain a balanced diet with fruits, vegetables, and whole grains.",
            "Exercise regularly (at least 150 minutes of moderate activity per week).",
            "Monitor your weight monthly to stay on track.",
            "Stay hydrated by drinking at least 2-3 liters of water daily.",
            "Get 7-9 hours of quality sleep every night."
        ]
    elif 25 <= bmi_adjusted < 30:
        category = "Overweight ⚠️"
        color = "#f1c40f"
        tips = [
            "Reduce calorie intake by avoiding sugary and processed foods.",
            "Increase physical activity (e.g., walking, jogging, or cycling).",
            "Focus on portion control during meals.",
            "Include more fiber-rich foods like vegetables and whole grains.",
            "Limit alcohol consumption and avoid late-night snacking."
        ]
    else:
        category = "Obese ❌"
        color = "#e74c3c"
        tips = [
            "Consult a doctor or dietitian for a personalized weight-loss plan.",
            "Focus on portion control and avoid overeating.",
            "Engage in daily physical activity (e.g., 30 minutes of walking).",
            "Avoid sugary drinks and opt for water or herbal teas.",
            "Track your progress weekly to stay motivated."
        ]

    # Display results
    st.markdown(f"""
    <div class="result-box" style="border-color: {color};">
        <h3 style="color: {color};">Your BMI: {bmi_adjusted:.1f}</h3>
        <p style="color: {color}; font-size: 20px;">{category}</p>
    </div>
    """, unsafe_allow_html=True)

    # Health Tips
    st.subheader("💡 Health Tips")
    for tip in tips:
        st.markdown(f"- {tip}")

    # Add BMI to history
    st.session_state.bmi_history.append((bmi_adjusted, category, color))

# BMI Chart (Ranges)
st.subheader("📊 BMI Ranges Chart")
bmi_ranges = {
    "Category": ["Underweight", "Normal Weight", "Overweight", "Obese"],
    "BMI Range": ["< 18.5", "18.5 - 24.9", "25 - 29.9", "≥ 30"],
    "Color": ["#3498db", "#2ecc71", "#f1c40f", "#e74c3c"]
}
bmi_ranges_df = pd.DataFrame(bmi_ranges)

# Display the DataFrame with colored backgrounds
def color_cells(val):
    color = bmi_ranges["Color"][bmi_ranges["Category"].index(val)]
    return f"background-color: {color}; color: white;"

st.dataframe(
    bmi_ranges_df.style.applymap(color_cells, subset=["Category"]).set_properties(**{'text-align': 'left'})
)

# BMI Graph (Trend)
if st.session_state.bmi_history:
    st.subheader("📈 BMI Trend Over Time")
    fig, ax = plt.subplots()
    
    # Plot each BMI calculation with its category color
    for i, (bmi, cat, color) in enumerate(st.session_state.bmi_history):
        ax.plot(i + 1, bmi, marker='o', color=color, markersize=10, label=cat if i == 0 else "")
    
    ax.set_ylabel("BMI")
    ax.set_xlabel("Calculations")
    ax.set_title("Your BMI Over Time")
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc="upper right")
    st.pyplot(fig)

# BMI History
if st.session_state.bmi_history:
    st.subheader("📅 BMI Calculation History")
    history_df = pd.DataFrame({
        "Calculation": range(1, len(st.session_state.bmi_history) + 1),
        "BMI": [bmi for bmi, _, _ in st.session_state.bmi_history],
        "Category": [cat for _, cat, _ in st.session_state.bmi_history]
    })
    st.dataframe(history_df)

# Footer
st.markdown("---")
st.caption("ℹ️ Note: BMI is a simple screening tool and does not account for muscle mass or body composition.")