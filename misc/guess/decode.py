import io
import subprocess

from PIL import Image

with Image.open('output.png') as image:
    width, height = image.size
    data = list(image.getdata())

output = Image.new('1', (width, height))

# hopefully there are enough channels
output_data = []
for pixel in data:
    bit = 0
    for channel in pixel[:3]:
        bit ^= channel & 1
    output_data.append(bit)

output.putdata(output_data)

file = io.BytesIO()
output.save(file, format='png')

result = subprocess.check_output(
    ['tesseract', '-', '-', '--psm', '6'],
    input=file.getvalue(),
)

print(result.decode('utf-8').strip())
