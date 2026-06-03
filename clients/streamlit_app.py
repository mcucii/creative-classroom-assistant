import streamlit as st
from agentcore.orchestrator import ActivityOrchestrator
from agentcore.llm_providers import LLMCore, LLMProvider

st.set_page_config(layout="wide", page_title="Creative Classroom", page_icon="🎨")

llm_core = LLMCore()
provider = LLMProvider.CLAUDE
orchestrator = ActivityOrchestrator(llm_core, provider)

# ── Styling ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Fraunces:ital,wght@0,400;0,700;1,400&display=swap');

/* ── Root Variables ── */
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

/* ── Base ── */
.stApp {
    background-color: var(--cream) !important;
    font-family: 'Nunito', sans-serif !important;
}

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif !important;
    color: var(--text) !important;
}

/* ── Hide default Streamlit header decoration ── */
header[data-testid="stHeader"] {
    background: transparent !important;
}

/* ── Page title ── */
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

/* ── Sidebar ── */
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

/* Sidebar header decoration */
[data-testid="stSidebar"] > div:first-child::before {
    content: "🎨";
    display: block;
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

/* ── PRIMARY BUTTONS ── */
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

/* ── SECONDARY BUTTONS ── */
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

/* Disabled secondary */
div.stButton > button[kind="secondary"]:disabled {
    background: var(--yellow) !important;
    border-color: var(--yellow) !important;
    color: var(--dark) !important;
    opacity: 1 !important;
    font-weight: 800 !important;
}

/* ── CARDS ── */
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

/* ── TEXT INPUTS ── */
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

/* ── SELECT BOX ── */
[data-baseweb="select"] > div {
    border: 2px solid #E8E0D8 !important;
    border-radius: 12px !important;
    background: white !important;
}

/* ── INFO / WARNING / SUCCESS / ERROR boxes ── */
.stAlert {
    border-radius: 14px !important;
    border: none !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 600 !important;
}

div[data-testid="stAlert"][kind="info"] {
    background: #EEF4FF !important;
    color: #2563EB !important;
}

div[data-testid="stAlert"][kind="success"] {
    background: #ECFDF5 !important;
    color: #059669 !important;
}

div[data-testid="stAlert"][kind="warning"] {
    background: #FFFBEB !important;
    color: #D97706 !important;
}

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    background: #FFF3E8 !important;
    border-radius: 12px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    color: var(--dark) !important;
}

/* ── SPINNER ── */
.stSpinner > div {
    border-top-color: var(--coral) !important;
}

/* ── SUBHEADER / CAPTION ── */
.stMarkdown p {
    font-family: 'Nunito', sans-serif !important;
    line-height: 1.7 !important;
}

/* ── History column sticky ── */
.history-column {
    position: sticky;
    top: 1rem;
}

/* ── Decorative pill tags ── */
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

/* ── Page hero banner (top of main col) ── */
.hero-banner {
    background: linear-gradient(135deg, #1A1A2E 0%, #2D2D5E 100%);
    border-radius: 24px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    color: white;
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '';
    position: absolute;
    top: -30px; right: -30px;
    width: 140px; height: 140px;
    background: var(--yellow);
    border-radius: 50%;
    opacity: 0.15;
}

.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 40px;
    width: 100px; height: 100px;
    background: var(--coral);
    border-radius: 50%;
    opacity: 0.12;
}

.hero-banner h2 {
    color: white !important;
    font-size: 1.7rem !important;
    margin: 0 0 0.5rem 0 !important;
}

.hero-banner p {
    color: rgba(255,255,255,0.7) !important;
    margin: 0 !important;
    font-size: 0.95rem !important;
}

/* ── Idea card accent bar ── */
.idea-card-accent {
    width: 40px;
    height: 5px;
    border-radius: 10px;
    background: var(--coral);
    margin-bottom: 1rem;
}

