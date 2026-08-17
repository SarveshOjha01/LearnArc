import pandas as pd

# =========================================================
# LEARNARC — COURSE DATASET GENERATOR
# =========================================================
# This version uses a fixed professional course catalog.
# It avoids random course names/difficulty levels so the
# recommendation engine receives consistent training data.
# =========================================================

COURSE_TEMPLATES = [
    # ---------------- PROGRAMMING / CORE ----------------
    ("Python Programming", "Programming", "Beginner", ["python"]),
    ("Advanced Python", "Programming", "Advanced", ["python"]),
    ("Java Programming", "Programming", "Beginner", ["java"]),
    ("Advanced Java", "Programming", "Advanced", ["java"]),
    ("Object Oriented Programming", "Programming", "Beginner", ["java", "oop"]),
    ("Data Structures and Algorithms", "Programming", "Intermediate", ["java", "dsa"]),
    ("Advanced DSA", "Programming", "Advanced", ["java", "dsa"]),
    ("Git and GitHub", "Tools", "Beginner", ["git"]),
    ("Advanced Git and GitHub", "Tools", "Intermediate", ["git"]),

    # ---------------- BACKEND ----------------
    ("Backend Development Fundamentals", "Backend", "Beginner", ["backend"]),
    ("REST API Development", "Backend", "Beginner", ["backend"]),
    ("Spring Boot Development", "Backend", "Intermediate", ["java", "spring_boot", "backend"]),
    ("Advanced Spring Boot", "Backend", "Advanced", ["java", "spring_boot", "backend"]),
    ("Node.js Backend Development", "Backend", "Intermediate", ["javascript", "nodejs", "backend"]),
    ("Advanced Node.js", "Backend", "Advanced", ["javascript", "nodejs", "backend"]),
    ("Microservices Architecture", "Backend", "Advanced", ["java", "spring_boot", "backend", "system_design"]),
    ("System Design Fundamentals", "Software Engineering", "Intermediate", ["backend", "system_design"]),
    ("Advanced System Design", "Software Engineering", "Advanced", ["backend", "system_design"]),

    # ---------------- DATABASE ----------------
    ("SQL Fundamentals", "Database", "Beginner", ["sql", "database"]),
    ("Advanced SQL", "Database", "Intermediate", ["sql", "database"]),
    ("Database Management Systems", "Database", "Intermediate", ["database", "sql"]),
    ("Advanced Database Systems", "Database", "Advanced", ["database", "sql"]),
    ("MongoDB Development", "Database", "Intermediate", ["database", "backend"]),
    ("Database Design and Optimization", "Database", "Advanced", ["database", "sql", "system_design"]),

    # ---------------- WEB / FRONTEND ----------------
    ("HTML and CSS", "Web", "Beginner", ["web"]),
    ("JavaScript Fundamentals", "Web", "Beginner", ["javascript", "web"]),
    ("Advanced JavaScript", "Web", "Intermediate", ["javascript", "web"]),
    ("Frontend Development", "Web", "Intermediate", ["javascript", "web"]),
    ("React Development", "Web", "Intermediate", ["javascript", "react", "web"]),
    ("Advanced React", "Web", "Advanced", ["javascript", "react", "web"]),
    ("Frontend Performance and Architecture", "Web", "Advanced", ["javascript", "react", "web", "system_design"]),
    ("Full Stack Development", "Web", "Advanced", ["javascript", "react", "backend", "database", "web"]),

    # ---------------- AI / ML ----------------
    ("Artificial Intelligence Fundamentals", "AI", "Beginner", ["python", "ai"]),
    ("Machine Learning Basics", "AI", "Beginner", ["python", "ml", "ai", "data_science", "statistics"]),
    ("Intermediate Machine Learning", "AI", "Intermediate", ["python", "ml", "ai", "data_science", "statistics"]),
    ("Advanced Machine Learning", "AI", "Advanced", ["python", "ml", "ai", "data_science", "statistics"]),
    ("Deep Learning Fundamentals", "AI", "Intermediate", ["python", "ml", "deep_learning", "ai"]),
    ("Advanced Deep Learning", "AI", "Advanced", ["python", "ml", "deep_learning", "ai"]),
    ("Natural Language Processing", "AI", "Advanced", ["python", "ai", "ml", "nlp"]),
    ("Computer Vision", "AI", "Intermediate", ["python", "ai", "ml", "computer_vision"]),
    ("Generative AI", "AI", "Advanced", ["python", "ai", "ml", "nlp"]),
    ("Large Language Models", "AI", "Advanced", ["python", "ai", "ml", "nlp"]),
    ("AI Model Deployment", "AI", "Advanced", ["python", "ml", "ai", "cloud"]),
    ("MLOps Fundamentals", "MLOps", "Advanced", ["ml", "devops", "docker", "cloud", "python"]),

    # ---------------- DATA SCIENCE / ANALYTICS ----------------
    ("Python for Data Science", "Data Science", "Beginner", ["python", "data_science"]),
    ("Exploratory Data Analysis", "Data Science", "Intermediate", ["python", "data_science", "statistics"]),
    ("Data Visualization", "Data Science", "Beginner", ["python", "data_science"]),
    ("Statistics for Data Science", "Data Science", "Intermediate", ["statistics", "data_science"]),
    ("Advanced Statistics", "Data Science", "Advanced", ["statistics", "data_science"]),
    ("Data Analytics", "Data Science", "Beginner", ["python", "data_science", "sql"]),
    ("Advanced Data Analytics", "Data Science", "Intermediate", ["python", "data_science", "sql", "statistics"]),
    ("Power BI for Beginners", "Data Science", "Beginner", ["data_science"]),
    ("Data Science with Python", "Data Science", "Intermediate", ["python", "data_science", "statistics"]),

    # ---------------- DATA ENGINEERING ----------------
    ("Data Engineering Fundamentals", "Data Engineering", "Beginner", ["python", "sql", "data_engineering"]),
    ("ETL and Data Pipelines", "Data Engineering", "Intermediate", ["python", "sql", "data_engineering"]),
    ("Advanced Data Engineering", "Data Engineering", "Advanced", ["python", "sql", "data_engineering", "cloud"]),
    ("Data Warehousing", "Data Engineering", "Intermediate", ["sql", "database", "data_engineering"]),
    ("Cloud Data Engineering", "Data Engineering", "Advanced", ["sql", "data_engineering", "cloud"]),

    # ---------------- CLOUD / DEVOPS ----------------
    ("Cloud Computing Fundamentals", "Cloud", "Beginner", ["cloud"]),
    ("AWS Fundamentals", "Cloud", "Beginner", ["cloud"]),
    ("AWS Cloud Architecture", "Cloud", "Advanced", ["cloud", "system_design"]),
    ("DevOps Fundamentals", "DevOps", "Beginner", ["devops", "cloud"]),
    ("Docker and Containers", "DevOps", "Beginner", ["docker", "devops"]),
    ("Advanced Docker", "DevOps", "Intermediate", ["docker", "devops"]),
    ("CI/CD Fundamentals", "DevOps", "Intermediate", ["devops", "git", "cloud"]),
    ("Kubernetes Fundamentals", "DevOps", "Intermediate", ["docker", "devops", "cloud"]),
    ("Advanced Kubernetes", "DevOps", "Advanced", ["docker", "devops", "cloud", "system_design"]),
    ("Linux Fundamentals", "DevOps", "Beginner", ["linux"]),
    ("Linux for Developers", "DevOps", "Intermediate", ["linux", "devops"]),

    # ---------------- CYBERSECURITY ----------------
    ("Cyber Security Fundamentals", "Cybersecurity", "Beginner", ["cybersecurity"]),
    ("Network Security", "Cybersecurity", "Intermediate", ["cybersecurity", "linux"]),
    ("Ethical Hacking Basics", "Cybersecurity", "Beginner", ["cybersecurity", "linux"]),
    ("Web Application Security", "Cybersecurity", "Intermediate", ["cybersecurity", "web"]),
    ("Advanced Ethical Hacking", "Cybersecurity", "Advanced", ["cybersecurity", "linux", "web"]),
    ("Security Operations Fundamentals", "Cybersecurity", "Intermediate", ["cybersecurity", "linux"]),

    # ---------------- QA / AUTOMATION ----------------
    ("Software Testing Fundamentals", "QA", "Beginner", ["testing"]),
    ("Test Automation with Python", "QA", "Intermediate", ["testing", "python"]),
    ("Test Automation with Java", "QA", "Intermediate", ["testing", "java"]),
    ("Advanced Test Automation", "QA", "Advanced", ["testing", "java", "python"]),

    # ---------------- MOBILE DEVELOPMENT ----------------
    ("Mobile App Development Fundamentals", "Mobile Development", "Beginner", ["java", "javascript", "git"]),
    ("Android Development with Java", "Mobile Development", "Intermediate", ["java", "oop", "git"]),
    ("Android App Development", "Mobile Development", "Intermediate", ["java", "database", "git"]),
    ("React Native Development", "Mobile Development", "Intermediate", ["javascript", "react", "git"]),
    ("Advanced React Native", "Mobile Development", "Advanced", ["javascript", "react", "backend", "git"]),
    ("Mobile App UI and Navigation", "Mobile Development", "Beginner", ["javascript", "react"]),
    ("Mobile App Backend Integration", "Mobile Development", "Intermediate", ["backend", "database", "javascript"]),
    ("Mobile App Architecture", "Mobile Development", "Advanced", ["java", "javascript", "backend", "database", "system_design"]),
    ("Mobile App Testing", "Mobile Development", "Intermediate", ["testing", "javascript", "java"]),


    # ---------------- LEVEL-SPECIFIC COURSES ----------------
    ("Python Foundations", "Programming", "Beginner", ["python"]),
    ("Python Intermediate Projects", "Programming", "Intermediate", ["python", "git"]),
    ("Python Advanced Engineering", "Programming", "Advanced", ["python", "system_design", "testing"]),

    ("Java Foundations", "Programming", "Beginner", ["java"]),
    ("Java Intermediate Projects", "Programming", "Intermediate", ["java", "oop", "git"]),
    ("Advanced Java Engineering", "Programming", "Advanced", ["java", "oop", "system_design", "testing"]),

    ("SQL for Beginners", "Database", "Beginner", ["sql", "database"]),
    ("Intermediate SQL Queries", "Database", "Intermediate", ["sql", "database"]),
    ("Advanced SQL Optimization", "Database", "Advanced", ["sql", "database", "system_design"]),

    ("Statistics Foundations", "Data Science", "Beginner", ["statistics"]),
    ("Applied Statistics", "Data Science", "Intermediate", ["statistics", "data_science"]),
    ("Advanced Statistical Modeling", "Data Science", "Advanced", ["statistics", "data_science", "ml"]),

    ("Machine Learning Foundations", "AI", "Beginner", ["python", "ai", "ml"]),
    ("Applied Machine Learning", "AI", "Intermediate", ["python", "ai", "ml", "data_science"]),
    ("Advanced Machine Learning Engineering", "AI", "Advanced", ["python", "ai", "ml", "data_science", "git"]),

    ("Deep Learning Foundations", "AI", "Beginner", ["python", "ai", "deep_learning"]),
    ("Applied Deep Learning", "AI", "Intermediate", ["python", "ai", "deep_learning"]),
    ("Advanced Deep Learning Engineering", "AI", "Advanced", ["python", "ai", "deep_learning", "cloud"]),

    ("Web Development Foundations", "Web", "Beginner", ["web"]),
    ("Intermediate Frontend Development", "Web", "Intermediate", ["web", "javascript"]),
    ("Advanced Frontend Architecture", "Web", "Advanced", ["web", "javascript", "react", "testing"]),

    ("JavaScript Foundations", "Web", "Beginner", ["javascript", "web"]),
    ("JavaScript Application Development", "Web", "Intermediate", ["javascript", "web", "git"]),
    ("Advanced JavaScript Engineering", "Web", "Advanced", ["javascript", "web", "testing"]),

    ("React Foundations", "Web", "Beginner", ["react", "javascript", "web"]),
    ("React Application Development", "Web", "Intermediate", ["react", "javascript", "web"]),
    ("Advanced React Architecture", "Web", "Advanced", ["react", "javascript", "web", "testing"]),

    ("Backend Foundations", "Backend", "Beginner", ["backend"]),
    ("Intermediate Backend APIs", "Backend", "Intermediate", ["backend", "database"]),
    ("Advanced Backend Architecture", "Backend", "Advanced", ["backend", "database", "system_design", "docker"]),

    ("Spring Boot Foundations", "Backend", "Beginner", ["java", "backend"]),
    ("Spring Boot Application Development", "Backend", "Intermediate", ["java", "backend", "database"]),
    ("Advanced Spring Boot Microservices", "Backend", "Advanced", ["java", "backend", "database", "system_design"]),

    ("Data Analytics Foundations", "Data Science", "Beginner", ["data_science"]),
    ("Applied Data Analytics", "Data Science", "Intermediate", ["python", "data_science", "statistics"]),
    ("Advanced Analytics and Modeling", "Data Science", "Advanced", ["python", "data_science", "statistics", "ml"]),

    ("Data Engineering Foundations", "Data Engineering", "Beginner", ["python", "sql", "data_engineering"]),
    ("Intermediate Data Pipelines", "Data Engineering", "Intermediate", ["python", "sql", "data_engineering"]),
    ("Advanced Data Engineering Architecture", "Data Engineering", "Advanced", ["python", "sql", "data_engineering", "cloud"]),

    ("Cloud Foundations", "Cloud", "Beginner", ["cloud"]),
    ("Intermediate Cloud Engineering", "Cloud", "Intermediate", ["cloud", "linux", "devops"]),
    ("Advanced Cloud Architecture", "Cloud", "Advanced", ["cloud", "linux", "devops", "system_design"]),

    ("DevOps Foundations", "Cloud", "Beginner", ["devops", "git"]),
    ("Intermediate DevOps", "Cloud", "Intermediate", ["devops", "docker", "git"]),
    ("Advanced DevOps and Platform Engineering", "Cloud", "Advanced", ["devops", "docker", "cloud", "system_design"]),

    ("Cybersecurity Foundations", "Cybersecurity", "Beginner", ["cybersecurity"]),
    ("Intermediate Cybersecurity Operations", "Cybersecurity", "Intermediate", ["cybersecurity", "linux"]),
    ("Advanced Cybersecurity Engineering", "Cybersecurity", "Advanced", ["cybersecurity", "linux", "web", "testing"]),

    ("Ethical Hacking Foundations", "Cybersecurity", "Beginner", ["cybersecurity", "linux"]),
    ("Intermediate Ethical Hacking", "Cybersecurity", "Intermediate", ["cybersecurity", "linux", "web"]),
    ("Advanced Ethical Hacking and Web Security", "Cybersecurity", "Advanced", ["cybersecurity", "linux", "web"]),

    ("Mobile Development Foundations", "Mobile Development", "Beginner", ["java", "javascript", "git"]),
    ("Intermediate Mobile App Development", "Mobile Development", "Intermediate", ["java", "javascript", "backend", "database"]),
    ("Advanced Mobile App Architecture", "Mobile Development", "Advanced", ["java", "javascript", "backend", "database", "system_design", "testing"]),

    ("Android Foundations", "Mobile Development", "Beginner", ["java", "oop"]),
    ("Intermediate Android Development", "Mobile Development", "Intermediate", ["java", "oop", "database"]),
    ("Advanced Android Engineering", "Mobile Development", "Advanced", ["java", "oop", "database", "testing", "system_design"]),

    ("Generative AI Foundations", "AI", "Beginner", ["python", "ai"]),
    ("Applied Generative AI", "AI", "Intermediate", ["python", "ai", "nlp", "ml"]),
    ("Advanced Generative AI Engineering", "AI", "Advanced", ["python", "ai", "nlp", "ml", "deep_learning"]),

    ("NLP Foundations", "AI", "Beginner", ["python", "nlp"]),
    ("Applied NLP", "AI", "Intermediate", ["python", "nlp", "ml"]),
    ("Advanced NLP and LLM Engineering", "AI", "Advanced", ["python", "nlp", "ml", "deep_learning"]),

    ("Computer Vision Foundations", "AI", "Beginner", ["python", "computer_vision"]),
    ("Applied Computer Vision", "AI", "Intermediate", ["python", "computer_vision", "ml"]),
    ("Advanced Computer Vision Engineering", "AI", "Advanced", ["python", "computer_vision", "ml", "deep_learning"]),

    ("Software Testing Foundations", "QA", "Beginner", ["testing"]),
    ("Intermediate Test Automation", "QA", "Intermediate", ["testing", "java", "python"]),
    ("Advanced QA Automation Engineering", "QA", "Advanced", ["testing", "java", "python", "git"]),

    ("Database Foundations", "Database", "Beginner", ["database", "sql"]),
    ("Intermediate Database Development", "Database", "Intermediate", ["database", "sql", "backend"]),
    ("Advanced Database Engineering", "Database", "Advanced", ["database", "sql", "system_design", "data_engineering"]),

]

