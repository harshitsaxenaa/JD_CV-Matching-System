from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def match_cvs_to_jd(jd_text, cv_texts):
    jd_emb = model.encode(jd_text, convert_to_tensor=True)
    results = {}

    for cv_filename, cv_text in cv_texts:
        cv_emb = model.encode(cv_text, convert_to_tensor=True)
        score = util.pytorch_cos_sim(jd_emb, cv_emb)

        if score.dim() > 0:
            score = score.mean().item() 

        results[cv_filename] = {'match_score': score*100}

    return results
