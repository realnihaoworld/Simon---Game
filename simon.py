# Names: 
# Danison Zhang - implemented scoring feature
# Colin Bass - implemented lighting feature
# Jacob James - implemented speed increase feature

import pineworkslabs.RPi as GPIO
from time import sleep
from random import choice
import pygame
from pygame.mixer import Sound
import os

pygame.init()

GPIO.setmode(GPIO.LE_POTATO_LOOKUP)

class Button:

    def __init__(self, switch:int, led:int, sound:str, color:str):
        self.switch = switch
        self.led = led
        self.sound: Sound = Sound(sound)
        self.color = color
        self.setupGPIO()
        
    def setupGPIO(self):
        GPIO.setup(self.switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.led, GPIO.OUT)
        
    def turn_light_on(self):
        GPIO.output(self.led, True)
                    
    def turn_light_off(self):
        GPIO.output(self.led, False)
        
    def is_pressed(self):
        # returns true or false depending on the switch
        return GPIO.input(self.switch)
        
    def respond(self):
        self.turn_light_on()
        self.sound.play()
        sleep(1)
        self.turn_light_off()
        sleep(0.25)
    
    def __str__(self):
        return self.color
        
class Simon:
    
    WELCOME_MESSAGE = "Welcome to Simon! Press ctrl+c to quit at anytime"
    
    # Paths should use os.path.join(), so it works on all machines
    # do not use C:\\
    # Do not use the root directory of the VS code project
    BUTTONS = [
        Button(switch=20, led=6, sound=os.path.join("sounds", "one.wav"), color="red"),
        Button(switch=16, led=13, sound=os.path.join("sounds", "two.wav"), color="blue"),
        Button(switch=12, led=19, sound=os.path.join("sounds", "three.wav"), color="yellow"),
        Button(switch=26, led=21, sound=os.path.join("sounds", "four.wav"), color="green")
    ]
    
    def __init__(self, debug=False):
        self.debug = debug
        self.sequence: list[Button] = [] # python 3.10+ only, for the type hinting
        
    def debug_out(self, *args):
        if self.debug:
            print(*args)
            
    def blink_all_buttons(self):
        # leds = []
        # for button in Simon.BUTTONS:
        #     leds.append(button.led)
        # GPIO.output(leds, True)
        # sleep(0.5)
        # GPIO.output(leds, False)
        # sleep(0.5)
    
        for button in Simon.BUTTONS:
            button.turn_light_on()
            sleep(0.5)
            button.turn_light_off()
            sleep(0.5)
            
    def add_to_sequence(self):
        random_button = choice(Simon.BUTTONS)
        self.sequence.append(random_button)
    
    def lose(self):
        for _ in range(4):
            self.blink_all_buttons()
        self.scoring()
        GPIO.cleanup()
    
    def playback(self):
        for button in self.sequence:
            # changes the led sequence speed depending on the round you are on
            num = len(self.sequence)
            if num < 5:
                button.turn_light_on()
                button.sound.play()
                sleep(1)
                button.turn_light_off()
                sleep(0.5)
            elif num < 7:
                button.turn_light_on()
                button.sound.play()
                sleep(.9)
                button.turn_light_off()
                sleep(0.4)
            elif num < 10:
                button.turn_light_on()
                button.sound.play()
                sleep(0.8)
                button.turn_light_off()
                sleep(0.3)
            elif num < 13:
                button.turn_light_on()
                button.sound.play()
                sleep(0.7)
                button.turn_light_off()
                sleep(0.25)
            else:
                button.turn_light_on()
                button.sound.play()
                sleep(0.6)
                button.turn_light_off()
                sleep(0.15)
    
    def wait_for_press(self):
        while True:
            for button in Simon.BUTTONS:
                if button.is_pressed():
                    self.debug_out(button.color)
                    button.respond()
                    return button
    
    # checks if the button pressed corresponds with the correct color in the sequence
    def check_input(self, pressed_button, correct_button):
        if pressed_button.switch != correct_button.switch:
            self.lose()
    
    # celebrates milestones with a quick light show
    def light_show(self):
        """A function to ripple lights"""
        for button in Simon.BUTTONS:
            button.turn_light_on()
            sleep(0.5)
            button.turn_light_off()

        for button in reversed(Simon.BUTTONS):
            button.turn_light_on()
            sleep(0.5)
            button.turn_light_off()
    
    # prints out the players score at the end of a game
    def scoring(self):
        if len(self.sequence) == 3:
            print("You didn't even make it to a sequence!")
        else:
            print(f"You made it to a sequence of {len(self.sequence)}!")
            
    
    def run(self):
        print(Simon.WELCOME_MESSAGE)
        
        # game will start with 2 items in the sequence
        self.add_to_sequence()
        self.add_to_sequence()
        
        # use control+c to kill the game
        try:
            while True:
                self.add_to_sequence()
                self.playback()
                self.debug_out(*self.sequence)
                for button in self.sequence:
                    pressed_button = self.wait_for_press()
                    self.check_input(pressed_button, button)
                    
                if len(self.sequence) in [10, 15, 20, 25, 30, 35, 40, 45, 50]:   # Checks the score for when to run light_show.
                    print("Light show!")
                    self.light_show()

                # USE THIS WHEN TESTING
                #if len(self.sequence) in [1, 2, 3, 4, 5]: # Debug
                    #self.light_show()
                    
        except KeyboardInterrupt:
            GPIO.cleanup()
            
simon = Simon()
simon.run()
