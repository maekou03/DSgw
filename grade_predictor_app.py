# grade_predictor_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 成績予測アプリ")
st.write("授業ごとの出席率や試験点を入力すると、予測される成績を表示します。")

num_courses = st.slider("授業数を選んでください", 1, 10, 3)

data = []

for i in range(num_courses):
    st.subheader(f"【授業{i+1}】")
    course_name = st.text_input(f"授業名{i+1}", f"授業{i+1}")
    col1, col2 = st.columns(2)
    with col1:
        attendance = st.slider(f"出席率{i+1}", 0.0, 1.0, 0.9, step=0.01)
        report = st.slider(f"課題平均点{i+1}", 0, 100, 80)
        mid = st.slider(f"中間試験点{i+1}", 0, 100, 75)
        final = st.slider(f"期末試験点{i+1}", 0, 100, 85)
    with col2:
        ratio_att = st.slider(f"出席比率{i+1}", 0.0, 1.0, 0.1, step=0.05)
        ratio_rep = st.slider(f"課題比率{i+1}", 0.0, 1.0, 0.2, step=0.05)
        ratio_mid = st.slider(f"中間比率{i+1}", 0.0, 1.0, 0.3, step=0.05)
        ratio_fin = st.slider(f"期末比率{i+1}", 0.0, 1.0, 0.4, step=0.05)

    total_ratio = ratio_att + ratio_rep + ratio_mid + ratio_fin
    if abs(total_ratio - 1.0) > 0.01:
        st.warning(f"⚠️ 『{course_name}』の比率の合計が1.0ではありません！（現在: {total_ratio:.2f}）")

    data.append({
        "授業名": course_name,
        "出席率": attendance,
        "課題平均": report,
        "中間試験": mid,
        "期末試験": final,
        "出席比率": ratio_att,
        "課題比率": ratio_rep,
        "中間比率": ratio_mid,
        "期末比率": ratio_fin
    })

if st.button("成績を予測"):
    df = pd.DataFrame(data)
    df["予測成績"] = (
        df["出席率"] * 100 * df["出席比率"] +
        df["課題平均"] * df["課題比率"] +
        df["中間試験"] * df["中間比率"] +
        df["期末試験"] * df["期末比率"]
    )

    st.subheader("📋 予測成績一覧")
    st.dataframe(df[["授業名", "予測成績"]])

    st.subheader("📈 成績グラフ")
    fig, ax = plt.subplots()
    ax.bar(df["授業名"], df["予測成績"], color="skyblue")
    ax.set_ylim(0, 100)
    ax.set_ylabel("予測成績")
    ax.set_title("授業ごとの予測成績")
    ax.grid(True, axis='y')
    st.pyplot(fig)
