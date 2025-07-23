# AI-Mood-Journal-Bot
Ai mood journal in telegram bot - your personal helper


AI-MOOD-JOURNAL-BOT/
├── alembic/
│   ├── versions/ (миграции)
│   ├── env.py
│   └── script.py.mako
├── config/
│   └── config.py
├── logs/
│   └── bot.log
├── src/
│   ├── bot/
│   │   ├── handlers/
│   │   │   ├── base.py (стартовые команды)
│   │   │   ├── mood.py (отслеживание настроения)
│   │   │   ├── report.py (генерация отчетов)
│   │   │   └── analytics.py (аналитика)
│   │   ├── utils/
│   │   │   ├── keyboards.py
│   │   │   └── states.py (FSM состояния)
│   │   └── launcher.py
│   ├── core/
│   │   ├── models.py (сущности БД)
│   │   ├── database.py (подключение к БД)
│   │   ├── logger.py (система логирования)
│   │   └── enums.py (перечисления)
│   └── ml/
│       ├── emotion_detection.py
│       └── prediction.py
├── .env
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md