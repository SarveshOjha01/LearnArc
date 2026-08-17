from pathlib import Path

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# =========================================================
# LEARNARC — RECOMMENDATION ENGINE
# =========================================================

# Always resolve the CSV relative to recommender.py.
# This prevents Streamlit/VS Code working-directory issues.
BASE_DIR = Path(__file__).resolve().parent
COURSES_PATH = BASE_DIR / "data" / "courses.csv"

if not COURSES_PATH.exists():
    raise FileNotFoundError(
        f"courses.csv not found at: {COURSES_PATH}"
    )

courses = pd.read_csv(COURSES_PATH)

# Keep this list EXACTLY in sync with generate_courses.py
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

# Make older course CSVs compatible with the newer recommender.
# Missing skill columns are treated as 0 instead of crashing the import.
for _feature in FEATURE_COLUMNS:
    if _feature not in courses.columns:
        courses[_feature] = 0

# Human-readable names for UI/reasons.
SKILL_DISPLAY = {
    "python": "Python",
    "java": "Java",
    "javascript": "JavaScript",
    "web": "Web Development",
    "react": "React",
    "backend": "Backend Development",
    "nodejs": "Node.js",
    "spring_boot": "Spring Boot",
    "dsa": "Data Structures & Algorithms",
    "oop": "OOP",
    "sql": "SQL",
    "database": "Database",
    "system_design": "System Design",
    "ai": "Artificial Intelligence",
    "ml": "Machine Learning",
    "deep_learning": "Deep Learning",
    "nlp": "NLP",
    "computer_vision": "Computer Vision",
    "data_science": "Data Science",
    "statistics": "Statistics",
    "data_engineering": "Data Engineering",
    "cloud": "Cloud",
    "devops": "DevOps",
    "docker": "Docker",
    "linux": "Linux",
    "cybersecurity": "Cybersecurity",
    "testing": "Software Testing",
    "git": "Git & GitHub",
}

# =========================================================
# CAREER PROFILES
# =========================================================
# Higher number = more important for that career.
# These are used to calculate goal relevance, not just
# category matching.

GOAL_SKILLS = {
    "Software Engineer": {
        "java": .8, "python": .7, "dsa": 1.0, "oop": .9,
        "git": .7, "system_design": .9, "testing": .7,
        "database": .5, "sql": .5, "backend": .6,
    },
    "AI / ML Engineer": {
        "python": 1.0, "ml": 1.0, "ai": .9, "data_science": .9,
        "statistics": .8, "deep_learning": .8, "git": .5, "cloud": .4,
    },
    "Data Scientist": {
        "python": 1.0, "data_science": 1.0, "statistics": 1.0,
        "ml": .9, "ai": .7, "sql": .7, "database": .5,
    },
    "Data Analyst": {
        "python": .8, "data_science": 1.0, "statistics": .9,
        "sql": 1.0, "database": .7,
    },
    "Data Engineer": {
        "python": .9, "sql": 1.0, "database": .9, "data_engineering": 1.0,
        "cloud": .8, "backend": .6, "git": .6,
    },
    "Backend Developer": {
        "backend": 1.0, "java": .8, "spring_boot": .9, "nodejs": .8,
        "database": .8, "sql": .8, "system_design": .8, "docker": .5, "git": .6,
    },
    "Java Backend Developer": {
        "java": 1.0, "oop": .9, "backend": 1.0, "spring_boot": 1.0,
        "sql": .8, "database": .8, "dsa": .7, "system_design": .8, "git": .7,
    },
    "Python Backend Developer": {
        "python": 1.0, "backend": 1.0, "nodejs": .4, "sql": .8,
        "database": .8, "api": .8, "docker": .5, "git": .7,
    },
    "Frontend Developer": {
        "javascript": 1.0, "web": 1.0, "react": .9, "git": .6, "testing": .5,
    },
    "React Developer": {
        "javascript": 1.0, "react": 1.0, "web": .9, "git": .7, "testing": .5,
    },
    "Full Stack Developer": {
        "javascript": .9, "react": .9, "web": 1.0, "backend": 1.0,
        "database": .8, "sql": .7, "git": .7, "system_design": .6,
    },
    "Mobile App Developer": {
        "java": .9, "javascript": .9, "react": .8, "oop": .8,
        "backend": .7, "database": .6, "testing": .6, "git": .7,
        "system_design": .5,
    },
    "Android Developer": {
        "java": 1.0, "oop": .9, "database": .7, "backend": .5,
        "testing": .6, "git": .7, "system_design": .5,
    },
    "React Native Developer": {
        "javascript": 1.0, "react": 1.0, "backend": .6,
        "database": .5, "testing": .7, "git": .8,
    },
    "DevOps Engineer": {
        "devops": 1.0, "docker": 1.0, "cloud": .9, "linux": .9,
        "git": .8, "backend": .5, "system_design": .6,
    },
    "Cloud Engineer": {
        "cloud": 1.0, "linux": .8, "devops": .9, "docker": .8,
        "system_design": .8, "git": .6,
    },
    "Cloud Architect": {
        "cloud": 1.0, "system_design": 1.0, "devops": .8,
        "docker": .7, "linux": .7, "git": .5,
    },
    "Cybersecurity Engineer": {
        "cybersecurity": 1.0, "linux": .9, "web": .5, "backend": .4,
        "testing": .4, "git": .4,
    },
    "Ethical Hacker": {
        "cybersecurity": 1.0, "linux": .9, "web": .8,
        "backend": .4, "git": .4,
    },
    "MLOps Engineer": {
        "ml": .9, "python": .8, "devops": 1.0, "docker": 1.0,
        "cloud": 1.0, "git": .8, "system_design": .6,
    },
    "Generative AI Engineer": {
        "python": 1.0, "ai": 1.0, "ml": .9, "nlp": 1.0,
        "deep_learning": .8, "cloud": .5, "git": .5,
    },
    "NLP Engineer": {
        "python": 1.0, "nlp": 1.0, "ml": .9, "ai": .9,
        "deep_learning": .8, "data_science": .6,
    },
    "Computer Vision Engineer": {
        "python": 1.0, "computer_vision": 1.0, "ml": .9,
        "ai": .9, "deep_learning": .9, "data_science": .6,
    },
    "QA / Automation Engineer": {
        "testing": 1.0, "python": .7, "java": .7, "git": .7,
        "web": .5, "backend": .4,
    },
    "Database Engineer": {
        "sql": 1.0, "database": 1.0, "data_engineering": .7,
        "backend": .5, "system_design": .7, "git": .5,
    },
    "Data / BI Analyst": {
        "sql": 1.0, "data_science": .9, "statistics": .8,
        "database": .7, "python": .6,
    },
}

