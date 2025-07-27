import sys
import os
from pathlib import Path

print("Environment variables:", dict(os.environ))  # DEBUG: shows all env vars

CI_MODE = os.environ.get("CI", "").lower() == "true" or os.environ.get("RUN_IN_CI", "").lower() == "true"

if CI_MODE:
    print("Running in CI mode, using CLI file selectors.")
else:
    print("Running in local mode with GUI.")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.parser import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def cli_pick_file_from_folder(folder_path: Path, extension="*.txt", prompt="Select a file"):
    files = sorted(folder_path.glob(extension))
    if not files:
        print(f"[CI] No files found in '{folder_path}' with extension '{extension}'. Exiting.")
        exit(1)

    print(f"\nAvailable files in '{folder_path}':")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f.name}")

    choice = input(f"{prompt} (enter number): ")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(files):
            return files[idx]
        else:
            print("Invalid selection number. Exiting.")
            exit(1)
    except ValueError:
        print("Invalid input, please enter a number. Exiting.")
        exit(1)


def pick_file(title="Select a file", filetypes=None):
    if CI_MODE:
        jd_folder = Path("data/job_descriptions")
        return cli_pick_file_from_folder(jd_folder, "*.txt", "Choose the Job Description file")

    try:
        from tkinter import Tk, filedialog

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
    except Exception as e:
        print("GUI not supported. Exiting.")
        print(e)
        return None


def cli_pick_multiple_files_from_folder(folder_path: Path, extensions=("*.pdf", "*.docx", "*.txt"), prompt="Select files"):
    files = []
    for ext in extensions:
        files.extend(folder_path.glob(ext))
    files = sorted(files)
    if not files:
        print(f"[CI] No files found in '{folder_path}' with extensions {extensions}. Exiting.")
        exit(1)

    print(f"\nAvailable resume files in '{folder_path}':")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f.name}")

    print("Enter the numbers of the resumes you want to select, separated by commas (e.g., 1,3,5):")
    choice = input("Your choice: ")
    try:
        indices = [int(x.strip()) - 1 for x in choice.split(",")]
        selected = []
        for idx in indices:
            if 0 <= idx < len(files):
                selected.append(files[idx])
            else:
                print(f"Invalid index: {idx+1}. Ignoring.")
        if not selected:
            print("No valid resumes selected. Exiting.")
            exit(1)
        return selected
    except ValueError:
        print("Invalid input, please enter numbers separated by commas. Exiting.")
        exit(1)


def pick_files(title="Select one or more resume files"):
    if CI_MODE:
        resumes_folder = Path("data/test_resumes/resumes")
        return cli_pick_multiple_files_from_folder(resumes_folder, ("*.pdf", "*.docx", "*.txt"), "Choose resume files")

    try:
        from tkinter import Tk, filedialog

        root = Tk()
        root.withdraw()
        file_paths = filedialog.askopenfilenames(
            title=title,
            filetypes=[("Documents", "*.pdf *.docx *.txt")],
        )
        root.update()
        return [Path(p) for p in file_paths] if file_paths else []
    except Exception as e:
        print("GUI not supported. Exiting.")
        print(e)
        return []


def score_resumes(jd_text, resume_texts):
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
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
