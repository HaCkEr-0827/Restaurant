import random
from django.core.cache import cache

def generate_otp():
    return str(random.randint(100000, 999999))

def save_otp_to_cache(phone_number, otp, timeout=300):  # 5 daqiqa
    cache.set(f"otp:{phone_number}", otp, timeout)

def verify_otp_from_cache(phone_number, otp):
    cached_otp = cache.get(f"otp:{phone_number}")
    return cached_otp == otp