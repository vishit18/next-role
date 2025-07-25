import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pathlib import Path
from tkinter import Tk, filedialog

from app.parser import extract_text

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def pick_file(title="Select a file", filetypes=None):
    if filetypes is None:
        filetypes = [
            ("Text files", "*.txt"),
            ("PDF files", "*.pdf"),
            ("Word documents", "*.docx"),
        ]
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    root.update()
    return Path(file_path) if file_path else None


def pick_files(title="Select one or more resume files"):
    root = Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(
        title=title,
        filetypes=[
            ("Documents", "*.pdf *.docx *.txt"),
        ],
    )
    root.update()
    return [Path(p) for p in file_paths] if file_paths else []


def score_resumes(jd_text, resume_texts):
    vectorizer = TfidfVectorizer(stop_words="english")
    vectorizer.fit([jd_text])
    jd_vector = vectorizer.transform([jd_text])
    resume_vectors = vectorizer.transform(resume_texts)
    similarities = cosine_similarity(jd_vector, resume_vectors)[0]
    return similarities.tolist()


def convert_to_10pt(score, max_score):
    if max_score == 0:
        return 0
    return round((score / max_score) * 10, 2)


if __name__ == "__main__":
    print("Starting Job Description file picker...")
    jd_path = pick_file("Select Job Description file")
    if not jd_path:
        print("No job description file selected. Exiting.")
        exit(1)

    print("Starting Resume files picker...")
    resume_paths = pick_files("Select one or more resume files")
    if not resume_paths:
        print("No resumes selected. Exiting.")
        exit(1)

    print("Extracting text from Job Description and resumes...")
    jd_text = extract_text(jd_path)
    resume_texts = [extract_text(p) for p in resume_paths]

    print("Scoring resumes...")
    scores = score_resumes(jd_text, resume_texts)

    max_score = max(scores) if scores else 0

    results = [
        (p.name, convert_to_10pt(score, max_score), score)
        for p, score in zip(resume_paths, scores)
    ]
    results.sort(key=lambda x: x[1], reverse=True)

    print("\nResume Scores (Highest to Lowest):")
    for fname, score_10pt, raw_score in results:
        print(f"{fname}: {score_10pt}/10 (cosine: {round(raw_score, 4)})")
