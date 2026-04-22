import streamlit as st
import reveal_slides as rs

def presentation_page():
    st.title("📽️ Презентация проекта")

    presentation_markdown = """
# Предиктивное обслуживание оборудования
## Бинарная классификация отказов

---

### Актуальность
- Предиктивное обслуживание снижает простои и затраты
- Прогнозирование отказа оборудования повышает безопасность

---

### Датасет
- **AI4I 2020 Predictive Maintenance Dataset** (UCI ID 601)
- 10 000 записей, 14 признаков
- Целевая переменная: `Machine failure` (0/1)

---

### Этапы работы
1. Загрузка и предобработка данных
2. Масштабирование числовых признаков
3. Разделение на обучающую и тестовую выборки (80/20)
4. Обучение 4 моделей
5. Оценка по метрикам: Accuracy, ROC-AUC, Confusion Matrix

---

### Результаты (пример)
| Модель | Accuracy | ROC-AUC |
|--------|----------|---------|
| Logistic Regression | 0.97 | 0.98 |
| Random Forest | 0.98 | 0.99 |
| XGBoost | 0.98 | 0.99 |
| SVM | 0.97 | 0.97 |

---

### Streamlit-приложение
- **Страница 1**: анализ данных, обучение модели, предсказания
- **Страница 2**: презентация (вы здесь)

---

### Заключение
- Лучшая модель: Random Forest / XGBoost
- Возможные улучшения:
  - подбор гиперпараметров
  - учёт временных рядов
  - интеграция с реальными датчиками

---

### Спасибо за внимание!
Вопросы?
    """

    with st.sidebar:
        st.header("Настройки презентации")
        theme = st.selectbox("Тема", ["black", "white", "league", "beige", "sky", "night", "serif", "simple", "solarized"], index=0)
        height = st.number_input("Высота слайдов (px)", value=500, step=50)
        transition = st.selectbox("Переход", ["slide", "convex", "concave", "zoom", "none"], index=0)
        plugins = st.multiselect("Плагины", ["highlight", "notes", "search", "zoom"], default=["highlight"])

    # Генерация презентации
    result = rs.slides(
        presentation_markdown,
        height=height,
        theme=theme,
        config={"transition": transition, "plugins": plugins},
        markdown_props={"data-separator-vertical": "^--$"},
    )

    # Извлечение HTML из результата (библиотека возвращает словарь)
    if isinstance(result, dict):
        slides_html = result.get('html', '')
    else:
        slides_html = result

    # Кастомный CSS для отключения переносов слов
    custom_css = """
    <style>
        .reveal section {
            -webkit-hyphens: manual !important;
            -moz-hyphens: manual !important;
            hyphens: manual !important;
            word-wrap: normal !important;
        }
        .reveal p, .reveal li, .reveal h1, .reveal h2, .reveal h3, .reveal h4 {
            -webkit-hyphens: manual !important;
            -moz-hyphens: manual !important;
            hyphens: manual !important;
        }
    </style>
    """
    # Вставляем CSS перед закрывающим тегом </head>
    if "</head>" in slides_html:
        slides_html = slides_html.replace("</head>", custom_css + "</head>")
    else:
        slides_html = custom_css + slides_html

    st.markdown(slides_html, unsafe_allow_html=True)

if __name__ == "__main__":
    presentation_page()