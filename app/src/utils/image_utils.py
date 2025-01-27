from PIL import Image

def resize_and_crop_image(image_path: str, goal_height: int, goal_width: int):
    img = Image.open(image_path)

    ratio = goal_width / goal_height
    image_ratio = img.width / img.height
    if image_ratio > ratio:
        new_width = int(goal_height * image_ratio)
        new_height = goal_height
    else:
        new_width = goal_width
        new_height = int(goal_width / image_ratio)

    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    start_x = (new_width - goal_width) // 2
    start_y = (new_height - goal_height) // 2

    img = img.crop((start_x, start_y, goal_width+start_x, goal_height+start_y))
    img.save(image_path) # Overwrite the original image


if __name__ == "__main__":
    resize_and_crop_image("test.jpg", 100, 100)