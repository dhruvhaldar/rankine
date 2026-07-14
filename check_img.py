from PIL import Image

img = Image.open('invalid_screenshot.png')
print(img.size)
# P0 input field is near the top
# Let's crop the area around P0 and see
