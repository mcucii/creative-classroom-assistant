import boto3
import json
import streamlit as st
import base64
import os

# ── Config ────────────────────────────────────────────────────────────────────
st.set_page_config(layout="wide", page_title="Creative Classroom")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(SCRIPT_DIR, "..", "images", "background2.png")
AGENT_RUNTIME_ARN = "arn:aws:bedrock-agentcore:eu-central-1:963649480732:runtime/classroom_agent-XAQfz84DXl"

client = boto3.client("bedrock-agentcore", region_name="eu-central-1")

# ── Background ────────────────────────────────────────────────────────────────
def set_background(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64 = base64.b64encode(img_data).decode()
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """, unsafe_allow_html=True)

set_background(IMAGE_PATH)

# ── Agent calls ───────────────────────────────────────────────────────────────
def _decode_bedrock_response(response):
    if "payload" in response:
        body = response["payload"].read()
    elif "response" in response:
        body = response["response"].read()
    else:
        raise RuntimeError(f"Unexpected Bedrock response shape: {list(response.keys())}")
    return json.loads(body)


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
    result = _decode_bedrock_response(response)
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
    return _decode_bedrock_response(response)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Fraunces:ital,wght@0,400;0,700;1,400&display=swap');

:root {
    --dark:         #342E37;
    --text:         #342E37;
    --muted:        #8A8A9A;
    --orange:       #FA824C;
    --orange-dark:  #C75A2E;
    --orange-light: #FDE3D6;
    --blue:         #3C91E6;
    --blue-light:   #E8F1FC;
    --green:        #9FD356;
    --green-dark:   #5C8A2E;
    --green-light:  #EFF8E6;
    --border-light: #E4ECE7;
    --border-radius: 20px;
    --shadow:       0 4px 24px rgba(0,0,0,0.08);
    --shadow-hover: 0 8px 32px rgba(0,0,0,0.14);
    --sidebar-bg:   #0f3d22;
    --cream:        #f6f4eb;
}

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif !important;
    color: var(--text) !important;
}

header[data-testid="stHeader"] { background: transparent !important; }

h1 { font-family: 'Fraunces', serif !important; font-size: 2.6rem !important; font-weight: 700 !important; color: var(--dark); }
h2 { font-family: 'Fraunces', serif !important; font-weight: 700 !important; color: var(--dark); }
h3 { font-family: 'Nunito', sans-serif !important; font-weight: 800 !important; color: var(--dark); }

[data-testid="stMarkdownContainer"],
.stMarkdown { color: var(--text); }

[data-testid="stAlertContainer"],
[data-testid="stAlert"],
.stAlert {
    background: white !important;
    border: 2px solid var(--border-light) !important;
    border-radius: 14px !important;
}
[data-testid="stAlertContainer"] *,
[data-testid="stAlert"] *,
.stAlert * { color: var(--text) !important; fill: var(--text) !important; }

[data-testid="stExpander"] summary {
    background: var(--orange-light) !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
    color: var(--dark) !important;
    fill: var(--dark) !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: var(--cream) !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--cream) !important;
    font-family: 'Fraunces', serif !important;
}
[data-testid="stSidebar"] label {
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
    opacity: 0.7 !important;
}
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] [data-baseweb="select"],
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(112,198,165,0.18) !important;
    border: 1.5px solid rgba(112,198,165,0.35) !important;
    border-radius: 12px !important;
    color: var(--cream) !important;
}
[data-testid="stSidebar"] .stTextInput input::placeholder {
    color: rgba(246,244,235,0.6) !important;
}

[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
    background: #e75e35 !important;
    color: white !important;
    border-radius: 50px !important;
    border: none !important;
    padding: 0.6rem 1.6rem !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
    box-shadow: 0 4px 0px #b84425 !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebar"] div.stButton > button[kind="primary"]:hover {
    background: #ec7a57 !important;
    box-shadow: 0 6px 0px #b84425 !important;
    transform: translateY(-2px) !important;
}

div.stButton > button[kind="primary"] {
    background: var(--cream) !important;
    color: #0f3d22 !important;
    border-radius: 50px !important;
    border: none !important;
    padding: 0.65rem 1.6rem !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
    box-shadow: 0 4px 0px rgba(15,61,34,0.4) !important;
    transition: all 0.2s ease !important;
}

div.stButton > button[kind="primary"]:hover {
    background: #ffffff !important;
    color: #0f3d22 !important;
    box-shadow: 0 6px 0px rgba(15,61,34,0.4) !important;
    transform: translateY(-2px) !important;
}
            
div.stButton > button[kind="primary"]:active {
    transform: translateY(2px) !important;
    box-shadow: 0 2px 0px #0b2b18 !important;
}

div.stButton > button[kind="secondary"] {
    background: white !important;
    border: 2px solid var(--border-light) !important;
    color: var(--text) !important;
    border-radius: 50px !important;
    font-weight: 700 !important;
    transition: all 0.2s ease !important;
}
div.stButton > button[kind="secondary"]:hover {
    border-color: var(--blue) !important;
    color: var(--blue) !important;
    background: var(--blue-light) !important;
    transform: translateY(-1px) !important;
}
div.stButton > button[kind="secondary"]:disabled {
    background: var(--orange) !important;
    border-color: var(--orange) !important;
    color: white !important;
    opacity: 1 !important;
    font-weight: 800 !important;
}

[data-testid="stContainer"] > div[style*="border"] {
    background: rgba(255,255,255,0.88) !important;
    backdrop-filter: blur(8px) !important;
    border: 2px solid rgba(255,255,255,0.7) !important;
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
    border: 2px solid var(--border-light) !important;
    border-radius: 12px !important;
    padding: 0.6rem 1rem !important;
    font-size: 0.95rem !important;
    background: white !important;
    transition: border-color 0.2s !important;
}
.stTextInput input:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 3px rgba(250,130,76,0.15) !important;
}
[data-baseweb="select"] > div {
    border: 2px solid var(--border-light) !important;
    border-radius: 12px !important;
    background: white !important;
}

.stSpinner > div { border-top-color: var(--orange) !important; }
.stMarkdown p { line-height: 1.7 !important; }
hr { border: none !important; border-top: 2px dashed var(--border-light) !important; margin: 1rem 0 !important; }

@keyframes spin { to { transform: rotate(360deg); } }

.center-loader-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: rgba(255,255,255,0.92);
    border: 2px solid var(--border-light);
    border-radius: var(--border-radius);
    padding: 3rem 2rem;
    margin: 2rem 0;
    box-shadow: var(--shadow);
}
.center-loader-title {
    font-family: 'Fraunces', serif;
    font-weight: 700;
    font-size: 1.4rem;
    color: var(--dark);
    margin-bottom: 1.5rem;
}
.center-loader-circle {
    width: 48px;
    height: 48px;
    border: 5px solid var(--border-light);
    border-top: 5px solid var(--orange);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f0f0f0; }
::-webkit-scrollbar-thumb { background: var(--border-light); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--orange); }
</style>
""", unsafe_allow_html=True)

