import streamlit as st
import os
import sys
import json
import docx
import re
import pandas as pd
from docx import Document
from datetime import datetime
from io import BytesIO

# 添加模块路径
BASE_DIR = os.path.dirname(__file__)
MODULE_PATH = os.path.join(BASE_DIR, "Wrt_requirements", "modules")
sys.path.append(MODULE_PATH)

from formatter_ai import (
    load_text_from_file,
    guess_task_type,
    get_feedback_from_deepseek,
    save_feedback_to_docx
)
from tokenizer import basic_stats
from vocab_analysis import load_wordlist, analyze_vocab_levels
from coherence_analysis import load_linking_words, analyze_coherence
from scoring_engine import load_scoring_matrix, evaluate_band_scores

# 初始化资源路径
BASE_PATH = os.path.join(BASE_DIR, "Wrt_requirements")
wordlist_path = os.path.join(BASE_PATH, "wordlists")
criteria_path = os.path.join(BASE_PATH, "criteria")

ox3000 = load_wordlist(os.path.join(wordlist_path, "oxford_3000.json"))
c1c2 = load_wordlist(os.path.join(wordlist_path, "oxford5000_c1_c2.json"))
linking_dict = load_linking_words(os.path.join(wordlist_path, "linking_words.json"))
scoring_df = load_scoring_matrix(os.path.join(criteria_path, "scoring_matrix.xlsx"))

st.set_page_config(page_title="雅思作文评分系统", layout="centered")
st.title("📄 雅思作文自动评分与反馈生成")

uploaded_files = st.file_uploader(
    "请上传一篇或多篇作文文件（支持 .txt 或 .docx）", 
    type=["txt", "docx"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.info(f"共上传 {len(uploaded_files)} 篇作文。请逐一处理并下载👇")

    for idx, uploaded_file in enumerate(uploaded_files):
        with st.expander(f"📄 作文 {idx+1}：{uploaded_file.name}", expanded=False):
            file_bytes = uploaded_file.read()
            suffix = uploaded_file.name.split(".")[-1]

            if suffix == "txt":
                text = file_bytes.decode("utf-8")
            else:
                doc = Document(BytesIO(file_bytes))
                text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

            st.text_area("✍️ 作文内容预览", value=text, height=200, key=f"preview_{idx}")

            if st.button(f"🚀 开始评分：{uploaded_file.name}", key=f"process_{idx}"):
                with st.spinner("正在生成反馈，请稍候..."):
                    task_type = guess_task_type(text)
                    basic = basic_stats(text)
                    word_list = basic["word_list"]
                    vocab = analyze_vocab_levels(word_list, ox3000, c1c2)
                    coherence = analyze_coherence(text, linking_dict)
                    metrics = {
                        **basic,
                        **vocab,
                        **coherence,
                        "has_position": "i think" in text.lower() or "i believe" in text.lower()
                    }

                    band_scores = evaluate_band_scores(metrics, scoring_df)

                    feedback_text = get_feedback_from_deepseek(text, st.secrets["DEEPSEEK_API_KEY"], task_type=task_type)

                    output_doc = BytesIO()
                    save_feedback_to_docx(feedback_text, output_doc, task_type, band_scores, original_text=text)
                    output_doc.seek(0)

                    now = datetime.now().strftime("%Y%m%d_%H%M")
                    filename = f"反馈_{uploaded_file.name.replace('.txt','').replace('.docx','')}_{now}.docx"

                    st.success(f"✅ {uploaded_file.name} 处理完成")
                    st.download_button("📥 下载反馈报告", output_doc, file_name=filename, key=f"download_{idx}")

#cd "D:\Python\Code\EduTech\streamlit_wrt_app"   
#streamlit run streamlit_wrt_app.py
