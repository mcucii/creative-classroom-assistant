import streamlit as st
from bedrock_client import generate_activities
import json
from datetime import datetime

st.title("🤖 Creative Classroom Assistant")

age_group = st.selectbox("Age Group", ["elementary", "middle", "high"])
lesson_goal = st.selectbox("Lesson Goal", ["discussion", "group activity", "drawing", "role-play", "debate", "writing"])
topic = st.text_input("Topic", value="water cycle")

if st.button("Generate 3 Ideas"):
    with st.spinner("Calling Bedrock..."):
        result = generate_activities(topic, age_group, lesson_goal)
        
        run = {"timestamp": datetime.now().isoformat(), "topic": topic, 
               "age_group": age_group, "lesson_goal": lesson_goal, "output": result}
        with open("outputs.json", "a") as f:
            json.dump(run, f); f.write("\n")
        
        st.json(result)