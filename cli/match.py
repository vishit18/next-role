import os
import sys
import argparse
from app.match import score_resumes, convert_to_10pt

# Fix import path for GitHub Actions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def match_resume_to_jd(jd_path: str, resumes_folder: str) -> list[tuple[str, float]]:
    # Load JD
    with open(jd_path, 'r', encoding='utf-8') as f:
        jd_text = f.read()

    # Collect resume files
    resume_files = [
        os.path.join(resumes_folder, f)
        for f in os.listdir(resumes_folder)
        if f.endswith('.txt')
    ]

    if not resume_files:
        raise FileNotFoundError("No .txt files found in resume folder.")

    # Read resumes
    resume_texts = []
    resume_names = []
    for file in resume_files:
        with open(file, 'r', encoding='utf-8') as f:
            resume_texts.append(f.read())
            resume_names.append(os.path.basename(file))

    # Score
    raw_scores = score_resumes(jd_text, resume_texts)
    final_scores = [convert_to_10pt(score) for score in raw_scores]

    return list(zip(resume_names, final_scores))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Match resumes to a job description.")
    parser.add_argument('--jd', type=str, required=True, help='Path to the job description file')
    parser.add_argument('--resumes', type=str, required=True, help='Path to folder containing resumes')
    args = parser.parse_args()

    results = match_resume_to_jd(args.jd, args.resumes)

    print("\nMatch Results:")
    for name, score in sorted(results, key=lambda x: x[1], reverse=True):
        print(f"{name:<30} Score: {score}/10")