# All skill columns used by Courses.csv.
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


# ---------------------------------------------------------
# LEARNING-PATH METADATA
# ---------------------------------------------------------

PATH_RULES = {
    "Python Programming": (1, "Foundation", []),
    "Advanced Python": (3, "Core", ["python"]),
    "Python for Data Science": (2, "Foundation", ["python"]),
    "Machine Learning Basics": (4, "Core", ["python", "statistics"]),
    "Intermediate Machine Learning": (5, "Core", ["python", "ml", "statistics"]),
    "Advanced Machine Learning": (6, "Advanced", ["python", "ml", "statistics"]),
    "Deep Learning Fundamentals": (7, "Advanced", ["python", "ml"]),
    "Advanced Deep Learning": (8, "Advanced", ["python", "ml", "deep_learning"]),
    "Natural Language Processing": (9, "Specialization", ["python", "ml"]),
    "Computer Vision": (9, "Specialization", ["python", "ml"]),
    "Generative AI": (10, "Specialization", ["python", "ml", "nlp"]),
    "Large Language Models": (11, "Specialization", ["python", "ml", "nlp"]),
    "AI Model Deployment": (12, "Advanced", ["python", "ml", "cloud"]),
    "MLOps Fundamentals": (13, "Advanced", ["python", "ml", "docker", "devops", "cloud"]),

    "Java Programming": (1, "Foundation", []),
    "Advanced Java": (3, "Core", ["java", "oop"]),
    "Object Oriented Programming": (2, "Foundation", ["java"]),
    "Data Structures and Algorithms": (3, "Core", ["java", "dsa"]),
    "Advanced DSA": (4, "Advanced", ["java", "dsa"]),

    "Backend Development Fundamentals": (3, "Core", ["programming"]),
    "REST API Development": (5, "Core", ["backend"]),
    "Spring Boot Development": (6, "Core", ["java", "backend"]),
    "Advanced Spring Boot": (7, "Advanced", ["java", "spring_boot", "backend"]),
    "Node.js Backend Development": (6, "Core", ["javascript", "backend"]),
    "Advanced Node.js": (7, "Advanced", ["javascript", "nodejs", "backend"]),
    "Microservices Architecture": (9, "Advanced", ["backend", "spring_boot", "system_design"]),
    "System Design Fundamentals": (8, "Advanced", ["backend", "database"]),
    "Advanced System Design": (10, "Advanced", ["backend", "system_design"]),

    "SQL Fundamentals": (2, "Foundation", []),
    "Advanced SQL": (4, "Core", ["sql", "database"]),
    "Database Management Systems": (3, "Core", ["sql"]),
    "Advanced Database Systems": (5, "Advanced", ["database", "sql"]),
    "MongoDB Development": (5, "Core", ["database", "backend"]),
    "Database Design and Optimization": (7, "Advanced", ["database", "sql", "system_design"]),

    "HTML and CSS": (1, "Foundation", []),
    "JavaScript Fundamentals": (2, "Foundation", ["web"]),
    "Advanced JavaScript": (3, "Core", ["javascript", "web"]),
    "Frontend Development": (4, "Core", ["javascript", "web"]),
    "React Development": (5, "Core", ["javascript", "web"]),
    "Advanced React": (6, "Advanced", ["javascript", "react", "web"]),
    "Frontend Performance and Architecture": (7, "Advanced", ["javascript", "react", "web"]),
    "Full Stack Development": (8, "Advanced", ["javascript", "react", "backend", "database"]),

    "Exploratory Data Analysis": (3, "Core", ["python", "statistics"]),
    "Data Visualization": (3, "Core", ["python", "data_science"]),
    "Statistics for Data Science": (2, "Foundation", []),
    "Advanced Statistics": (4, "Advanced", ["statistics"]),
    "Data Analytics": (3, "Core", ["python", "sql"]),
    "Advanced Data Analytics": (5, "Core", ["python", "sql", "statistics"]),
    "Power BI for Beginners": (3, "Core", ["data_science"]),
    "Data Science with Python": (4, "Core", ["python", "statistics", "data_science"]),

    "Data Engineering Fundamentals": (3, "Foundation", ["python", "sql"]),
    "ETL and Data Pipelines": (4, "Core", ["python", "sql", "data_engineering"]),
    "Advanced Data Engineering": (6, "Advanced", ["python", "sql", "data_engineering", "cloud"]),
    "Data Warehousing": (5, "Core", ["sql", "database"]),
    "Cloud Data Engineering": (7, "Advanced", ["sql", "data_engineering", "cloud"]),

    "Cloud Computing Fundamentals": (1, "Foundation", []),
    "AWS Fundamentals": (2, "Foundation", ["cloud"]),
    "AWS Cloud Architecture": (5, "Advanced", ["cloud", "system_design"]),
    "DevOps Fundamentals": (2, "Foundation", ["cloud"]),
    "Docker and Containers": (3, "Core", ["devops"]),
    "Advanced Docker": (4, "Core", ["docker", "devops"]),
    "CI/CD Fundamentals": (5, "Core", ["git", "devops"]),
    "Kubernetes Fundamentals": (6, "Advanced", ["docker", "devops", "cloud"]),
    "Advanced Kubernetes": (7, "Advanced", ["docker", "devops", "cloud", "system_design"]),
    "Linux Fundamentals": (1, "Foundation", []),
    "Linux for Developers": (2, "Core", ["linux"]),

    "Cyber Security Fundamentals": (1, "Foundation", []),
    "Network Security": (3, "Core", ["cybersecurity", "linux"]),
    "Ethical Hacking Basics": (4, "Core", ["cybersecurity", "linux"]),
    "Web Application Security": (5, "Core", ["cybersecurity", "web"]),
    "Advanced Ethical Hacking": (6, "Advanced", ["cybersecurity", "linux", "web"]),
    "Security Operations Fundamentals": (5, "Core", ["cybersecurity", "linux"]),

    "Software Testing Fundamentals": (1, "Foundation", []),
    "Test Automation with Python": (3, "Core", ["testing", "python"]),
    "Test Automation with Java": (3, "Core", ["testing", "java"]),
    "Advanced Test Automation": (5, "Advanced", ["testing", "java", "python"]),
    "Python Foundations": (1, "Foundation", []),
    "Python Intermediate Projects": (3, "Core", ["python"]),
    "Python Advanced Engineering": (5, "Advanced", ["python", "git"]),

    "Java Foundations": (1, "Foundation", []),
    "Java Intermediate Projects": (3, "Core", ["java", "oop"]),
    "Advanced Java Engineering": (5, "Advanced", ["java", "oop"]),

    "SQL for Beginners": (1, "Foundation", []),
    "Intermediate SQL Queries": (3, "Core", ["sql"]),
    "Advanced SQL Optimization": (5, "Advanced", ["sql", "database"]),

    "Statistics Foundations": (1, "Foundation", []),
    "Applied Statistics": (3, "Core", ["statistics"]),
    "Advanced Statistical Modeling": (5, "Advanced", ["statistics", "data_science"]),

    "Machine Learning Foundations": (4, "Foundation", ["python"]),
    "Applied Machine Learning": (5, "Core", ["python", "statistics"]),
    "Advanced Machine Learning Engineering": (7, "Advanced", ["python", "ml", "statistics"]),

    "Deep Learning Foundations": (6, "Foundation", ["python", "ml"]),
    "Applied Deep Learning": (7, "Core", ["python", "ml"]),
    "Advanced Deep Learning Engineering": (8, "Advanced", ["python", "ml", "deep_learning"]),

    "Web Development Foundations": (1, "Foundation", []),
    "Intermediate Frontend Development": (4, "Core", ["javascript", "web"]),
    "Advanced Frontend Architecture": (6, "Advanced", ["javascript", "react", "web"]),

    "JavaScript Foundations": (1, "Foundation", []),
    "JavaScript Application Development": (3, "Core", ["javascript"]),
    "Advanced JavaScript Engineering": (5, "Advanced", ["javascript", "web"]),

    "React Foundations": (3, "Foundation", ["javascript"]),
    "React Application Development": (5, "Core", ["javascript", "react"]),
    "Advanced React Architecture": (7, "Advanced", ["javascript", "react", "web"]),

    "Backend Foundations": (1, "Foundation", []),
    "Intermediate Backend APIs": (4, "Core", ["backend"]),
    "Advanced Backend Architecture": (7, "Advanced", ["backend", "database", "system_design"]),

    "Spring Boot Foundations": (4, "Foundation", ["java", "backend"]),
    "Spring Boot Application Development": (6, "Core", ["java", "backend", "database"]),
    "Advanced Spring Boot Microservices": (8, "Advanced", ["java", "backend", "system_design"]),

    "Data Analytics Foundations": (1, "Foundation", []),
    "Applied Data Analytics": (3, "Core", ["python", "statistics"]),
    "Advanced Analytics and Modeling": (6, "Advanced", ["python", "statistics", "ml"]),

    "Data Engineering Foundations": (1, "Foundation", ["python", "sql"]),
    "Intermediate Data Pipelines": (4, "Core", ["python", "sql"]),
    "Advanced Data Engineering Architecture": (7, "Advanced", ["python", "sql", "cloud"]),

    "Cloud Foundations": (1, "Foundation", []),
    "Intermediate Cloud Engineering": (4, "Core", ["cloud", "linux"]),
    "Advanced Cloud Architecture": (7, "Advanced", ["cloud", "linux", "system_design"]),

    "DevOps Foundations": (1, "Foundation", ["git"]),
    "Intermediate DevOps": (4, "Core", ["devops", "docker"]),
    "Advanced DevOps and Platform Engineering": (7, "Advanced", ["devops", "docker", "cloud"]),

    "Cybersecurity Foundations": (1, "Foundation", []),
    "Intermediate Cybersecurity Operations": (4, "Core", ["cybersecurity", "linux"]),
    "Advanced Cybersecurity Engineering": (7, "Advanced", ["cybersecurity", "linux", "web"]),

    "Ethical Hacking Foundations": (2, "Foundation", ["cybersecurity"]),
    "Intermediate Ethical Hacking": (4, "Core", ["cybersecurity", "linux"]),
    "Advanced Ethical Hacking and Web Security": (6, "Advanced", ["cybersecurity", "linux", "web"]),

    "Mobile Development Foundations": (1, "Foundation", []),
    "Intermediate Mobile App Development": (4, "Core", ["java", "javascript"]),
    "Advanced Mobile App Architecture": (7, "Advanced", ["java", "javascript", "backend"]),

    "Android Foundations": (1, "Foundation", ["java"]),
    "Intermediate Android Development": (4, "Core", ["java", "oop"]),
    "Advanced Android Engineering": (7, "Advanced", ["java", "oop", "database"]),

    "Generative AI Foundations": (6, "Foundation", ["python", "ai"]),
    "Applied Generative AI": (8, "Core", ["python", "ml", "nlp"]),
    "Advanced Generative AI Engineering": (10, "Advanced", ["python", "nlp", "deep_learning"]),

    "NLP Foundations": (7, "Foundation", ["python", "ml"]),
    "Applied NLP": (9, "Core", ["python", "nlp", "ml"]),
    "Advanced NLP and LLM Engineering": (11, "Advanced", ["python", "nlp", "deep_learning"]),

    "Computer Vision Foundations": (7, "Foundation", ["python", "ml"]),
    "Applied Computer Vision": (9, "Core", ["python", "computer_vision", "ml"]),
    "Advanced Computer Vision Engineering": (11, "Advanced", ["python", "computer_vision", "deep_learning"]),

    "Software Testing Foundations": (1, "Foundation", []),
    "Intermediate Test Automation": (3, "Core", ["testing"]),
    "Advanced QA Automation Engineering": (5, "Advanced", ["testing", "java", "python"]),

    "Database Foundations": (1, "Foundation", []),
    "Intermediate Database Development": (4, "Core", ["sql", "database"]),
    "Advanced Database Engineering": (7, "Advanced", ["sql", "database", "system_design"]),


    "Mobile App Development Fundamentals": (1, "Foundation", []),
    "Mobile App UI and Navigation": (2, "Foundation", ["javascript"]),
    "Android Development with Java": (3, "Core", ["java", "oop"]),
    "Android App Development": (4, "Core", ["java", "database"]),
    "React Native Development": (3, "Core", ["javascript", "react"]),
    "Advanced React Native": (5, "Advanced", ["javascript", "react", "backend"]),
    "Mobile App Backend Integration": (5, "Core", ["backend", "database"]),
    "Mobile App Architecture": (6, "Advanced", ["backend", "database", "system_design"]),
    "Mobile App Testing": (6, "Advanced", ["testing", "javascript", "java"]),
}

