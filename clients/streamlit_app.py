import boto3
import json
import streamlit as st

AGENT_RUNTIME_ARN = "arn:aws:bedrock-agentcore:eu-central-1:963649480732:runtime/classroom_agent-XAQfz84DXl"

client = boto3.client("bedrock-agentcore", region_name="eu-central-1")

def generate_ideas(topic, age, goal):
    response = client.invoke_agent_runtime(
        agentRuntimeArn=AGENT_RUNTIME_ARN,
        qualifier="default",
        payload=json.dumps({
            "action": "generate",
            "topic": topic,
            "age_group": age,
            "goal": goal
        }).encode()
    )
    result = json.loads(response["response"].read())
    return result.get("ideas", [])

def refine_activity(selected_idea, age):
    response = client.invoke_agent_runtime(
        agentRuntimeArn=AGENT_RUNTIME_ARN,
        qualifier="default",
        payload=json.dumps({
            "action": "refine",
            "activity": selected_idea,
            "age_group": age
        }).encode()
    )
    return json.loads(response["response"].read())

st.set_page_config(layout="wide", page_title="Creative Classroom")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Fraunces:ital,wght@0,400;0,700;1,400&display=swap');

:root {
    --cream: #FFF8F0;
    --peach: #FFE8D6;
    --coral: #FF6B6B;
    --yellow: #FFD93D;
    --green: #6BCB77;
    --blue: #4D96FF;
    --dark: #1A1A2E;
    --text: #2D2D2D;
    --muted: #8A8A9A;
    --card-bg: #FFFFFF;
    --border-radius: 20px;
    --shadow: 0 4px 24px rgba(0,0,0,0.08);
    --shadow-hover: 0 8px 32px rgba(0,0,0,0.14);
}

.stApp {
    background-color: var(--cream) !important;
    font-family: 'Nunito', sans-serif !important;
}

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif !important;
    color: var(--text) !important;
}

/* ===== FORCE READABLE TEXT EVERYWHERE (fixes white-on-bright issue) ===== */
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] *,
[data-testid="stText"],
.stMarkdown, .stMarkdown * {
    color: var(--text) !important;
}
/* ===== END FIX ===== */

/* ===== Alerts: neutral white cards with dark text, regardless of type ===== */
[data-testid="stAlertContainer"],
[data-testid="stAlert"],
.stAlert {
    background: #FFFFFF !important;
    border: 2px solid #F0EBE3 !important;
    border-radius: 14px !important;
}

[data-testid="stAlertContainer"] *,
[data-testid="stAlert"] *,
.stAlert * {
    color: var(--text) !important;
    fill: var(--text) !important;
}
/* ===== END ALERT FIX ===== */

