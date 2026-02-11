# config.py

# Constants
DEFAULT_SETTING = 'default'
API_URL = 'https://api.example.com'

# Configuration Settings Management
class Configuration:
    def __init__(self):
        self.settings = {
            'setting1': DEFAULT_SETTING,
            'setting2': 42,
            'setting3': True
        }

    def set_setting(self, key, value):
        self.settings[key] = value

    def get_setting(self, key):
        return self.settings.get(key, None)

# Example usage
if __name__ == '__main__':
    config = Configuration()
    print(config.get_setting('setting1'))
    config.set_setting('setting1', 'new_value')
    print(config.get_setting('setting1'))
