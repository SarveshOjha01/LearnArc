import pandas as pd
import random

# =========================================================
# LEARNARC — STUDENT DATASET GENERATOR
# =========================================================

random.seed(42)

# Must stay in sync with generate_courses.py / recommender.py
SKILL_COLUMNS = [
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

GOALS = [
    "Software Engineer",
    "AI / ML Engineer",
    "Data Scientist",
    "Data Analyst",
    "Data Engineer",
    "Backend Developer",
    "Frontend Developer",
    "Full Stack Developer",
    "Mobile App Developer",
    "DevOps Engineer",
    "Cloud Engineer",
    "Cybersecurity Engineer",
    "MLOps Engineer",
    "QA / Automation Engineer",
]

INTERESTS = [
    "AI / Machine Learning",
    "Data Science",
    "Backend Development",
    "Web Development",
    "Cloud & DevOps",
    "Cybersecurity",
    "Software Engineering",
    "Data Engineering",
]

LEVELS = [
    "Beginner",
    "Intermediate",
    "Advanced",
]

students = []

for student_id in range(1, 301):

    # Real-valued confidence scores are better for cosine similarity
    # than randomly mixing 0/1 values for every skill.
    skill_scores = {
        skill: round(random.uniform(0.05, 0.95), 2)
        for skill in SKILL_COLUMNS
    }

    # Keep the user's broad profile fields.
    interest = random.choice(INTERESTS)
    goal = random.choice(GOALS)
    level = random.choice(LEVELS)

    performance = round(random.uniform(40, 95), 2)

    student = {
        "student_id": student_id,
        **skill_scores,
        "interest": interest,
        "goal": goal,
        "level": level,
        "performance": performance,
    }

    students.append(student)

df = pd.DataFrame(students)

# Explicit column order
df = df[
    [
        "student_id",
        *SKILL_COLUMNS,
        "interest",
        "goal",
        "level",
        "performance",
    ]
]

df.to_csv("data/students.csv", index=False)

print("========================================")
print("LearnArc student dataset created!")
print("========================================")
print(f"Total students : {len(df)}")
print(f"Total skills   : {len(SKILL_COLUMNS)}")
print(f"Total goals    : {len(GOALS)}")

print("\nStudent columns:")
print(", ".join(df.columns))

print("\nFirst 5 students:")
print(df.head().to_string(index=False))

print("\nGoal distribution:")
print(df["goal"].value_counts().to_string())