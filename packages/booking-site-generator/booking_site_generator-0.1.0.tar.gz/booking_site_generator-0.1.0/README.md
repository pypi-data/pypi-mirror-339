# Генератор сайта для системы бронирования

## Описание

Этот инструмент позволяет быстро создавать статические веб-сайты для систем бронирования с предустановленным функционалом.

## Возможности

- Создание полностью готового проекта с шаблонной структурой
- Простая кастомизация через конфигурационный файл
- Поддержка различных параметров настройки

## Установка

```bash
# Клонирование репозитория
git clone https://github.com/Y3ppi3/booking-site-generator.git

# Переход в директорию проекта
cd booking-site-generator

# Установка пакета
pip install .
```

## Использование

### Создание нового проекта

```bash
# Создание проекта с именем по умолчанию
booking-site-gen create

# Создание проекта с произвольным именем
booking-site-gen create --name my-custom-site

# Создание проекта в определенной директории
booking-site-gen create --output /path/to/project
```

### Кастомизация проекта

```bash
# Кастомизация с использованием файла конфигурации
booking-site-gen customize --config custom_config.json
```

## Файл конфигурации

Пример `custom_config.json`:

```json
{
    "site_name": "Мой сервис бронирования",
    "company_name": "Моя Компания",
    "contact_email": "info@mycompany.com",
    "phone": "+7 (999) 123-45-67",
    "color_scheme": {
        "primary": "#e74c3c",
        "secondary": "#2c3e50"
    }
}
```

## Требования

- Python 3.7+
- pip

## Лицензия

MIT License

## Contributing

1. Форкните репозиторий
2. Создайте свою ветку (`git checkout -b feature/AmazingFeature`)
3. Закоммитьте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Запушьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request