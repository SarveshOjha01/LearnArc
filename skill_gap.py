import pandas as pd

# Load student data
students = pd.read_csv("data/students.csv")

skill_columns = [
    "python",
    "java",
    "ai",
    "backend",
    "database",
    "data_science",
    "web",
    "javascript",
    "cloud",
    "git",
    "cybersecurity"
]


def analyze_skill_gap(student_id):

    student = students[
        students["student_id"] == student_id
    ].iloc[0]

    current_skills = []
    missing_skills = []

    for skill in skill_columns:

        if student[skill] >= 0.5:
            current_skills.append(skill)
        else:
            missing_skills.append(skill)

    return current_skills, missing_skills


# Test
student_id = 1

current, missing = analyze_skill_gap(student_id)

print("\nSKILL GAP ANALYSIS")
print("------------------")

print("\nCurrent Skills:")
for skill in current:
    print(f"✓ {skill}")

print("\nSkills to Improve:")
for skill in missing:
    print(f"→ {skill}")