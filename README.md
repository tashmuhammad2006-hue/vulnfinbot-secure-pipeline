# Mini-VulnFinBot — DevSecOps & AI Security Pipeline

Учебный проект **Mini-VulnFinBot** — лёгкое веб-приложение на **Flask**, предназначенное для демонстрации полного цикла DevSecOps: автоматического тестирования, статического анализа кода (SAST), проверки зависимостей, сканирования Docker-образа, динамического анализа (DAST), базовых проверок ИИ-безопасности и демонстрации обнаружения/устранения уязвимостей в CI/CD на базе **GitHub Actions**.

## 1. Описание проекта

Приложение предоставляет REST API на базе Flask с двумя основными эндпоинтами:
- `GET /health` — проверка работоспособности сервиса (возвращает `{"status": "healthy"}`).
- `POST /api/chat` — обработка пользовательских сообщений с валидацией входных данных (проверка JSON, обязательного поля `message`, типа данных, длины сообщения) и генерацией ответа помощника с базовыми защитными проверками.

## 2. Технологический стек

- **Язык и веб-фреймворк:** Python, Flask, Gunicorn
- **Тестирование:** `pytest` (unit-тесты API и набор проверок ИИ-безопасности)
- **Контейнеризация:** Docker
- **CI/CD:** GitHub Actions (`.github/workflows/security-pipeline.yml`)
- **Инструменты безопасности:**
  - **Bandit** — SAST для Python-кода
  - **Semgrep** — SAST с пользовательскими правилами (`security/semgrep/rules.yml`)
  - **pip-audit** — проверка известных уязвимостей в Python-зависимостях
  - **Trivy** — сканирование Docker-образа и пакетов ОС на уязвимости
  - **OWASP ZAP** — динамическое тестирование безопасности (DAST / baseline scan)

## 3. Архитектура проекта

```text
vulnfinbot-secure-pipeline/
├── .github/
│   └── workflows/
│       └── security-pipeline.yml   # Конвейер CI/CD и проверок безопасности
├── app/
│   ├── __init__.py                 # Инициализация Flask-приложения
│   └── routes.py                   # Маршруты /health и /api/chat, логика ответов
├── reports/
│   └── .gitkeep                    # Директория для отчётов
├── security/
│   └── semgrep/
│       └── rules.yml               # Кастомные правила Semgrep (например, eval/exec)
├── tests/
│   ├── __init__.py
│   ├── test_app.py                 # Unit-тесты эндпоинтов и валидации ввода
│   └── test_ai_security.py         # Тесты сценариев безопасности ИИ и генерация отчёта
├── Dockerfile                      # Сборка контейнерного образа приложения
├── .dockerignore
├── .gitignore
├── requirements.txt                # Зависимости Python
├── run.py                          # Точка входа для локального запуска
└── README.md