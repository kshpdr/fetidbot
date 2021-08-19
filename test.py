from PIL import Image, ExifTags
from PIL.ExifTags import TAGS

img = Image.open("photos/camphoto_342241519.JPG")
print(img.info["comment"].decode("utf-8"))