# ◌ LearnArc

### Your next, made clear.

> **Assess. Recommend. Connect.**

LearnArc is a personalized learning intelligence platform designed to help learners understand their current skills, identify skill gaps, discover relevant courses, and build a structured learning path toward their career goals.

Instead of showing learners a generic list of courses, LearnArc connects **Current Skills + Interests + Learning Level + Career Goal** to create a more focused and personalized learning journey.

---

## 🚀 Live Demo

🌐 **[Open LearnArc](https://learnarc-awwfmismp9gpitdv4yqjum.streamlit.app/)**

**Build My Arc → Create Profile → Skill Assessment → Recommendations → Personalized Learning Path**

---

## 💡 Why LearnArc?

There are thousands of courses available online. The difficult part isn't finding a course — it's knowing what to learn next.

LearnArc helps answer:

- What should I learn first?
- What skills am I missing?
- Which course is relevant to my goal?
- What should I learn before moving forward?
- How does my current skill level affect my learning path?

> **Don't just collect courses. Build a direction.**

---

## ✨ Key Features

### 🧑‍💻 Personalized Learner Profile

Learners provide their career goal, current learning level, areas of interest, and existing technical skills. This profile becomes the foundation for personalization.

### 📊 Skill Assessment

LearnArc evaluates self-assessed technical skills to understand the learner's current capabilities and identify areas that need attention.

### 🔎 Skill Gap Analysis

The system compares the learner's current skills with skills relevant to their target career direction to identify meaningful learning gaps.

### 🎯 Personalized Course Recommendations

Courses are ranked using multiple signals including:

- Skill similarity
- Career goal relevance
- Category relevance
- Interest match
- Difficulty fit
- Current learning level

### 🗺️ Precise Learning Path

LearnArc goes beyond recommending courses. It organizes relevant courses into an ordered learning journey based on:

- Skill gaps
- Prerequisites
- Course difficulty
- Learning stage
- Career goal
- Existing skills

> **Turn a collection of courses into a journey.**

---

## 🧠 Recommendation Engine

LearnArc uses a content-based recommendation approach.

The learner's skill profile and course skill profiles are represented as feature vectors. Similarity between them is calculated using **Cosine Similarity**.

The recommendation process combines:

**Skill Similarity + Career Relevance + Category Relevance + Interest Match + Difficulty Fit**

This produces a ranked set of courses tailored to the learner's current situation and future direction.

---

## 🗺️ How the Learning Path Works

The learning path engine takes recommendations one step further.

Instead of simply saying:

> "Here are some courses."

LearnArc tries to answer:

> "Here is the order in which you should approach them."

**Current Skills → Skill Gap Analysis → Course Matching → Prerequisite Check → Difficulty & Level Fit → Personalized Learning Path → Career Goal**

---

## 🎯 Example Learning Journey

Suppose a learner wants to become a **Java Backend Developer** and currently has:

- Java → Intermediate
- OOP → Beginner
- DSA → Beginner
- SQL → Beginner
- Backend → Beginner
- Spring Boot → Beginner

LearnArc can identify missing foundations and create a progression such as:

**Java → Object-Oriented Programming → Data Structures → SQL & Databases → Backend Development → Spring Boot → Advanced Backend Concepts**

The exact path changes according to the learner's profile and assessment.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application and recommendation logic |
| Streamlit | Interactive web application |
| Pandas | Data processing |
| Scikit-learn | Similarity and recommendation calculations |
| CSV | Course and learner datasets |
| Git | Version control |
| GitHub | Source code management |
| Streamlit Cloud | Deployment |

---

## 📁 Project Structure

LearnArc/
├── Data/
│   ├── Courses.csv
│   └── students.csv
├── LearnArc Main .py
├── recommender.py
├── skill_gap.py
├── generate_courses.py
├── generate_students.py
├── requirements.txt
├── README.md
└── .gitignore

---

## ⚙️ Run Locally

### 1. Clone the repository

git clone https://github.com/SarveshOjha01/LearnArc.git

cd LearnArc

### 2. Create a virtual environment

python -m venv .venv

### 3. Activate the environment

Windows PowerShell:

.venv\Scripts\Activate.ps1

### 4. Install dependencies

pip install -r requirements.txt

### 5. Run the application

streamlit run "LearnArc Main .py"

The application will open in your browser.

---

## 🔄 Application Flow

**Learner Profile**
↓
**Skill Assessment**
↓
**Skill Gap Analysis**
↓
**Recommendation Engine**
↓
**Course Ranking**
↓
**Precise Learning Path**
↓
**Career Goal**

---

## 📌 Current Features

- [x] Personalized learner profile
- [x] Career goal selection
- [x] Interest selection
- [x] Skill assessment
- [x] Skill-gap analysis
- [x] Course recommendation
- [x] Course relevance scoring
- [x] Learning-level awareness
- [x] Personalized learning path
- [x] Course prerequisites
- [x] Ordered learning journey
- [x] Interactive Streamlit UI
- [x] Cloud deployment

---

## 🔮 Future Improvements

- User authentication
- Persistent learner profiles
- Learning progress tracking
- Course completion tracking
- Real-world course links
- Larger course catalogue
- Real-time course data
- Resume-based skill extraction
- AI-powered learning assistant
- Adaptive skill assessments
- Progress-based path updates
- Personalized learning-time estimation

---

## 🌱 Project Vision

LearnArc is based on a simple idea:

> **The problem isn't a lack of learning resources. The problem is knowing what comes next.**

LearnArc aims to connect:

**Where You Are → What You're Missing → What You Should Learn → Why You Should Learn It → Where It Takes You**

The goal is to make learning more **focused, structured, and purposeful**.

---

## 👨‍💻 Project

### LearnArc — Personalized Learning Intelligence

Built with:

**Python · Streamlit · Pandas · Scikit-learn**

**GitHub:**  
https://github.com/SarveshOjha01/LearnArc

**Live Demo:**  
https://learnarc-awwfmismp9gpitdv4yqjum.streamlit.app/

---

### ◌ LearnArc

**Your next, made clear.**
