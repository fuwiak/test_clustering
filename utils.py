import streamlit as st
import pandas as pd


def load_data():
    text_file = st.sidebar.file_uploader("Загрузите текстовый файл",type=["xlsx", "xls"])
    if text_file is None:
        st.sidebar.warning("No file uploaded.")

    else:
        try:
            df = pd.read_excel(text_file)
        except ValueError:
            st.sidebar.error(
               "Неверный файл. Пожалуйста, загрузите текстовый файл.")

def save_dataframe(posts: pd.DataFrame, group_name: str, type_file: str):
    """Save DataFrame to file.
    """
    if type_file == "csv":
        posts.to_csv(f"{group_name}.csv", index=False)
    elif type_file in ("xlsx", "xls"):
        posts.to_excel(f"{group_name}.xlsx", index=False)
    else:
        raise ValueError("Неверный тип файла.")

    st.write("Посты успешно получены.")