def get_path_metadata(course_name, skills):
    if course_name in PATH_RULES:
        return PATH_RULES[course_name]
    if not skills:
        return 1, "Foundation", []
    return 2, "Core", skills[:2]


courses = []

for course_id, (course_name, category, difficulty, skills) in enumerate(
    COURSE_TEMPLATES, start=1
):
    path_order, course_stage, prerequisites = get_path_metadata(
        course_name,
        skills,
    )

    row = {
        "course_id": course_id,
        "course_name": course_name,
        "category": category,
        "difficulty": difficulty,
        "course_stage": course_stage,
        "prerequisites": "|".join(prerequisites),
        "path_order": path_order,
    }

    for skill in SKILL_COLUMNS:
        row[skill] = int(skill in skills)

    courses.append(row)

df = pd.DataFrame(courses)

# Safety checks
df = df.drop_duplicates(subset=["course_name"], keep="first")

required_columns = [
    "course_id",
    "course_name",
    "category",
    "difficulty",
    "course_stage",
    "prerequisites",
    "path_order",
    *SKILL_COLUMNS,
]

df = df[required_columns]

# Save
df.to_csv("data/courses.csv", index=False)

print("========================================")
print("LearnArc course dataset created!")
print("========================================")
print(f"Total courses : {len(df)}")
print(f"Total skills  : {len(SKILL_COLUMNS)}")
print("\nSkill columns:")
print(", ".join(SKILL_COLUMNS))

print("\nFirst 5 courses:")
print(df.head().to_string(index=False))

print("\nCourses by category:")
print(df["category"].value_counts().to_string())