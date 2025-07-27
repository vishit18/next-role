import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import glob
import pandas as pd
from app.matcher import score_resumes, convert_to_10pt

def load_text_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_resumes(resumes_folder: str) -> dict[str, str]:
    resumes = {}
    # Support .txt and .pdf if you add PDF parsing later; for now only .txt
    for filepath in glob.glob(os.path.join(resumes_folder, '*.txt')):
        with open(filepath, 'r', encoding='utf-8') as f:
            resumes[os.path.basename(filepath)] = f.read()
    return resumes

def check_path_exists(path: str, is_dir: bool = False):
    if not os.path.exists(path):
        what = "folder" if is_dir else "file"
        print(f"Error: The specified {what} '{path}' does not exist.")
        print("Please add your own files as described in the README.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Match resumes to a job description")
    parser.add_argument('--jd', required=True, help="Path to job description text file")
    parser.add_argument('--resumes', required=True, help="Path to folder containing resume text files")
    args = parser.parse_args()

    # Check paths before proceeding
    check_path_exists(args.jd, is_dir=False)
    check_path_exists(args.resumes, is_dir=True)

    jd_text = load_text_file(args.jd)
    resumes = load_resumes(args.resumes)

    if not resumes:
        print(f"Error: No resume text files found in folder '{args.resumes}'.")
        print("Please add your own resume files as described in the README.")
        sys.exit(1)

    scores = score_resumes(jd_text, list(resumes.values()))
    scaled_scores = [convert_to_10pt(score) for score in scores]

    # Create a DataFrame for pretty output
    df = pd.DataFrame({
        'Resume File': list(resumes.keys()),
        'Score (0-10)': scaled_scores
    })

    df = df.sort_values(by='Score (0-10)', ascending=False).reset_index(drop=True)
    print(df)

    # Save to CSV
    output_csv = 'resume_matching_results.csv'
    df.to_csv(output_csv, index=False)
    print(f"\nResults saved to {output_csv}")

if __name__ == "__main__":
    main()
