from cryptography.fernet import Fernet
from agencybackend.settings import FERNET_KEY
from dotenv import load_dotenv
load_dotenv()
import os

key = os.getenv('FERNET_KEY')
print(key)
f = Fernet(key)

token = b"gAAAAABpOPx0zaJTQ-yx5L_bpqMZPp9z1aMYZYzRBb_7p8eTL1TVSod7MS0Gp8ckdfD-dnIDjxt50Og6aPMFaDRUuLl_H0TOKA14f8KU4D05UuRmOQApb_U="

print(f.decrypt(token))
