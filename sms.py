import machine
import time

#  UART    SIM800L
uart = machine.UART(0, baudrate=9600)

SMS_FILE = "sms.txt"  
LOG_FILE = "sms_log.json" 

def send_at_command(command, delay=2, return_response=False):
    """
     AT-  SIM800L   .
    """
    uart.write((command + '\r\n').encode())
    time.sleep(delay)
    if uart.any():
        response = uart.read().decode()
        print(response)  #    
        if return_response:
            return response
    else:
        print("No response")
        if return_response:
            return ""

def check_sim_card():
    """
      SIM-   SIM800L.
    """
    response = send_at_command('AT+CPIN?', 2, True)
    if "+CPIN: NOT INSERTED" in response:
        print("SIM-  .")
        return False
    elif "+CPIN: READY" in response:
        print("SIM-   .")
        return True
    else:
        print("    SIM-.")
        return False

def enable_sms_receive():
    """
         SMS.
    """
    send_at_command('AT+CMGF=1')  
    send_at_command('AT+CSCS="GSM"')
    send_at_command('AT+CNMI=2,2,0,0,0') 

def send_sms(number, message):
    """
     SMS-   .
    """
    print(f" SMS   {number}  : {message}")
    send_at_command('AT+CMGF=1')  
    send_at_command('AT+CSCS="GSM"')
    send_at_command(f'AT+CMGS="{number}"', delay=1, return_response=False)
    response = send_at_command(message + chr(26), delay=5, return_response=True)
    if "OK" in response:
        print("SMS  .")
    else:
        print("   SMS.")
def read_sms(index):
    """
     SMS       .
    """
    response = send_at_command(f'AT+CMGR={index}', 3, True)
    if "+CMGR:" in response:
        print(response)
    else:
        print("     .")

def list_all_sms():
    """
        SMS.
    """
    print("    SMS...")
    response = send_at_command('AT+CMGL="ALL"', 5, True)
    if "+CMGL:" in response:
        print(response)
    else:
        print("     .")

def main():
    if not check_sim_card():
        exit(1)

    enable_sms_receive()

    #   SMS    
    print("  SMS...")
    msg_id = wait_for_msg(250)  # 250  
    if msg_id is not None:
        print(f"    ID: {msg_id}")
        #   
        read_sms(msg_id)
    else:
        print("  .   .")
        #    
        list_all_sms()

    #  SMS     
    try:
        with open(SMS_FILE, "r") as file:
            sms_list = file.readlines()
    except OSError:
        print(f"  SMS ({SMS_FILE})  .")
        exit(1)

    with open(LOG_FILE, "w") as log_file:
        log_file.write("[\n")

    for sms in sms_list:
        number, message = sms.strip().split(';')
        send_sms(number, message)
        #      LOG_FILE    SMS

    #  JSON   LOG_FILE
    with open(LOG_FILE, "a") as log_file:
        log_file.write("\n]")

    print(" SMS    .")

if __name__ == "__main__":
    main()
