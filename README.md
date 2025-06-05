## Структура проекта
### /tf-idf
    - tfidf_app # Основное приложение
    - Dockerfile # Конфигурация Docker
    - .example.env # Шаблон переменных окружения
    - README.md # Описание проекта
    - docker-compose.yml # Оркестрация контейнеров
    - entrypoint.prod.sh Конфигурации точки входа при сборке приложения
    - nginx.conf # Конфигурация nginx
    - requirements.txt # Зависимости Python

## Запуск приложения
### Зависимости
    - Docker 28.2+
    - docker-compose 2.19+
    - PostgreSQL 17+

### Запуск 
    - Скопировать конфиг: 'cp .example.env .env.prod'
    - Заполнить параметры в '.env.prod'
    - Запустить: 'docker compose up --build'
    - Приложение будет доступно на порту 8001

### Конфигурируемые параметры 
    - Параметры настраиваются в '.env.prod':
    # Django Settings
    - DEBUG: режим отладки  - по умолчанию False
    - SECRET_KEY: секретный ключ для api
    - DJANGO_ALLOWED_HOSTS: допустимые хосты
    - DJANGO_CSRF_TRUSTED_ORIGINS
    
    # Database Settings
    - DATABASE_NAME: название базы данных - должно совподать с POSTGRES_DB
    - DATABASE_USERNAME: имя пользователя для базы данных - должно совподать с POSTGRES_USER
    - DATABASE_PASSWORD: пароль базы данных - должно совподать с POSTGRES_PASSWORD
    - DATABASE_HOST: хост базы данных
    - DATABASE_PORT: порт базы данных - по умолчанию 5432
    
    # Postgres Settings
    - POSTGRES_DB: название базы данных
    - POSTGRES_USER: имя пользователя для базы данных
    - POSTGRES_PASSWORD: пароль базы данных