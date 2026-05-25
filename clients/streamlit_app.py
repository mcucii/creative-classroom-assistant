import streamlit as st
from agentcore.orchestrator import ActivityOrchestrator
from agentcore.llm_providers import LLMCore, LLMProvider

llm_core = LLMCore()
provider = LLMProvider.CLAUDE 
orchestrator = ActivityOrchestrator(llm_core, provider)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>

.stApp {
    background-color: #0e1117;
}

label, .stRadio label {
    color: white !important;
}

.history-column {
    position: sticky;
    top: 1rem;
}
            
/* 🟣 PRIMARY BUTTONS (Purple Gradient) */
div.stButton > button[kind="primary"] {
    background: linear-gradient(45deg, #624af2, #8f44fd) !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 0.5rem 1rem !important;
    transition: transform 0.2s !important;
}

div.stButton > button[kind="primary"]:hover {
    transform: scale(1.02) !important;
}

div.stButton > button[kind="secondary"] {
    background: #1f2937 !important;
    border: 1px solid #374151 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    transition: transform 0.2s !important;
}

div.stButton > button[kind="secondary"]:hover {
    background: #2b3545 !important;
    transform: scale(1.02) !important;
}
</style>
""", unsafe_allow_html=True)

# st.title("Attention is all you need! 🚀")

# ── Session State ─────────────────────────────────────────────────────────────
defaults = {
    "ideas": [],
    "history": {},
    "selected": None,
    "refine_triggered": False,
    "refine_result": None,
    "age": None
}

st.set_page_config(layout="wide")

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

if not isinstance(st.session_state.history, dict):
    st.session_state.history = {}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Activity Settings")
    topic = st.text_input("Topic", placeholder="e.g. Water Cycle")
    age = st.selectbox(
        "Age Group",
        ["5-7", "8-10", "11-12", "12-14", "15-17"]
    )

    goal = st.text_input(
        "Goal",
        placeholder="e.g. discussion, experiment, roleplay...",
        help="What should students do?"
    )

    if st.button("Generate Ideas", type="primary"):
        if not topic.strip():
            st.warning("Please enter a topic.")
        elif not goal.strip():
            st.warning("Please enter a goal.")
        else:
            with st.spinner("Brainstorming..."):
                new_ideas = orchestrator.run_generate(topic, age, goal)
                st.session_state.ideas = new_ideas
                st.session_state.age = age
                st.session_state.selected = None
                st.session_state.refine_triggered = False
                st.session_state.refine_result = None

                for idea in new_ideas:
                    title = idea.get("title", "Untitled")
                    st.session_state.history[title] = idea

    if st.session_state.ideas:
        st.caption("Not happy with these? Click Generate again for fresh ideas.")

# ── Layout ────────────────────────────────────────────────────────────────────

# main_col, history_col = st.columns([4, 3], gap="large")
main_col, spacer, history_col = st.columns([4, 1, 1.8])

# ── Helper ────────────────────────────────────────────────────────────────────
def render_idea_card(idea, index):
    title = idea.get("title", f"Idea {index + 1}")
    why = idea.get("why_it_works", "")
    time = idea.get("time", "")
    materials = idea.get("materials", [])
    steps = idea.get("steps", [])

    with st.container(border=True):
        st.markdown(f"### {title}")

        if why:
            st.markdown(f"💡 **Why it works:** {why}")

        st.markdown("&nbsp;", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("⏱ **Time**")
            st.markdown(time or "—")

        with col2:
            st.markdown("🧰 **Needed**")
            st.markdown("\n".join(f"- {m}" for m in materials) if materials else "—")

        with col3:
            st.markdown("📋 **Steps**")
            st.markdown(f"{len(steps)} steps" if steps else "—")

        st.markdown("---")

        if st.button("✅ Select & Refine", key=f"idea_{index}", type="primary"):

            st.session_state.selected = idea
            st.session_state.refine_triggered = True
            st.session_state.refine_result = None

            st.rerun()

# ── Main Content ──────────────────────────────────────────────────────────────
with main_col:

    if not st.session_state.ideas:
        st.info("👈 Enter a topic in the sidebar and click *Generate Ideas*")

    else:
        ideas = st.session_state.ideas
        selected = st.session_state.selected
        refine_result = st.session_state.refine_result

        # ── No Selected Idea ────────────────────────────────────────────────
        if not selected:
            st.subheader("💡 Choose an Idea")

            for i, idea in enumerate(ideas):
                render_idea_card(idea, i)

        # ── Selected Idea ───────────────────────────────────────────────────
        else:

            other_ideas = [idea for idea in ideas if idea != selected]

            if other_ideas:
                with st.expander("💡 View Other Options"):

                    cols = st.columns(len(other_ideas))

                    for i, idea in enumerate(other_ideas):
                        with cols[i]:

                            title = idea.get("title", f"Idea {i + 1}")
                            st.markdown(f"**{title}**")

                            if st.button("🔄 Switch", key=f"switch_{i}", use_container_width=True):

                                st.session_state.selected = idea
                                st.session_state.refine_triggered = True
                                st.session_state.refine_result = None

                                st.rerun()

            # ── Run Refinement ─────────────────────────────────────────────
            if st.session_state.refine_triggered:

                st.session_state.refine_triggered = False

                st.subheader(f"🔍 Refining: *{selected.get('title')}*")

                with st.spinner("Adapting and checking safety..."):

                    result = orchestrator.run_refine(selected, st.session_state.age)

                    st.session_state.refine_result = result
                    refine_result = result

            # ── Show Results ───────────────────────────────────────────────
            if refine_result:

                status = refine_result.get("status")

                if status == "ok":

                    st.success("✨ Refinement Complete!")

                    final_plan = refine_result.get("final_plan", {})

                    with st.container(border=True):

                        st.markdown(f"### 🎯 {final_plan.get('title', selected.get('title'))}")

                        st.markdown(
                            final_plan.get(
                                "adapted_description",
                                "No description returned."
                            )
                        )

                        if "steps" in final_plan:
                            st.markdown("**Steps:**")
                            for step in final_plan["steps"]:
                                st.markdown(f"- {step}")

                    with st.expander("🛡️ Safety Audit", expanded=True):
                        safety_data = refine_result.get("safety", {})

                        if isinstance(safety_data, dict):
                            safety_status = safety_data.get("status", "Unknown").upper()

                            if safety_status == "SAFE":
                                st.success(f"✅ Status: {safety_status}")
                            else:
                                st.warning(f"⚠️ Status: {safety_status}")

                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(
                                    f"**Severity:** {safety_data.get('severity', 'none').title()}"
                                )

                            with col2:
                                st.markdown(
                                    f"**Safe to Use:** {'Yes' if safety_data.get('safe_to_use', False) else 'No'}"
                                )

                            st.divider()
                            for key in ["risks", "suggestions"]:
                                value = safety_data.get(key)
                                st.markdown(f"#### {key.title()}")
                                if not value or value == "none":
                                    st.write(f"No {key} identified.")
                                    continue

                                if isinstance(value, list):
                                    for item in value:
                                        if isinstance(item, dict):
                                            category = item.get("category") or item.get("addresses_risk")
                                            content = item.get("description") or item.get("change")

                                            if content:

                                                if category and category.lower() != "general":
                                                    label = category.replace("_", " ").title()
                                                    st.markdown(f"**{label}**: {content}")
                                                else:
                                                    st.markdown(f"- {content}")

                                        else:
                                            st.markdown(f"- {item}")

                                else:
                                    st.write(value)

                        else:
                            st.info("No structured safety data available.")
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

# ── History ───────────────────────────────────────────────────────────────────

with history_col:
    st.markdown('<div class="history-column">', unsafe_allow_html=True)
    st.markdown('<h2 style="font-size: 24px;">Previous Ideas</h2>', unsafe_allow_html=True)
    history = st.session_state.history
    
    if not history:
        st.markdown('<p style="font-size: 14px; color: gray;">No ideas yet.</p>', unsafe_allow_html=True)
    else:
        for idx, (title, idea) in enumerate(reversed(list(history.items()))):
            selected = st.session_state.selected == idea
            with st.container(border=True):
                st.markdown(f'<h3 style="font-size: 18px;">💡 {title}</h3>', unsafe_allow_html=True)
                if selected:
                    st.markdown('<p style="font-size: 12px; color: gray;">Currently viewing</p>', unsafe_allow_html=True)
                
                st.markdown('<div class="history-button">', unsafe_allow_html=True)

                if st.button(
                    "Current" if selected else "Choose",
                    key=f"history_{idx}",
                    use_container_width=True,
                    disabled=selected, 
                    type="secondary"
                ):
                    st.session_state.selected = idea
                    st.session_state.refine_triggered = True
                    st.session_state.refine_result = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)