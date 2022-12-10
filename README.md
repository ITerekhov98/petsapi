# petsapi
## simple api, based on drf and psql

## Установка и запуск:

### Dev версия

Скачайте репозиторий с кодом, перейдите в каталог. Создайте `.env` файл и наполните его следующими настройками, в формате `Ключ=значение`:

- `DEBUG` — дебаг-режим
- `DJANGO_SECRET_KEY` — секретный ключ проекта. Он отвечает за шифрование на сайте. Например, им зашифрованы все пароли на вашем сайте.
- `ALLOWED_HOSTS` — [см. документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts)
- `YANDEX_API_TOKEN`  - ключ доступа для [API Яндекс-геокодера](https://passport.yandex.ru/auth?origin=apikeys&retpath=https%3A%2F%2Fdeveloper.tech.yandex.ru%2F) 
- `DB_URL` - url с учётными данными для postgres, в формате: postgres://DB_USER:DB_PASSWORD@DB_HOST:DB_PORT/DB_NAME
- `ROLLBAR_TOKEN` - ваш токен доступа для учёта логов в [rollbar](https://rollbar.com)
- `ROLLBAR_ENVIRONMENT` - переменная среды, по умолчанию development (но не стоит её оставлять таковой в prod-версии)
