# 🤖 AI Resume Analyzer

An intelligent web-based application that analyzes resumes and compares them with job descriptions to help users improve their resumes and increase their chances of getting shortlisted.

The application extracts text from PDF resumes, identifies relevant skills, calculates a resume match score, evaluates ATS compatibility, predicts a suitable job role, checks resume completeness, and provides useful resume insights through an interactive dashboard.

---

## 📌 Project Overview

In today's competitive job market, many companies use Applicant Tracking Systems (ATS) to automatically screen resumes before they are reviewed by recruiters.

The **AI Resume Analyzer** helps students, fresh graduates, and job seekers understand how well their resume matches a particular job description.

The system uses Natural Language Processing (NLP) techniques such as **TF-IDF Vectorization** and **Cosine Similarity** to compare resume content with job requirements.

---

## 🎯 Objectives

The main objectives of this project are:

- Extract text from PDF resumes automatically.
- Identify technical skills from resumes.
- Compare resumes with job descriptions.
- Calculate an overall resume match score.
- Evaluate ATS compatibility.
- Check resume completeness.
- Predict a suitable job role based on detected skills.
- Provide useful feedback for resume improvement.
- Provide an interactive and user-friendly dashboard.

---

## ✨ Key Features

### 📄 Resume Upload
Users can upload their resume in PDF format.

### 🔍 Resume Text Extraction
The application extracts readable text from the uploaded PDF using PyPDF2.

### 🛠️ Skill Extraction
The system identifies predefined technical and soft skills such as:

- Python
- Java
- C++
- HTML
- CSS
- JavaScript
- SQL
- Git
- Machine Learning
- AI
- Data Analysis
- Streamlit
- MySQL
- React
- Node.js
- REST API
- AWS
- Docker
- Kubernetes
- Communication
- Problem Solving

### 🎯 Resume Match Score

The final match score is calculated using:

- **60% Skill Matching**
- **40% Overall Text Similarity**

Formula:

```text
Final Score =
(0.60 × Skill Score) +
(0.40 × Text Similarity Score)
