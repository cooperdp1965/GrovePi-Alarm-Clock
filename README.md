# GrovePi-Alarm-Clock
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
