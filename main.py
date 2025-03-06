import streamlit as st
import pandas as pd

st.title("🏋 Personal Fitness Tracker")

# Custom CSS for background image
page_bg_img = f"""
<style>
.st-emotion-cache-bm2z3a {{
    background-image: url("https://images.pexels.com/photos/841130/pexels-photo-841130.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2.jpg");
    background-size: cover;
    background-attachment: fixed;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Initialize session state for tracking today's data
if "today_data" not in st.session_state:
    st.session_state.today_data = {"Exercises": [], "Calories Burned": []}

# User Input
st.subheader("Enter Your Details:")
name = st.text_input("Name")
age = st.number_input("Age", min_value=10, max_value=100, step=1)
weight = st.number_input("Weight (kg)", min_value=20.0, max_value=200.0, step=0.1)
height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, step=0.01)

# Calculate BMI and Show Recommended Exercises
if st.button("Calculate BMI & Show Exercises"):
    if name and weight and height:
        bmi = round(weight / (height ** 2), 2)

        # Determine BMI Category & Recommended Exercises
        if bmi < 18.5:
            category = "Underweight"
            exercises = {"Strength Training": 250, "High-Calorie Diet (Extra)": 0}
        elif 18.5 <= bmi < 24.9:
            category = "Normal Weight"
            exercises = {"Jogging": 300, "Yoga": 150, "Strength Training": 250}
        elif 25 <= bmi < 29.9:
            category = "Overweight"
            exercises = {"Brisk Walking": 200, "Cycling": 400, "Swimming": 500}
        else:
            category = "Obese"
            exercises = {"Light Walking": 150, "Yoga": 100, "Trainer Consultation": 0}

        st.success(f"Hello, {name}! Your BMI is *{bmi}* ({category})")

        # Display Recommended Exercises
        st.subheader("🏋 Recommended Exercises for You:")
        for ex in exercises.keys():
            st.write(f"- {ex}")

        # Save exercises in session state
        st.session_state.exercises = exercises

    else:
        st.warning("Please enter all details to calculate BMI.")

# Select Completed Exercises After Recommendation
if "exercises" in st.session_state:
    st.subheader("✅ Select the Exercises You Completed Today:")
    selected_exercises = st.multiselect("Choose exercises:", list(st.session_state.exercises.keys()))

    # Calculate Calories Burned
    total_calories = sum(st.session_state.exercises[ex] for ex in selected_exercises)
    
    # Update session state with selected exercises & calories burned
    st.session_state.today_data = {
        "Exercises": selected_exercises,
        "Calories Burned": [st.session_state.exercises[ex] for ex in selected_exercises]  
    }

    if selected_exercises:
        # Show pop-up message
        st.success("🎉 Congratulations! You did it! Keep pushing forward! 💪")
        st.balloons()  # Shows balloons animation

    # Show Calories Burned
    st.subheader("🔥 Calories Burned Today:")
    st.write(f"You burned *{total_calories} calories* today!")

    # Show Progress Graph
    if st.session_state.today_data["Exercises"]:
        st.subheader("📊 Today's Progress")
        df = pd.DataFrame(st.session_state.today_data)
        st.bar_chart(df.set_index("Exercises"))