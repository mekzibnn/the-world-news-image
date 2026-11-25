from PIL import Image

def verify():
    img = Image.open("entry.png")
    if img.size != (1024, 1024):
        print(f"FAILED: Expected 1024x1024, got {img.size}")
        exit(1)
    else:
        print("SUCCESS: 1024x1024 confirmed")

if __name__ == "__main__":
    verify()
