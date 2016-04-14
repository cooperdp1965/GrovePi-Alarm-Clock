#!/usr/bin/python
"""
In order to run this program, the followong sensors must be connected:

Light sensor             => Port A0
Rotary angle switch      => Port A1
Button                   => Port D2
Buzzer                   => Port D3 (PWM)
DHT sensor               => Port D4
LCD Screen               => Any I2C port

The clock will pick up the system time and date. Pressing the button will initially take you into
alarm set mode. Thereafter, it will display a menu that allows the alarm time to be viewed, changed
or cancelled.
The rotary angle switch is used to dial in hour and minute values and to scroll through the menu
items. Once the required item is displayed, press the button to select it.
"""
import time
import datetime
import LCD_Screen_Control
import grovepi

sleep = time.sleep
lcd = LCD_Screen_Control.LCDControl(50,50,50)

light_sensor = 0
grovepi.pinMode(light_sensor, "INPUT")

rotary = 1
grovepi.pinMode(rotary, "INPUT")

button = 2
grovepi.pinMode(button, "INPUT")

buzzer = 3
grovepi.pinMode(buzzer, "OUTPUT")

dht_sensor = 4
grovepi.pinMode(dht_sensor, "INPUT")

now = datetime.datetime.now()

temp = 0
hum = 0
line2 = ""

alm = {
    "set" : "",
    "hour" : 12,
    "minute" : 44,
    "quiet" : ""
}

menu_items = ["View alarm", "Change alarm", "Cancel alarm", "Return"]

# Set Alarm time
def set_alarm_time():
    alm["hour"] = get_value("hour", 24.0)
    alm["minute"] = get_value("min.", 60.0)
    lcd.text("Alarm set for:\n%02d:%02d" % (alm["hour"], alm["minute"]))
    sleep(2)
    alm["set"] = "X"
    alm["quiet"] = ""
    lcd.text("")    

def menu():
    while grovepi.digitalRead(button) == True:
        pass
    
    if alm["set"] == "":
        set_alarm_time()
    else:
        items = float(len(menu_items))
        val = int(grovepi.analogRead(rotary) / (1023 / items))
        old_val = val
        lcd.text("Select option:\n" + menu_items[val])
        
        while True:
            lcd.text

            try:
                val = int(grovepi.analogRead(rotary) / (1023 / items))

                if val == items:
                    val = items - 1

                if val <> old_val:
                    lcd.text("Select option:\n" + menu_items[val])
                    old_val = val

                if grovepi.digitalRead(button) == True:
                    break
                
            except IOError:
                pass

        if val == 0:
            lcd.text("Alarm set for:\n%02d:%02d" % (alm["hour"], alm["minute"]))
            sleep(2)
            lcd.text("")            
        elif val == 1:
            set_alarm_time()
        elif val == 2:
            alm["set"] = ""
            lcd.text("Alarm cancelled.")
            sleep(2)
            lcd.text("")
        else:
            lcd.text("")

    #Ensure button has been released:
    while True:
        try:
            if grovepi.digitalRead(button) == False:
                break

        except IOError:
            pass

def get_value(name, max):
    lcd.text("")

    while True:
        try:
            val = int(grovepi.analogRead(rotary) / (1023 / max))
            if val > (max - 1):
                val = max - 1
                
            lcd.text_norefresh("Alarm Set\nSelect %s: %02d" % (name, val))

            if grovepi.digitalRead(button) == True:
                break
        
        except IOError:
            pass
        
    sleep(0.5)
    return val

# Add zero to supplied integer
def zero_prefix(int, length):
    string = str(int)
    for i in range(length - len(str(int))):
        string = "0" + string
    return string

# Get the light level
def get_light_level():
    #Light sensor reading
    try:
        level = int(grovepi.analogRead(light_sensor) / 15) + 3
        lcd.rgb(level, level, level)

    except IOError:
        pass

# Sound the alarm
def sound_alarm():
    type = ""
    exit_flag = False

    now = datetime.datetime.now()
    alm_min = now.minute
    now_min = now.minute
  
    val = 10
    lcd.rgb(255, 0, 0)
    lcd.text("    Alarm!!!")
    
    while alm_min == now_min:
        now = datetime.datetime.now()
        now_min = now.minute

        grovepi.analogWrite(buzzer, val)

        if grovepi.digitalRead(button) == True:
            break
        else:
            if val == 10:
                val = 70
            else:
                val = 10

        sleep(1)

    grovepi.analogWrite(buzzer, 0)

    #Wait for button to be releasd
    while True:
        try:
            if grovepi.digitalRead(button) == False:
                break

        except IOError:
            pass
        
    lcd.text("")
    lcd.rgb(50,50,50)
    alm["quiet"] = "X"
    

lcd.text("")
[temp, hum] = grovepi.dht(dht_sensor, 0)
lcd.text("Time: %02d:%02d" % (now.hour, now.minute))
second = now.second
get_light_level()

while True:
    now = datetime.datetime.now()

    #Check if alarm should sound
    if alm["set"] == 'X' and alm["quiet"] == "" and alm["hour"] == now.hour and alm["minute"] == now.minute:
        sound_alarm()
    elif alm["quiet"] == "X" and alm["minute"] <> now.minute:
        alm["quiet"] = ""

    #Read temp and humidity every 20 seconds
    if now.second in range(0, 60, 20):
        [temp, hum] = grovepi.dht(dht_sensor, 0)
    
    if int(zero_prefix(now.second, 2)[1]) > 4:
        #Display temp and humidity
        t = str(int(temp))
        h= str(int(hum))
        line2 = "Temp/Hum:" + t + "C/" +  h + "%"
    else:
        line2 = "Date: " + zero_prefix(now.day, 2) + "/" + zero_prefix(now.month, 2) + "/" + zero_prefix(now.year, 4)

    #Only update time if second has changed
    if now.second in range(0,60,5):  
        second = now.second
        get_light_level()

        while True:
            try:
                lcd.text_norefresh("Time: %02d:%02d\n%s" % (now.hour, now.minute, line2))
                break

            except IOError:
                pass

    #Check for button press only after it has been released
    try: 
        if grovepi.digitalRead(button) == True:
            menu()
            
    except IOError:
        pass






        

