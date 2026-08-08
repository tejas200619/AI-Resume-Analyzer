import streamlit as st
from streamlit_option_menu import option_menu
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)
st.markdown("""
<style>

div[data-testid="metric-container"]{
    background:white;
    padding:18px;
    border-radius:15px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.15);
    border-left:6px solid #4F8BF9;
}

h1,h2,h3{
    color:#4F8BF9;
}

</style>
""", unsafe_allow_html=True)
# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to extract skills
def extract_skills(text):
    skills_list = [
    "python", "java", "c++", "html", "css", "javascript",
    "sql", "git", "machine learning", "ai", "data analysis",
    "streamlit", "mysql", "react", "node.js", "rest api",
    "rest apis", "cloud computing", "aws", "docker", "kubernetes",
    "communication", "problem-solving"
]

    found_skills = []
    text = text.lower()

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills

# Function to calculate skill match score (60%)
def calculate_skill_score(resume_skills, job_skills):
    if not job_skills:
        return 0

    matched_skills = [skill for skill in job_skills if skill in resume_skills]
    score = (len(matched_skills) / len(job_skills)) * 100

    return round(score, 2)

# Function to calculate overall text similarity (40%)
def calculate_text_similarity(resume_text, job_description):
    texts = [resume_text, job_description]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return round(similarity[0][0] * 100, 2)

# Function to calculate final weighted score
def calculate_final_score(skill_score, text_score):
    final_score = (0.6 * skill_score) + (0.4 * text_score)
    return round(final_score, 2)
import re

# -----------------------------
# ATS SCORE CALCULATION
# -----------------------------
def calculate_ats_score(resume_text, resume_skills):
    score = 0
    text = resume_text.lower()

    # Contact Information
    if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", resume_text):
        score += 10

    if re.search(r"\+?\d[\d\s-]{8,}", resume_text):
        score += 10

    # Sections
    if "education" in text:
        score += 10

    if "skills" in text:
        score += 10

    if "project" in text:
        score += 10

    if "experience" in text:
        score += 10

    if "certification" in text or "certifications" in text:
        score += 10

    # Skill Count
    if len(resume_skills) >= 8:
        score += 20
    elif len(resume_skills) >= 5:
        score += 15
    elif len(resume_skills) >= 3:
        score += 10

    # Resume Length
    words = len(resume_text.split())

    if words >= 300:
        score += 10
    elif words >= 150:
        score += 5

    return min(score, 100)
# -----------------------------
# RESUME RATING
# -----------------------------
def get_resume_rating(score):

    if score >= 90:
        return "⭐⭐⭐⭐⭐"

    elif score >= 75:
        return "⭐⭐⭐⭐☆"

    elif score >= 60:
        return "⭐⭐⭐☆☆"

    elif score >= 40:
        return "⭐⭐☆☆☆"

    else:
        return "⭐☆☆☆☆"
    # -----------------------------
# RESUME STRENGTH
# -----------------------------
def resume_strength(score):

    if score >= 85:
        return "🟢 Excellent"

    elif score >= 70:
        return "🟡 Good"

    elif score >= 50:
        return "🟠 Average"

    else:
        return "🔴 Needs Improvement"
    # -----------------------------
# RESUME COMPLETENESS
# -----------------------------
def resume_completeness(resume_text):

    text = resume_text.lower()

    sections = [
        "education",
        "skills",
        "projects",
        "experience",
        "certifications"
    ]

    found = 0

    for section in sections:
        if section in text:
            found += 1

    return round((found / len(sections)) * 100, 2)
# -----------------------------
# SECTION CHECKER
# -----------------------------
def check_sections(resume_text):

    text = resume_text.lower()

    results = {}

    results["Education"] = "education" in text
    results["Skills"] = "skills" in text
    results["Projects"] = "project" in text
    results["Experience"] = "experience" in text
    results["Certifications"] = (
        "certification" in text or
        "certifications" in text
    )

    return results
