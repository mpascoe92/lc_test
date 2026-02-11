class SettingsManager:
    def __init__(self, settings):
        self.settings = settings

    def get_setting(self, key):
        return self.settings.get(key)

    def set_setting(self, key, value):
        self.settings[key] = value

    def load_from_file(self, file_path):
        # Logic to load settings from a file
        pass

    def save_to_file(self, file_path):
        # Logic to save settings to a file
        pass


class EmailConfigManager:
    def __init__(self, smtp_server, port, sender_email, password):
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.password = password

    def send_email(self, recipient_email, subject, body):
        # Logic for sending an email
        pass

    def validate_email(self):
        # Logic for validating email configuration
        pass


if __name__ == "__main__":
    settings = {
        'debug': True,
        'smtp_server': 'smtp.example.com',
        'smtp_port': 587,
        'sender_email': 'user@example.com',
        'email_password': 'password123'
    }
    
    settings_manager = SettingsManager(settings)
    email_manager = EmailConfigManager(settings_manager.get_setting('smtp_server'),
                                       settings_manager.get_setting('smtp_port'),
                                       settings_manager.get_setting('sender_email'),
                                       settings_manager.get_setting('email_password'))