/* ===== Expander (Safety Audit) header fix ===== */
[data-testid="stExpander"] summary {
    background: #FFF3E8 !important;
    border-radius: 12px !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary *,
[data-testid="stExpander"] summary span,
[data-testid="stExpander"] summary p {
    color: var(--dark) !important;
    fill: var(--dark) !important;
    font-weight: 700 !important;
}
/* ===== END EXPANDER FIX ===== */

header[data-testid="stHeader"] {
    background: transparent !important;
}

h1 {
    font-family: 'Fraunces', serif !important;
    font-size: 2.6rem !important;
    font-weight: 700 !important;
    color: var(--dark) !important;
    letter-spacing: -0.5px !important;
}

h2 {
    font-family: 'Fraunces', serif !important;
    font-weight: 700 !important;
    color: var(--dark) !important;
}

h3 {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    color: var(--dark) !important;
}

[data-testid="stSidebar"] {
    background: var(--dark) !important;
    border-right: none !important;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stSelectbox select,
[data-testid="stSidebar"] [data-baseweb="select"] {
    background: rgba(255,255,255,0.08) !important;
    border: 1.5px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    color: white !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1.5px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
}

[data-testid="stSidebar"] label {
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
    opacity: 0.7 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: white !important;
    font-family: 'Fraunces', serif !important;
}

div.stButton > button[kind="primary"] {
    background: var(--coral) !important;
    color: white !important;
    border-radius: 50px !important;
    border: none !important;
    padding: 0.6rem 1.6rem !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.2px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 0px #cc4444 !important;
}

div.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 0px #cc4444 !important;
    background: #ff5252 !important;
}

div.stButton > button[kind="primary"]:active {
    transform: translateY(2px) !important;
    box-shadow: 0 2px 0px #cc4444 !important;
}

div.stButton > button[kind="secondary"] {
    background: white !important;
    border: 2px solid #E0E0E0 !important;
    color: var(--text) !important;
    border-radius: 50px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    transition: all 0.2s ease !important;
}

div.stButton > button[kind="secondary"]:hover {
    border-color: var(--blue) !important;
    color: var(--blue) !important;
    background: #f0f6ff !important;
    transform: translateY(-1px) !important;
}

div.stButton > button[kind="secondary"]:disabled {
    background: var(--yellow) !important;
    border-color: var(--yellow) !important;
    color: var(--dark) !important;
    opacity: 1 !important;
    font-weight: 800 !important;
}

[data-testid="stContainer"] > div[style*="border"] {
    background: var(--card-bg) !important;
    border: 2px solid #F0EBE3 !important;
    border-radius: var(--border-radius) !important;
    box-shadow: var(--shadow) !important;
    transition: box-shadow 0.2s ease, transform 0.2s ease !important;
    padding: 1.5rem !important;
    margin-bottom: 1rem !important;
}

[data-testid="stContainer"] > div[style*="border"]:hover {
    box-shadow: var(--shadow-hover) !important;
    transform: translateY(-2px) !important;
}

.stTextInput input {
    border: 2px solid #E8E0D8 !important;
    border-radius: 12px !important;
    padding: 0.6rem 1rem !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.95rem !important;
    background: white !important;
    transition: border-color 0.2s !important;
}

.stTextInput input:focus {
    border-color: var(--coral) !important;
    box-shadow: 0 0 0 3px rgba(255,107,107,0.12) !important;
}

[data-baseweb="select"] > div {
    border: 2px solid #E8E0D8 !important;
    border-radius: 12px !important;
    background: white !important;
}

.stSpinner > div {
    border-top-color: var(--coral) !important;
}

.stMarkdown p {
    font-family: 'Nunito', sans-serif !important;
    line-height: 1.7 !important;
}

.history-column {
    position: sticky;
    top: 1rem;
}

.tag-pill {
    display: inline-block;
    background: var(--peach);
    color: var(--coral);
    font-weight: 800;
    font-size: 0.75rem;
    padding: 0.25rem 0.75rem;
    border-radius: 50px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-right: 0.4rem;
    margin-bottom: 0.4rem;
}

.tag-pill.green { background: #E8F8EA; color: #2E8B41; }
.tag-pill.blue  { background: #EEF4FF; color: #2563EB; }
.tag-pill.yellow { background: #FFFBEB; color: #B45309; }

hr {
    border: none !important;
    border-top: 2px dashed #F0EBE3 !important;
    margin: 1rem 0 !important;
}

.history-current {
    background: #FFF8F0 !important;
    border-color: var(--yellow) !important;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.custom-loader-wrap {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: white;
    border: 2px solid #F0EBE3;
    border-radius: var(--border-radius);
    padding: 1.5rem 2rem;
    margin: 1rem 0;
    box-shadow: var(--shadow);
}

.custom-loader {
    width: 36px;
    height: 36px;
    border: 4px solid #F0EBE3;
    border-top: 4px solid var(--coral);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    flex-shrink: 0;
}

.custom-loader-text {
    font-weight: 700;
    color: var(--text) !important;
    font-size: 0.95rem;
}

.custom-loader-subtext {
    font-size: 0.8rem;
    color: var(--muted) !important;
    margin-top: 0.2rem;
}

/* ===== Centered main-screen loader ===== */
.center-loader-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: white;
    border: 2px solid #F0EBE3;
    border-radius: var(--border-radius);
    padding: 3rem 2rem;
    margin: 2rem 0;
    box-shadow: var(--shadow);
}

.center-loader-title {
    font-family: 'Fraunces', serif;
    font-weight: 700;
    font-size: 1.4rem;
    color: var(--dark) !important;
    margin-bottom: 1.5rem;
}

.center-loader-circle {
    width: 48px;
    height: 48px;
    border: 5px solid #F0EBE3;
    border-top: 5px solid var(--coral);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}
/* ===== END CENTERED LOADER ===== */

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--cream); }
::-webkit-scrollbar-thumb { background: #D9CFC7; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--coral); }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display:flex; align-items:center; gap:1rem; margin-bottom: 0.25rem;">
    <h1 style="margin:0; line-height:1.1;">Creative Classroom</h1>
</div>
""", unsafe_allow_html=True)

defaults = {
    "ideas": [],
    "history": {},
    "selected": None,
    "refine_triggered": False,
    "refine_result": None,
    "age": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

if not isinstance(st.session_state.history, dict):
    st.session_state.history = {}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Start Here")
    st.markdown("""
    <p style="color:rgba(255,255,255,0.7);font-size:0.88rem;margin-top:-0.5rem;margin-bottom:1rem;">
    Fill in the details below to generate classroom activity ideas.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    topic = st.text_input("Topic", placeholder="e.g. Water Cycle")
    age = st.selectbox(
        "Age Group",
        ["5-7", "8-10", "11-12", "12-14", "15-17"]
    )

    goal = st.selectbox(
        "Goal",
        ["Discussion", "Experiment", "Group Project", "Game/Quiz", "Individual Writing", "Outdoor Activity"],
        help="What should students do?"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    generate_clicked = st.button("Generate Ideas", type="primary", use_container_width=True)

    if st.session_state.ideas:
        st.markdown(
            '<p style="font-size:0.8rem; color:rgba(255,255,255,0.45); text-align:center; margin-top:0.5rem;">'
            'Click Generate again for fresh ideas</p>',
            unsafe_allow_html=True
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
        <div style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);
        border-radius:12px;padding:0.75rem 1rem;margin-bottom:1rem;">
            <div style="font-size:0.75rem;color:rgba(255,255,255,0.5);line-height:1.6;">
                AI-generated content may contain errors. Always review activities before use in the classroom.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Layout ────────────────────────────────────────────────────────────────────
main_col, spacer, history_col = st.columns([4, 0.3, 1.8])

ACCENT_COLORS = ["#FF6B6B", "#4D96FF", "#6BCB77", "#FFD93D", "#C77DFF"]

def render_idea_card(idea, index):
    title     = idea.get("title", f"Idea {index + 1}")
    why       = idea.get("why_it_works", "")
    time      = idea.get("time", "")
    materials = idea.get("materials", [])
    steps     = idea.get("steps", [])
    accent    = ACCENT_COLORS[index % len(ACCENT_COLORS)]

    if index > 0:
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(
            f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.75rem;">'
            f'<div style="width:40px;height:5px;border-radius:10px;background:{accent};"></div>'
            f'<div style="background:{accent}22;color:{accent};font-weight:900;font-size:0.75rem;'
            f'padding:0.2rem 0.7rem;border-radius:50px;letter-spacing:0.5px;">IDEA {index + 1}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown(f"### {title}")
        if why:
            st.markdown(
                f'<p style="color:#555; font-size:0.9rem; margin-bottom:1rem;">{why}</p>',
                unsafe_allow_html=True
            )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f'<div style="background:#FFF8F0;border:1.5px solid #F0EBE3;border-radius:12px;padding:0.6rem 0.8rem;">'
                f'<div style="font-size:0.7rem;font-weight:800;color:#999999;text-transform:uppercase;letter-spacing:0.5px;">Time</div>'
                f'<div style="font-weight:700;font-size:0.95rem;margin-top:2px;color:#2D2D2D;">{time or "—"}</div>'
                f'</div>', unsafe_allow_html=True
            )
        with col2:
            mat_count = len(materials) if materials else 0
            st.markdown(
                f'<div style="background:#FFF8F0;border:1.5px solid #F0EBE3;border-radius:12px;padding:0.6rem 0.8rem;">'
                f'<div style="font-size:0.7rem;font-weight:800;color:#999999;text-transform:uppercase;letter-spacing:0.5px;">Materials</div>'
                f'<div style="font-weight:700;font-size:0.95rem;margin-top:2px;color:#2D2D2D;">{mat_count} items</div>'
                f'</div>', unsafe_allow_html=True
            )
        with col3:
            step_count = len(steps) if steps else 0
            st.markdown(
                f'<div style="background:#FFF8F0;border:1.5px solid #F0EBE3;border-radius:12px;padding:0.6rem 0.8rem;">'
                f'<div style="font-size:0.7rem;font-weight:800;color:#999999;text-transform:uppercase;letter-spacing:0.5px;">Steps</div>'
                f'<div style="font-weight:700;font-size:0.95rem;margin-top:2px;color:#2D2D2D;">{step_count} steps</div>'
                f'</div>', unsafe_allow_html=True
            )

        if materials:
            st.markdown("<br>", unsafe_allow_html=True)
            pills_html = "".join(
                f'<span style="display:inline-block;background:#FFF3E8;color:#E05C00;'
                f'font-weight:700;font-size:0.75rem;padding:0.2rem 0.65rem;'
                f'border-radius:50px;margin:0.2rem 0.2rem 0 0;">{m}</span>'
                for m in materials[:5]
            )
            if len(materials) > 5:
                pills_html += f'<span style="display:inline-block;background:#F0F0F0;color:#888;font-weight:700;font-size:0.75rem;padding:0.2rem 0.65rem;border-radius:50px;margin:0.2rem 0.2rem 0 0;">+{len(materials)-5} more</span>'
            st.markdown(pills_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Select & Refine", key=f"idea_{index}", type="primary"):
            st.session_state.selected = idea
            st.session_state.refine_triggered = True
            st.session_state.refine_result = None
            st.rerun()

# ── Main Content ──────────────────────────────────────────────────────────────
with main_col:

    # Handle "Generate Ideas" click here so the centered loader renders in main column
    if generate_clicked:
        if not topic.strip():
            st.warning("Please enter a topic.")
        elif not goal.strip():
            st.warning("Please enter a goal.")
        else:
            loader = st.empty()
            loader.markdown(f"""
            <div class="center-loader-wrap">
                <div class="center-loader-title">Generating ideas for: {topic}</div>
                <div class="center-loader-circle"></div>
            </div>
            """, unsafe_allow_html=True)
            new_ideas = generate_ideas(topic, age, goal)
            loader.empty()
            st.session_state.ideas = new_ideas
            st.session_state.age = age
            st.session_state.selected = None
            st.session_state.refine_triggered = False
            st.session_state.refine_result = None
            for idea in new_ideas:
                title = idea.get("title", "Untitled")
                st.session_state.history[title] = idea
            st.rerun()

    if not st.session_state.ideas:

        # How it works
        st.markdown("### How it works")
        st.markdown("""
        <div style="display:flex;gap:1rem;margin-bottom:2rem;">
            <div style="flex:1;background:white;border:2px solid #F0EBE3;border-radius:20px;padding:1.2rem;text-align:center;">
                <div style="font-weight:800;margin-bottom:0.3rem;color:#FF6B6B;">Step 1</div>
                <div style="font-weight:700;margin-bottom:0.3rem;">Fill in the sidebar</div>
                <div style="font-size:0.82rem;color:#8A8A9A;">Enter your topic, choose the age group, and describe what you want students to do</div>
            </div>
            <div style="flex:1;background:white;border:2px solid #F0EBE3;border-radius:20px;padding:1.2rem;text-align:center;">
                <div style="font-weight:800;margin-bottom:0.3rem;color:#4D96FF;">Step 2</div>
                <div style="font-weight:700;margin-bottom:0.3rem;">Generate ideas</div>
                <div style="font-size:0.82rem;color:#8A8A9A;">Hit Generate and get 3 creative activity ideas tailored to your class</div>
            </div>
            <div style="flex:1;background:white;border:2px solid #F0EBE3;border-radius:20px;padding:1.2rem;text-align:center;">
                <div style="font-weight:800;margin-bottom:0.3rem;color:#6BCB77;">Step 3</div>
                <div style="font-weight:700;margin-bottom:0.3rem;">Refine & safety check</div>
                <div style="font-size:0.82rem;color:#8A8A9A;">Pick your favourite and let AI adapt it for your age group with a full safety audit</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


    else:
        ideas = st.session_state.ideas
        selected = st.session_state.selected
        refine_result = st.session_state.refine_result

        if not selected:
            st.markdown("""
            <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:1.5rem;">
                <h2 style="margin:0;font-size:1.5rem;">Choose an Activity</h2>
            </div>
            """, unsafe_allow_html=True)
            for i, idea in enumerate(ideas):
                render_idea_card(idea, i)

        else:
            if st.session_state.refine_triggered:
                st.session_state.refine_triggered = False
                st.session_state.risks_acknowledged = False

                loader = st.empty()
                loader.markdown(f"""
                <div class="center-loader-wrap">
                    <div class="center-loader-title">Refining idea: {selected.get("title")}</div>
                    <div class="center-loader-circle"></div>
                </div>
                """, unsafe_allow_html=True)
                result = refine_activity(selected, st.session_state.age)
                loader.empty()
                st.session_state.refine_result = result
                refine_result = result

            if refine_result:
                status = refine_result.get("status")

                if status == "ok":
                    final_plan = refine_result.get("final_plan", {})

                    st.markdown(
                        f'<div style="background:white;border:2px solid #F0EBE3;'
                        f'border-radius:18px;padding:1.2rem 1.6rem;margin-bottom:1.5rem;'
                        f'display:flex;align-items:center;gap:1rem;box-shadow:var(--shadow);">'
                        f'<div style="width:6px;height:36px;background:#FFD93D;border-radius:10px;flex-shrink:0;"></div>'
                        f'<div>'
                        f'<div style="font-size:0.7rem;font-weight:800;color:#999999;'
                        f'text-transform:uppercase;letter-spacing:1.5px;margin-bottom:0.2rem;">Refining Activity</div>'
                        f'<div style="font-family:\'Fraunces\', serif;font-weight:700;font-size:1.4rem;color:#2D2D2D;">'
                        f'{selected.get("title")}</div>'
                        f'</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    st.success("Refinement Complete — your activity is ready!")

                    with st.container(border=True):
                        st.markdown(
                            '<div style="width:40px;height:5px;border-radius:10px;background:#6BCB77;margin-bottom:0.75rem;"></div>',
                            unsafe_allow_html=True
                        )
                        st.markdown(f"### {final_plan.get('title', selected.get('title'))}")
                        st.markdown(
                            f'<p style="font-size:0.95rem;color:#444;line-height:1.7;">'
                            f'{final_plan.get("adapted_description", "No description returned.")}'
                            f'</p>',
                            unsafe_allow_html=True
                        )

                        if "steps" in final_plan:
                            st.markdown("**Steps:**")
                            for j, step in enumerate(final_plan["steps"], 1):
                                st.markdown(
                                    f'<div style="display:flex;gap:0.75rem;align-items:flex-start;margin-bottom:0.5rem;">'
                                    f'<div style="min-width:26px;height:26px;background:#FF6B6B;color:white;border-radius:50%;'
                                    f'display:flex;align-items:center;justify-content:center;font-weight:800;font-size:0.8rem;">{j}</div>'
                                    f'<div style="padding-top:3px;color:#2D2D2D;">{step}</div>'
                                    f'</div>',
                                    unsafe_allow_html=True
                                )

                    with st.expander("Safety Audit", expanded=True):
                        safety_data = refine_result.get("safety", {})
                        if isinstance(safety_data, dict):
                            safety_status = safety_data.get("status", "Unknown").upper()
                            if safety_status == "SAFE":
                                st.markdown(
                                    '<div style="background:#ECFDF5;border-radius:12px;padding:0.8rem 1rem;'
                                    'font-weight:800;color:#059669;font-size:1rem;">Status: SAFE</div>',
                                    unsafe_allow_html=True
                                )
                            else:
                                st.markdown(
                                    f'<div style="background:#FFFBEB;border-radius:12px;padding:0.8rem 1rem;'
                                    f'font-weight:800;color:#D97706;font-size:1rem;">Status: {safety_status}</div>',
                                    unsafe_allow_html=True
                                )

                            st.markdown("<br>", unsafe_allow_html=True)
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(
                                    f'<div style="background:#FFF8F0;border:1.5px solid #F0EBE3;border-radius:12px;padding:0.7rem 1rem;">'
                                    f'<div style="font-size:0.75rem;color:#999999;text-transform:uppercase;font-weight:700;">Severity</div>'
                                    f'<div style="font-weight:800;color:#2D2D2D;">{safety_data.get("severity", "none").title()}</div>'
                                    f'</div>', unsafe_allow_html=True
                                )
                            with col2:
                                safe = safety_data.get("safe_to_use", False)
                                st.markdown(
                                    f'<div style="background:#FFF8F0;border:1.5px solid #F0EBE3;border-radius:12px;padding:0.7rem 1rem;">'
                                    f'<div style="font-size:0.75rem;color:#999999;text-transform:uppercase;font-weight:700;">Safe to Use</div>'
                                    f'<div style="font-weight:800;color:#2D2D2D;">{"Yes" if safe else "No"}</div>'
                                    f'</div>', unsafe_allow_html=True
                                )

                            st.markdown("<br>", unsafe_allow_html=True)

                            for key in ["risks", "suggestions"]:
                                value = safety_data.get(key)
                                st.markdown(f"#### {key.title()}")
                                if not value or value == "none":
                                    st.markdown(
                                        f'<p style="color:#aaa;font-style:italic;">No {key} identified.</p>',
                                        unsafe_allow_html=True
                                    )
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

                    if not st.session_state.get("risks_acknowledged"):
                        st.markdown("""
                        <div style="background:#FFFBEB;border:2px solid #FFD93D;border-radius:16px;
                        padding:1rem 1.5rem;margin-top:1rem;display:flex;align-items:center;gap:1rem;">
                            <div style="font-size:0.88rem;color:#92400E;line-height:1.6;">
                                <strong>Please review before use.</strong> AI-generated activities and safety assessments 
                                may contain errors or omissions. You are responsible for evaluating suitability 
                                for your specific classroom context.
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("I understand — I will review this activity before use", type="secondary", use_container_width=True):
                            st.session_state.risks_acknowledged = True
                            st.rerun()
                    else:
                        st.success("Acknowledged — remember to review before use!")

                elif status == "rejected":
                    st.error("This activity was flagged as unsafe and could not be resolved.")
                    st.write(refine_result.get("assessment"))
                elif status == "unresolved":
                    st.warning("Could not produce a safe version after multiple attempts.")
                    st.write(refine_result.get("last_safety"))
                else:
                    st.error(f"Pipeline error: {refine_result}")
                    st.write(refine_result.get("detail"))

# ── History Sidebar ───────────────────────────────────────────────────────────
with history_col:
    st.markdown('<div class="history-column">', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:1.2rem;">
        <div style="width:5px;height:28px;background:#FFD93D;border-radius:10px;"></div>
        <h2 style="margin:0;font-size:1.2rem;">Previous Ideas</h2>
    </div>
    """, unsafe_allow_html=True)

    history = st.session_state.history

    if not history:
        st.markdown(
            '<div style="background:white;border:2px dashed #E8E0D8;border-radius:16px;'
            'padding:1.5rem;text-align:center;">'
            '<div style="color:#aaa;font-size:0.85rem;font-weight:600;">No ideas yet.<br>Generate some to get started!</div>'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        for idx, (title, idea) in enumerate(reversed(list(history.items()))):
            is_selected = st.session_state.selected == idea
            accent = ACCENT_COLORS[idx % len(ACCENT_COLORS)]
            why = idea.get("why_it_works", "") or idea.get("description", "")
            short_desc = why[:80] + "…" if len(why) > 80 else why

            with st.container(border=True):
                st.markdown(
                    f'<div style="width:30px;height:4px;border-radius:10px;background:{accent};margin-bottom:0.6rem;"></div>'
                    f'<div style="font-weight:800;font-size:0.88rem;margin-bottom:0.3rem;color:#2D2D2D;line-height:1.3;">{title}</div>'
                    + (f'<div style="font-size:0.78rem;color:#888;margin-bottom:0.4rem;line-height:1.4;">{short_desc}</div>' if short_desc else ""),
                    unsafe_allow_html=True
                )
                if is_selected:
                    st.markdown(
                        '<div style="background:#FFF9E0;border-radius:8px;padding:0.3rem 0.6rem;'
                        'font-size:0.75rem;font-weight:700;color:#B45309;margin-bottom:0.5rem;display:inline-block;">'
                        'Currently viewing</div>',
                        unsafe_allow_html=True
                    )
                if st.button(
                    "Active" if is_selected else "Choose →",
                    key=f"history_{idx}",
                    use_container_width=True,
                    disabled=is_selected,
                    type="secondary"
                ):
                    st.session_state.selected = idea
                    st.session_state.refine_triggered = True
                    st.session_state.refine_result = None
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)