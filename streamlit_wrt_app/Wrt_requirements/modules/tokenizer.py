
import re

def clean_text(text: str) -> str:
    """清理非法字符、空格等，统一格式"""
    return text.replace("\u202f", " ").replace("\xa0", " ").strip()

def tokenize_words(text: str) -> list:
    """分词，返回单词列表（小写处理）"""
    return re.findall(r"\b[a-zA-Z'-]+\b", text.lower())

def count_paragraphs(text: str) -> int:
    """统计段落数"""
    paragraphs = [p for p in text.split("\n") if p.strip()]
    return len(paragraphs)

def count_sentences(text: str) -> int:
    """统计句子数量（按标点划分）"""
    sentences = re.split(r"[.!?]+\s+", text.strip())
    return len([s for s in sentences if len(s.strip().split()) > 2])

def basic_stats(text: str) -> dict:
    """返回段落数、句子数、总词数、不重复词数"""
    cleaned = clean_text(text)
    words = tokenize_words(cleaned)
    return {
        "paragraph_count": count_paragraphs(cleaned),
        "sentence_count": count_sentences(cleaned),
        "word_count": len(words),
        "unique_word_count": len(set(words)),
        "word_list": words
    }
