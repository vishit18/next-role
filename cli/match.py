import os
import sys
import glob
import argparse
from app.matcher import score_resumes, convert_to_10pt
from app.parser import parse_pdf_to_text  # Assuming you have a parser function for PDF

def load_text_file(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_resume_texts(resumes_folder):
    resume_texts = []
    resume_files = glob.glob(os.path.join(resumes_folder, '*.pdf'))
    resume_files += glob.glob(os.path.join(resumes_folder, '*.txt'))

    if not resume_files:
        print(f"Error: No resume files (.pdf or .txt) found in folder '{resumes_folder}'.")
        print("Please add your own resume files as described in the README.")
        sys.exit(1)

    for file in resume_files:
        ext = os.path.splitext(file)[1].lower()
        if ext == '.pdf':
            # parse PDF to text using your parser function
            text = parse_pdf_to_text(file)
            if text.strip():
                resume_texts.append(text)
            else:
                print(f"Warning: PDF '{file}' is empty after parsing.")
        elif ext == '.txt':
            with open(file, 'r', encoding='utf-8') as f:
                resume_texts.append(f.read())
        else:
            print(f"Skipping unsupported file type: {file}")

    if not resume_texts:
        print(f"Error: No readable resume texts found in '{resumes_folder}'.")
        sys.exit(1)
    return resume_texts

def main():
    parser = argparse.ArgumentParser(description="Match resumes to a job description.")
    parser.add_argument('--jd', type=str, required=True, help="Path to job description text file")
    parser.add_argument('--resumes', type=str, required=True, help="Folder containing resume files (.pdf or .txt)")
    args = parser.parse_args()

    jd_text = load_text_file(args.jd)
    resumes = load_resume_texts(args.resumes)

    scores = score_resumes(jd_text, resumes)
    scaled_scores = [convert_to_10pt(score) for score in scores]

    # Print scores with resume file names
    print(f"\nMatching results for job description: {args.jd}\n")
    resume_files = glob.glob(os.path.join(args.resumes, '*.pdf')) + glob.glob(os.path.join(args.resumes, '*.txt'))
    for fname, score in sorted(zip(resume_files, scaled_scores), key=lambda x: x[1], reverse=True):
        print(f"{os.path.basename(fname)} : {score}/10")

if __name__ == '__main__':
    main()
