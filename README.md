# API для онлайн-кинотеатра

## Развертывание приложения
1. Склонируйте [репозиторий с ETL](https://github.com/PyotrAristov/new_admin_panel_sprint_3) и разверните его по инструкции
2. Создайте и заполните файл `.env` по образцу `.env.example`
3. Соберите и запустите docker контейнеры
4. Сервер запуститься по адресу `localhost:80`

## Тестирование приложения
1. Добавьте к значениям переменных `REDIS_HOST` и `ELASTIC_HOST` префикс `test-`
2. Запустите контейнеры `movies-api` и `movies-nginx`
3. Запустите `tests/functional/docker-compose.yml`
4. Смотрите результат тестирования в логах `docker logs movies-tests`

### Ссылки
* [Документация OpenAPI](http://localhost:80/api/openapi)
* [Репозиторий с ETL](https://github.com/PyotrAristov/new_admin_panel_sprint_3)