import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_curve, roc_auc_score

def analysis_and_model_page():
    st.title("📊 Анализ данных и модель предиктивного обслуживания")

    # -------------------- ЗАГРУЗКА ДАННЫХ --------------------
    @st.cache_data
    def load_data():
        try:
            from ucimlrepo import fetch_ucirepo
            dataset = fetch_ucirepo(id=601)
            data = pd.concat([dataset.data.features, dataset.data.targets], axis=1)
            return data
        except:
            uploaded = st.file_uploader("Загрузите CSV-файл с данными", type="csv")
            if uploaded:
                return pd.read_csv(uploaded)
            else:
                st.warning("Пожалуйста, загрузите файл predictive_maintenance.csv")
                return None

    data = load_data()
    if data is None:
        return

    # -------------------- ПРЕДОБРАБОТКА --------------------
    with st.spinner("Предобработка данных..."):
        cols_to_drop = ['UDI', 'Product ID', 'TWF', 'HDF', 'PWF', 'OSF', 'RNF']
        data = data.drop(columns=[col for col in cols_to_drop if col in data.columns])

        if 'Type' in data.columns:
            le = LabelEncoder()
            data['Type'] = le.fit_transform(data['Type'])  # L=0, M=1, H=2

        target_col = 'Machine failure' if 'Machine failure' in data.columns else 'Target'
        if target_col not in data.columns:
            st.error("Целевая переменная не найдена.")
            return

        X = data.drop(columns=[target_col])
        y = data[target_col]

        # Определяем числовые колонки для масштабирования (все, кроме Type)
        numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
        if 'Type' in numeric_cols:
            numeric_cols.remove('Type')

        # Масштабирование
        scaler = StandardScaler()
        X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # -------------------- ВЫБОР МОДЕЛИ И ОБУЧЕНИЕ --------------------
    st.sidebar.header("Настройки модели")
    model_name = st.sidebar.selectbox(
        "Выберите модель",
        ["Логистическая регрессия", "Random Forest", "XGBoost", "SVM (линейный)"]
    )

    with st.spinner(f"Обучение модели {model_name}..."):
        if model_name == "Логистическая регрессия":
            model = LogisticRegression(random_state=42, class_weight='balanced')
        elif model_name == "Random Forest":
            model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
        elif model_name == "XGBoost":
            model = XGBClassifier(n_estimators=100, learning_rate=0.1, random_state=42, use_label_encoder=False, eval_metric='logloss')
        else:
            model = SVC(kernel='linear', random_state=42, probability=True, class_weight='balanced')

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        accuracy = accuracy_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)
        class_report = classification_report(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_proba)

    # -------------------- ОТОБРАЖЕНИЕ РЕЗУЛЬТАТОВ --------------------
    st.header("📈 Результаты обучения модели")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Accuracy", f"{accuracy:.4f}")
        st.metric("ROC-AUC", f"{roc_auc:.4f}")
    with col2:
        st.text("Classification Report:")
        st.code(class_report)

    st.subheader("Матрица ошибок")
    fig, ax = plt.subplots()
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', ax=ax,
                xticklabels=['Нет отказа', 'Отказ'], yticklabels=['Нет отказа', 'Отказ'])
    ax.set_xlabel("Предсказано")
    ax.set_ylabel("Фактически")
    st.pyplot(fig)

    fpr, tpr, _ = roc_curve(y_test, y_proba)
    fig_roc, ax_roc = plt.subplots()
    ax_roc.plot(fpr, tpr, label=f'{model_name} (AUC = {roc_auc:.2f})')
    ax_roc.plot([0, 1], [0, 1], 'k--')
    ax_roc.set_xlabel("False Positive Rate")
    ax_roc.set_ylabel("True Positive Rate")
    ax_roc.set_title("ROC-кривая")
    ax_roc.legend()
    st.pyplot(fig_roc)

    # -------------------- ПРЕДСКАЗАНИЕ ДЛЯ НОВЫХ ДАННЫХ (АВТОМАТИЧЕСКОЕ ОПРЕДЕЛЕНИЕ КОЛОНОК) --------------------
    st.header("🔮 Предсказание отказа для нового оборудования")
    
    # Словарь для сопоставления пользовательских полей с именами колонок в данных
    # Ключи — это метки, которые видит пользователь, значения — список возможных подстрок в названиях колонок
    col_mapping = {
        "air_temp": ["air temperature", "air temp", "air"],
        "process_temp": ["process temperature", "process temp", "process"],
        "rotational_speed": ["rotational speed", "rotational", "speed"],
        "torque": ["torque"],
        "tool_wear": ["tool wear", "tool"]
    }

    # Функция для поиска реального имени колонки по шаблону
    def find_column_name(patterns, columns_list):
        for col in columns_list:
            col_lower = col.lower()
            for pattern in patterns:
                if pattern in col_lower:
                    return col
        return None

    # Получаем реальные имена колонок из X (кроме Type)
    actual_col_names = {}
    for key, patterns in col_mapping.items():
        found = find_column_name(patterns, X.columns)
        if found:
            actual_col_names[key] = found

    # Выводим для отладки (можно закомментировать)
    # st.write("Обнаруженные колонки:", actual_col_names)

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        with col1:
            product_type = st.selectbox("Тип продукта (Type)", ["L", "M", "H"])
            air_temp = st.number_input("Температура воздуха (K)", value=300.0, step=1.0)
            process_temp = st.number_input("Температура процесса (K)", value=310.0, step=1.0)
            rotational_speed = st.number_input("Скорость вращения (rpm)", value=1500, step=10)
        with col2:
            torque = st.number_input("Крутящий момент (Nm)", value=40.0, step=1.0)
            tool_wear = st.number_input("Износ инструмента (min)", value=100, step=5)

        submit = st.form_submit_button("Предсказать")

        if submit:
            type_map = {'L': 0, 'M': 1, 'H': 2}
            type_encoded = type_map[product_type]

            # Создаём строку данных
            input_row = {col: 0 for col in X.columns}  # заполняем нулями все колонки
            input_row['Type'] = type_encoded

            # Заполняем найденные колонки значениями из формы
            if 'air_temp' in actual_col_names:
                input_row[actual_col_names['air_temp']] = air_temp
            if 'process_temp' in actual_col_names:
                input_row[actual_col_names['process_temp']] = process_temp
            if 'rotational_speed' in actual_col_names:
                input_row[actual_col_names['rotational_speed']] = rotational_speed
            if 'torque' in actual_col_names:
                input_row[actual_col_names['torque']] = torque
            if 'tool_wear' in actual_col_names:
                input_row[actual_col_names['tool_wear']] = tool_wear

            input_df = pd.DataFrame([input_row])

            # Масштабируем числовые колонки (те, что в numeric_cols)
            input_df[numeric_cols] = scaler.transform(input_df[numeric_cols])

            # Убеждаемся, что порядок колонок совпадает с X_train
            input_final = input_df[X.columns]

            pred = model.predict(input_final)[0]
            proba = model.predict_proba(input_final)[0][1]

            if pred == 1:
                st.error(f"⚠️ **Прогноз: ОТКАЗ** (вероятность отказа: {proba:.2f})")
            else:
                st.success(f"✅ **Прогноз: НОРМАЛЬНАЯ РАБОТА** (вероятность отказа: {proba:.2f})")

if __name__ == "__main__":
    analysis_and_model_page()