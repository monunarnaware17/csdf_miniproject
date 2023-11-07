from PIL import Image, ImageChops, ImageEnhance

def ela_analysis(image_path, output_path, quality=90):
    try:
        original_image = Image.open(image_path)
        original_image.save("temp.jpg", "JPEG", quality=quality)
        temp_image = Image.open("temp.jpg")

        # Adjusting brightness and contrast of the original image for clarity
        original_image = ImageEnhance.Brightness(original_image).enhance(1.5)  # Adjust brightness
        original_image = ImageEnhance.Contrast(original_image).enhance(1.5)  # Adjust contrast

        ela_image = ImageChops.difference(temp_image, original_image)
        extrema = ela_image.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        scale = 255.0 / max_diff

        ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
        ela_image.save(output_path)
        return ela_image
    except Exception as e:
        print("Error performing ELA analysis:", str(e))
        return None


def forgery_detection(image_path, output_path, block_size=16, threshold=30):
    ela_image = ela_analysis(image_path, output_path)

    if ela_image is not None:
        width, height = ela_image.size
        for x in range(0, width, block_size):
            for y in range(0, height, block_size):
                block = ela_image.crop((x, y, x + block_size, y + block_size))
                extrema = block.getextrema()
                max_diff = max([ex[1] for ex in extrema])
                if max_diff > threshold:
                    print(f"Potential forgery detected in block at ({x}, {y})")

if __name__ == "__main__":
    image_path = "C:/Users/Admin/Desktop/CSDF/monu.jpeg"  # Replace with the correct input image path
    output_ela_path = "C:/Users/Admin/Desktop/CSDF/temp.jpeg"  # Replace with the desired output path for ELA result

    forgery_detection(image_path, output_ela_path)