/* ── Stat chips inside cards ── */
.stat-chip {
    background: var(--cream);
    border: 1.5px solid #F0EBE3;
    border-radius: 12px;
    padding: 0.5rem 0.8rem;
    font-size: 0.85rem;
    font-weight: 700;
}

/* ── Dividers ── */
hr {
    border: none !important;
    border-top: 2px dashed #F0EBE3 !important;
    margin: 1rem 0 !important;
}

/* ── History item highlight ── */
.history-current {
    background: #FFF8F0 !important;
    border-color: var(--yellow) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--cream); }
::-webkit-scrollbar-thumb { background: #D9CFC7; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--coral); }
</style>
""", unsafe_allow_html=True)

# ── Page title with decorative subtitle ──────────────────────────────────────
st.markdown("""
<div style="display:flex; align-items:center; gap:1rem; margin-bottom: 0.25rem;">
    <span style="font-size:2.4rem;">🎨</span>
    <div>
        <h1 style="margin:0; line-height:1.1;">Creative Classroom</h1>
        <p style="margin:0; color:#8A8A9A; font-size:0.95rem; font-family:'Nunito',sans-serif;">
            AI-powered activity ideas for curious learners
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
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
    st.markdown("## Activity Settings")
    st.markdown("---")

    topic = st.text_input("📚 Topic", placeholder="e.g. Water Cycle")
    age = st.selectbox(
        "👶 Age Group",
        ["5-7", "8-10", "11-12", "12-14", "15-17"]
    )
    goal = st.text_input(
        "🎯 Goal",
        placeholder="e.g. discussion, experiment...",
        help="What should students do?"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("✨ Generate Ideas", type="primary", use_container_width=True):
        if not topic.strip():
            st.warning("Please enter a topic.")
        elif not goal.strip():
            st.warning("Please enter a goal.")
        else:
            with st.spinner("Brainstorming ideas..."):
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
        st.markdown(
            '<p style="font-size:0.8rem; color:rgba(255,255,255,0.45); text-align:center; margin-top:0.5rem;">'
            'Click Generate again for fresh ideas</p>',
            unsafe_allow_html=True
        )

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:0.75rem; color:rgba(255,255,255,0.3); text-align:center;">'
        'Powered by Claude AI 🤖</p>',
        unsafe_allow_html=True
    )

# ── Layout ────────────────────────────────────────────────────────────────────
main_col, spacer, history_col = st.columns([4, 0.3, 1.8])

# ── Helper: Idea Card ─────────────────────────────────────────────────────────
ACCENT_COLORS = ["#FF6B6B", "#4D96FF", "#6BCB77", "#FFD93D", "#C77DFF"]

def render_idea_card(idea, index):
    title   = idea.get("title", f"Idea {index + 1}")
    why     = idea.get("why_it_works", "")
    time    = idea.get("time", "")
    materials = idea.get("materials", [])
    steps   = idea.get("steps", [])
    accent  = ACCENT_COLORS[index % len(ACCENT_COLORS)]

    # Spacer between cards
    if index > 0:
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        # Top row: accent bar + idea number badge
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
                f'<p style="color:#555; font-size:0.9rem; margin-bottom:1rem;">💡 {why}</p>',
                unsafe_allow_html=True
            )

        # Stats row
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f'<div style="background:#FFF8F0;border:1.5px solid #F0EBE3;border-radius:12px;padding:0.6rem 0.8rem;">'
                f'<div style="font-size:0.7rem;font-weight:800;color:#999999;text-transform:uppercase;letter-spacing:0.5px;">⏱ Time</div>'
                f'<div style="font-weight:700;font-size:0.95rem;margin-top:2px;color:#2D2D2D;">{time or "—"}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        with col2:
            mat_count = len(materials) if materials else 0
            st.markdown(
                f'<div style="background:#FFF8F0;border:1.5px solid #F0EBE3;border-radius:12px;padding:0.6rem 0.8rem;">'
                f'<div style="font-size:0.7rem;font-weight:800;color:#999999;text-transform:uppercase;letter-spacing:0.5px;">🧰 Materials</div>'
                f'<div style="font-weight:700;font-size:0.95rem;margin-top:2px;color:#2D2D2D;">{mat_count} items</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        with col3:
            step_count = len(steps) if steps else 0
            st.markdown(
                f'<div style="background:#FFF8F0;border:1.5px solid #F0EBE3;border-radius:12px;padding:0.6rem 0.8rem;">'
                f'<div style="font-size:0.7rem;font-weight:800;color:#999999;text-transform:uppercase;letter-spacing:0.5px;">📋 Steps</div>'
                f'<div style="font-weight:700;font-size:0.95rem;margin-top:2px;color:#2D2D2D;">{step_count} steps</div>'
                f'</div>',
                unsafe_allow_html=True
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

        if st.button("✅ Select & Refine", key=f"idea_{index}", type="primary"):
            st.session_state.selected = idea
            st.session_state.refine_triggered = True
            st.session_state.refine_result = None
            st.rerun()

# ── Main Content ──────────────────────────────────────────────────────────────
with main_col:
    if not st.session_state.ideas:
        st.markdown("""
        <div style="margin-bottom:1.5rem;">
            <h2 style="font-size:1.5rem;margin:0 0 0.3rem 0;">Ready to inspire your students? 🎨</h2>
            <p style="color:#8A8A9A;font-size:0.9rem;margin:0;">
                Enter a topic, age group and goal in the sidebar — then hit Generate Ideas.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Feature highlights
        c1, c2, c3 = st.columns(3)
        for col, emoji, label, desc in [
            (c1, "🧠", "AI-Powered", "Ideas generated by Claude, tailored to your age group"),
            (c2, "🛡️", "Safety First", "Every activity is audited for classroom safety"),
            (c3, "⚡", "Instant", "Fresh ideas in seconds, refine with one click"),
        ]:
            with col:
                st.markdown(
                    f'<div style="background:white;border:2px solid #F0EBE3;border-radius:20px;padding:1.2rem;text-align:center;">'
                    f'<div style="font-size:2rem;">{emoji}</div>'
                    f'<div style="font-weight:800;margin:0.5rem 0 0.3rem;color:#2D2D2D;">{label}</div>'
                    f'<div style="font-size:0.82rem;color:#8A8A9A;">{desc}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
    else:
        ideas = st.session_state.ideas
        selected = st.session_state.selected
        refine_result = st.session_state.refine_result

        # ── No Selected Idea ──────────────────────────────────────────────
        if not selected:
            st.markdown("""
            <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:1.5rem;">
                <div style="width:6px;height:36px;background:#FF6B6B;border-radius:10px;"></div>
                <h2 style="margin:0;font-size:1.5rem;">Choose an Activity</h2>
            </div>
            """, unsafe_allow_html=True)
            for i, idea in enumerate(ideas):
                render_idea_card(idea, i)

        # ── Selected Idea ─────────────────────────────────────────────────
        else:
            # Other ideas switcher
            other_ideas = [idea for idea in ideas if idea != selected]
            if other_ideas:
                with st.expander("🔄 Switch to another idea"):
                    cols = st.columns(len(other_ideas))
                    for i, idea in enumerate(other_ideas):
                        with cols[i]:
                            title = idea.get("title", f"Idea {i + 1}")
                            st.markdown(f"**{title}**")
                            if st.button("Switch →", key=f"switch_{i}", use_container_width=True):
                                st.session_state.selected = idea
                                st.session_state.refine_triggered = True
                                st.session_state.refine_result = None
                                st.rerun()

            # ── Run Refinement ────────────────────────────────────────────
            if st.session_state.refine_triggered:
                st.session_state.refine_triggered = False
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:1.5rem;">'
                    f'<div style="width:6px;height:36px;background:#4D96FF;border-radius:10px;"></div>'
                    f'<h2 style="margin:0;font-size:1.5rem;">Refining: <em>{selected.get("title")}</em></h2>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                with st.spinner("✨ Adapting and checking safety..."):
                    result = orchestrator.run_refine(selected, st.session_state.age)
                    st.session_state.refine_result = result
                    refine_result = result

            # ── Show Results ──────────────────────────────────────────────
            if refine_result:
                status = refine_result.get("status")

                if status == "ok":
                    st.success("✨ Refinement Complete — your activity is ready!")
                    final_plan = refine_result.get("final_plan", {})

                    with st.container(border=True):
                        st.markdown(
                            f'<div style="width:40px;height:5px;border-radius:10px;background:#6BCB77;margin-bottom:0.75rem;"></div>',
                            unsafe_allow_html=True
                        )
                        st.markdown(f"### 🎯 {final_plan.get('title', selected.get('title'))}")
                        st.markdown(
                            f'<p style="font-size:0.95rem;color:#444;line-height:1.7;">'
                            f'{final_plan.get("adapted_description", "No description returned.")}'
                            f'</p>',
                            unsafe_allow_html=True
                        )

                        if "steps" in final_plan:
                            st.markdown("**📋 Steps:**")
                            for j, step in enumerate(final_plan["steps"], 1):
                                st.markdown(
                                    f'<div style="display:flex;gap:0.75rem;align-items:flex-start;margin-bottom:0.5rem;">'
                                    f'<div style="min-width:26px;height:26px;background:#FF6B6B;color:white;border-radius:50%;'
                                    f'display:flex;align-items:center;justify-content:center;font-weight:800;font-size:0.8rem;">{j}</div>'
                                    f'<div style="padding-top:3px;">{step}</div>'
                                    f'</div>',
                                    unsafe_allow_html=True
                                )

                    # Safety Audit
                    with st.expander("🛡️ Safety Audit", expanded=True):
                        safety_data = refine_result.get("safety", {})
                        if isinstance(safety_data, dict):
                            safety_status = safety_data.get("status", "Unknown").upper()
                            if safety_status == "SAFE":
                                st.markdown(
                                    '<div style="background:#ECFDF5;border-radius:12px;padding:0.8rem 1rem;'
                                    'font-weight:800;color:#059669;font-size:1rem;">✅ Status: SAFE</div>',
                                    unsafe_allow_html=True
                                )
                            else:
                                st.markdown(
                                    f'<div style="background:#FFFBEB;border-radius:12px;padding:0.8rem 1rem;'
                                    f'font-weight:800;color:#D97706;font-size:1rem;">⚠️ Status: {safety_status}</div>',
                                    unsafe_allow_html=True
                                )

                            st.markdown("<br>", unsafe_allow_html=True)
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(
                                    f'<div style="background:#FFF8F0;border-radius:12px;padding:0.7rem 1rem;">'
                                    f'<div style="font-size:0.75rem;color:#aaa;text-transform:uppercase;font-weight:700;">Severity</div>'
                                    f'<div style="font-weight:800;">{safety_data.get("severity", "none").title()}</div>'
                                    f'</div>',
                                    unsafe_allow_html=True
                                )
                            with col2:
                                safe = safety_data.get("safe_to_use", False)
                                st.markdown(
                                    f'<div style="background:#FFF8F0;border-radius:12px;padding:0.7rem 1rem;">'
                                    f'<div style="font-size:0.75rem;color:#aaa;text-transform:uppercase;font-weight:700;">Safe to Use</div>'
                                    f'<div style="font-weight:800;">{"✅ Yes" if safe else "❌ No"}</div>'
                                    f'</div>',
                                    unsafe_allow_html=True
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

                elif status == "rejected":
                    st.error("⛔ This activity was flagged as unsafe and could not be resolved.")
                    st.write(refine_result.get("assessment"))
                elif status == "unresolved":
                    st.warning("⚠️ Could not produce a safe version after multiple attempts.")
                    st.write(refine_result.get("last_safety"))
                else:
                    st.error(f"Pipeline error at stage: {refine_result}")
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
            '<div style="font-size:2rem;margin-bottom:0.5rem;">🌱</div>'
            '<div style="color:#aaa;font-size:0.85rem;font-weight:600;">No ideas yet.<br>Generate some to get started!</div>'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        for idx, (title, idea) in enumerate(reversed(list(history.items()))):
            is_selected = st.session_state.selected == idea
            accent = ACCENT_COLORS[idx % len(ACCENT_COLORS)]

            with st.container(border=True):
                st.markdown(
                    f'<div style="width:30px;height:4px;border-radius:10px;background:{accent};margin-bottom:0.6rem;"></div>'
                    f'<div style="font-weight:800;font-size:0.88rem;margin-bottom:0.5rem;color:#2D2D2D;line-height:1.3;">💡 {title}</div>',
                    unsafe_allow_html=True
                )
                if is_selected:
                    st.markdown(
                        '<div style="background:#FFF9E0;border-radius:8px;padding:0.3rem 0.6rem;'
                        'font-size:0.75rem;font-weight:700;color:#B45309;margin-bottom:0.5rem;display:inline-block;">'
                        '⭐ Currently viewing</div>',
                        unsafe_allow_html=True
                    )
                if st.button(
                    "✓ Active" if is_selected else "Choose →",
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


# import streamlit as st
# from agentcore.orchestrator import ActivityOrchestrator
# from agentcore.llm_providers import LLMCore, LLMProvider

# llm_core = LLMCore()
# provider = LLMProvider.CLAUDE 
# orchestrator = ActivityOrchestrator(llm_core, provider)

# # ── Styling ───────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>

# .stApp {
#     background-color: #0e1117;
# }

# label, .stRadio label {
#     color: white !important;
# }

# .history-column {
#     position: sticky;
#     top: 1rem;
# }
            
# /* 🟣 PRIMARY BUTTONS (Purple Gradient) */
# div.stButton > button[kind="primary"] {
#     background: linear-gradient(45deg, #624af2, #8f44fd) !important;
#     color: white !important;
#     border-radius: 8px !important;
#     border: none !important;
#     padding: 0.5rem 1rem !important;
#     transition: transform 0.2s !important;
# }

# div.stButton > button[kind="primary"]:hover {
#     transform: scale(1.02) !important;
# }

# div.stButton > button[kind="secondary"] {
#     background: #1f2937 !important;
#     border: 1px solid #374151 !important;
#     color: white !important;
#     border-radius: 8px !important;
#     padding: 0.5rem 1rem !important;
#     transition: transform 0.2s !important;
# }

# div.stButton > button[kind="secondary"]:hover {
#     background: #2b3545 !important;
#     transform: scale(1.02) !important;
# }
# </style>
# """, unsafe_allow_html=True)

# st.title("Creative Classroom 🚀")

# # ── Session State ─────────────────────────────────────────────────────────────
# defaults = {
#     "ideas": [],
#     "history": {},
#     "selected": None,
#     "refine_triggered": False,
#     "refine_result": None,
#     "age": None
# }

# st.set_page_config(layout="wide")

# for key, value in defaults.items():
#     if key not in st.session_state:
#         st.session_state[key] = value

# if not isinstance(st.session_state.history, dict):
#     st.session_state.history = {}

# # ── Sidebar ───────────────────────────────────────────────────────────────────
# with st.sidebar:
#     st.header("Activity Settings")
#     topic = st.text_input("Topic", placeholder="e.g. Water Cycle")
#     age = st.selectbox(
#         "Age Group",
#         ["5-7", "8-10", "11-12", "12-14", "15-17"]
#     )

#     goal = st.text_input(
#         "Goal",
#         placeholder="e.g. discussion, experiment, roleplay...",
#         help="What should students do?"
#     )

#     if st.button("Generate Ideas", type="primary"):
#         if not topic.strip():
#             st.warning("Please enter a topic.")
#         elif not goal.strip():
#             st.warning("Please enter a goal.")
#         else:
#             with st.spinner("Brainstorming..."):
#                 new_ideas = orchestrator.run_generate(topic, age, goal)
#                 st.session_state.ideas = new_ideas
#                 st.session_state.age = age
#                 st.session_state.selected = None
#                 st.session_state.refine_triggered = False
#                 st.session_state.refine_result = None

#                 for idea in new_ideas:
#                     title = idea.get("title", "Untitled")
#                     st.session_state.history[title] = idea

#     if st.session_state.ideas:
#         st.caption("Not happy with these? Click Generate again for fresh ideas.")

# # ── Layout ────────────────────────────────────────────────────────────────────

# # main_col, history_col = st.columns([4, 3], gap="large")
# main_col, spacer, history_col = st.columns([4, 1, 1.8])

# # ── Helper ────────────────────────────────────────────────────────────────────
# def render_idea_card(idea, index):
#     title = idea.get("title", f"Idea {index + 1}")
#     why = idea.get("why_it_works", "")
#     time = idea.get("time", "")
#     materials = idea.get("materials", [])
#     steps = idea.get("steps", [])

#     with st.container(border=True):
#         st.markdown(f"### {title}")

#         if why:
#             st.markdown(f"💡 **Why it works:** {why}")

#         st.markdown("&nbsp;", unsafe_allow_html=True)

#         col1, col2, col3 = st.columns(3)

#         with col1:
#             st.markdown("⏱ **Time**")
#             st.markdown(time or "—")

#         with col2:
#             st.markdown("🧰 **Needed**")
#             st.markdown("\n".join(f"- {m}" for m in materials) if materials else "—")

#         with col3:
#             st.markdown("📋 **Steps**")
#             st.markdown(f"{len(steps)} steps" if steps else "—")

#         st.markdown("---")

#         if st.button("✅ Select & Refine", key=f"idea_{index}", type="primary"):

#             st.session_state.selected = idea
#             st.session_state.refine_triggered = True
#             st.session_state.refine_result = None

#             st.rerun()

# # ── Main Content ──────────────────────────────────────────────────────────────
# with main_col:

#     if not st.session_state.ideas:
#         st.info("👈 Enter a topic in the sidebar and click *Generate Ideas*")

#     else:
#         ideas = st.session_state.ideas
#         selected = st.session_state.selected
#         refine_result = st.session_state.refine_result

#         # ── No Selected Idea ────────────────────────────────────────────────
#         if not selected:
#             st.subheader("💡 Choose an Idea")

#             for i, idea in enumerate(ideas):
#                 render_idea_card(idea, i)

#         # ── Selected Idea ───────────────────────────────────────────────────
#         else:

#             other_ideas = [idea for idea in ideas if idea != selected]

#             if other_ideas:
#                 with st.expander("💡 View Other Options"):

#                     cols = st.columns(len(other_ideas))

#                     for i, idea in enumerate(other_ideas):
#                         with cols[i]:

#                             title = idea.get("title", f"Idea {i + 1}")
#                             st.markdown(f"**{title}**")

#                             if st.button("🔄 Switch", key=f"switch_{i}", use_container_width=True):

#                                 st.session_state.selected = idea
#                                 st.session_state.refine_triggered = True
#                                 st.session_state.refine_result = None

#                                 st.rerun()

#             # ── Run Refinement ─────────────────────────────────────────────
#             if st.session_state.refine_triggered:
#                 st.session_state.refine_triggered = False
#                 st.subheader(f"🔍 Refining: *{selected.get('title')}*")

#                 with st.spinner("Adapting and checking safety..."):
#                     result = orchestrator.run_refine(selected, st.session_state.age)
#                     st.session_state.refine_result = result
#                     refine_result = result

#             # ── Show Results ───────────────────────────────────────────────
#             if refine_result:
#                 status = refine_result.get("status")
#                 if status == "ok":
#                     st.success("✨ Refinement Complete!")
#                     final_plan = refine_result.get("final_plan", {})

#                     with st.container(border=True):
#                         st.markdown(f"### 🎯 {final_plan.get('title', selected.get('title'))}")
#                         st.markdown(
#                             final_plan.get(
#                                 "adapted_description",
#                                 "No description returned."
#                             )
#                         )

#                         if "steps" in final_plan:
#                             st.markdown("**Steps:**")
#                             for step in final_plan["steps"]:
#                                 st.markdown(f"- {step}")

#                     with st.expander("🛡️ Safety Audit", expanded=True):
#                         safety_data = refine_result.get("safety", {})

#                         if isinstance(safety_data, dict):
#                             safety_status = safety_data.get("status", "Unknown").upper()

#                             if safety_status == "SAFE":
#                                 st.success(f"✅ Status: {safety_status}")
#                             else:
#                                 st.warning(f"⚠️ Status: {safety_status}")

#                             col1, col2 = st.columns(2)
#                             with col1:
#                                 st.markdown(
#                                     f"**Severity:** {safety_data.get('severity', 'none').title()}"
#                                 )

#                             with col2:
#                                 st.markdown(
#                                     f"**Safe to Use:** {'Yes' if safety_data.get('safe_to_use', False) else 'No'}"
#                                 )

#                             st.divider()
#                             for key in ["risks", "suggestions"]:
#                                 value = safety_data.get(key)
#                                 st.markdown(f"#### {key.title()}")
#                                 if not value or value == "none":
#                                     st.write(f"No {key} identified.")
#                                     continue

#                                 if isinstance(value, list):
#                                     for item in value:
#                                         if isinstance(item, dict):
#                                             category = item.get("category") or item.get("addresses_risk")
#                                             content = item.get("description") or item.get("change")

#                                             if content:

#                                                 if category and category.lower() != "general":
#                                                     label = category.replace("_", " ").title()
#                                                     st.markdown(f"**{label}**: {content}")
#                                                 else:
#                                                     st.markdown(f"- {content}")

#                                         else:
#                                             st.markdown(f"- {item}")

#                                 else:
#                                     st.write(value)

#                         else:
#                             st.info("No structured safety data available.")
#                             st.write(safety_data)

#                 elif status == "rejected":
#                     st.error("⛔ This activity was flagged as unsafe and could not be resolved.")
#                     st.write(refine_result.get("assessment"))

#                 elif status == "unresolved":
#                     st.warning("⚠️ Could not produce a safe version after multiple attempts.")
#                     st.write(refine_result.get("last_safety"))

#                 else:
#                     st.error(f"Pipeline error at stage: {refine_result}")
#                     st.write(refine_result.get("detail"))

# # ── History ───────────────────────────────────────────────────────────────────

# with history_col:
#     st.markdown('<div class="history-column">', unsafe_allow_html=True)
#     st.markdown('<h2 style="font-size: 24px;">Previous Ideas</h2>', unsafe_allow_html=True)
#     history = st.session_state.history
    
#     if not history:
#         st.markdown('<p style="font-size: 14px; color: gray;">No ideas yet.</p>', unsafe_allow_html=True)
#     else:
#         for idx, (title, idea) in enumerate(reversed(list(history.items()))):
#             selected = st.session_state.selected == idea
#             with st.container(border=True):
#                 st.markdown(f'<h3 style="font-size: 18px;">💡 {title}</h3>', unsafe_allow_html=True)
#                 if selected:
#                     st.markdown('<p style="font-size: 12px; color: gray;">Currently viewing</p>', unsafe_allow_html=True)
                
#                 st.markdown('<div class="history-button">', unsafe_allow_html=True)

#                 if st.button(
#                     "Current" if selected else "Choose",
#                     key=f"history_{idx}",
#                     use_container_width=True,
#                     disabled=selected, 
#                     type="secondary"
#                 ):
#                     st.session_state.selected = idea
#                     st.session_state.refine_triggered = True
#                     st.session_state.refine_result = None
#                     st.rerun()
#                 st.markdown('</div>', unsafe_allow_html=True)
#     st.markdown("</div>", unsafe_allow_html=True)