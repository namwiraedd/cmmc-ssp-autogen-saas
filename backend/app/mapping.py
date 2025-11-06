# backend/app/mapping.py
import json, os
from sentence_transformers import SentenceTransformer, util

class CMMCMapper:
    def __init__(self):
        # load control corpus (docs/cmmc_controls.json)
        base = os.path.join(os.path.dirname(__file__), "..", "docs")
        self.controls = json.load(open(os.path.join(base, "cmmc_controls.json")))
        # small sentence transformer for semantic matching; swap for API embeddings in prod
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.control_texts = [c["text"] for c in self.controls]
        self.control_embeddings = self.model.encode(self.control_texts, convert_to_tensor=True)

    def map_text_to_controls(self, text: str, top_k:int=3):
        # split input into chunks & embed
        chunks = [text[i:i+2000] for i in range(0, len(text), 2000)]
        chunk_embs = self.model.encode(chunks, convert_to_tensor=True)
        results = {}
        for i, emb in enumerate(chunk_embs):
            hits = util.semantic_search(emb, self.control_embeddings, top_k=top_k)[0]
            for h in hits:
                idx = h["corpus_id"]
                sim = h["score"]
                ctrl = self.controls[idx]
                results.setdefault(ctrl["id"], {"control":ctrl, "score":0, "evidence":[]})
                results[ctrl["id"]]["score"] = max(results[ctrl["id"]]["score"], sim)
                results[ctrl["id"]]["evidence"].append({"chunk_index": i, "sim": sim})
        return list(results.values())