# ── Title ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:inline-block;background:rgba(255,255,255,0.88);backdrop-filter:blur(10px);
border-radius:16px;padding:0.5rem 1.5rem;margin-bottom:1rem;
border:1.5px solid rgba(255,255,255,0.7);box-shadow:0 2px 12px rgba(0,0,0,0.08);">
    <h1 style="margin:0;line-height:1.1;color:#342E37;">Creative Classroom</h1>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
defaults = {
    "ideas": [], "history": {}, "selected": None,
    "refine_triggered": False, "refine_result": None,
    "age": None, "risks_acknowledged": False
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
    <p style="color:rgba(246,244,235,0.7);font-size:0.88rem;margin-top:-0.5rem;margin-bottom:1rem;">
    Fill in the details below to generate classroom activity ideas.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    topic = st.text_input("Topic", placeholder="e.g. Water Cycle")
    age = st.selectbox("Age Group", ["5-7", "8-10", "11-12", "12-14", "15-17"])
    goal = st.selectbox("Goal", [
        "Discussion", "Experiment", "Group Project",
        "Game/Quiz", "Individual Writing", "Outdoor Activity"
    ])

    st.markdown("<br>", unsafe_allow_html=True)
    generate_clicked = st.button("Generate Ideas", type="primary", use_container_width=True)

    if st.session_state.ideas:
        st.markdown(
            '<p style="font-size:0.8rem;color:rgba(246,244,235,0.45);text-align:center;margin-top:0.5rem;">'
            'Click Generate to get fresh ideas</p>', unsafe_allow_html=True
        )

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);
    border-radius:12px;padding:0.75rem 1rem;">
        <div style="font-size:0.75rem;color:rgba(246,244,235,0.7);line-height:1.6;">
            ⚠️ AI-generated content may contain errors. Always review activities before use in the classroom.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Layout ────────────────────────────────────────────────────────────────────
