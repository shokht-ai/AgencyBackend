from django.db import models
from cryptography.fernet import Fernet
from agencybackend.settings import FERNET_KEY
# from cryptography.exceptions import InvalidKey

cipher_suite = Fernet(FERNET_KEY)

class EncryptedField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255  # Shifrlangan qiymatning uzunligi
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value:
            # Ma'lumotni shifrlash
            return cipher_suite.encrypt(value.encode('utf-8')).decode('utf-8')
        return value

    def from_db_value(self, value, expression, connection):
        try:
            # print(type(value), value)
            # print(cipher_suite.decrypt(value).decode('utf-8'))
            if value:
                # DB dan olib kelganda shifrlangan qiymatni dekryptekatsiya qilish
                return cipher_suite.decrypt(value.encode('utf-8')).decode('utf-8')
            return value
        except :
            return value

    def to_python(self, value):
        return value
