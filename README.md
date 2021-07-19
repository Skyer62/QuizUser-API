# QuizUser API
API для системы опросов пользователей.
# Стек технологий
- Python + Django REST Framework
- Simple JWT - работа с токеном
- SQLite3 - база данных
# Установка
1. Клонирйте репозиторий с проектом
```sh
https://github.com/vadim62/quiz_user_api
```
2. В созданной директории установите виртуальное окружение, активируйте его и установите необходимые зависимости:
```sh
python -m venv venv

. venv/bin/activate

pip install -r requirements.txt
```
3. Создайте и выполните миграции:
```sh
python manage.py makemigrations

python manage.py migrate
```
4. Загрузите тестовые данные:
```sh
python manage.py loaddata fixtures.json
```
5. Запуск проекта:
```sh
python manage.py runserver
```

Полная документация (redoc.yaml) доступна по адресу http://127.0.0.1/redoc/

Автоматически сгенерированная документация http://127.0.0.1/api/swagger/
