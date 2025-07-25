# NextRole

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)  
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)  
[![Dockerized](https://img.shields.io/badge/dockerized-yes-blue)](#)  
[![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)](#)

---

## Intelligent Resume Matching for Faster, Fairer Hiring

---

## Project Overview

**NextRole** is a resume screening system that parses and ranks resumes against a job description using NLP. Built with production readiness in mind, it exposes both a web interface and a CLI, and is fully Dockerized. Unlike toy classifiers, NextRole focuses on similarity-based ranking with explainable scoring using TF-IDF and cosine similarity, ensuring transparency and flexibility.

---

## The Problem

Recruiters face the repetitive and error-prone task of shortlisting resumes from large applicant pools. Manual screening is time-consuming and subjective. Many AI resume screeners act as black boxes, which leads to trust issues, fairness concerns, and poor generalizability. Moreover, most existing projects are either static or lack production deployment.

---

## The Solution

- Parses real PDF resumes using `pdfminer.six` and extracts key content (skills, experience, etc.).
- Cleans and vectorizes both resumes and job descriptions using TF-IDF with `ngram_range=(1,2)` for richer context.
- Calculates similarity scores using cosine distance and scales to a 10-point system for readability.
- Offers two usage modes:
  - **Web app** (Flask-based) for non-technical users to upload resumes and job descriptions.
  - **CLI mode** for technical users or automation pipelines.
- Modular architecture (parsing, scoring, and interfaces separated).
- Fully containerized with a Dockerfile for consistent deployment across systems.

---

## Business Impact

- Saves recruiters hours by automatically shortlisting top-matching resumes.
- Enables fairer candidate evaluation based on textual alignment with the job role.
- Transparent scoring helps hiring managers understand *why* a resume ranked higher.
- Extensible for companies, consultancies, or job platforms looking to add explainable screening features.
- Shows end-to-end production skills: modular design, CLI + API modes, logging, and Docker.

---

## Project Structure

```plaintext
.
├── app/
│ ├── _init_.py 
│ ├── web.py 
│ ├── matcher.py 
│ └── parser.py 
├── cli/
│ └── match.py 
├── data/
│ ├── job_descriptions/
│ └── test_resumes/
├── tests/ 
├── Dockerfile 
├── requirements.txt
└── README.md

```

---

## Setup and Usage

### Run Locally (Non-Docker)

1. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the web app**

```bash
python app/web.py
```
Then visit: http://localhost:5000

4. **OR Run CLI to match resumes**

```bash
python cli/match.py --jd data/job_descriptions/sample_jd.txt --resumes data/test_resumes
```

## Run with Docker

1. **Build Docker image**

```bash
docker build -t next-role .
```

2. **Run container**

```bash
docker run -p 5000:5000 next-role
```

3. **Open in browser**

```bash
http://localhost:5000
```

---

## Dependencies

Main libraries include:

- Flask – web app
- scikit-learn – TF-IDF + cosine similarity
- pdfminer.six – PDF resume parsing
- pandas – tabular output and export
- numpy – vector calculations
- tqdm – CLI progress bar

---

## Results

- Scales resume scores from 0 to 10 for clearer interpretation.
- Outputs sorted CSV showing how well each resume matches the job description.
- Enables transparency via textual similarity, not black-box predictions.

---

## Why this Project?

- Built on real messy PDFs, not synthetic resume data.
- End-to-end system with both CLI and web usage — no notebook demo.
- Dockerized for production-readiness and consistent deployment.
- Aligns with Production ML Engineering from industry readiness scale.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Contact

Questions, suggestions, or collaborations welcome.

---

*Built by Vishit Jiwane*  


