
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def match_cvs_to_jd(jd_text, cv_text):
    jd_emb = model.encode(jd_text, convert_to_tensor=True)
    cv_emb = model.encode(cv_text, convert_to_tensor=True)
    score = util.pytorch_cos_sim(jd_emb, cv_emb).item()
    return score
