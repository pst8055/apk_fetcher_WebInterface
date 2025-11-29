import os
from gpapi.googleplay import GooglePlayAPI
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("GOOGLE_EMAIL")
PASSWORD = os.getenv("GOOGLE_PASSWORD")
GSF_ID = os.getenv("GOOGLE_GSF_ID")
LOCALE = "en_US"
TIMEZONE = "UTC"

# Monkey patch DNS for android.clients.google.com
import socket
original_getaddrinfo = socket.getaddrinfo

def patched_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    if host == 'android.clients.google.com':
        # Use one of the IPs we found
        return original_getaddrinfo('142.251.222.110', port, family, type, proto, flags)
    return original_getaddrinfo(host, port, family, type, proto, flags)

socket.getaddrinfo = patched_getaddrinfo

print(f"Testing with Email: {EMAIL}, GSF_ID: {GSF_ID}")

try:
    api = GooglePlayAPI(locale=LOCALE, timezone=TIMEZONE)
    if GSF_ID:
        print("Logging in with GSF ID...")
        api.login(email=EMAIL, password=PASSWORD, gsfId=GSF_ID)
    else:
        print("Logging in without GSF ID...")
        api.login(email=EMAIL, password=PASSWORD)
    
    print("Login successful!")
    
    package_id = "com.google.android.keep"
    print(f"Attempting to download {package_id}...")
    
    data = api.download(package_id)
    print("Download generator created successfully.")
    
    # Try to fetch the first chunk
    first_chunk = next(data)
    print(f"First chunk received, size: {len(first_chunk)} bytes")
    
except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()
