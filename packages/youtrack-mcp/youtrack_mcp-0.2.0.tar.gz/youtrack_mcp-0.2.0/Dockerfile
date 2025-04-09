# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код в контейнер
COPY . .

# Устанавливаем переменные окружения
ENV YOUTRACK_URL=https://frox.youtrack.cloud \
    YOUTRACK_TOKEN=perm-YS52YXNpbGV2.NjMtNw==.PaBAyFMLFGKrPDLE8XMD2z6h6fmu0K \
    MCP_SERVER_NAME="YouTrack MCP Server" \
    MCP_LOG_LEVEL=INFO

# Определяем команду запуска
CMD ["python", "server.py"] 