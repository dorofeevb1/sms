import serial
import json
from datetime import datetime

# Путь к файлу с номерами и сообщениями
SMS_FILE = "sms.txt"

# Путь к JSON файлу лога
LOG_FILE = "sms_log.json"

# Путь к устройству GSM модуля
COM_PORT = "/dev/ttyUSB0"

# Скорость порта
BAUD_RATE = 9600

# Функция отправки SMS
def send_sms(number, message):
    with serial.Serial(COM_PORT, BAUD_RATE, timeout=1) as ser:
        ser.write(b'AT+CMGF=1\r')
        ser.write(b'AT+CSCS="GSM"\r')
        ser.write(bytes('AT+CMGS="{}"\r'.format(number), 'utf-8'))
        ser.write(bytes('{}\x1A'.format(message), 'utf-8'))

        # Логирование отправки сообщения
        datetime_now = datetime.now().isoformat()
        log_entry = {"date": datetime_now, "number": number, "message": message}
        with open(LOG_FILE, "a") as log_file:
            json.dump(log_entry, log_file)
            log_file.write(",\n")

# Проверка наличия файла с SMS и создание или очистка файла лога
if __name__ == "__main__":
    try:
        with open(SMS_FILE, "r") as file:
            sms_list = file.readlines()
    except FileNotFoundError:
        print(f"Файл с SMS ({SMS_FILE}) не найден.")
        exit(1)
    
    with open(LOG_FILE, "w") as log_file:
        log_file.write("[\n")
    
    for sms in sms_list:
        number, message = sms.strip().split(';')
        send_sms(number, message)
    
    # Удаление последней запятой и закрытие JSON массива
    with open(LOG_FILE, "rb+") as log_file:
        log_file.seek(-2, 2)  # Перемещаемся на два байта назад от конца файла
        log_file.truncate()  # Удаляем последние два байта (запятую и перевод строки)
    with open(LOG_FILE, "a") as log_file:
        log_file.write("\n]")
    
    print("Все SMS отправлены и лог обновлен.")

