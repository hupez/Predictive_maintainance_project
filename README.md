
# Проект: Бинарная классификация для предиктивного обслуживания оборудования
## Описание проекта
Цель проекта — разработать модель машинного обучения, которая
предсказывает, произойдет ли отказ оборудования (Target = 1) или нет
(Target = 0). Результаты работы оформлены в виде Streamlit-приложени
## Датасет
Используется датасет **"AI4I 2020 Predictive Maintenance Dataset"**,
содержащий 10 000 записей с 14 признаками. Подробное описание датасе
можно найти в 
(https://archive.ics.uci.edu/dataset/601/predictive+maintenance+data)
## Установка и запуск
1. Клонируйте репозиторий:
 git clone https://github.com/hupez/Predictive_maintainance_project.git
2. Установите зависимости:
 pip install -r requirements.txt
3. Запустите приложение:
 streamlit run app.py
## Структура репозитория
- `app.py`: Основной файл приложения.
- `analysis_and_model.py`: Страница с анализом данных и моделью.
- `presentation.py`: Страница с презентацией проекта.
- `requirements.txt`: Файл с зависимостями.
- `predictive_maintenance.csv`: Файл с данными.
- `README.md`: Описание проекта.
- `video.mp4`: Видео-демонстрации реализации проекта
## Видео демонстрация
[<video src="video.mp4" controls width="100%"></video>](https://drive.google.com/file/d/1WUWM6N4x0cT_JxK2M79kCXtSW4_Ms6L9/view?usp=drive_link)
