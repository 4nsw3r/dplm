# API for shop

## Для запуска выполните след шаги:
- склонируйте репозиторий

- запустите из корня проекта
```bash
python pip install -r requirements.txt
```

- запустите миграции
```bash
python manage.py migrate
```

- Загрузить тестовые данные:
```bash
python manage.py loaddata fixtures.json
```

- Запустить отладочный веб-сервер проекта:
```bash
python manage.py runserver
```


## Описание приложения

В адресной строке:
- /admin - вход в админку
- /auth/login -api авторизация
- /api/v1/ - api 

- /api/v1/products - получение всех товаров (для определенного ID: /api/v1/products/id/)
- /api/v1/orders - получение всех заказов 
- /api/v1/collections - получение всех подборок
- /api/v1/rewiews - получение всех отзывов