# Categories that support each career.
GOAL_CATEGORIES = {
    "Software Engineer": ["Programming", "Software Engineering", "Backend", "QA", "Database"],
    "AI / ML Engineer": ["AI", "Data Science", "MLOps"],
    "Data Scientist": ["Data Science", "AI"],
    "Data Analyst": ["Data Science", "Database"],
    "Data Engineer": ["Data Engineering", "Database", "Cloud", "Backend"],
    "Backend Developer": ["Backend", "Database", "Programming"],
    "Java Backend Developer": ["Backend", "Database", "Programming"],
    "Python Backend Developer": ["Backend", "Database", "Programming"],
    "Frontend Developer": ["Web"],
    "React Developer": ["Web"],
    "Full Stack Developer": ["Web", "Backend", "Database"],
    "Mobile App Developer": ["Mobile Development", "Backend", "Programming"],
    "Android Developer": ["Mobile Development"],
    "React Native Developer": ["Mobile Development"],
    "DevOps Engineer": ["DevOps", "Cloud"],
    "Cloud Engineer": ["Cloud", "DevOps"],
    "Cloud Architect": ["Cloud", "DevOps"],
    "Cybersecurity Engineer": ["Cybersecurity"],
    "Ethical Hacker": ["Cybersecurity"],
    "MLOps Engineer": ["MLOps", "DevOps", "Cloud", "AI"],
    "Generative AI Engineer": ["AI"],
    "NLP Engineer": ["AI"],
    "Computer Vision Engineer": ["AI"],
    "QA / Automation Engineer": ["QA", "Programming"],
    "Database Engineer": ["Database", "Data Engineering", "Backend"],
    "Data / BI Analyst": ["Data Science", "Database"],
}


# =========================================================
# DISTINCT CAREER ROADMAPS
# =========================================================
# Each goal has its own ordered curriculum. This prevents the
# same generic path from appearing for unrelated career goals.

