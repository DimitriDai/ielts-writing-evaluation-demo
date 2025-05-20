
import json
import re
from collections import Counter

def load_linking_words(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def count_linking_words(text, linking_dict):
    text = text.lower()
    category_counts = {}
    total_count = 0

    for category, phrases in linking_dict.items():
        count = sum(len(re.findall(r"\\b" + re.escape(phrase.lower()) + r"\\b", text)) for phrase in phrases)
        category_counts[category] = count
        total_count += count

    used_categories = sum(1 for c in category_counts.values() if c > 0)
    diversity_score = round(used_categories / len(linking_dict), 3) if linking_dict else 0

    return {
        "total_linking_words": total_count,
        "linking_category_counts": category_counts,
        "linking_diversity_score": diversity_score
    }

def analyze_coherence(text, linking_dict):
    paragraph_count = len([p for p in text.split("\n") if p.strip()])
    linking_result = count_linking_words(text, linking_dict)
    return {
        "paragraph_count": paragraph_count,
        **linking_result
    }
