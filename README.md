# README.md для Telegram Client Management System

```markdown
# Telegram Client Management System

![App Screenshot](static/images/screenshot.png)

Веб-додаток для управління клієнтами Telegram з аналітикою та звітністю.

## Особливості

- 📊 Панель управління з ключовими метриками
- 👥 Управління клієнтською базою
- 🔥 Аналіз "гарячих" лідів
- 📈 Візуальні звіти по крипто-активності
- 🔐 Система автентифікації

## Технологічний стек

- **Backend**: Python 3.11, Flask
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Бази даних**: CSV, Excel (для демо-даних)
- **Інші бібліотеки**: Pandas, NumPy, Pillow

## Встановлення

1. Клонуйте репозиторій:
   ```bash
   git clone https://github.com/yourusername/telegram_client_system.git
   cd telegram_client_system
   ```

2. Створіть та активуйте віртуальне оточення:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate    # Windows
   ```

3. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   ```

4. Налаштуйте конфігурацію:
   - Відредагуйте `config.py` за потреби
   - Для генерації тестових даних встановіть `MOCK_DATA = True`

5. Запустіть додаток:
   ```bash
   python app.py
   ```

6. Відкрийте у браузері:
   ```
   http://localhost:5000
   ```

## Деплой на Render.com

1. Створіть новий Web Service на Render
2. Підключіть ваш GitHub репозиторій
3. Вкажіть наступні налаштування:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Додайте змінні середовища:
   - `SECRET_KEY` - секретний ключ для Flask
   - `PYTHON_VERSION` - `3.11.8`

## Доступні облікові записи

- **Адміністратор**: 
  - Логін: `admin`
  - Пароль: `admin123`
- **Менеджер**: 
  - Логін: `manager`
  - Пароль: `manager123`

## Структура проекту

```
telegram_client_system/
├── app.py                # Основний додаток Flask
├── config.py             # Конфігурація додатку
├── requirements.txt      # Залежності Python
├── runtime.txt           # Версія Python для Render
├── data/                 # Тестові дані
├── static/               # Статичні файли
│   ├── css/              # Стилі CSS
│   └── images/           # Зображення
└── templates/            # Шаблони HTML
    ├── base.html         # Базовий шаблон
    ├── dashboard.html    # Панель управління
    ├── clients.html      # Клієнтська база
    └── ...              # Інші шаблони
```

## Ліцензія

Цей проект ліцензований за умовами MIT License. Див. файл [LICENSE](LICENSE) для деталей.

---

**Примітка**: Це демо-версія системи. Для використання у продакшені необхідні додаткові налаштування безпеки.
```

Цей README.md містить всі необхідні розділи для швидкого старту з проектом, включаючи:
1. Опис системи
2. Інструкції з встановлення
3. Деталі деплою
4. Технічні деталі
5. Структуру проекту

Файл оптимізований для GitHub та Render.com, з чіткими інструкціями для розробників.