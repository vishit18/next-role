from flask import Flask, request, render_template_string
from pathlib import Path
import tempfile

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from docx import Document
import PyPDF2

app = Flask(__name__)

def extract_text(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    try:
        if suffix == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        elif suffix == ".pdf":
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                return "\n".join([page.extract_text() or "" for page in reader.pages])
        elif suffix == ".docx":
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        else:
            return ""
    except Exception:
        return ""

def score_resumes_fixed(jd_text, resume_texts):
    vectorizer = TfidfVectorizer(stop_words="english")
    # Fit vectorizer only on JD text
    vectorizer.fit([jd_text])
    jd_vector = vectorizer.transform([jd_text])

    # Transform resumes using the same vectorizer (no refit)
    resume_vectors = vectorizer.transform(resume_texts)

    similarity_scores = cosine_similarity(jd_vector, resume_vectors)[0]
    return similarity_scores

def convert_to_10pt(score, max_score):
    if max_score == 0:
        return 0
    return round((score / max_score) * 10, 2)

@app.route("/", methods=["GET"])
def home():
    return render_template_string("""
    <html>
    <head>
        <title>NextRole Matcher</title>
        <style>
            body {
                font-family: sans-serif;
                background: #f7f7f7;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 40px;
            }
            form {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                width: 400px;
            }
            input, button {
                margin-top: 10px;
                width: 100%;
            }
            h2 {
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <h2>NextRole Resume Matcher</h2>
        <form method="POST" action="/match" enctype="multipart/form-data">
            <label>Job Description (.pdf or .docx or .txt):</label><br>
            <input type="file" name="jd" required><br><br>

            <label>Resumes (.pdf or .docx or .txt, multiple allowed):</label><br>
            <input type="file" name="resumes" multiple required><br><br>

            <button type="submit">Match</button>
        </form>
    </body>
    </html>
    """)

@app.route("/match", methods=["POST"])
def match():
    if 'jd' not in request.files:
        return "Missing job description file", 400

    jd_file = request.files['jd']
    resumes = request.files.getlist("resumes")

    if not resumes:
        return "No resumes uploaded", 400

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        jd_path = tmpdir / jd_file.filename
        jd_file.save(jd_path)
        jd_text = extract_text(jd_path)

        resume_texts = []
        filenames = []
        for resume_file in resumes:
            resume_path = tmpdir / resume_file.filename
            resume_file.save(resume_path)
            text = extract_text(resume_path)
            resume_texts.append(text)
            filenames.append(resume_file.filename)

        similarity_scores = score_resumes_fixed(jd_text, resume_texts)
        max_score = max(similarity_scores) if similarity_scores.size > 0 else 0

        results = []
        for fname, score in zip(filenames, similarity_scores):
         score_10pt = convert_to_10pt(score, max_score)
         results.append({
        "filename": fname,
        "cosine": round(score, 4),
        "score_10pt": score_10pt
    })

# Sort results by cosine similarity descending
        results.sort(key=lambda x: x["cosine"], reverse=True)


    return render_template_string("""
    <html>
    <head>
        <title>Results - NextRole</title>
        <style>
            body {
                font-family: sans-serif;
                background: #f7f7f7;
                padding: 40px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            table {
                border-collapse: collapse;
                width: 600px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            th, td {
                text-align: center;
                padding: 12px;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #f2f2f2;
            }
            h2 {
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <h2>Match Results</h2>
        <table>
            <tr>
                <th>Resume</th>
                <th>Cosine Similarity</th>
                <th>Score (out of 10)</th>
            </tr>
            {% for r in results %}
            <tr>
                <td>{{ r.filename }}</td>
                <td>{{ r.cosine }}</td>
                <td>{{ r.score_10pt }}</td>
            </tr>
            {% endfor %}
        </table>
        <br>
        <a href="/">Back to Upload</a>
    </body>
    </html>
    """, results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

