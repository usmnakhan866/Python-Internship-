#Python Program to Shorten URLs (Using TinyURL)

import pyshorteners

def shorturl(longurl):
    shortener = pyshorteners.Shortener()
    short_url = shortener.tinyurl.short(longurl)
    return short_url
long_url=input("ENTER THE LONG URL:")
try:
    print("Short URL is :",shorturl(long_url))
except Exception as e:
    print("An error occurred:", e)
