from PIL import Image


def paste_cropped_image(original_image_path, cropped_image_path, position=(0, 0)):
    try:
        # Open the original image
        original_image = Image.open(original_image_path)

        # Open the cropped image with an alpha channel
        cropped_image = Image.open(cropped_image_path).convert("RGBA")

        # Paste the cropped image onto the original image
        original_image.paste(cropped_image, position, cropped_image)

        # Save the modified image
        original_image.save("combined_image.png")

        print("Image pasting successful!")
    except Exception as e:
        print(f"An error occurred: {e}")


# 輸入原圖路徑和帶有透明通道的切割後的圖片路徑，position是切割圖片貼回原圖的位置，默認為(0, 0)左上角。
original_image_path = "parking_with_alpha.png"
cropped_image_path = "img2.png"
position = (58, 143)  # 修改position數值調整切割圖片在原圖中的位置

paste_cropped_image(original_image_path, cropped_image_path, position)