GOAL_PATHS = {
    "Software Engineer": [
        "Java Programming", "Object Oriented Programming",
        "Data Structures and Algorithms", "Advanced DSA",
        "SQL Fundamentals", "Backend Development Fundamentals",
        "System Design Fundamentals", "Software Testing Fundamentals",
    ],
    "AI / ML Engineer": [
        "Python Programming", "Statistics for Data Science",
        "Python for Data Science", "Machine Learning Basics",
        "Intermediate Machine Learning", "Advanced Machine Learning",
        "Deep Learning Fundamentals", "Generative AI", "MLOps Fundamentals",
    ],
    "Data Scientist": [
        "Python Programming", "Statistics for Data Science",
        "Python for Data Science", "Exploratory Data Analysis",
        "Data Visualization", "SQL Fundamentals",
        "Machine Learning Basics", "Advanced Machine Learning",
    ],
    "Data Analyst": [
        "SQL Fundamentals", "Statistics for Data Science",
        "Data Analytics", "Exploratory Data Analysis",
        "Data Visualization", "Power BI for Beginners",
        "Advanced Data Analytics",
    ],
    "Data Engineer": [
        "Python Programming", "SQL Fundamentals",
        "Database Management Systems", "Data Engineering Fundamentals",
        "ETL and Data Pipelines", "Data Warehousing",
        "Cloud Data Engineering", "Advanced Data Engineering",
    ],
    "Backend Developer": [
        "Java Programming", "Object Oriented Programming",
        "SQL Fundamentals", "Backend Development Fundamentals",
        "REST API Development", "Spring Boot Development",
        "Database Design and Optimization", "System Design Fundamentals",
        "Docker and Containers", "Microservices Architecture",
    ],
    "Java Backend Developer": [
        "Java Programming", "Object Oriented Programming",
        "Data Structures and Algorithms", "SQL Fundamentals",
        "Backend Development Fundamentals", "Spring Boot Development",
        "Advanced Spring Boot", "Database Design and Optimization",
        "System Design Fundamentals", "Microservices Architecture",
    ],
    "Python Backend Developer": [
        "Python Programming", "SQL Fundamentals",
        "Backend Development Fundamentals", "REST API Development",
        "Node.js Backend Development", "MongoDB Development",
        "Docker and Containers", "Advanced System Design",
    ],
    "Frontend Developer": [
        "HTML and CSS", "JavaScript Fundamentals",
        "Advanced JavaScript", "Frontend Development",
        "React Development", "Advanced React",
        "Frontend Performance and Architecture",
    ],
    "React Developer": [
        "HTML and CSS", "JavaScript Fundamentals",
        "Advanced JavaScript", "React Development",
        "Advanced React", "Frontend Performance and Architecture",
        "Software Testing Fundamentals",
    ],
    "Full Stack Developer": [
        "HTML and CSS", "JavaScript Fundamentals",
        "React Development", "Backend Development Fundamentals",
        "REST API Development", "SQL Fundamentals",
        "MongoDB Development", "Full Stack Development",
        "Docker and Containers", "System Design Fundamentals",
    ],
    "Mobile App Developer": [
        "Java Programming", "Object Oriented Programming",
        "Mobile App Development Fundamentals", "Android App Development",
        "React Native Development", "Mobile App Backend Integration",
        "Mobile App Architecture", "Mobile App Testing",
    ],
    "Android Developer": [
        "Java Programming", "Object Oriented Programming",
        "Mobile App Development Fundamentals", "Android Development with Java",
        "Android App Development", "Mobile App Backend Integration",
        "Mobile App Architecture", "Mobile App Testing",
    ],
    "React Native Developer": [
        "JavaScript Fundamentals", "React Development",
        "Mobile App Development Fundamentals", "React Native Development",
        "Mobile App Backend Integration", "Advanced React Native",
        "Mobile App Architecture", "Mobile App Testing",
    ],
    "DevOps Engineer": [
        "Linux Fundamentals", "Git and GitHub",
        "Cloud Computing Fundamentals", "DevOps Fundamentals",
        "Docker and Containers", "CI/CD Fundamentals",
        "Kubernetes Fundamentals", "Advanced Kubernetes",
    ],
    "Cloud Engineer": [
        "Linux Fundamentals", "Cloud Computing Fundamentals",
        "AWS Fundamentals", "DevOps Fundamentals",
        "Docker and Containers", "AWS Cloud Architecture",
        "Kubernetes Fundamentals", "Advanced Kubernetes",
    ],
    "Cloud Architect": [
        "Linux Fundamentals", "Cloud Computing Fundamentals",
        "AWS Fundamentals", "DevOps Fundamentals",
        "Docker and Containers", "System Design Fundamentals",
        "AWS Cloud Architecture", "Advanced Kubernetes",
    ],
    "Cybersecurity Engineer": [
        "Linux Fundamentals", "Cyber Security Fundamentals",
        "Network Security", "Web Application Security",
        "Ethical Hacking Basics", "Security Operations Fundamentals",
        "Advanced Ethical Hacking",
    ],
    "Ethical Hacker": [
        "Linux Fundamentals", "Cyber Security Fundamentals",
        "Network Security", "Web Application Security",
        "Ethical Hacking Basics", "Advanced Ethical Hacking",
    ],
    "MLOps Engineer": [
        "Python Programming", "Machine Learning Basics",
        "Git and GitHub", "Linux Fundamentals",
        "Docker and Containers", "DevOps Fundamentals",
        "Kubernetes Fundamentals", "AI Model Deployment",
        "MLOps Fundamentals",
    ],
    "Generative AI Engineer": [
        "Python Programming", "Machine Learning Basics",
        "Deep Learning Fundamentals", "Natural Language Processing",
        "Generative AI", "Large Language Models",
        "AI Model Deployment", "MLOps Fundamentals",
    ],
    "NLP Engineer": [
        "Python Programming", "Statistics for Data Science",
        "Machine Learning Basics", "Deep Learning Fundamentals",
        "Natural Language Processing", "Large Language Models",
        "AI Model Deployment",
    ],
    "Computer Vision Engineer": [
        "Python Programming", "Statistics for Data Science",
        "Machine Learning Basics", "Deep Learning Fundamentals",
        "Computer Vision", "Advanced Deep Learning",
        "AI Model Deployment",
    ],
    "QA / Automation Engineer": [
        "Java Programming", "Object Oriented Programming",
        "Software Testing Fundamentals", "Test Automation with Java",
        "Test Automation with Python", "Advanced Test Automation",
    ],
    "Database Engineer": [
        "SQL Fundamentals", "Database Management Systems",
        "Advanced SQL", "MongoDB Development",
        "Database Design and Optimization", "Data Warehousing",
        "System Design Fundamentals",
    ],
    "Data / BI Analyst": [
        "SQL Fundamentals", "Statistics for Data Science",
        "Data Analytics", "Data Visualization",
        "Power BI for Beginners", "Exploratory Data Analysis",
        "Advanced Data Analytics",
    ],
}

