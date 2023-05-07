import secrets
import string

char_string = string.ascii_letters + string.digits

def generate_random_string(size):
    return ''.join(secrets.choice(char_string) for _ in range(size))
