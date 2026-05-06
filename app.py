import streamlit as st
from orchestrator import run_generate, run_refine

st.markdown("""
    <style>
    /* Dark background */
    .stApp {
        background-color: #0e1117;
    }

    /* Sleeker buttons - removed the bulky wrapper and 100% width */
    div.stButton > button {
        background: linear-gradient(45deg, #624af2, #8f44fd);
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        transition: transform 0.2s;
    }
    
    div.stButton > button:hover {
        transform: scale(1.02);
        border: none;
    }

    /* Clean white labels */
    label, .stRadio label {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Attention is all you need! 🚀")

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Activity Settings")

    topic = st.text_input("Topic", placeholder="e.g. Water Cycle")
    age = st.selectbox("Age Group", ["5-7", "8-10", "11-12", "12-14", "15-17"])
    goal = st.text_input(
        "Goal",
        placeholder="e.g. discussion, experiment, roleplay...",
        help="What should students do? Examples: discussion, drawing, building, experiment, roleplay, debate, storytelling, mapping, presenting, journaling, research"
    )

    if st.button("Generate Ideas"):
        if not topic.strip():
            st.warning("Please enter a topic.")
        elif not goal.strip():
            st.warning("Please enter a goal.")
        else:
            with st.spinner("Brainstorming..."):
                new_ideas = run_generate(topic, age, goal)

                if "ideas" not in st.session_state:
                    st.session_state.ideas = []

                st.session_state.ideas.extend(new_ideas)
                st.session_state.age = age
                st.session_state.selected = None
                st.session_state.refine_triggered = False
                st.session_state.refine_result = None

    if "ideas" in st.session_state and st.session_state.ideas:
        st.caption("Not happy with these? Click Generate again for fresh ideas.")


# ── Helper to render a compact idea card ──────────────────────────────────────
def render_idea_card(idea, index, show_button=True):
    title = idea.get("title", f"Idea {index+1}")
    why = idea.get("why_it_works", "")
    time = idea.get("time", "")
    materials = idea.get("materials", [])
    steps = idea.get("steps", [])

    with st.container(border=True):
        st.markdown(f"### {title}")

        if why:
            st.markdown(f"💡 **Why it works:** {why}")

        st.markdown("&nbsp;", unsafe_allow_html=True)

        meta_col1, meta_col2, meta_col3 = st.columns(3)
        with meta_col1:
            st.markdown("⏱ **Time**")
            st.markdown(time if time else "—")
        with meta_col2:
            st.markdown("🧰 **Needed**")
            st.markdown("\n".join(f"- {m}" for m in materials) if materials else "—")
        with meta_col3:
            st.markdown("📋 **Steps**")
            st.markdown(f"{len(steps)} steps" if steps else "—")

        if show_button:
            st.markdown("---")
            if st.button("✅ Select & Refine", key=f"idea_{index}"):
                st.session_state.selected = idea
                st.session_state.refine_triggered = True
                st.session_state.refine_result = None


# ── Main layout ────────────────────────────────────────────────────────────────
if "ideas" in st.session_state and st.session_state.ideas:
    ideas = st.session_state.ideas
    selected = st.session_state.get("selected")
    refine_result = st.session_state.get("refine_result")

    # ── No idea selected yet — show all cards ─────────────────────────────────
    if not selected:
        st.subheader("💡 Choose an Idea")
        for i, idea in enumerate(ideas):
            render_idea_card(idea, i)

    # ── Idea selected — split layout ──────────────────────────────────────────
    else:
        main_col, side_col = st.columns([2, 1])
        
        with side_col:
            other_ideas = [idea for idea in ideas if idea != selected]
            if other_ideas:
                st.markdown("### 💡 Other options")
                
                for i, idea in enumerate(other_ideas):
                    with st.container(border=True):
                        title = idea.get("title", f"Idea {i+1}")
                        why = idea.get("why_it_works", "")
                        
                        st.markdown(f"**{title}**")
                        
                        if why:
                            short_why = why[:300] + "..." if len(why) > 300 else why
                            st.caption(short_why)
                            
                        if st.button("🔄 Switch to this", key=f"switch_{i}", use_container_width=True):
                            st.session_state.selected = idea
                            st.session_state.refine_triggered = True
                            st.session_state.refine_result = None

        with main_col:
            # ── Trigger refine ─────────────────────────────────────────────
            if st.session_state.get("refine_triggered"):
                st.session_state.refine_triggered = False

                st.subheader(f"🔍 Refining: *{selected.get('title')}*")
                with st.spinner("Adapting and checking safety..."):
                    result = run_refine(selected, st.session_state.get("age", "middle"))
                    st.session_state.refine_result = result
                    refine_result = result

            # ── Show refine result ─────────────────────────────────────────
            if refine_result:
                status = refine_result.get("status")

                if status == "ok":
                    st.success("✨ Refinement Complete!")
                    final_plan = refine_result.get("final_plan", {})
                    
                    # Better layout for the final result
                    with st.container(border=True):
                        st.markdown(f"### 🎯 {final_plan.get('title', selected.get('title'))}")
                        st.markdown(final_plan.get("adapted_description", "No description returned."))
                        
                        if "steps" in final_plan:
                            st.markdown("**Steps:**")
                            for step in final_plan["steps"]:
                                st.markdown(f"- {step}")

                    with st.expander("🛡️ Safety Audit"):
                        safety_data = refine_result.get("safety", {})
                        if isinstance(safety_data, dict):
                            for key, value in safety_data.items():
                                # Pretvara ključeve tipa "is_safe" u "Is Safe"
                                clean_key = str(key).replace("_", " ").title()
                                st.markdown(f"**{clean_key}:** {value}")
                        else:
                            st.write(safety_data)

                elif status == "rejected":
                    st.error("⛔ This activity was flagged as unsafe and could not be resolved.")
                    st.write(refine_result.get("assessment"))

                elif status == "unresolved":
                    st.warning("⚠️ Could not produce a safe version after multiple attempts.")
                    st.write(refine_result.get("last_safety"))

                else:
                    st.error(f"Pipeline error at stage: {refine_result.get('stage')}")
                    st.write(refine_result.get("detail"))

else:
    st.info("👈 Enter a topic in the sidebar and click *Generate Ideas*")


