import os
import glob
import sys
from app.matcher import match_resume_to_jd

# Constants for data folders
JD_FOLDER = "data/job_descriptions"
RESUMES_FOLDER = "data/test_resumes"

def exit_with_message(msg):
    print(f"Error: {msg}")
    sys.exit(1)

def check_required_folders():
    if not os.path.exists(JD_FOLDER):
        exit_with_message(f"Job Descriptions folder '{JD_FOLDER}' not found. Please create and add your JD files.")
    if not os.path.exists(RESUMES_FOLDER):
        exit_with_message(f"Resumes folder '{RESUMES_FOLDER}' not found. Please create and add your resume files.")

    if len(os.listdir(JD_FOLDER)) == 0:
        exit_with_message(f"No job description files found in '{JD_FOLDER}'. Please add your JD files before running.")
    if len(os.listdir(RESUMES_FOLDER)) == 0:
        exit_with_message(f"No resumes found in '{RESUMES_FOLDER}'. Please add your resume files before running.")

def list_files(folder, pattern="*.txt"):
    files = sorted(glob.glob(os.path.join(folder, pattern)))
    return files

def pick_file_interactive(files, prompt):
    print(f"\nAvailable files to choose from ({len(files)}):")
    for i, f in enumerate(files, start=1):
        print(f"{i}. {os.path.basename(f)}")
    while True:
        choice = input(f"{prompt} (enter number): ").strip()
        if not choice.isdigit():
            print("Invalid input. Please enter a number.")
            continue
        idx = int(choice)
        if 1 <= idx <= len(files):
            return files[idx - 1]
        else:
            print(f"Please enter a number between 1 and {len(files)}.")

def load_text_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    import argparse

    check_required_folders()

    parser = argparse.ArgumentParser(description="Match resumes against a job description.")
    parser.add_argument("--jd", type=str, help="Path to the Job Description text file")
    parser.add_argument("--resumes", type=str, help="Path to folder containing resume files (optional)")
    args = parser.parse_args()

    jd_path = None

    # Job Description file selection logic
    if args.jd:
        if not os.path.isfile(args.jd):
            exit_with_message(f"JD file '{args.jd}' does not exist.")
        jd_path = args.jd
    else:
        # Pick interactively from JD_FOLDER
        jd_files = list_files(JD_FOLDER)
        jd_path = pick_file_interactive(jd_files, "Select Job Description file")

    print(f"\nUsing Job Description file: {os.path.basename(jd_path)}")
    jd_text = load_text_file(jd_path)

    # Resumes folder (default to RESUMES_FOLDER)
    resumes_folder = args.resumes if args.resumes else RESUMES_FOLDER
    if not os.path.isdir(resumes_folder):
        exit_with_message(f"Resumes folder '{resumes_folder}' does not exist.")
    resume_files = list_files(resumes_folder)
    if len(resume_files) == 0:
        exit_with_message(f"No resumes found in '{resumes_folder}'. Please add resume files before running.")

    print(f"Found {len(resume_files)} resumes in '{resumes_folder}'. Starting matching...")

    # Run matching for each resume
    for resume_path in resume_files:
        resume_text = load_text_file(resume_path)
        score = match_resume_to_jd(jd_text, resume_text)
        print(f"Score for {os.path.basename(resume_path)}: {score:.2f}")

if __name__ == "__main__":
    print("\nWelcome to NextRole Resume Matcher CLI")
    print("Make sure you have added your Job Descriptions in 'data/job_descriptions/'")
    print("and your resumes in 'data/test_resumes/' before running this script.\n")
    main()
