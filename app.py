import streamlit as st
from bedrock_client import invoke_model
from agents.idea_agent import generate_ideas
import json
import re
from datetime import datetime   

import streamlit as st
from orchestrator import run_generate, run_refine


st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
    }

    /* Glass container */
    [data-testid="stVerticalBlock"] > div:has(div.stButton) {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Buttons */
    div.stButton > button {
        background: linear-gradient(45deg, #624af2, #8f44fd);
        color: white;
        border-radius: 8px;
        border: none;
        width: 100%;
    }

    /* FIX: ensure text is visible */
    label, .stRadio label {
        color: white !important;
    }

    </style>
""", unsafe_allow_html=True)



st.title("Attention is all you need! 🚀")


def format_idea(x):
    if isinstance(x, dict):
        return x.get("title") or str(x)
    return str(x)

with st.sidebar:
    st.header("Activity Settings")

    topic = st.text_input("Topic", "Water Cycle")
    age = st.selectbox("Age", ["elementary", "middle", "high"])
    goal = st.selectbox("Goal", ["discussion", "drawing"])


    if st.button("Generate Ideas"):
        with st.spinner("Brainstorming..."):
            ideas = run_generate(topic, age, goal)
            st.session_state.ideas = ideas



if "ideas" in st.session_state and st.session_state.ideas:

    st.subheader("💡 Choose an Idea")

    # Optional debug (remove later)
    with st.expander("🔍 Debug (ideas data)"):
        st.write(st.session_state.ideas)

    selected = st.radio(
        "Which activity looks best?",
        st.session_state.ideas,
        format_func=format_idea
    )

    st.session_state.selected = selected

    if st.button("✨ Refine & Check Safety"):
        if not selected:
            st.warning("Please select an idea first.")
        else:
            with st.spinner("Polishing and checking safety..."):
                final_version, safety_report = run_refine(selected, age)

                st.markdown("---")
                st.subheader("🚀 Final Adapted Activity")
                st.info(final_version)

                with st.expander("🛡️ Safety Audit"):
                    st.write(safety_report)

else:
    st.info("👈 Enter a topic in the sidebar and click *Generate Ideas*")