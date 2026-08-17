import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# =========================================================
# LEARNARC — Your next, made clear.
# =========================================================

st.set_page_config(
    page_title="LearnArc — Your Next, Made Clear",
    page_icon="◌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# SESSION STATE
# =========================================================

DEFAULTS = {
    "started": False,
    "profile_done": False,
    "assessment_done": False,
    "profile": {},
    "skill_values": {},
    "show_course_details": False,
    "selected_course_id": None,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


def go_back_to_home():
    st.session_state.started = False
    st.session_state.profile_done = False
    st.session_state.assessment_done = False
    st.session_state.profile = {}
    st.session_state.skill_values = {}


def go_back_to_profile():
    st.session_state.profile_done = False
    st.session_state.assessment_done = False


def go_back_to_assessment():
    st.session_state.assessment_done = False


# =========================================================
# DATA
# =========================================================

try:
    courses = pd.read_csv("data/Courses.csv")
except FileNotFoundError:
    try:
        courses = pd.read_csv("data/courses.csv")
    except FileNotFoundError:
        st.error("Courses CSV not found. Put Courses.csv inside the data folder.")
        st.stop()

FEATURE_COLUMNS = [
    "python",
    "java",
    "javascript",
    "web",
    "react",
    "backend",
    "nodejs",
    "spring_boot",
    "dsa",
    "oop",
    "sql",
    "database",
    "system_design",
    "ai",
    "ml",
    "deep_learning",
    "nlp",
    "computer_vision",
    "data_science",
    "statistics",
    "data_engineering",
    "cloud",
    "devops",
    "docker",
    "linux",
    "cybersecurity",
    "testing",
    "git",
]

SKILL_LABELS = [
    ("Python", "python"),
    ("Java", "java"),
    ("JavaScript", "javascript"),
    ("Web Development", "web"),
    ("React", "react"),
    ("Backend Development", "backend"),
    ("Node.js", "nodejs"),
    ("Spring Boot", "spring_boot"),
    ("Data Structures & Algorithms", "dsa"),
    ("Object Oriented Programming", "oop"),
    ("SQL", "sql"),
    ("Database", "database"),
    ("System Design", "system_design"),
    ("Artificial Intelligence", "ai"),
    ("Machine Learning", "ml"),
    ("Deep Learning", "deep_learning"),
    ("Natural Language Processing", "nlp"),
    ("Computer Vision", "computer_vision"),
    ("Data Science", "data_science"),
    ("Statistics", "statistics"),
    ("Data Engineering", "data_engineering"),
    ("Cloud", "cloud"),
    ("DevOps", "devops"),
    ("Docker", "docker"),
    ("Linux", "linux"),
    ("Cybersecurity", "cybersecurity"),
    ("Software Testing", "testing"),
    ("Git & GitHub", "git"),
]

SKILL_DISPLAY = dict(SKILL_LABELS)

# Make sure every recommendation feature exists.
for column in FEATURE_COLUMNS:
    if column not in courses.columns:
        courses[column] = 0

# The recommendation logic now lives in recommender.py so the
# Streamlit UI and the standalone recommender use the same engine.
try:
    from recommender import (
        recommend_courses,
        get_course_reason,
        build_learning_arc,
        build_precise_learning_path,
        get_path_summary,
    )
except ImportError as exc:
    st.error(
        "Could not load recommender.py. "
        "Make sure recommender.py is in the same folder as app.py."
    )
    st.exception(exc)
    st.stop()

# =========================================================
# DESIGN
# =========================================================

st.html("""
<style>
.stApp {
    background:#F7F6F0;
    color:#111318;
}

.block-container {
    max-width:1280px;
    padding:24px 48px 90px;
}

#MainMenu, footer, [data-testid="stHeader"] {
    visibility:hidden;
}

.nav {
    height:52px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    margin-bottom:30px;
}

.brand {
    display:flex;
    align-items:center;
    gap:9px;
}

.brand-mark {
    width:30px;
    height:30px;
    position:relative;
}

.brand-mark:before {
    content:"";
    position:absolute;
    width:21px;
    height:21px;
    border:2px solid #315CFF;
    border-left-color:transparent;
    border-bottom-color:transparent;
    border-radius:50%;
    transform:rotate(-35deg);
    top:2px;
    left:1px;
}

.brand-mark:after {
    content:"";
    position:absolute;
    width:6px;
    height:6px;
    background:#C9F36A;
    border-radius:50%;
    right:0;
    top:4px;
}

.brand-name {
    font-size:21px;
    font-weight:850;
    letter-spacing:-1px;
}

.brand-name span {
    color:#315CFF;
}

.nav-tag {
    color:#737B89;
    font-size:12px;
}

.hero {
    position:relative;
    min-height:470px;
    overflow:hidden;
    border-radius:30px;
    background:#111827;
    color:white;
    padding:58px 64px;
    display:flex;
    align-items:center;
}

.hero-copy {
    position:relative;
    z-index:5;
    max-width:570px;
}

.eyebrow {
    color:#C9F36A;
    font-size:11px;
    font-weight:800;
    letter-spacing:2.1px;
    margin-bottom:21px;
}

.hero-title {
    margin:0;
    font-size:clamp(55px, 6vw, 76px);
    line-height:.92;
    letter-spacing:-5px;
    font-weight:850;
}

.hero-title span {
    color:#C9F36A;
}

.hero-description {
    max-width:500px;
    margin-top:24px;
    color:#AEB6C5;
    font-size:16px;
    line-height:1.65;
}

.hero-note {
    margin-top:18px;
    color:#68748A;
    font-size:12px;
}

.arc-graphic {
    position:absolute;
    right:10px;
    top:0;
    width:52%;
    height:100%;
}

.arc-main {
    position:absolute;
    width:440px;
    height:325px;
    right:85px;
    top:72px;
    border-top:2px solid #315CFF;
    border-right:2px solid #315CFF;
    border-radius:0 330px 0 0;
    transform:rotate(10deg);
}

.arc-inner {
    position:absolute;
    width:335px;
    height:245px;
    right:140px;
    top:130px;
    border-top:1px solid rgba(201,243,106,.45);
    border-right:1px solid rgba(201,243,106,.45);
    border-radius:0 250px 0 0;
    transform:rotate(10deg);
}

.arc-node {
    position:absolute;
    width:12px;
    height:12px;
    border-radius:50%;
}

.node-assess {
    background:#C9F36A;
    right:385px;
    top:108px;
    box-shadow:0 0 0 7px rgba(201,243,106,.08);
}

.node-recommend {
    background:#315CFF;
    right:95px;
    top:275px;
    box-shadow:0 0 0 7px rgba(49,92,255,.10);
}

.node-connect {
    background:#C9F36A;
    right:220px;
    bottom:74px;
    box-shadow:0 0 0 7px rgba(201,243,106,.08);
}

.arc-label {
    position:absolute;
    color:#7C879A;
    font-size:10px;
    font-weight:600;
    letter-spacing:1.4px;
    text-transform:uppercase;
}

.label-assess { right:408px; top:88px; }
.label-recommend { right:32px; top:294px; }
.label-connect { right:201px; bottom:49px; }

div.stButton > button {
    background:#C9F36A !important;
    color:#111318 !important;
    border:none !important;
    border-radius:10px !important;
    min-height:46px !important;
    padding:0 22px !important;
    font-size:14px !important;
    font-weight:800 !important;
    transition:.2s ease !important;
}

div.stButton > button:hover {
    background:#D8FF83 !important;
    transform:translateY(-1px);
}

.hero-cta {
    margin-top:-65px;
    margin-left:64px;
    position:relative;
    z-index:20;
    margin-bottom:45px;
}

.story {
    display:grid;
    grid-template-columns:repeat(3,1fr);
    border-top:1px solid #DDDCD5;
    border-bottom:1px solid #DDDCD5;
}

.story-item {
    padding:22px 25px 22px 0;
}

.story-item + .story-item {
    border-left:1px solid #DDDCD5;
    padding-left:25px;
}

.story-number,
.section-number {
    color:#315CFF;
    font-size:10px;
    font-weight:800;
    letter-spacing:1.5px;
}

.story-title {
    margin-top:6px;
    font-size:16px;
    font-weight:800;
}

.story-text {
    margin-top:5px;
    color:#737B89;
    font-size:12px;
    line-height:1.5;
}

.profile-box {
    margin-top:65px;
    padding:48px;
    border-radius:24px;
    background:white;
    border:1px solid #E4E3DC;
}

.section-title {
    font-size:42px;
    line-height:1;
    font-weight:850;
    letter-spacing:-2px;
    margin-top:9px;
}

.section-description {
    color:#737B89;
    margin-top:12px;
}

.assessment-box {
    margin-top:50px;
    padding:48px;
    border-radius:24px;
    background:#111827;
    color:white;
}

.assessment-box .section-number {
    color:#C9F36A;
}

.assessment-title {
    font-size:42px;
    font-weight:850;
    letter-spacing:-2px;
    margin-top:8px;
}

.assessment-description {
    color:#AEB6C5;
    margin-top:12px;
    margin-bottom:30px;
}

[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stMultiSelect"] label,
[data-testid="stSlider"] label,
[data-testid="stSlider"] label p,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p {
    color:#111318 !important;
    opacity:1 !important;
    font-weight:700 !important;
}

[data-testid="stMetric"] {
    padding:20px 28px !important;
    border:1px solid #E2E1DA !important;
    border-radius:16px !important;
    background:#FFFFFF !important;
}

[data-testid="stMetricLabel"] {
    color:#737B89 !important;
    font-size:13px !important;
}

[data-testid="stMetricValue"] {
    color:#111318 !important;
    font-size:30px !important;
    font-weight:750 !important;
}

.course-card {
    background:#FFFFFF;
    border:1px solid #E2E1DA;
    border-radius:22px;
    padding:28px;
    margin-bottom:8px;
}

.match-pill {
    background:#EAF7C8;
    color:#315CFF;
    border-radius:999px;
    padding:10px 15px;
    font-size:14px;
    font-weight:850;
    white-space:nowrap;
}


/* ---------- UI POLISH ---------- */

.profile-box,
.assessment-box {
    box-shadow:0 12px 35px rgba(17,24,39,.045);
}

.profile-box {
    margin-top:52px;
}

.assessment-box {
    margin-top:42px;
}

.skill-grid {
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:12px;
    margin-top:18px;
}

.skill-mini {
    background:#FFFFFF;
    border:1px solid #E2E1DA;
    border-radius:15px;
    padding:16px;
}

.skill-mini-name {
    color:#111318;
    font-size:13px;
    font-weight:750;
}

.skill-mini-value {
    color:#315CFF;
    font-size:17px;
    font-weight:850;
    margin-top:7px;
}

.skill-bar {
    height:5px;
    border-radius:99px;
    background:#ECEDE8;
    margin-top:10px;
    overflow:hidden;
}

.skill-bar > div {
    height:100%;
    border-radius:99px;
    background:#C9F36A;
}

.skill-category {
    margin-top:24px;
    margin-bottom:8px;
    color:#315CFF;
    font-size:10px;
    font-weight:850;
    letter-spacing:1.6px;
    text-transform:uppercase;
}

.gap-card {
    transition:transform .18s ease, box-shadow .18s ease;
}

.gap-card:hover,
.course-card:hover {
    transform:translateY(-2px);
    box-shadow:0 12px 28px rgba(17,24,39,.06);
}

.course-card {
    transition:transform .18s ease, box-shadow .18s ease;
    margin-bottom:4px;
}

.course-actions {
    margin-top:16px;
}

[data-testid="stHorizontalBlock"] {
    gap:18px !important;
}

@media (max-width:1050px) {
    .skill-grid {
        grid-template-columns:repeat(3,1fr);
    }
}

@media (max-width:700px) {
    .skill-grid {
        grid-template-columns:repeat(2,1fr);
    }
}

@media (max-width:900px) {
    .block-container { padding:20px; }

    .hero {
        min-height:610px;
        padding:45px 30px;
    }

    .hero-title {
        font-size:55px;
    }

    .arc-graphic {
        opacity:.25;
        right:-100px;
        width:80%;
    }

    .hero-cta {
        margin-left:30px;
    }

    .story {
        grid-template-columns:1fr;
    }

    .story-item + .story-item {
        border-left:none;
        border-top:1px solid #DDDCD5;
        padding-left:0;
    }

    .profile-box,
    .assessment-box {
        padding:30px;
    }
}
</style>
""")

# =========================================================
# NAVBAR
# =========================================================

st.html("""
<div class="nav">
    <div class="brand">
        <div class="brand-mark"></div>
        <div class="brand-name">learn<span>arc</span></div>
    </div>
    <div class="nav-tag">Assess · Recommend · Connect</div>
</div>
""")

# =========================================================
# HERO
# =========================================================

st.html("""
<div class="hero">
    <div class="hero-copy">
        <div class="eyebrow">PERSONALIZED LEARNING INTELLIGENCE</div>

        <div class="hero-title">
            Your next<br>
            starts <span>here.</span>
        </div>

        <div class="hero-description">
            LearnArc understands where you are,
            finds the skills that will move you forward,
            and connects you to the right learning path.
        </div>

        <div class="hero-note">
            Built around your skills, interests & goals.
        </div>
    </div>

    <div class="arc-graphic">
        <div class="arc-main"></div>
        <div class="arc-inner"></div>

        <div class="arc-node node-assess"></div>
        <div class="arc-node node-recommend"></div>
        <div class="arc-node node-connect"></div>

        <div class="arc-label label-assess">Assess</div>
        <div class="arc-label label-recommend">Recommend</div>
        <div class="arc-label label-connect">Connect</div>
    </div>
</div>
""")

# =========================================================
# HERO CTA
# =========================================================

st.markdown('<div class="hero-cta">', unsafe_allow_html=True)

build = st.button(
    "Build my Arc  →",
    key="build_arc",
)

st.markdown("</div>", unsafe_allow_html=True)

if build:
    st.session_state.started = True
    st.rerun()

# =========================================================
# STORY
# =========================================================

if not st.session_state.started:
    st.html("""
    <div class="story">
        <div class="story-item">
            <div class="story-number">01 / ASSESS</div>
            <div class="story-title">Know where you are.</div>
            <div class="story-text">
                Understand your current skills, interests and learning level.
            </div>
        </div>

        <div class="story-item">
            <div class="story-number">02 / RECOMMEND</div>
            <div class="story-title">Find what fits.</div>
            <div class="story-text">
                Discover courses that match your learning profile.
            </div>
        </div>

        <div class="story-item">
            <div class="story-number">03 / CONNECT</div>
            <div class="story-title">See where it leads.</div>
            <div class="story-text">
                Turn recommendations into a focused learning journey.
            </div>
        </div>
    </div>
    """)

# =========================================================
# PROFILE
# =========================================================

if (
    st.session_state.started
    and not st.session_state.profile_done
):
    back_home = st.button(
        "← Back to home",
        key="back_home_from_profile",
    )
    if back_home:
        go_back_to_home()
        st.rerun()

    st.html("""
    <div class="profile-box">
        <div class="section-number">BUILD YOUR PROFILE</div>
        <div class="section-title">Tell us where you are.</div>
        <div class="section-description">
            Your skills, interests and goals help us understand what you should learn next.
        </div>
    </div>
    """)

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input(
            "What should we call you?",
            placeholder="Your name",
            key="name_input",
        )

    with col2:
        level = st.selectbox(
            "Where are you right now?",
            ["Beginner", "Intermediate", "Advanced"],
            key="level_input",
        )

    goal = st.selectbox(
        "What do you want to become?",
        [
            "Software Engineer",
            "AI / ML Engineer",
            "Data Scientist",
            "Data Analyst",
            "Data / BI Analyst",
            "Data Engineer",
            "Backend Developer",
            "Java Backend Developer",
            "Python Backend Developer",
            "Frontend Developer",
            "React Developer",
            "Full Stack Developer",
            "Mobile App Developer",
            "Android Developer",
            "React Native Developer",
            "DevOps Engineer",
            "Cloud Engineer",
            "Cloud Architect",
            "Cybersecurity Engineer",
            "Ethical Hacker",
            "MLOps Engineer",
            "Generative AI Engineer",
            "NLP Engineer",
            "Computer Vision Engineer",
            "QA / Automation Engineer",
            "Database Engineer",
        ],
        key="goal_input",
    )

    interests = st.multiselect(
        "What are you interested in?",
        [
            "Python", "Java", "C++", "Data Structures & Algorithms",
            "Object Oriented Programming",
            "HTML & CSS", "JavaScript", "React",
            "Frontend Development", "Backend Development",
            "Full Stack Development", "REST APIs", "Spring Boot",
            "Node.js", "Microservices", "System Design",
            "Artificial Intelligence", "Machine Learning", "Deep Learning",
            "Natural Language Processing", "Computer Vision",
            "Generative AI", "Large Language Models",
            "Data Science", "Data Analytics", "Statistics", "SQL",
            "Database", "Data Engineering", "Business Intelligence",
            "Cloud Computing", "AWS", "Azure", "Google Cloud",
            "DevOps", "Docker", "Kubernetes", "CI/CD", "Linux",
            "Cybersecurity", "Ethical Hacking", "Network Security",
            "Web Security", "Mobile Development", "Android Development",
            "React Native", "Software Testing", "Test Automation",
            "Git & GitHub",
        ],
        key="interests_input",
        placeholder="Select the topics you want to learn",
    )

    st.write("")

    continue_button = st.button(
        "Continue to assessment  →",
        key="continue_button",
    )

    if continue_button:
        if not name.strip():
            st.warning("Please enter your name.")
        elif not interests:
            st.warning("Please select at least one interest.")
        else:
            st.session_state.profile = {
                "name": name.strip(),
                "level": level,
                "goal": goal,
                "interests": interests,
            }

            st.session_state.profile_done = True
            st.rerun()

# =========================================================
# ASSESSMENT
# =========================================================

if (
    st.session_state.profile_done
    and not st.session_state.assessment_done
):
    profile = st.session_state.profile

    st.html("""
    <div class="assessment-box">
        <div class="section-number">01 / ASSESS</div>
        <div class="assessment-title">Know where you are.</div>
        <div class="assessment-description">
            Rate your confidence in each skill. Be honest —
            LearnArc uses this to identify your learning gaps.
        </div>
    </div>
    """)

    st.write("")

    st.caption(
        f"Profile: {profile['name']} · "
        f"{profile['level']} · "
        f"{profile['goal']}"
    )

    st.write("")

    skill_values = {}

    SKILL_GROUPS = {
        "Programming": [
            ("Python", "python"),
            ("Java", "java"),
            ("JavaScript", "javascript"),
            ("Data Structures & Algorithms", "dsa"),
            ("Object Oriented Programming", "oop"),
            ("Git & GitHub", "git"),
        ],
        "Web & Backend": [
            ("Web Development", "web"),
            ("React", "react"),
            ("Backend Development", "backend"),
            ("Node.js", "nodejs"),
            ("Spring Boot", "spring_boot"),
            ("SQL", "sql"),
            ("Database", "database"),
            ("System Design", "system_design"),
        ],
        "AI & Data": [
            ("Artificial Intelligence", "ai"),
            ("Machine Learning", "ml"),
            ("Deep Learning", "deep_learning"),
            ("Natural Language Processing", "nlp"),
            ("Computer Vision", "computer_vision"),
            ("Data Science", "data_science"),
            ("Statistics", "statistics"),
            ("Data Engineering", "data_engineering"),
        ],
        "Cloud, DevOps & Security": [
            ("Cloud", "cloud"),
            ("DevOps", "devops"),
            ("Docker", "docker"),
            ("Linux", "linux"),
            ("Cybersecurity", "cybersecurity"),
            ("Software Testing", "testing"),
        ],
    }

    st.html("""
    <div style="
        padding:18px 20px;
        border:1px solid #E2E1DA;
        border-radius:16px;
        background:#FFFFFF;
        color:#737B89;
        font-size:13px;
        line-height:1.6;
        margin-bottom:20px;
    ">
        <b style="color:#111318;">How to rate yourself:</b>
        0 = No experience &nbsp;·&nbsp;
        50 = Comfortable &nbsp;·&nbsp;
        100 = Highly confident
    </div>
    """)

    for group_name, group_skills in SKILL_GROUPS.items():

        st.markdown(
            f'<div class="skill-category">{group_name}</div>',
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        for i, (label, key) in enumerate(group_skills):
            target = col1 if i % 2 == 0 else col2

            with target:
                skill_values[key] = st.slider(
                    label,
                    0,
                    100,
                    0,
                    5,
                    key=f"assessment_{key}",
                )

    st.write("")

    map_button = st.button(
        "Map my learning Arc  →",
        key="map_learning_arc",
    )

    if map_button:
        st.session_state.skill_values = skill_values
        st.session_state.assessment_done = True
        st.rerun()

# =========================================================
# RESULTS + RECOMMENDATIONS
# IMPORTANT: EVERYTHING BELOW USES SAVED SESSION STATE.
# This prevents the previous 'skills is not defined' error.
# =========================================================

if st.session_state.assessment_done:

    profile = st.session_state.profile
    skills = st.session_state.skill_values

    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    average_confidence = (
        sum(skills.values()) / len(skills)
        if skills
        else 0
    )

    st.html("""
    <div class="assessment-box">
        <div class="section-number">02 / RECOMMEND</div>
        <div class="assessment-title">Your Arc is taking shape.</div>
        <div class="assessment-description">
            We've understood your learning profile.
            LearnArc can now match your skills, interests
            and goals with the course catalog.
        </div>
    </div>
    """)

    st.write("")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Learning level", profile["level"])

    with c2:
        st.metric("Interests", len(profile["interests"]))

    with c3:
        st.metric(
            "Average confidence",
            f"{average_confidence:.0f}%",
        )

    st.write("")
    st.write("")

    # -----------------------------------------------------
    # SKILL PROFILE
    # -----------------------------------------------------

    st.markdown("## Your skill profile")
    st.write("")

    skill_grid_html = '<div class="skill-grid">'

    for label, key in SKILL_LABELS:
        score = int(skills.get(key, 0))

        skill_grid_html += f"""
        <div class="skill-mini">
            <div class="skill-mini-name">{label}</div>
            <div class="skill-mini-value">{score}%</div>
            <div class="skill-bar">
                <div style="width:{score}%"></div>
            </div>
        </div>
        """

    skill_grid_html += "</div>"

    st.html(skill_grid_html)

    st.write("")
    st.write("")

    # -----------------------------------------------------
    # SKILL GAPS

    # -----------------------------------------------------

    st.markdown("### What needs attention?")
    st.caption(
        "Your lowest-confidence areas are the skills "
        "LearnArc will prioritize."
    )

    sorted_skills = sorted(
        skills.items(),
        key=lambda item: item[1],
    )

    weakest = sorted_skills[:3]

    gap_cols = st.columns(3)

    for i, (key, value) in enumerate(weakest):
        with gap_cols[i]:
            st.html(f"""
            <div style="
                padding:22px;
                border-radius:16px;
                background:#FFFFFF;
                border:1px solid #E4E3DC;
                min-height:120px;
            ">
                <div style="
                    font-size:11px;
                    color:#737B89;
                    font-weight:800;
                    letter-spacing:1.3px;
                ">
                    SKILL GAP
                </div>

                <div style="
                    font-size:18px;
                    font-weight:800;
                    color:#111318;
                    margin-top:10px;
                ">
                    {SKILL_DISPLAY.get(key, key.replace("_", " ").title())}
                </div>

                <div style="
                    margin-top:8px;
                    color:#315CFF;
                    font-weight:750;
                ">
                    {int(value)}% confidence
                </div>
            </div>
            """)

    st.write("")
    st.write("")

    # =====================================================
    # GENERATE RECOMMENDATIONS
    # This MUST be inside assessment_done.
    # =====================================================

    recommendations = recommend_courses(
        skill_values=skills,
        interests=profile["interests"],
        goal=profile["goal"],
        level=profile["level"],
        top_n=5,
    )

    # -----------------------------------------------------
    # RECOMMENDATION HEADER
    # -----------------------------------------------------

    st.html("""
    <div style="
        padding:32px;
        border-radius:20px;
        background:#111827;
        color:white;
        margin-top:20px;
        margin-bottom:25px;
    ">
        <div style="
            color:#C9F36A;
            font-size:11px;
            font-weight:800;
            letter-spacing:1.8px;
        ">
            YOUR NEXT MOVE
        </div>

        <div style="
            font-size:32px;
            font-weight:850;
            letter-spacing:-1.5px;
            margin-top:8px;
        ">
            Courses that fit your next step.
        </div>

        <div style="
            color:#AEB6C5;
            font-size:14px;
            line-height:1.6;
            margin-top:10px;
            max-width:720px;
        ">
            Ranked using your current skills,
            interests, career goal and learning level.
        </div>
    </div>
    """)

    # =====================================================
    # TOP 5 INTERACTIVE COURSE CARDS
    # =====================================================

    for index, (_, course) in enumerate(
        recommendations.iterrows(),
        start=1,
    ):

        score = max(
            0,
            min(
                100,
                round(float(course["final_score"]) * 100),
            ),
        )

        matched_skills = []

        for skill in FEATURE_COLUMNS:
            if (
                skills.get(skill, 0) > 0
                and float(course[skill]) > 0
            ):
                matched_skills.append(
                    SKILL_DISPLAY.get(skill, skill)
                )

        if matched_skills:
            reason = (
                "Matches your "
                + ", ".join(matched_skills[:4])
                + " skills."
            )
        else:
            reason = (
                "Fits your overall learning profile "
                "and career direction."
            )

        st.html(f"""
        <div class="course-card">

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:flex-start;
                gap:20px;
            ">

                <div>
                    <div style="
                        color:#315CFF;
                        font-size:10px;
                        font-weight:850;
                        letter-spacing:1.7px;
                        margin-bottom:9px;
                    ">
                        #{index:02d} · RECOMMENDED FOR YOU
                    </div>

                    <div style="
                        color:#111318;
                        font-size:25px;
                        font-weight:850;
                        letter-spacing:-.8px;
                        line-height:1.15;
                    ">
                        {course["course_name"]}
                    </div>
                </div>

                <div class="match-pill">
                    {score}% match
                </div>
            </div>

            <div style="
                display:flex;
                gap:8px;
                margin-top:20px;
                flex-wrap:wrap;
            ">
                <span style="
                    background:#F1F2F4;
                    color:#4E5562;
                    padding:7px 11px;
                    border-radius:8px;
                    font-size:11px;
                    font-weight:750;
                ">
                    {course["category"]}
                </span>

                <span style="
                    background:#F1F2F4;
                    color:#4E5562;
                    padding:7px 11px;
                    border-radius:8px;
                    font-size:11px;
                    font-weight:750;
                ">
                    {course["difficulty"]}
                </span>
            </div>

            <div style="
                border-top:1px solid #ECEBE5;
                margin-top:21px;
                padding-top:18px;
            ">
                <div style="
                    color:#111318;
                    font-size:13px;
                    font-weight:800;
                    margin-bottom:5px;
                ">
                    Why this fits
                </div>

                <div style="
                    color:#737B89;
                    font-size:13px;
                    line-height:1.6;
                ">
                    {reason}
                </div>
            </div>

        </div>
        """)

        # Real Streamlit interaction.
        st.markdown('<div class="course-actions">', unsafe_allow_html=True)

        view_course = st.button(
            "View course  →",
            key=f"view_course_{index}",
        )

        if view_course:
            # Store only the currently expanded course.
            if (
                st.session_state.get("selected_course_id")
                == course["course_id"]
                and st.session_state.get("show_course_details", False)
            ):
                st.session_state.show_course_details = False
                st.session_state.selected_course_id = None
            else:
                st.session_state.show_course_details = True
                st.session_state.selected_course_id = course["course_id"]
            st.rerun()

        # Render the details directly below THIS course card.
        if (
            st.session_state.get("show_course_details", False)
            and str(st.session_state.get("selected_course_id"))
            == str(course["course_id"])
        ):
            inline_skills = [
                SKILL_DISPLAY.get(
                    skill,
                    skill.replace("_", " ").title()
                )
                for skill in FEATURE_COLUMNS
                if float(course.get(skill, 0)) > 0
            ]

            matched_for_user = [
                SKILL_DISPLAY.get(
                    skill,
                    skill.replace("_", " ").title()
                )
                for skill in FEATURE_COLUMNS
                if skills.get(skill, 0) > 0
                and float(course.get(skill, 0)) > 0
            ]

            inline_skill_text = (
                ", ".join(inline_skills[:8])
                if inline_skills
                else "Core skills"
            )

            inline_match_text = (
                ", ".join(matched_for_user[:6])
                if matched_for_user
                else "Your overall profile"
            )

            st.html(f"""
            <div style="
                margin: -2px 0 18px 0;
                padding:24px 28px;
                border-radius:0 0 18px 18px;
                background:#111827;
                color:white;
                border-top:1px solid #2A3344;
            ">
                <div style="
                    color:#C9F36A;
                    font-size:9px;
                    font-weight:850;
                    letter-spacing:1.5px;
                ">COURSE DETAILS</div>

                <div style="
                    margin-top:8px;
                    font-size:20px;
                    font-weight:850;
                ">{course["course_name"]}</div>

                <div style="
                    margin-top:12px;
                    color:#AEB6C5;
                    font-size:13px;
                    line-height:1.65;
                ">
                    <b style="color:white;">Why this course:</b>
                    It matches {inline_match_text} and supports your
                    <b style="color:#C9F36A;">{profile["goal"]}</b> goal.
                </div>

                <div style="
                    margin-top:12px;
                    color:#AEB6C5;
                    font-size:13px;
                    line-height:1.65;
                ">
                    <b style="color:white;">You'll learn:</b>
                    {inline_skill_text}
                </div>

                <div style="
                    margin-top:14px;
                    display:flex;
                    gap:8px;
                    flex-wrap:wrap;
                ">
                    <span style="
                        background:#202A3A;
                        color:#C9F36A;
                        padding:6px 10px;
                        border-radius:8px;
                        font-size:11px;
                        font-weight:750;
                    ">{course["difficulty"]}</span>

                    <span style="
                        background:#202A3A;
                        color:#AEB6C5;
                        padding:6px 10px;
                        border-radius:8px;
                        font-size:11px;
                        font-weight:750;
                    ">{course["category"]}</span>

                    <span style="
                        background:#202A3A;
                        color:#AEB6C5;
                        padding:6px 10px;
                        border-radius:8px;
                        font-size:11px;
                        font-weight:750;
                    ">{score}% match</span>
                </div>
            </div>
            """)

            if st.button(
                "Hide details ↑",
                key=f"hide_course_{index}",
            ):
                st.session_state.show_course_details = False
                st.session_state.selected_course_id = None
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


    # =====================================================
    # PRECISE PERSONALIZED LEARNING PATH
    # =====================================================

    precise_path = build_precise_learning_path(
        skill_values=skills,
        goal=profile["goal"],
        level=profile["level"],
        max_courses=8,
        interests=profile.get("interests", []),
    )

    path_summary = get_path_summary(
        precise_path,
        profile["goal"],
    )

    st.write("")
    st.write("")

    st.html(f"""
    <div style="
        padding:32px;
        border-radius:20px;
        background:#111827;
        color:white;
        margin-top:20px;
    ">
        <div style="
            color:#C9F36A;
            font-size:11px;
            font-weight:800;
            letter-spacing:1.8px;
        ">
            03 / CONNECT
        </div>

        <div style="
            font-size:32px;
            font-weight:850;
            letter-spacing:-1.5px;
            margin-top:8px;
        ">
            Your precise learning path.
        </div>

        <div style="
            color:#AEB6C5;
            font-size:14px;
            line-height:1.6;
            margin-top:10px;
            max-width:760px;
        ">
            An ordered path built around your current skills,
            prerequisites, skill gaps and your
            {profile["goal"]} goal.
        </div>
    </div>
    """)

    if precise_path:

        # Summary cards
        st.html(f"""
        <div style="
            display:flex;
            gap:12px;
            margin-top:18px;
            flex-wrap:wrap;
        ">
            <div style="
                flex:1;
                min-width:180px;
                padding:18px;
                border-radius:16px;
                background:#EAF7C8;
                border:1px solid #D5EAA5;
            ">
                <div style="
                    color:#315CFF;
                    font-size:9px;
                    font-weight:850;
                    letter-spacing:1.3px;
                ">CAREER GOAL</div>
                <div style="
                    margin-top:7px;
                    font-size:17px;
                    font-weight:850;
                ">{path_summary["goal"]}</div>
            </div>

            <div style="
                flex:1;
                min-width:180px;
                padding:18px;
                border-radius:16px;
                background:#FFFFFF;
                border:1px solid #E2E1DA;
            ">
                <div style="
                    color:#315CFF;
                    font-size:9px;
                    font-weight:850;
                    letter-spacing:1.3px;
                ">PERSONALIZED STEPS</div>
                <div style="
                    margin-top:7px;
                    font-size:17px;
                    font-weight:850;
                ">{path_summary["total_steps"]}</div>
            </div>
        </div>
        """)

        # Precise ordered path
        for item in precise_path:
            skills_text = ", ".join([
                SKILL_DISPLAY.get(
                    skill,
                    skill.replace("_", " ").title()
                )
                for skill in item["skills"][:4]
            ])

            prerequisites = item["prerequisites"]
            prerequisite_text = (
                ", ".join([
                    SKILL_DISPLAY.get(
                        p,
                        p.replace("_", " ").title()
                    )
                    for p in prerequisites.split("|")
                    if p
                ])
                if prerequisites
                else "None"
            )

            st.html(f"""
            <div style="
                display:flex;
                gap:18px;
                margin-top:14px;
                padding:22px;
                border-radius:18px;
                background:#FFFFFF;
                border:1px solid #E2E1DA;
                box-shadow:0 4px 16px rgba(17,24,39,.04);
            ">
                <div style="
                    min-width:46px;
                    height:46px;
                    border-radius:50%;
                    background:#111827;
                    color:#C9F36A;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:16px;
                    font-weight:900;
                ">
                    {item["step"]}
                </div>

                <div style="flex:1;">
                    <div style="
                        color:#315CFF;
                        font-size:9px;
                        font-weight:850;
                        letter-spacing:1.4px;
                    ">
                        {item["status"]} · {item["course_stage"]}
                    </div>

                    <div style="
                        font-size:20px;
                        font-weight:850;
                        margin-top:5px;
                        color:#111318;
                    ">
                        {item["course_name"]}
                    </div>

                    <div style="
                        color:#5D6470;
                        font-size:12px;
                        margin-top:6px;
                    ">
                        {item["category"]} · {item["difficulty"]}
                    </div>

                    <div style="
                        margin-top:12px;
                        color:#111318;
                        font-size:13px;
                        line-height:1.55;
                    ">
                        {item["reason"]}
                    </div>

                    <div style="
                        margin-top:10px;
                        color:#315CFF;
                        font-size:11px;
                        font-weight:700;
                    ">
                        Builds: {skills_text}
                    </div>

                    <div style="
                        margin-top:7px;
                        color:#7A808B;
                        font-size:11px;
                    ">
                        Prerequisites: {prerequisite_text}
                    </div>
                </div>
            </div>
            """)

        st.html(f"""
        <div style="
            margin-top:18px;
            padding:20px;
            border-radius:17px;
            background:#EAF7C8;
            border:1px solid #D5EAA5;
        ">
            <div style="
                color:#315CFF;
                font-size:9px;
                font-weight:850;
                letter-spacing:1.4px;
            ">
                DESTINATION
            </div>
            <div style="
                margin-top:6px;
                font-size:20px;
                font-weight:900;
            ">
                {profile["goal"]}
            </div>
            <div style="
                margin-top:5px;
                color:#505760;
                font-size:12px;
            ">
                Start with <b>{path_summary["start"]}</b> and progress
                through the ordered path toward your goal.
            </div>
        </div>
        """)

    else:
        st.warning(
            "No precise path could be generated for this goal. "
            "Try adjusting your skill assessment."
        )

    # =====================================================
    # COMPLETION
    # =====================================================

    st.write("")
    st.write("")

    st.html("""
    <div style="
        padding:25px 28px;
        border-radius:18px;
        background:#EAF7C8;
        border:1px solid #D5EAA5;
        color:#315CFF;
    ">
        <div style="
            font-size:11px;
            font-weight:800;
            letter-spacing:1.5px;
        ">
            YOUR ARC
        </div>

        <div style="
            font-size:22px;
            font-weight:850;
            color:#111318;
            margin-top:6px;
        ">
            Your next step is now clear.
        </div>

        <div style="
            color:#596171;
            font-size:13px;
            margin-top:6px;
        ">
            LearnArc has mapped your current profile
            to the courses that best fit your direction.
        </div>
    </div>
    """)



# =========================================================
# PRESENTATION FOOTER
# =========================================================

st.html("""
<div style="
    margin-top:55px;
    padding-top:20px;
    border-top:1px solid #DDDCD5;
    display:flex;
    justify-content:space-between;
    gap:20px;
    color:#7A808B;
    font-size:11px;
    line-height:1.5;
">
    <div>
        <b style="color:#111318;">learn<span style="color:#315CFF;">arc</span></b>
        · Personalized Learning Intelligence
    </div>
    <div>
        Assess · Recommend · Connect
    </div>
</div>
""")

# =========================================================
# APP NAVIGATION
# =========================================================
if st.session_state.assessment_done:
    st.write("")
    if st.button("↻ Start over", key="start_over"):
        go_back_to_home()
        st.rerun()