#!/usr/bin/python
# RGB LCD Screen
import time
import grove_rgb_lcd

sleep = time.sleep
setText = grove_rgb_lcd.setText
setText_norefresh = grove_rgb_lcd.setText_norefresh
setRGB = grove_rgb_lcd.setRGB

class LCDControl(object):
    def __init__(self, red = 100, green = 100, blue = 100):
        #Set default background colour
        self.red = red
        self.green = green
        self.blue = blue
        self.rgb(self.red, self.green, self.blue)

    #Send text to LCD with refresh but no scroll
    def text(self, text):
        setText(text)
        
    #Send text to LCD with no refresh and no scroll
    def text_norefresh(self, text):
        setText_norefresh(text)
        
    #Refresh LCD
    def refresh(self):
        self.text("")
        
    #Send text to LCD with scroll
    def text_scroll(self, text, cycles = 1, speed = 1):
        try:
            if cycles < 1 or cycles > 10:
                raise ValueError("Cycles value must be between 1 an 10.")
            
            if speed < 1 or speed > 10:
                raise ValueError("Speed value must be between 1 an 5.")            
            
            length = len(text)

            if length > 32:  #Scroll required   
                scroll_text = text + " "
                length = len(scroll_text)
                for i in range(cycles):
                    for s in range(length):
                        self.text_norefresh(scroll_text)
                        
                        #Move first character to the end of the string
                        char = scroll_text[0]
                        scroll_text = scroll_text[1: length] + char
                        sleep(0.1 / (speed * 0.25))
                        
                self.text_norefresh(scroll_text)
            else:
                #No scroll required
                self.text(text)
                
        except ValueError as e:
            print e.args[0]
            exit()
                
    #Set RGB values for background display
    def rgb(self, red, green ,blue):
        setRGB(red, green, blue)

    #Prompt with input and input echo
    def input(self, prompt):
        try:
            if len(prompt) > 16:
                raise Exception("Prompt cannot be longer than 16 characters.")

            self.text(prompt + "\n")
            reply = raw_input(prompt + " ")
            self.text(prompt + "\n" + reply)
            return(reply)

        except Exception as e:
            print e.args[0]
            exit()


# An example of what the class can do
if __name__ == "__main__":
    lcd = LCDControl(100, 20, 20)
    lcd.text_scroll("This is an LCD screen scrolling module.", 1, 3 )
    sleep(5)
    lcd.rgb(50, 50, 50)
    name = lcd.input("Name please:")

    print("Name = " + name)
    sleep(1)

    while True:
        age = lcd.input("Age please:")
        try:
            age = int(age)
            break
        except ValueError:
            print "Integer please"
        
    print("Age = %d" % age)
    sleep(1)
    lcd.rgb(100, 20, 20)
    lcd.text_scroll("Well, hello %s, you're not looking bad for %d years old." % (name, age), 2, 3)
    sleep(2)
    lcd.refresh()
    lcd.rgb(0, 0, 0)