# -----------------------------
# JOB ROLE PREDICTION
# -----------------------------
def predict_role(skills):

    skills = [s.lower() for s in skills]

    if "machine learning" in skills or "ai" in skills:
        return " AI / Machine Learning Engineer"

    elif "react" in skills or "javascript" in skills:
        return " Full Stack Web Developer"

    elif "python" in skills and "sql" in skills:
        return " Python Developer"

    elif "java" in skills:
        return " Java Developer"

    else:
        return " Software Developer"

# Streamlit app
#st.title("AI Resume Analyzer")
st.markdown("""
<h1 style='text-align:center;
color:#4F8BF9;
font-size:45px;'>
 AI Resume Analyzer
</h1>

<h4 style='text-align:center;
color:gray;'>
Upload Resume • Compare with Job Description • ATS Score Prediction
</h4>

<hr>
""", unsafe_allow_html=True)

st.write("Upload your resume and compare it with a job description.")

# Upload resume
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Job description input
job_description = st.text_area("Paste Job Description")

if uploaded_file is not None:
    # Extract resume text
    resume_text = extract_text_from_pdf(uploaded_file)

    st.subheader("Extracted Resume Text")
    st.write(resume_text)

    # Extract skills from resume
    resume_skills = extract_skills(resume_text)

    #st.subheader("Skills Found in Resume")
    #st.write(resume_skills)

    # Process job description
    if job_description.strip() != "":

        # Extract skills from job description
        job_skills = extract_skills(job_description)

        # Calculate scores
        skill_score = calculate_skill_score(resume_skills, job_skills)
        text_score = calculate_text_similarity(resume_text, job_description)
        final_score = calculate_final_score(skill_score, text_score)

        # Calculate ATS metrics
        ats_score = calculate_ats_score(resume_text, resume_skills)
        rating = get_resume_rating(final_score)
        strength = resume_strength(final_score)
        completeness = resume_completeness(resume_text)

    # ---------------- Dashboard ----------------
    st.markdown("---")
    #st.header("📊 Resume Analysis Dashboard")
    st.markdown("""
<h2 style='text-align:center;color:#4F8BF9;'>
📊 Resume Analysis Dashboard
</h2>
""", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🎯 Match Score", f"{final_score}%")
        st.progress(final_score/100)
    with col2:
        st.metric("🛡 ATS Score", f"{ats_score}/100")
        st.progress(ats_score/100)
    with col3:
        st.metric("⭐ Rating", rating)
    with col4:
        st.metric("💪 Strength", strength)

    # ---------------- Score Breakdown --- -------------
    st.markdown("---")
    st.subheader("📈 Score Breakdown")

    st.write(f"**Skill Match (60% Weight):** {skill_score}%")
    st.write(f"**Overall Text Similarity (40% Weight):** {text_score}%")

    # ---------------- Skills ----------------
    

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("✅ Skills Found")

        if resume_skills:
            for skill in resume_skills:
                st.success(skill)
        else:
            st.warning("No skills detected.")

    with col4:
        st.subheader("❌ Missing Skills")

        missing_skills = [skill for skill in job_skills if skill not in resume_skills]

        if missing_skills:
            for skill in missing_skills:
                st.error(skill)
        else:
            st.success("No missing skills found!")
    # ---------------- Resume Sections ----------------
    st.markdown("---")

    with st.expander("📂 Resume Sections"):

        sections = check_sections(resume_text)

        for section, present in sections.items():

            if present:
                st.success(f"✔ {section}")
            else:
                st.error(f"✘ {section}")

    sections = check_sections(resume_text)

    for section, present in sections.items():

        if present:
            st.success(f"✔ {section}")
        else:
            st.error(f"✘ {section}")

    # ---------------- Job Role ----------------
    role = predict_role(resume_skills)
    st.markdown("---")

    with st.expander("💼 Predicted Job Role"):

        st.success(f"🎯 {role}") 

    # ---------------- Feedback ----------------
    st.markdown("---")

    st.subheader("📢 Resume Feedback")

    if final_score >= 80:
        st.success("Excellent Resume! You are highly suitable for this job.")

    elif final_score >= 60:
        st.warning("Good Resume. Add the missing skills to improve your chances.")

    else:
        st.error("Your resume needs improvement. Add more relevant skills and projects.")  
