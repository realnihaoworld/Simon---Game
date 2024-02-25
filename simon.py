 def __str__(self):
        return self.color

class Simon:

    WELCOME_MESSAGE = "Welcome to Simon! Press ctrl+c to quit at anytime"

    # Paths should use os.path.join(), so it works on all machines
    # do not use C:\\
    # Do not use the root directory of the VS code project
    BUTTONS = [
        Button(switch=20, led=6, sound=os.path.join("sounds" + "one.wav"), color="red"),
        Button(switch=16, led=13, sound=os.path.join("sounds", "two.wav"), color="blue"),
        Button(switch=12, led=19, sound=os.path.join("sounds", "three.wav"), color="yellow"),
        Button(switch=26, led=21, sound=os.path.join("sounds", "four.wav"), color="green")
    ]

    def __init__(self, debug=True):
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
        GPIO.cleanup()

    def playback(self):
        for button in self.sequence:
            button.respond()

    def wait_for_press(self):
        while True:
            for button in Simon.BUTTONS:
                if button.is_pressed():
                    self.debug_out(button.color)
                    button.respond()
                    return button

    def check_input(self, pressed_button, correct_button):
        if pressed_button.switch != correct_button.switch:
            self.lose()

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

                if len(self.sequence) in [15, 20, 25, 30, 35, 40, 45, 50]:   # Checks the score for when to run light_show.
                    self.light_show()

                # USE THIS WHEN TESTING
                #if len(self.sequence) in [1, 2, 3, 4, 5]: # Debug
                    #self.light_show()

        except KeyboardInterrupt:
            GPIO.cleanup()

simon = Simon()
simon.run()
