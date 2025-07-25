from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def score_resumes(jd_text: str, resumes: list[str]) -> list[float]:
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([jd_text] + resumes)
    similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    return similarities.tolist()

def convert_to_10pt(score: float) -> float:
    return round(score * 10, 2)