# =========================================================
# INTEREST -> SKILL MAPPING
# =========================================================
INTEREST_SKILLS = {
    "Python": ["python"], "Java": ["java"], "C++": ["dsa"],
    "Data Structures & Algorithms": ["dsa"], "Object Oriented Programming": ["oop"],
    "HTML & CSS": ["web"], "JavaScript": ["javascript", "web"],
    "React": ["react", "javascript", "web"],
    "Frontend Development": ["web", "javascript", "react"],
    "Backend Development": ["backend"], "Full Stack Development": ["web", "javascript", "backend", "database"],
    "REST APIs": ["backend"], "Spring Boot": ["spring_boot", "java", "backend"],
    "Node.js": ["nodejs", "javascript", "backend"],
    "Microservices": ["backend", "system_design"], "System Design": ["system_design", "backend", "database"],
    "Artificial Intelligence": ["ai"], "Machine Learning": ["ml", "ai", "python"],
    "Deep Learning": ["deep_learning", "ml", "ai"], "Natural Language Processing": ["nlp", "ml", "ai"],
    "Computer Vision": ["computer_vision", "ml", "ai"],
    "Generative AI": ["ai", "ml", "nlp", "deep_learning"],
    "Large Language Models": ["nlp", "ml", "deep_learning", "ai"],
    "Data Science": ["data_science", "python", "statistics"],
    "Data Analytics": ["data_science", "statistics", "sql"], "Statistics": ["statistics"],
    "SQL": ["sql", "database"], "Database": ["database", "sql"],
    "Data Engineering": ["data_engineering", "sql", "database"],
    "Business Intelligence": ["data_science", "sql"],
    "Cloud Computing": ["cloud"], "AWS": ["cloud"], "Azure": ["cloud"],
    "Google Cloud": ["cloud"], "DevOps": ["devops", "cloud"],
    "Docker": ["docker", "devops"], "Kubernetes": ["docker", "devops", "cloud"],
    "CI/CD": ["devops", "git"], "Linux": ["linux"],
    "Cybersecurity": ["cybersecurity"], "Ethical Hacking": ["cybersecurity", "linux"],
    "Network Security": ["cybersecurity", "linux"], "Web Security": ["cybersecurity", "web"],
    "Mobile Development": ["java", "javascript", "git"],
    "Android Development": ["java", "oop", "database"], "React Native": ["javascript", "react", "git"],
    "Software Testing": ["testing"], "Test Automation": ["testing", "python", "java"],
    "Git & GitHub": ["git"],
}

def _interest_skill_boost(interests):
    boost = {}
    for interest in interests or []:
        for skill in INTEREST_SKILLS.get(interest, []):
            boost[skill] = boost.get(skill, 0.0) + 0.15
    return boost

