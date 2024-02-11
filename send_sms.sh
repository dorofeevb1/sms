#!/bin/bash

# Файл, откуда берутся номер и текст сообщения
SMS_FILE="sms.txt"

# Файл для логирования
LOG_FILE="sms_log.json"

# Функция отправки SMS
send_sms() {
    local number=$1
    local message=$2

    # Здесь должна быть команда или вызов программы для отправки SMS например: gammu sendsms TEXT "$number" -text "$message"
    echo "Отправка SMS на номер $number с текстом: $message"
}

# Функция записи лога в формат JSON
log_to_json() {
    local number=$1
    local message=$2
    local timestamp=$(date -I'seconds')

    # Добавляем запятую, если файл лога не пустой
    [ -s "$LOG_FILE" ] && echo "," >> "$LOG_FILE"

    # Добавляем запись в лог
    echo "{\"date\":\"$timestamp\",\"number\":\"$number\",\"message\":\"$message\"}" >> "$LOG_FILE"
}

# Проверяем наличие файла с номерами и сообщениями
if [ ! -f "$SMS_FILE" ]; then
    echo "Файл с SMS ($SMS_FILE) не найден."
    exit 1
fi

# Создаем или очищаем файл лога
echo "[" > "$LOG_FILE"

# Читаем номера и сообщения из файла
while IFS=';' read -r number message
do
    send_sms "$number" "$message"
    log_to_json "$number" "$message"
done < "$SMS_FILE"

# Закрываем массив в JSON
echo "]" >> "$LOG_FILE"

# Выводим сообщение о завершении работы скрипта
echo "SMS отправлены и лог обновлен."

