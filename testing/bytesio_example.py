from io import BytesIO

with open("sample_image.jpg", "rb") as f:
    buf = BytesIO(f.read())

with open("image_from_memory.jpg", "wb") as f:
    f.write(buf.read())