# =========================================================
# NORMALIZATION
# =========================================================

def _normalise_student_skills(skill_values):
    """
    Convert user slider values from 0-100 to 0-1.
    If values are already 0-1, keep them.
    """
    result = {}

    for skill in FEATURE_COLUMNS:
        value = float(skill_values.get(skill, 0))

        if value > 1:
            value = value / 100.0

        result[skill] = max(0.0, min(1.0, value))

    return result


def _goal_skill_score(course, goal):
    """
    Measures how strongly a course covers the important skills
    for the selected career goal.
    """
    goal_skills = GOAL_SKILLS.get(goal, {})

    if not goal_skills:
        return 0.0

    weighted_total = 0.0
    weight_total = 0.0

    for skill, weight in goal_skills.items():

        # Some legacy aliases may exist in goal profiles but not
        # in the course dataset. Ignore them safely.
        if skill not in courses.columns:
            continue

        course_value = float(course.get(skill, 0))
        weighted_total += course_value * weight
        weight_total += weight

    if weight_total == 0:
        return 0.0

    return weighted_total / weight_total


def _goal_category_score(category, goal):
    categories = GOAL_CATEGORIES.get(goal, [])

    if not categories:
        return 0.0

    category_lower = str(category).lower()

    return 1.0 if any(
        category_lower == str(target).lower()
        for target in categories
    ) else 0.0


def _interest_score(category, interests):
    if not interests:
        return 0.0

    category_lower = str(category).lower()

    for interest in interests:
        interest_lower = str(interest).lower()

        # Small compatibility aliases for the UI's interest labels.
        aliases = {
            "ai": ["ai"],
            "artificial intelligence": ["ai"],
            "data science": ["data science"],
            "backend": ["backend"],
            "backend development": ["backend"],
            "web": ["web"],
            "web development": ["web"],
            "cloud": ["cloud"],
            "cloud & devops": ["cloud", "devops"],
            "cybersecurity": ["cybersecurity"],
            "software engineering": ["software engineering", "programming"],
            "data engineering": ["data engineering"],
        }

        targets = aliases.get(interest_lower, [interest_lower])

        if any(target in category_lower for target in targets):
            return 1.0

    return 0.0


def _difficulty_score(course_difficulty, student_level):
    """
    Small preference for a course appropriate to the learner's
    current level. It never dominates career relevance.
    """
    levels = {
        "Beginner": 0,
        "Intermediate": 1,
        "Advanced": 2,
    }

    course_level = levels.get(str(course_difficulty), 1)
    student_level = levels.get(str(student_level), 1)

    difference = abs(course_level - student_level)

    if difference == 0:
        return 1.0
    if difference == 1:
        return 0.65

    return 0.25


# =========================================================
# MAIN RECOMMENDER
# =========================================================

def recommend_courses(
    skill_values,
    interests=None,
    goal="Software Engineer",
    level="Beginner",
    top_n=5,
):
    """
    Return the best courses for a learner.

    Scoring:
        45% current-skill similarity
        25% career-goal relevance
        15% goal category relevance
        10% interest match
         5% difficulty fit

    This makes the career goal strong enough to prevent an
    unrelated high-similarity course from taking over the list.
    """
    interest_boost = _interest_skill_boost(interests)


    interests = interests or []

    student_skills = _normalise_student_skills(skill_values)

    for _skill, _boost in interest_boost.items():
        if _skill in student_skills:
            student_skills[_skill] = min(
                1.0,
                float(student_skills.get(_skill, 0)) + _boost
            )

    student_vector = [
        student_skills[skill]
        for skill in FEATURE_COLUMNS
    ]

    # Ensure every feature exists in the course dataframe.
    for skill in FEATURE_COLUMNS:
        if skill not in courses.columns:
            courses[skill] = 0

    course_vectors = courses[FEATURE_COLUMNS].fillna(0).astype(float)

    if sum(student_vector) == 0:
        similarity_scores = [0.0] * len(courses)
    else:
        similarity_scores = cosine_similarity(
            [student_vector],
            course_vectors,
        )[0]

    recommendations = courses.copy()

    recommendations["similarity"] = similarity_scores

    recommendations["goal_skill_score"] = recommendations.apply(
        lambda row: _goal_skill_score(row, goal),
        axis=1,
    )

    recommendations["goal_category_score"] = recommendations[
        "category"
    ].apply(
        lambda category: _goal_category_score(category, goal)
    )

    recommendations["interest_match"] = recommendations[
        "category"
    ].apply(
        lambda category: _interest_score(category, interests)
    )

    recommendations["difficulty_fit"] = recommendations.apply(
        lambda row: _difficulty_score(
            row["difficulty"],
            level,
        ),
        axis=1,
    )

    recommendations["final_score"] = (
        recommendations["similarity"] * 0.45
        + recommendations["goal_skill_score"] * 0.25
        + recommendations["goal_category_score"] * 0.15
        + recommendations["interest_match"] * 0.10
        + recommendations["difficulty_fit"] * 0.05
    )

    recommendations = recommendations.sort_values(
        by=["final_score", "goal_skill_score", "similarity"],
        ascending=False,
    )

    return recommendations.head(top_n).reset_index(drop=True)


