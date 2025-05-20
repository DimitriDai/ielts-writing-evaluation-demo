
import json

def load_wordlist(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 修复：兼容 Oxford 3000 / 5000 词表结构
    if isinstance(data, dict):
        return set(
            entry.get("word", "").lower()
            for entry in data.values()
            if isinstance(entry, dict) and "word" in entry
        )
    elif isinstance(data, list):
        return set(
            entry["word"].lower()
            for entry in data
            if "word" in entry
        )
    else:
        return set()

def analyze_vocab_levels(word_list, oxford3000_set, c1c2_set):
    word_set = set(word_list)

    in_ox3000 = sum(1 for w in word_set if w in oxford3000_set)
    in_c1c2 = sum(1 for w in word_set if w in c1c2_set)
    other = len(word_set) - in_ox3000 - in_c1c2

    return {
        "unique_word_count": len(word_set),
        "oxford_3000_unique_count": in_ox3000,
        "oxford_c1_c2_unique_count": in_c1c2,
        "other_words_unique_count": other,
        "band7_plus_ratio": round(in_c1c2 / len(word_set), 3) if word_set else 0
    }
