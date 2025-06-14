# Changelog

## [1.3.2]
### Добавлено:
- Новый эндпоинт для входа зарегистрированного пользователя.
  - api/v1/auth/login/
- Новый эндпоинт для выхода зарегистрированного пользователя.
  - api/v1/auth/logout/
- Новый эндпоинт для изменения пароля зарегистрированного пользователя.
  - api/v1/auth/password/change/
- Новый эндпоинт для сброса пароля зарегистрированного пользователя.
  - api/v1/auth/password/reset/
- Новый эндпоинт для подтверждения сброса пароля зарегистрированного пользователя.
  - api/v1/auth/password/reset/confirm/
- Новый эндпоинт для подтверждения email зарегистрированного пользователя.
  - api/v1/auth/registration/verify-email/
- Новый эндпоинт для регистрации нового пользователя. После регистрации требуется подтверждения email.
  - api/v1/auth/registration/
- Новый эндпоинт для удаления пользователем своего аккаунта.
  - api/v1/user/delete/
- Новый эндпоинт для удаления зарегистрированного пользователя. Удалять может только админ.
  - api/v1/user/delete/{id}/
- Приложение user для управления пользователями.
- Вью для управления удалением пользователя.
- Новые схема user_delete_schema.
- Новые зависимости в requirements.txt
### Изменено:
- Структура папок проекта.
- example.env

## [1.2.1]
### Добавлено:
- Новый эндпоинт для получения документации о приложении реализованно при помощи drf-spectacular (OpenAPI 3) и  SwaggerUi: 
  - api/
- Новая папка docs/ - в ней хранятся фабрика схем и схемы для документации api (OpenAPI 3)
  - docs/schema_factory.py - фабрика схем
  - docs/schemas.py - схемы
  - схемы - upload_response_schema, status_response_schema, api_info_response_schema, metrics_response_schema
### Изменено:
- docker-compose: монтирование staticfiles


## [1.1.1]
### Изменено:
- Dockerfile: manage.py collectstatic теперь происходит из под root юзера для устранения ошибки со сборкой статик файлов при сборке контейнера 
- docker-compose: для безопасности убран проброс портов у базы данных.


## [1.1.0]
### Добавлено:
- Новый эндпоинт для загрузки и обработки файла: 
  - api/v1/upload/
- Новый эндпоинт для получения статуса приложения: 
  - api/v1/status/
  - пример ответа: {"status": "Ok"} status_code 200 
- Новый эндпоинт для получения актуальной версии приложения: 
  - api/v1/version/
  - пример ответа: {"name": "TF-IDF API", "version": "1.0.0"} status_code 200 
- Новый эндпоинт для получения метрик обработанных файлов: 
  - api/v1/metrics/
  - пример ответа: 
    - {
    "files_processed": 4,
    "min_time_processed": 0.0,
    "avg_time_processed": 0.17025,
    "max_time_processed": 0.345,
    "latest_file_processed_timestamp": "2025-01-01 00:00:00",
    "success_files": 4,
    "peak_memory_usage": 24851.565
}
    - "files_processed": количество файлов, обработанных приложением
    - "min_time_processed": (float) минимальное время в секундах с точностью 3 знака после
запятой, затраченное на обработку файла
    - "avg_time_processed": (float) среднее время в секундах с точностью 3 знака после запятой,
затраченное на обработку файл
    - "max_time_processed": (float)максимальное время в секундах с точностью 3 знака после
запятой, затраченное на обработку файла
    - "latest_file_processed_timestamp": время обработки последнего файла в формате timestamp
    - "success_files": количество удачных обработок.
    - "peak_memory_usage": пиковая память во время выполнения расчетов в KB для отслеживания пиковой нагрузки.
- Docker контейнеризация приложения
- Поддержка переменных окружения
- Автоматическая сборка через 'docker compose'
- Интеграция с PostgreSQL
- Документация в README
- добавлен Changelog

### Изменено:
- Конфигурация продакшена вынесена в 'env.prod'
- Файл с конфигурациями 'example.env'

## [1.0.0]
- Первый вариант api для расчета tf-idf