# =========================================================
# WHY THIS COURSE?
# =========================================================

def get_course_reason(course, skill_values, goal):
    """
    Generate a concise explanation for why a course was selected.
    """

    student_skills = _normalise_student_skills(skill_values)
    goal_skills = GOAL_SKILLS.get(goal, {})

    matched_goal_skills = []
    gap_skills = []

    for skill, importance in sorted(
        goal_skills.items(),
        key=lambda item: item[1],
        reverse=True,
    ):
        if skill not in FEATURE_COLUMNS:
            continue

        course_value = float(course.get(skill, 0))

        if course_value > 0:
            matched_goal_skills.append(
                SKILL_DISPLAY.get(skill, skill)
            )

        elif student_skills.get(skill, 0) < 0.5:
            gap_skills.append(
                SKILL_DISPLAY.get(skill, skill)
            )

    if matched_goal_skills:
        reason = (
            f"Builds skills important for your {goal} path: "
            + ", ".join(matched_goal_skills[:4])
            + "."
        )
    else:
        reason = (
            f"Supports your {goal} direction."
        )

    if gap_skills:
        reason += (
            " It also targets gaps in "
            + ", ".join(gap_skills[:2])
            + "."
        )

    return reason


# =========================================================
# LEARNING ARC
# =========================================================

def build_learning_arc(
    recommendations,
    skill_values,
    goal,
    max_courses=3,
):
    """
    Turn recommendations into a simple learning sequence.

    IMPORTANT:
    This is goal-aware. It does not blindly take random courses.
    """

    student_skills = _normalise_student_skills(skill_values)
    goal_skills = GOAL_SKILLS.get(goal, {})

    # Current weakest skills that actually matter for the goal.
    goal_gaps = []

    for skill, importance in goal_skills.items():
        if skill not in FEATURE_COLUMNS:
            continue

        confidence = student_skills.get(skill, 0)

        goal_gaps.append(
            (
                skill,
                confidence,
                importance,
            )
        )

    goal_gaps.sort(
        key=lambda item: (
            item[1],
            -item[2],
        )
    )

    weakest_goal_skills = [
        skill
        for skill, _, _ in goal_gaps[:3]
    ]

    # Re-rank the recommended courses by goal skill coverage,
    # while preserving relevance from the recommendation engine.
    selected = recommendations.copy()

    if not selected.empty:
        selected["_arc_score"] = selected.apply(
            lambda row: _goal_skill_score(row, goal),
            axis=1,
        )

        selected = selected.sort_values(
            by=["_arc_score", "final_score"],
            ascending=False,
        )

    selected = selected.head(max_courses)

    return {
        "current_level": "Current skill profile",
        "goal": goal,
        "skill_gaps": [
            SKILL_DISPLAY.get(
                skill,
                skill.replace("_", " ").title(),
            )
            for skill in weakest_goal_skills
        ],
        "courses": [
            str(row["course_name"])
            for _, row in selected.iterrows()
        ],
    }


# =========================================================
# LEVEL-AWARE COURSE SELECTION
# =========================================================

LEVEL_RANK = {
    "Beginner": 0,
    "Intermediate": 1,
    "Advanced": 2,
}


def _difficulty_distance(course_difficulty, learner_level):
    course_rank = LEVEL_RANK.get(str(course_difficulty), 1)
    learner_rank = LEVEL_RANK.get(str(learner_level), 1)
    return abs(course_rank - learner_rank)


def _select_level_appropriate_course(course_names, learner_level):
    """
    From a set of course variants for the same learning step,
    choose the variant appropriate to the learner's level.

    Priority:
      1. Exact level
      2. One level away
      3. Closest available level
    """
    available = []

    for name in course_names:
        row = courses[courses["course_name"] == name]
        if row.empty:
            continue

        item = row.iloc[0]
        available.append(item)

    if not available:
        return None

    available.sort(
        key=lambda item: (
            _difficulty_distance(item["difficulty"], learner_level),
            LEVEL_RANK.get(str(item["difficulty"]), 1),
        )
    )

    return available[0]


