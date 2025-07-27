import os
from app.match import score_resumes, convert_to_10pt

def match_resume_to_jd(jd_path: str, resumes_folder: str) -> list[tuple[str, float]]:
    # Load the JD text
    with open(jd_path, 'r', encoding='utf-8') as f:
        jd_text = f.read()

    # Collect resume file paths
    resume_files = [
        os.path.join(resumes_folder, f)
        for f in os.listdir(resumes_folder)
        if f.endswith(".txt")
    ]

    if not resume_files:
        raise FileNotFoundError("No .txt resumes found in the specified folder.")

    # Read resume contents
    resume_texts = []
    resume_names = []

    for file in resume_files:
        with open(file, 'r', encoding='utf-8') as f:
            resume_texts.append(f.read())
            resume_names.append(os.path.basename(file))

    # Score and convert to 10-pt scale
    raw_scores = score_resumes(jd_text, resume_texts)
    scaled_scores = [convert_to_10pt(score) for score in raw_scores]

    return list(zip(resume_names, scaled_scores))
