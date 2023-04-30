# Дипломный проект FOODGRAM.

![Deploy_badge](https://github.com/MikeEr21/foodgram-project-react/blob/master/.github/workflows/foodgram.yml/badge.svg)

### Технологии
* Python 3.7
* Django 2.2.19
* DRF 3.12.4
* Nginx
* docker-compose

### Запуск проекта в dev-режиме

- Применить миграции
```
sudo docker-compose exec web python manage.py migrate
```
- Загрузить статику
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
- Cоздать суперпользователя 
```
sudo docker-compose exec web python manage.py createsuperuser --username admin --email 'admin@admin.com'
```
- Cоздать  базу данных
```
sudo docker-compose exec web python manage.py loaddata ./data/fixtures.json
```
### Проверка работоспособности приложения: перейти на страницу:
```
http://127.0.0.1:8000/admin/
```
### Документация:
```
http://127.0.0.1:8000/redoc/
```
### Автор
Михаил Ермолаев