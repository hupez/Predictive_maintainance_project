import streamlit as st

st.set_page_config(page_title="Predictive Maintenance", layout="wide")

# Создаём список страниц
page_list = [
    st.Page("analysis_and_model.py", title="Анализ данных и модель", icon="📊"),
    st.Page("presentation.py", title="Презентация проекта", icon="📽️"),
]

# Навигация
current_page = st.navigation(page_list, position="sidebar", expanded=True)
current_page.run()