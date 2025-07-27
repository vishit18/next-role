import os
import glob
import sys

# Add root directory to sys.path so 'app' can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.parser import parse_resume, parse_job_description
from app.matcher import match_resume_to_jd
import pandas as pd
from tqdm import tqdm

def list_txt_files(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    if not files:
        print("No job descriptions found in:", directory)
        sys.exit(1)
    print("\nSelect a job description:")
    for i, f in enumerate(files):
        print(f"{i + 1}. {f}")
    index = int(input("\nEnter the number of the job description to use: ")) - 1
    return os.path.join(directory, files[index])

def main():
    jd_path = list_txt_files("data/job_descriptions")
    resumes_folder = "data/test_resumes/resumes"
    resume_files = [
        os.path.join(resumes_folder, f)
        for f in os.listdir(resumes_folder)
        if f.endswith(".pdf")
    ]

    job_description = parse_job_description(jd_path)
    results = []

    print("\nMatching resumes...\n")
    for resume_file in tqdm(resume_files):
        resume_text = parse_resume(resume_file)
        score = match_resume_to_jd(resume_text, job_description)
        results.append({"Resume": os.path.basename(resume_file), "Score": round(score, 2)})

    df = pd.DataFrame(results).sort_values(by="Score", ascending=False)
    df.to_csv("results.csv", index=False)
    print("\nDone. Results saved to results.csv")

if __name__ == "__main__":
    main()
