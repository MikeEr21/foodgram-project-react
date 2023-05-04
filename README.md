# Дипломный проект FOODGRAM.

[//]: # (![Deploy_badge]&#40;https://img.shields.io/github/actions/workflow/status/MikeEr21/foodgram-project-react/foodgram?logo=github&logoColor=%2300ff00&#41;)

[//]: # ([![foodgram-project-react workflow]&#40;https://github.com/MikeEr21/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg&#41;]&#40;https://github.com/MikeEr21/foodgram-project-react/actions/workflows/foodgram.yml&#41;)

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
http://localhost/admin/
```
### Документация:
```
http://localhost/redoc/
```
### Автор
Михаил Ермолаев