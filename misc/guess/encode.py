import random

from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)

IMAGE_PATH = 'image.png'
OUTPUT_PATH = 'output.png'

FLAG_PATH = 'flag.txt'
FONT_PATH = 'font.ttf'

PADDING = 100

with open(FLAG_PATH, 'r') as f:
    flag = f.read().strip()

with Image.open(IMAGE_PATH) as original_image:
    width, height = original_image.size
    mode = original_image.mode
    original_data = list(original_image.getdata())

# figure out what font size to use
scale = 1 << 10
test_font = ImageFont.truetype(FONT_PATH, size=scale)
text_width = int(sum(test_font.getlength(c) for c in flag))
font_size = scale * (width - 2 * PADDING) // text_width

# write the flag text
flag_image = Image.new('1', (width, height), 1)
font = ImageFont.truetype(FONT_PATH, font_size)
context = ImageDraw.Draw(flag_image)
context.text(
    (width // 2, height // 2),
    flag,
    anchor='mm',
    font=font,
    fill=0
)
flag_data = flag_image.getdata()

# create the output image
output_image = Image.new(mode, (width, height))

# let's hope the image has the relevant channels
def set_channel_bits(pixel, bits):
    new = []
    for channel, bit in zip(pixel, bits):
        channel &= ~1
        channel |= bit
        new.append(channel)
    new.extend(pixel[len(bits):])
    return tuple(new)

# THE IMPORTANT PART!!!
output_data = []
for original_pixel, flag_pixel in zip(original_data, flag_data):
    a = random.randrange(2)
    b = random.randrange(2)
    c = a ^ b ^ flag_pixel
    output_data.append(
        set_channel_bits(original_pixel, (a, b, c))
    )

output_image.putdata(output_data)
output_image.save(OUTPUT_PATH)