# =========================================================
# PRECISE PERSONALIZED PATH ENGINE
# =========================================================

def build_precise_learning_path(
    skill_values,
    goal,
    level="Beginner",
    max_courses=8,
    interests=None,
):
    """
    Dynamically build a precise path from:
    Goal + Interests + Skill Gaps + Learning Level.

    This version does NOT depend on GOAL_PATHS having exact course names.
    It works with the regenerated level-specific course catalogue.
    """
    student_skills = _normalise_student_skills(skill_values)
    goal_skills = set(GOAL_SKILLS.get(goal, {}).keys())
    selected_interests = interests or []

    # Convert selected interests into skills when the mapping exists.
    interest_skills = set()
    if "_interest_skill_boost" in globals():
        try:
            interest_boost = _interest_skill_boost(selected_interests)
            interest_skills.update(interest_boost.keys())
        except Exception:
            pass

    # Fallback for common interest labels.
    interest_map = {
        "Python": {"python"},
        "Java": {"java"},
        "C++": {"dsa"},
        "Data Structures & Algorithms": {"dsa"},
        "Object Oriented Programming": {"oop"},
        "HTML & CSS": {"web"},
        "JavaScript": {"javascript", "web"},
        "React": {"react", "javascript", "web"},
        "Frontend Development": {"web", "javascript", "react"},
        "Backend Development": {"backend"},
        "Full Stack Development": {"web", "javascript", "backend", "database"},
        "REST APIs": {"backend"},
        "Spring Boot": {"java", "backend"},
        "Node.js": {"javascript", "backend"},
        "Microservices": {"backend", "system_design"},
        "System Design": {"system_design", "backend", "database"},
        "Artificial Intelligence": {"ai"},
        "Machine Learning": {"ml", "ai", "python"},
        "Deep Learning": {"deep_learning", "ml", "ai"},
        "Natural Language Processing": {"nlp", "ml", "ai"},
        "Computer Vision": {"computer_vision", "ml", "ai"},
        "Generative AI": {"ai", "ml", "nlp", "deep_learning"},
        "Large Language Models": {"nlp", "ml", "deep_learning", "ai"},
        "Data Science": {"data_science", "python", "statistics"},
        "Data Analytics": {"data_science", "statistics", "sql"},
        "Statistics": {"statistics"},
        "SQL": {"sql", "database"},
        "Database": {"database", "sql"},
        "Data Engineering": {"data_engineering", "sql", "database"},
        "Business Intelligence": {"data_science", "sql"},
        "Cloud Computing": {"cloud"},
        "AWS": {"cloud"},
        "Azure": {"cloud"},
        "Google Cloud": {"cloud"},
        "DevOps": {"devops", "cloud"},
        "Docker": {"docker", "devops"},
        "Kubernetes": {"docker", "devops", "cloud"},
        "CI/CD": {"devops", "git"},
        "Linux": {"linux"},
        "Cybersecurity": {"cybersecurity"},
        "Ethical Hacking": {"cybersecurity", "linux"},
        "Network Security": {"cybersecurity", "linux"},
        "Web Security": {"cybersecurity", "web"},
        "Mobile Development": {"java", "javascript", "git"},
        "Android Development": {"java", "oop", "database"},
        "React Native": {"javascript", "react", "git"},
        "Software Testing": {"testing"},
        "Test Automation": {"testing", "python", "java"},
        "Git & GitHub": {"git"},
    }

    for interest in selected_interests:
        interest_skills.update(interest_map.get(interest, set()))

    # Goal is primary. Interests refine the route; they do not override the goal.
    target_skills = goal_skills | interest_skills

    if not target_skills:
        return []

    learner_rank = LEVEL_RANK.get(str(level), 0)

    strong_threshold = {
        "Beginner": 0.75,
        "Intermediate": 0.60,
        "Advanced": 0.45,
    }.get(str(level), 0.75)

    learned = {
        skill
        for skill in FEATURE_COLUMNS
        if float(student_skills.get(skill, 0)) >= strong_threshold
    }

    # Current gaps should be prioritized.
    gaps = {
        skill for skill in target_skills
        if float(student_skills.get(skill, 0)) < strong_threshold
    }

    if not gaps:
        gaps = target_skills - learned

    if not gaps:
        gaps = target_skills

    if courses.empty:
        return []

    candidates = []

    for _, row in courses.iterrows():
        course_name = str(row.get("course_name", "")).strip()
        if not course_name:
            continue

        course_skills = {
            skill
            for skill in FEATURE_COLUMNS
            if float(row.get(skill, 0)) > 0
        }

        # Only courses that actually teach something relevant to the
        # selected goal/interests can enter the path.
        relevant = course_skills & target_skills
        gap_skills = course_skills & gaps

        if not relevant:
            continue

        difficulty = str(row.get("difficulty", "Beginner"))
        course_rank = LEVEL_RANK.get(difficulty, 0)

        # Level-aware filtering:
        # Beginner: don't jump straight to Advanced.
        if learner_rank == 0 and course_rank == 2:
            continue

        # Intermediate: Advanced is allowed only with reasonably strong
        # overall skill confidence.
        if learner_rank == 1 and course_rank == 2:
            avg_conf = sum(
                float(student_skills.get(skill, 0))
                for skill in relevant
            ) / max(len(relevant), 1)
            if avg_conf < 0.55:
                continue

        # Score components.
        goal_match = len(course_skills & goal_skills)
        interest_match = len(course_skills & interest_skills)
        gap_match = len(gap_skills)

        # Prefer the learner's requested level, but allow nearby levels
        # when they make the path more useful.
        level_distance = abs(course_rank - learner_rank)
        level_score = max(0, 2 - level_distance)

        # Don't recommend something the learner already knows well unless
        # it is strongly relevant to the selected goal.
        known_count = len(course_skills & learned)
        novelty = max(0, len(relevant) - known_count)

        score = (
            gap_match * 5.0
            + goal_match * 4.0
            + interest_match * 2.5
            + level_score * 2.0
            + novelty * 1.5
            - known_count * 1.0
        )

        candidates.append({
            "row": row,
            "score": score,
            "gap_skills": list(gap_skills),
            "relevant_skills": list(relevant),
        })

    if not candidates:
        return []

    # Highest relevance first.
    candidates.sort(key=lambda item: item["score"], reverse=True)

    selected = []
    covered = set()
    used_courses = set()

    # First pass: greedily cover different skill gaps so the path is not
    # five variations of the same topic.
    while candidates and len(selected) < max_courses:
        best_index = None
        best_value = float("-inf")

        for i, item in enumerate(candidates):
            row = item["row"]
            name = str(row["course_name"])

            if name in used_courses:
                continue

            new_gaps = set(item["gap_skills"]) - covered

            value = item["score"] + len(new_gaps) * 4.0

            # Keep the first step at or near the learner's current level.
            if not selected:
                if LEVEL_RANK.get(
                    str(row.get("difficulty", "Beginner")), 0
                ) == learner_rank:
                    value += 3.0

            if value > best_value:
                best_value = value
                best_index = i

        if best_index is None:
            break

        item = candidates.pop(best_index)
        row = item["row"]
        name = str(row["course_name"])
        used_courses.add(name)

        gap_skills = item["gap_skills"]
        relevant_skills = item["relevant_skills"]

        if not gap_skills:
            # Don't fill the path with courses that add no new knowledge.
            continue

        skill_names = [
            SKILL_DISPLAY.get(
                skill,
                skill.replace("_", " ").title(),
            )
            for skill in gap_skills[:4]
        ]

        difficulty = str(row.get("difficulty", "Beginner"))

        if not selected:
            status = "START HERE"
        elif difficulty == "Advanced":
            status = "ADVANCED"
        elif difficulty == "Intermediate":
            status = "NEXT"
        else:
            status = "FOUNDATION"

        selected.append({
            "step": len(selected) + 1,
            "course_id": row.get("course_id"),
            "course_name": row["course_name"],
            "category": row.get("category", ""),
            "difficulty": difficulty,
            "course_stage": row.get("course_stage", "Core"),
            "path_order": row.get("path_order", len(selected) + 1),
            "prerequisites": str(row.get("prerequisites", "")).strip(),
            "skills": gap_skills,
            "status": status,
            "reason": (
                "Builds "
                + ", ".join(skill_names)
                + f" for your {goal} path at {level} level."
            ),
        })

        covered.update(relevant_skills)

        # Remove courses that add nothing new after this step.
        candidates = [
            item for item in candidates
            if set(item["gap_skills"]) - covered
        ]

    # Re-number after selection.
    for index, item in enumerate(selected, start=1):
        item["step"] = index

    return selected

# =========================================================
# PATH SUMMARY — UI COMPATIBILITY
# =========================================================

def get_path_summary(path, goal):
    """
    Return a small summary object used by app.py for the
    precise learning path section.
    """
    if not path:
        return {
            "goal": goal,
            "total_steps": 0,
            "start": None,
            "end": None,
        }

    return {
        "goal": goal,
        "total_steps": len(path),
        "start": path[0].get("course_name"),
        "end": path[-1].get("course_name"),

        }