# config.py

class SettingsManager:
    """
    A class to manage application settings.
    """
    APP_NAME = 'MyApplication'
    VERSION = '1.0.0'
    DEBUG = True
    CONFIG_PATH = '/path/to/config'

    @classmethod
    def get_config(cls):
        return {
            'app_name': cls.APP_NAME,
            'version': cls.VERSION,
            'debug': cls.DEBUG,
            'config_path': cls.CONFIG_PATH
        }

class EmailConfigManager:
    """
    A class to manage email configurations.
    """
    EMAIL_HOST = 'smtp.example.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'user@example.com'
    EMAIL_HOST_PASSWORD = 'password'

    @classmethod
    def get_email_config(cls):
        return {
            'host': cls.EMAIL_HOST,
            'port': cls.EMAIL_PORT,
            'use_tls': cls.EMAIL_USE_TLS,
            'user': cls.EMAIL_HOST_USER,
            'password': cls.EMAIL_HOST_PASSWORD
        }