class TemperatureSensor:
    def __init__(self, sensor_id):
        self.sensor_id = sensor_id
        self.temperature = None

    def read_temperature(self):
        # Simulate reading temperature from the sensor
        import random
        self.temperature = random.uniform(-20.0, 50.0)
        return self.temperature

    def get_temperature(self):
        return self.temperature

    def __str__(self):
        return f"TemperatureSensor(id={self.sensor_id}, temperature={self.temperature})"