# MovieFinderApp
![GitHub last commit](https://img.shields.io/github/last-commit/MRGiorgiosDev8/django-moviefinder-api?color=blue)
![Repository size](https://img.shields.io/github/repo-size/MRGiorgiosDev8/django-moviefinder-api)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-informational)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/MRGiorgiosDev8/django-moviefinder-api)
![License](https://img.shields.io/github/license/MRGiorgiosDev8/django-moviefinder-api?color=blue)

MovieFinderApp — это веб-приложение для поиска фильмов, сериалов и получения подробной информации о них. Приложение использует **Django** на бэкенде и **JavaScript**, **HTML**, **CSS**, **Bootstrap** на фронтенде с анимациями через **GSAP (GreenSock Animation Platform).** и **jQuery**.

## Описание проекта

MovieFinderApp позволяет пользователям искать фильмы и сериалы, а также получать их подробную информацию, такую как рейтинг, описание, актерский состав и постеры. В проекте используется **OMDb API** для получения данных о фильмах и **Django** с **Django Rest Framework** для создания RESTful API.

Фронтенд использует **JavaScript**, **HTML**, **CSS**, **Bootstrap** для стилизации и **GSAP** для анимаций при взаимодействии с пользователем, например, анимации при загрузке данных или при открытии карточек фильмов. **jQuery** используется для работы с DOM и управления событиями.

В приложении реализована возможность аутентификации пользователей, добавления фильмов в избранное и просмотра избранных фильмов в личном кабинете пользователя.

## Стек технологий

### Backend

- **Django**: Фреймворк для разработки веб-приложений на Python, используемый для реализации серверной логики и работы с базой данных.
- **Django REST Framework**: Пакет для создания RESTful API на Django.
- **Gunicorn**: WSGI сервер для запуска приложения Django в продуктивной среде.
- **Pillow**: Библиотека для обработки изображений.
- **Whitenoise**: Пакет для обработки статических файлов, улучшает производительность при развертывании приложения.
- **Requests**: Библиотека для выполнения HTTP-запросов, используется для работы с внешними API (например, OMDb API для получения данных о фильмах).

### Frontend

- **JavaScript**: Язык программирования для реализации динамического контента на клиентской стороне, управления событиями и взаимодействия с сервером.
- **CSS**: Язык для стилизации веб-страниц и оформления внешнего вида элементов.
- **HTML**: Структура веб-страниц, используется для создания разметки сайта.
- **Bootstrap**: CSS-фреймворк для быстрой и удобной стилизации и создания адаптивных веб-интерфейсов.
- **Font Awesome**: Библиотека иконок, используется для добавления иконок, таких как социальные сети, рейтинги и другие визуальные элементы.
- **jQuery**: Библиотека JavaScript, используется для упрощения работы с DOM.
- **GSAP (GreenSock Animation Platform)**: Библиотека для создания высокопроизводительных анимаций и визуальных эффектов на веб-страницах.

## Развернутая версия

Вы можете ознакомиться с развернутой версией приложения на хостинге по следующей ссылке:

<a href="https://moviefinderapp-4vjn.onrender.com" target="_blank">MovieFinderApp</a>

Здесь вы можете протестировать приложение.


## Запуск и установка

Для локальной установки и работы с проектом выполните следующие шаги:

### Локальная установка

1. **Клонируйте репозиторий**:
    ```bash
    git clone https://github.com/MRGiorgiosDev8/django-moviefinder-api.git
    ```

2. Перейдите в директорию проекта:
    ```bash
    cd django-moviefinder-api
    cd finder_movie
    ```

3. **Создайте виртуальное окружение**:
    ```bash
    python -m venv venv
    ```

4. **Активируйте виртуальное окружение**:
    - Для Windows:
      ```bash
      venv\Scripts\activate
      ```
    - Для macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

5. **Установите зависимости**:
    ```bash
    pip install -r requirements.txt
    ```

8. **Запустите сервер**:
    ```bash
    python manage.py runserver
    ```

    После этого проект будет доступен по адресу: `http://127.0.0.1:8000/`.