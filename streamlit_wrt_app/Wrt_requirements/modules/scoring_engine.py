
import pandas as pd

def load_scoring_matrix(excel_path):
    return pd.read_excel(excel_path)

def evaluate_band_scores(metrics: dict, rule_df: pd.DataFrame) -> dict:
    results = {}
    default_start = 6.5  # 默认中位起评分

    for dimension in rule_df["评分维度"].unique():
        sub_df = rule_df[rule_df["评分维度"] == dimension]
        score = default_start
        reasons = []

        for _, row in sub_df.iterrows():
            field = row["系统字段"]
            suggestion = row["不满足时评分建议"]
            standard = str(row["明确标准"])

            if field not in metrics:
                continue

            value = metrics[field]

            try:
                if "≥" in standard:
                    thresh = float(standard.split("≥")[-1].split("；")[0].strip())
                    if value >= thresh and "加分" in suggestion:
                        score = min(score + 0.5, 9.0)
                        reasons.append(f"{row['检测项']}：{value} ≥ {thresh} → 加分 +0.5")
                    elif value < thresh and "≤" in suggestion:
                        down = float(suggestion.split("≤")[-1])
                        score = min(score, down)
                        reasons.append(f"{row['检测项']}：{value} < {thresh} → 降至 ≤{down}")
                elif "≤" in standard:
                    thresh = float(standard.split("≤")[-1].strip('% '))
                    if value > thresh and "≤" in suggestion:
                        down = float(suggestion.split("≤")[-1])
                        score = min(score, down)
                        reasons.append(f"{row['检测项']}：{value} > {thresh} → 降至 ≤{down}")
                elif "存在" in standard:
                    if not value and "≤" in suggestion:
                        down = float(suggestion.split("≤")[-1])
                        score = min(score, down)
                        reasons.append(f"{row['检测项']}：未满足 → 降至 ≤{down}")
            except Exception as e:
                reasons.append(f"[错误] {row['检测项']}：{e}")

        results[dimension] = {
            "score": round(score, 1),
            "reasons": reasons
        }

    return results
