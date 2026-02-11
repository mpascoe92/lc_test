class HardwareController:
    def __init__(self, relay_pin, led_pin, simulation=True):
        self.relay_pin = relay_pin
        self.led_pin = led_pin
        self.simulation = simulation
        if not self.simulation:
            from gpiozero import LED, OutputDevice
            self.relay = OutputDevice(relay_pin)
            self.led = LED(led_pin)
        else:
            self.relay = None  # Simulated relay
            self.led = None  # Simulated LED

    def turn_on_relay(self):
        if not self.simulation:
            self.relay.on()
        else:
            print("Simulated: Turning on relay")

    def turn_off_relay(self):
        if not self.simulation:
            self.relay.off()
        else:
            print("Simulated: Turning off relay")

    def turn_on_led(self):
        if not self.simulation:
            self.led.on()
        else:
            print("Simulated: Turning on LED")

    def turn_off_led(self):
        if not self.simulation:
            self.led.off()
        else:
            print("Simulated: Turning off LED")

class ButtonController:
    def __init__(self, button_pin, callback, simulation=True):
        self.button_pin = button_pin
        self.callback = callback
        self.simulation = simulation
        if not self.simulation:
            from gpiozero import Button
            self.button = Button(button_pin)
            self.button.when_pressed = self.callback
        else:
            self.button = None  # Simulated button
            print("Simulated: Button controller created")

    def simulate_button_press(self):
        if self.simulation:
            print("Simulated: Button press triggered")
            self.callback()  # Call the callback as if the button was pressed
