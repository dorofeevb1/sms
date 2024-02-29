import machine
import time
from machine import Pin

# Настройка UART для связи с SIM800L
uart = machine.UART(0, baudrate=2400)
# Создание файла sms.txt и запись в него текста

SMS_FILE = "sms.txt"  # Путь к файлу со списком SMS
LOG_FILE = "sms_log.json"  # Путь к файлу лога

def send_at_command(command, delay=2, return_response=False):
    """
    Отправляет AT-команду модулю SIM800L и возвращает ответ.
    """
    uart.write((command + '\r\n').encode())
    time.sleep(delay)
    response = uart.read()
    if response:
        print(response.decode())  # Вывод ответа для отладки
        if return_response:
            return response.decode()
    else:
        print("No response")
        if return_response:
            return ""


def check_sim_card():
    """
    Проверяет наличие SIM-карты в модуле SIM800L.
    """

    response = send_at_command('AT+CPIN?', 2, True)
    if "+CPIN: NOT INSERTED" in response:
        print("SIM-карта не обнаружена.")
        return False
    elif "+CPIN: READY" in response:
        print("SIM-карта готова к работе.")
        return True
    else:
        print("Не удалось проверить статус SIM-карты.")
        return False


def send_sms(number, message):
    """
    Отправляет SMS-сообщение на указанный номер.
    """
    print(f"Отправка SMS на номер {number} с текстом: {message}")
    send_at_command('AT+CMGF=1')  # Текстовый режим
    send_at_command(f'AT+CMGS="{number}"', delay=1, return_response=False)
    response = send_at_command(message + chr(26), delay=5, return_response=True)
    if "OK" in response:
        print("SMS успешно отправлено.")

    else:
        print("Ошибка при отправке SMS.")


if __name__ == "__main__":
    if not check_sim_card():
        exit(1)

    try:
        with open(SMS_FILE, "r") as file:
            sms_list = file.readlines()
    except OSError:
        print(f"Файл с SMS ({SMS_FILE}) не найден.")
        exit(1)

    with open(LOG_FILE, "w") as log_file:
        log_file.write("[\n")

    for sms in sms_list:
        number, message = sms.strip().split(';')
        send_sms(number, message)

    with open(LOG_FILE, "r") as log_file:
         content = log_file.read()
    modified = content[:-2]+"\n]"

    with open(LOG_FILE, "a") as log_file:
         log_file.write(modified)

    print("Все SMS отправлены и лог обновлен.")