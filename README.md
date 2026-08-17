# LearnArc

AI-powered personalized learning path and course recommendation system.

LearnArc recommends courses and generates personalized learning paths based on a student's skills, interests, career goal, learning level, and performance.

## Features

- Personalized course recommendations
- Goal-based recommendations
- Interest-based filtering
- Skill-based course matching
- Beginner, Intermediate and Advanced recommendations
- Personalized learning path generation
- Course details with match score
- Skill-gap analysis
- Interactive Streamlit interface

## Tech Stack

- Python
- Pandas
- Streamlit
- Recommendation System
- CSV Dataset

## Project Structure

```text
LearnArc/
├── LearnArc Main .py
├── recommender.py
├── skill_gap.py
├── generate_courses.py
├── generate_students.py
├── requirements.txt
├── README.md
├── .gitignore
└── Data/
    ├── Courses.csv
    └── students.csv
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/SarveshOjha01/LearnArc.git
cd LearnArc
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
streamlit run "LearnArc Main .py"
```

## How It Works

1. The student selects a career goal.
2. The student selects areas of interest.
3. The student provides their skill levels.
4. The student selects their learning level.
5. LearnArc analyzes the student's profile.
6. Relevant courses are recommended.
7. A personalized and precise learning path is generated.
8. The student can view course details and match scores.

## Recommendation System

LearnArc considers multiple factors while recommending courses:

- Career goal
- Areas of interest
- Existing technical skills
- Learning level
- Student performance
- Course difficulty
- Course category
- Skill requirements

This helps provide recommendations that are more relevant to the student's current profile and learning objectives.

## Future Improvements

- User authentication
- Database integration
- Advanced machine learning-based recommendation models
- Student progress tracking
- Course completion tracking
- More learning resources and course providers
- Improved recommendation accuracy

## Author

**Sarvesh Ojha**

Computer Science Engineering Student