main_col, _, history_col = st.columns([4, 0.3, 1.8])

ACCENT_COLORS = ["#FA824C", "#3C91E6", "#9FD356", "#342E37"]

# ── Idea card ─────────────────────────────────────────────────────────────────

st.markdown("""
<style>
/* Force frosted white window onto ALL bordered containers */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.92) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 24px !important;
    border: 1.5px solid rgba(255, 255, 255, 0.7) !important;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08) !important;
    padding: 1.5rem !important;
    margin-bottom: 1.5rem !important;
}

/* Force the pink buttons inside these containers */
div[data-testid="stVerticalBlockBorderWrapper"] button {
    background-color: #6fa0d6 !important;
    border: none !important;
    border-radius: 50px !important;
    box-shadow: 0 4px 0px #c14d85 !important;
    padding: 0.4rem 1.5rem !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] button p {
    color: #f6f4eb !important;
    font-weight: 800 !important;
    margin: 0 !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] button:hover {
    background-color: #f07ab5 !important;
    box-shadow: 0 6px 0px #c14d85 !important;
    transform: translateY(-2px) !important;
}
</style>
""", unsafe_allow_html=True)

def render_idea_card(idea, index):
    title = idea.get("title", f"Idea {index + 1}")
    why = idea.get("why_it_works", "")
    time = idea.get("time", "")
    materials = idea.get("materials", [])
    steps = idea.get("steps", [])
    accent = ACCENT_COLORS[index % len(ACCENT_COLORS)]

    # Add targeted CSS to make primary buttons inside columns pink
    st.markdown("""
    <style>
    div[data-testid="stColumn"] button[kind="primary"] {
        background-color: #6fa0d6 !important;
        border: none !important;
        border-radius: 50px !important;
        box-shadow: 0 4px 0px #c14d85 !important;
        padding: 0.4rem 1.5rem !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stColumn"] button[kind="primary"] p {
        color: #f6f4eb !important;
        font-weight: 800 !important;
        margin: 0 !important;
    }
    div[data-testid="stColumn"] button[kind="primary"]:hover {
        background-color: #f07ab5 !important;
        box-shadow: 0 6px 0px #c14d85 !important;
        transform: translateY(-2px) !important;
    }
    div[data-testid="stColumn"] button[kind="primary"]:active {
        transform: translateY(2px) !important;
        box-shadow: 0 0px 0px #c14d85 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    html = f"""<div style="background:rgba(255,255,255,0.7);backdrop-filter:blur(10px);border-radius:24px;border:1.5px solid rgba(255,255,255,0.7);box-shadow:0 4px 24px rgba(0,0,0,0.08);padding:1.5rem;padding-bottom:4.5rem;margin-bottom:-3.5rem;position:relative;z-index:0;">
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;">
<div style="width:40px;height:5px;border-radius:10px;background:{accent};"></div>
<div style="background:{accent}22;color:{accent};font-weight:900;font-size:0.75rem;padding:0.2rem 0.7rem;border-radius:50px;letter-spacing:0.5px;">IDEA {index + 1}</div>
</div>
<h3 style="margin:0 0 0.5rem 0;color:#342E37;">{title}</h3>
"""
    if why:
        html += f'<p style="color:#555;font-size:0.95rem;margin-bottom:1.5rem;line-height:1.6;">{why}</p>\n'

    html += f"""<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.75rem;margin-bottom:1rem;">
<div style="background:#F4F8F6;border:1.5px solid #E4ECE7;border-radius:12px;padding:0.65rem;">
    <div style="font-size:0.7rem;font-weight:800;color:#999;text-transform:uppercase;letter-spacing:0.5px;">Time</div>
    <div style="font-weight:800;font-size:0.9rem;margin-top:4px;color:#342E37;">{time or "—"}</div>
</div>
<div style="background:#F4F8F6;border:1.5px solid #E4ECE7;border-radius:12px;padding:0.65rem;">
    <div style="font-size:0.7rem;font-weight:800;color:#999;text-transform:uppercase;letter-spacing:0.5px;">Materials</div>
    <div style="font-weight:800;font-size:0.9rem;margin-top:4px;color:#342E37;">{len(materials)} items</div>
</div>
<div style="background:#F4F8F6;border:1.5px solid #E4ECE7;border-radius:12px;padding:0.65rem;">
    <div style="font-size:0.7rem;font-weight:800;color:#999;text-transform:uppercase;letter-spacing:0.5px;">Steps</div>
    <div style="font-weight:800;font-size:0.9rem;margin-top:4px;color:#342E37;">{len(steps)} steps</div>
</div>
</div>
"""
    if materials:
        pills = "".join(f'<span style="display:inline-block;background:#FDE3D6;color:#C75A2E;font-weight:800;font-size:0.75rem;padding:0.2rem 0.65rem;border-radius:50px;margin:0.2rem 0.2rem 0 0;">{m}</span>' for m in materials[:5])
        if len(materials) > 5:
            pills += f'<span style="display:inline-block;background:#F0F0F0;color:#888;font-weight:800;font-size:0.75rem;padding:0.2rem 0.65rem;border-radius:50px;margin:0.2rem 0.2rem 0 0;">+{len(materials)-5} more</span>'
        html += f'<div style="margin-bottom:0.5rem;">{pills}</div>\n'

    html += "</div>" 

    st.markdown(html, unsafe_allow_html=True)

    col1, col2 = st.columns([0.03, 0.97])
    with col2:
        # Note the added type="primary" here!
        if st.button("Select & Refine", key=f"idea_{index}", type="primary"):
            st.session_state.selected = idea
            st.session_state.refine_triggered = True
            st.session_state.refine_result = None
            st.rerun()
            
    st.markdown("<div style='margin-bottom: 2.5rem;'></div>", unsafe_allow_html=True)

# ── Main content ──────────────────────────────────────────────────────────────
with main_col:

    if generate_clicked:
        if not topic.strip():
            st.warning("Please enter a topic.")
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
            st.session_state.risks_acknowledged = False
            for idea in new_ideas:
                st.session_state.history[idea.get("title", "Untitled")] = idea
            st.rerun()

    if not st.session_state.ideas:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.88);backdrop-filter:blur(10px);border-radius:24px;
        padding:1.5rem 2rem;margin-bottom:1.5rem;border:1.5px solid rgba(255,255,255,0.7);
        box-shadow:0 4px 24px rgba(0,0,0,0.08);">
            <h3 style="margin-top:0;color:#342E37;">How it works</h3>
            <div style="display:flex;gap:1rem;">
                <div style="flex:1;background:rgba(255,255,255,0.7);border:2px solid #E4ECE7;border-radius:20px;padding:1.2rem;text-align:center;">
                    <div style="font-weight:800;margin-bottom:0.3rem;color:#FA824C;">Step 1</div>
                    <div style="font-weight:700;margin-bottom:0.3rem;color:#342E37;">Fill in the sidebar</div>
                    <div style="font-size:0.82rem;color:#666;">Enter your topic, choose the age group, and describe what you want students to do</div>
                </div>
                <div style="flex:1;background:rgba(255,255,255,0.7);border:2px solid #E4ECE7;border-radius:20px;padding:1.2rem;text-align:center;">
                    <div style="font-weight:800;margin-bottom:0.3rem;color:#3C91E6;">Step 2</div>
                    <div style="font-weight:700;margin-bottom:0.3rem;color:#342E37;">Generate ideas</div>
                    <div style="font-size:0.82rem;color:#666;">Hit Generate and get 3 creative activity ideas tailored to your class</div>
                </div>
                <div style="flex:1;background:rgba(255,255,255,0.7);border:2px solid #E4ECE7;border-radius:20px;padding:1.2rem;text-align:center;">
                    <div style="font-weight:800;margin-bottom:0.3rem;color:#9FD356;">Step 3</div>
                    <div style="font-weight:700;margin-bottom:0.3rem;color:#342E37;">Refine & safety check</div>
                    <div style="font-size:0.82rem;color:#666;">Pick your favourite and let AI adapt it for your age group with a full safety audit</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        ideas = st.session_state.ideas
        selected = st.session_state.selected
        refine_result = st.session_state.refine_result

        if not selected:
            st.markdown("""
            <div style="margin-top: 1rem; margin-bottom: 2rem; display: flex; align-items: center; gap: 1rem;">
                <h2 style="margin:0; font-size: 1.8rem; color: #342E37; font-weight: 800; letter-spacing: -0.5px;">Choose an Activity</h2>
                <div style="height: 3px; flex-grow: 1; background: linear-gradient(to right, rgba(231,104,168,0.4), transparent); border-radius: 10px;"></div>
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
                    <div class="center-loader-title">Refining: {selected.get("title")}</div>
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
                    st.success("Refinement Complete — your activity is ready!")

                    steps_html = ""
                    if "steps" in final_plan:
                        for j, step in enumerate(final_plan["steps"], 1):
                            steps_html += (
                                f'<div style="display:flex;gap:0.75rem;align-items:flex-start;margin-bottom:0.5rem;">'
                                f'<div style="min-width:26px;height:26px;background:#FA824C;color:white;border-radius:50%;'
                                f'display:flex;align-items:center;justify-content:center;font-weight:800;font-size:0.8rem;">{j}</div>'
                                f'<div style="padding-top:3px;color:#342E37;">{step}</div>'
                                f'</div>'
                            )

                    st.markdown(f"""
                    <div style="background:rgba(255,255,255,0.92);backdrop-filter:blur(10px);border-radius:24px;
                    padding:1.5rem 2rem;margin-bottom:1rem;border:1.5px solid rgba(255,255,255,0.7);
                    box-shadow:0 4px 24px rgba(0,0,0,0.08);">
                        <div style="width:40px;height:5px;border-radius:10px;background:#9FD356;margin-bottom:0.75rem;"></div>
                        <h3 style="margin:0 0 0.75rem 0;color:#342E37;">{final_plan.get("title", selected.get("title"))}</h3>
                        <p style="font-size:0.95rem;color:#555;line-height:1.7;margin-bottom:1.25rem;">
                            {final_plan.get("adapted_description", "No description returned.")}
                        </p>
                        {"<div style='font-weight:700;color:#342E37;margin-bottom:0.5rem;'>Steps:</div>" + steps_html if steps_html else ""}
                    </div>
                    """, unsafe_allow_html=True)

                    with st.expander("Safety Audit", expanded=True):
                        safety_data = refine_result.get("safety", {})
                        if isinstance(safety_data, dict):
                            safety_status = safety_data.get("status", "Unknown").upper()
                            bg  = "#EFF8E6" if safety_status == "SAFE" else "#FDE3D6"
                            col = "#5C8A2E" if safety_status == "SAFE" else "#C75A2E"
                            st.markdown(
                                f'<div style="background:{bg};border-radius:12px;padding:0.8rem 1rem;'
                                f'font-weight:800;color:{col};font-size:1rem;margin-bottom:1rem;">Status: {safety_status}</div>',
                                unsafe_allow_html=True
                            )
                            c1, c2 = st.columns(2)
                            with c1:
                                st.markdown(
                                    f'<div style="background:#F4F8F6;border:1.5px solid #E4ECE7;border-radius:12px;padding:0.7rem 1rem;">'
                                    f'<div style="font-size:0.75rem;color:#999;text-transform:uppercase;font-weight:700;">Severity</div>'
                                    f'<div style="font-weight:800;color:#342E37;">{safety_data.get("severity","none").title()}</div>'
                                    f'</div>', unsafe_allow_html=True
                                )
                            with c2:
                                safe = safety_data.get("safe_to_use", False)
                                st.markdown(
                                    f'<div style="background:#F4F8F6;border:1.5px solid #E4ECE7;border-radius:12px;padding:0.7rem 1rem;">'
                                    f'<div style="font-size:0.75rem;color:#999;text-transform:uppercase;font-weight:700;">Safe to Use</div>'
                                    f'<div style="font-weight:800;color:#342E37;">{"Yes" if safe else "No"}</div>'
                                    f'</div>', unsafe_allow_html=True
                                )
                            st.markdown("<br>", unsafe_allow_html=True)
                            for key in ["risks", "suggestions"]:
                                value = safety_data.get(key)
                                st.markdown(f"#### {key.title()}")
                                if not value or value == "none":
                                    st.markdown(f'<p style="color:#aaa;font-style:italic;">No {key} identified.</p>', unsafe_allow_html=True)
                                    continue
                                if isinstance(value, list):
                                    for item in value:
                                        if isinstance(item, dict):
                                            category = item.get("category") or item.get("addresses_risk")
                                            content  = item.get("description") or item.get("change")
                                            if content:
                                                label = category.replace("_"," ").title() if category and category.lower() != "general" else None
                                                st.markdown(f"**{label}**: {content}" if label else f"- {content}")
                                        else:
                                            st.markdown(f"- {item}")
                                else:
                                    st.write(value)
                        else:
                            st.info("No structured safety data available.")
                            st.write(safety_data)

                    if not st.session_state.get("risks_acknowledged"):
                        st.markdown("""
                        <div style="background:rgba(255,255,255,0.88);border:2px solid #E4ECE7;border-radius:16px;
                        padding:1rem 1.5rem;margin-top:1rem;">
                            <div style="font-size:0.88rem;color:#342E37;line-height:1.6;">
                                ⚠️ <strong>Please review before use.</strong> AI-generated activities and safety assessments
                                may contain errors. You are responsible for evaluating suitability for your classroom.
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("✅ I understand — I will review this activity before use", type="secondary", use_container_width=True):
                            st.session_state.risks_acknowledged = True
                            st.rerun()
                    else:
                        st.success("✅ Acknowledged — remember to review before use!")

                elif status == "rejected":
                    st.error("This activity was flagged as unsafe and could not be resolved.")
                    st.write(refine_result.get("assessment"))
                elif status == "unresolved":
                    st.warning("Could not produce a safe version after multiple attempts.")
                    st.write(refine_result.get("last_safety"))
                else:
                    st.error(f"Pipeline error: {refine_result}")


# ── History column ────────────────────────────────────────────────────────────
# ── History column ────────────────────────────────────────────────────────────
with history_col:
    history = st.session_state.history

    st.markdown("""
    <style>
    /* 1. BRUTE FORCE THE BACKGROUND ON THE 3RD COLUMN */
    div.block-container div[data-testid="stHorizontalBlock"] > div:nth-child(3) {
        background: rgba(15, 61, 34, 0.95) !important;
        border-radius: 16px !important;
        padding: 1.8rem 1.5rem !important;
        border: 1px solid rgba(246, 244, 235, 0.2) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15) !important;
        height: fit-content !important; 
        align-self: flex-start !important;
    }
    
    /* 2. OVERRIDE YOUR GLOBAL CSS TO FORCE CREAM TEXT */
    div.block-container div[data-testid="stHorizontalBlock"] > div:nth-child(3) h2,
    div.block-container div[data-testid="stHorizontalBlock"] > div:nth-child(3) p,
    div.block-container div[data-testid="stHorizontalBlock"] > div:nth-child(3) div,
    div.block-container div[data-testid="stHorizontalBlock"] > div:nth-child(3) span {
        color: #f6f4eb !important;
    }
    
    /* 3. SMALL BUTTONS WITH DARK GREEN TEXT */
    div.block-container div[data-testid="stHorizontalBlock"] > div:nth-child(3) div.stButton > button {
        background: #f6f4eb !important;
        padding: 0.2rem 0.8rem !important;
        border-radius: 8px !important;
        border: none !important;
        min-height: 0 !important;
        box-shadow: 0 2px 0 rgba(0,0,0,0.2) !important;
        margin-top: -0.5rem !important;
        margin-bottom: 1rem !important;
    }
    div.block-container div[data-testid="stHorizontalBlock"] > div:nth-child(3) div.stButton > button p {
        color: #0f3d22 !important;
        font-weight: 800 !important;
        font-size: 0.8rem !important;
    }
    div.block-container div[data-testid="stHorizontalBlock"] > div:nth-child(3) div.stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 0 rgba(0,0,0,0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='margin:0 0 1.5rem 0; font-size:1.3rem; font-family:\"Fraunces\",serif; border-bottom: 1px solid rgba(246,244,235,0.2); padding-bottom: 0.8rem;'>Previous Ideas</h2>", unsafe_allow_html=True)

    if not history:
        st.markdown("""
        <div style="text-align:center; padding: 2.5rem 0; opacity: 0.9;">
            <div style="font-size:2.5rem; margin-bottom:0.5rem;">💡</div>
            <div style="font-size:1.05rem !important; font-weight:700 !important; line-height:1.5 !important;">
                No ideas yet.
            </div>
            <div style="font-size:0.85rem; font-weight:400; opacity:0.7; margin-top:0.3rem;">
                Generate some to get started!
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for idx, (title, idea) in enumerate(reversed(list(history.items()))):
            is_selected = st.session_state.selected == idea
            accent = ACCENT_COLORS[idx % len(ACCENT_COLORS)]
            why = idea.get("why_it_works", "") or idea.get("description", "")
            short_desc = why[:80] + "…" if len(why) > 80 else why

            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.06); border-radius: 12px; padding: 1rem; margin-bottom: 0.8rem; border: 1px solid rgba(246,244,235,0.1);">
                <div style="width:30px; height:4px; border-radius:10px; background:{accent}; margin-bottom:0.5rem;"></div>
                <div style="font-weight:800; font-size:0.95rem; line-height:1.3; margin-bottom:0.4rem;">
                    {title}
                </div>
                <div style="font-size:0.8rem; opacity:0.75; line-height:1.4; margin-bottom:0.5rem;">
                    {short_desc}
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_btn, col_space = st.columns([1.2, 1])
            with col_btn:
                if st.button("✓ Active" if is_selected else "Choose →", key=f"hist_{idx}", disabled=is_selected):
                    st.session_state.selected = idea
                    st.session_state.refine_triggered = True
                    st.session_state.refine_result = None
                    st.rerun()