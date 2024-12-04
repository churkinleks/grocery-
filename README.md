# Grocery Shop

## Описание

Grocery Shop - это пример маленького магазинчика, где можно посмотреть
интересующий Вас хлебушек и положить его в корзинку, с уверенностью в том,
что Вы не перегрузили базу данных.

Данный проект носит исключительно демонстрационный характер,
поэтому иногда в коде может быть намеренная избыточность.

## Запуск

```shell
poetry install && poetry shell
```

```shell
python manage.py runserver
```

superuser = admin:admin

## Pre-Commit

- Установка хуков.

```shell
pre-commit install --hook-type pre-commit --hook-type pre-push
```

- При каждом `git push` будут запускаться все тесты локально.
