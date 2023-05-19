# Дипломный проект FOODGRAM.

[![foodgram-project-react workflow](https://github.com/MikeEr21/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg)](https://github.com/MikeEr21/foodgram-project-react/actions/workflows/foodgram.yml)
![Deploy_badge](https://github.com/MikeEr21/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg)

### Описание проекта Foodgram
«Продуктовый помощник»: сайт где можно публикавать рецепты кулинарных изделий, подписываться на публикации других авторов, а также добавлять рецепты в избранные и формировать список покупок, позволяющий пользователю скачать его. В списке будут указаны продукты, которые нужно купить для приготовления выбранных блюд.

### Технологии
* Python 3.9
* Django 3.2.19
* DRF 3.12.4
* Nginx
* docker-compose

### Запуск проекта в dev-режиме

- Применить миграции
```
sudo docker-compose exec backend python manage.py migrate
```
- Загрузить статику
```
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
- Cоздать суперпользователя 
```
sudo docker-compose exec backend python manage.py createsuperuser --username admin --email 'admin@admin.com'
```
- Cоздать  базу данных
```
sudo docker-compose exec backend python manage.py load_tags
sudo docker-compose exec backend python manage.py load_ingredients
```
### Проверка работоспособности приложения: перейти на страницу:
```
http://158.160.39.23/admin/
```

### Автор
Михаил Ермолаев

sansouci@ya.ru

https://github.com/MikeEr21