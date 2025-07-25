
---

# Foodgram

Foodgram — это веб-приложение для обмена рецептами, где пользователи могут публиковать свои рецепты, просматривать рецепты других пользователей, добавлять рецепты в избранное и составлять список покупок.

- Проект доступен по адресу: https://greatfood.zapto.org
- API проекта: https://greatfood.zapto.org/api/
- Документация в формате redoc: https://greatfood.zapto.org/api/docs/redoc.html
  
## Оглавление

- [Описание](#описание)
- [Функциональность](#функциональность)
- [Технологии](#технологии)
- [Установка](#установка)
- [Использование](#использование)
- [Вклад](#вклад)
- [Контакты](#контакты)

## Описание

Foodgram позволяет пользователям делиться своими кулинарными шедеврами и находить новые интересные рецепты. Приложение поддерживает функции регистрации и аутентификации пользователей, добавления и редактирования рецептов, а также создания списка покупок на основе выбранных рецептов.

## Функциональность

- Регистрация и аутентификация пользователей
- Публикация, редактирование и удаление рецептов
- Просмотр рецептов других пользователей
- Добавление рецептов в избранное
- Создание списка покупок на основе избранных рецептов
- Фильтрация рецептов по тегам и ингредиентам

## Технологии

- Python
- Django
- Django REST Framework
- PostgreSQL
- Docker
- Nginx
- Gunicorn
- JavaScript
- HTML/CSS
- React

## Установка

### Предварительные требования

- Docker и Docker Compose должны быть установлены на вашем компьютере.

### Шаги установки

1. Клонируйте репозиторий:

- git clone https://github.com/pullveryzator/foodgram.git
- cd foodgram
    

2. Создайте файл `.env` в корневой директории проекта и добавьте необходимые переменные окружения:

    SECRET_KEY=your_secret_key  
    DEBUG=True  
    ALLOWED_HOSTS=localhost, 127.0.0.1  
    DB_NAME=your_db_name  
    DB_USER=your_db_user  
    DB_PASSWORD=your_db_password  
    DB_HOST=db  
    DB_PORT=5432  
    

3. Запустите Docker Compose:

- docker-compose up -d --build
    

4. Выполните миграции, соберите статику и импортируйте ингредиенты из backend/data/ingredients.csv:

- docker-compose exec backend python manage.py makemigrations
- docker-compose exec backend python manage.py migrate
- docker-compose exec backend python manage.py collectstatic
- docker-compose exec backend python manage.py import
    

5. Создайте суперпользователя для доступа к административной панели:

- docker-compose exec backend python manage.py createsuperuser
    

6. Откройте браузер и перейдите по адресу `http://localhost:8000/` для доступа к приложению.

## Использование

После установки и запуска приложения вы можете:

- Зарегистрироваться и войти в систему
- Публиковать свои рецепты
- Просматривать рецепты других пользователей
- Добавлять рецепты в избранное
- Создавать список покупок

## Вклад

Если вы хотите внести вклад в проект, пожалуйста, следуйте этим шагам:

1. Форкните репозиторий
2. Создайте новую ветку (`git checkout -b feature/YourFeature`)
3. Внесите изменения и закоммитьте их (`git commit -m 'Add some feature'`)
4. Запушьте изменения в ветку (`git push origin feature/YourFeature`)
5. Создайте Pull Request

## Контакты

Если у вас есть вопросы или предложения, пожалуйста, свяжитесь со мной:

- Email: madlion@mail.ru
- GitHub: https://github.com/pullveryzator/

---
