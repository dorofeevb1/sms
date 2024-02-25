#!/bin/bash

# Путь к файлу с номерами и сообщениями
SMS_FILE="sms.txt"

# Путь к JSON файлу лога
LOG_FILE="sms_log.json"

# Путь к устройству GSM модуля
COM_PORT="/dev/ttyUSB0"

# Функция отправки SMS
send_sms() {
    local number=$1
    local message=$2

    # Подготовка и отправка сообщения через GSM модуль
    echo "AT+CMGF=1" > $COM_PORT
    echo "AT+CSCS=\"GSM\"" > $COM_PORT
    echo "AT+CMGS=\"$number\"" > $COM_PORT
    echo -e "$message\x1A" > $COM_PORT

    # Логирование отправки сообщения
    local datetime=$(date --iso-8601=seconds)
    echo "{\"date\":\"$datetime\",\"number\":\"$number\",\"message\":$(jq -aRs . <<< "$message")}," >> $LOG_FILE
}

# Проверка наличия файла с SMS
if [ ! -f "$SMS_FILE" ]; then
    echo "Файл с SMS ($SMS_FILE) не найден."
    exit 1
fi

# Создание или очистка файла лога
echo "[" > $LOG_FILE

# Чтение SMS из файла и их отправка
while IFS=';' read -r number message
do
    send_sms "$number" "$message"
done < "$SMS_FILE"

# Удаление последней запятой и закрытие JSON массива
sed -i '$ s/,$//' $LOG_FILE
echo "]" >> $LOG_FILE

echo "Все SMS отправлены и лог обновлен."

