<<<<<<< HEAD
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageOps

# Задайте путь к папке с изображениями
image_folder_path = "C:/Collage"  # Укажите сюда ваш путь
allowed_extensions = ('.jpg', '.jpeg', '.png')

def get_image_selection(image_folder):
    images = [f for f in os.listdir(image_folder) if f.lower().endswith(allowed_extensions)]

    if not images:
        print("Ошибка: В указанной папке нет изображений с выбранными расширениями.")
        return []

    print("Доступные изображения:")
    for i, image_name in enumerate(images):
        print(f"{i + 1}: {image_name}")

    selected_images = []
    while True:
        user_input = input("Введите номера изображений, которые вы хотите выбрать (через запятую), 'r' для случайного выбора, или 'q' для выхода: ")
        if user_input.lower() == 'q':
            break
        elif user_input.lower() == 'r':
            count = int(input("Сколько изображений случайно выбрать? (max {}): ".format(len(images))))
            if 0 < count <= len(images):
                selected_images = random.sample(images, count)
                print("Выбранные изображения:", selected_images)
                return selected_images
            else:
                print("Некорректное число.")
        else:
            try:
                indices = [int(x.strip()) - 1 for x in user_input.split(',')]
                selected_images = [images[i] for i in indices if 0 <= i < len(images)]
                if selected_images:
                    print("Выбранные изображения:", selected_images)
                    return selected_images
                else:
                    print("Не выбрано ни одного изображения.")
            except ValueError:
                print("Некорректный ввод. Попробуйте снова.")

def set_image_size():
    while True:
        user_input = input("Введите размер изображений в формате 'ширина,высота' (например, 200,200) или 'q' для выхода: ")
        if user_input.lower() == 'q':
            return (200, 200)  # Вернуть размер по умолчанию
        try:
            width, height = map(int, user_input.split(','))
            return (width, height)
        except ValueError:
            print("Некорректный ввод. Пожалуйста, попробуйте снова.")

def save_collage(output_file):
    valid_formats = ['JPEG', 'PNG', 'BMP']
    while True:
        user_input = input("Выберите формат для сохранения ({}): ".format(', '.join(valid_formats))).upper()
        if user_input in valid_formats:
            return user_input
        else:
            print("Некорректный формат. Пожалуйста, попробуйте снова.")

def generate_collage(selected_images, collage_title, output_file, img_size=(200, 200), border=10):
    if not selected_images:
        print("Ошибка: Не выбрано ни одного изображения для коллажа.")
        return

    try:
        title_font = ImageFont.truetype("Arial.ttf", 20)
    except IOError:
        title_font = ImageFont.load_default()

    n_images = len(selected_images)
    grid_size = int(n_images ** 0.5) + 1
    collage_width = grid_size * (img_size[0] + border) - border
    collage_height = collage_width + 50

    collage = Image.new('RGB', (collage_width, collage_height), color=(220, 220, 220))
    x_offset = 0
    y_offset = 50

    for i, image_name in enumerate(selected_images):
        img_path = os.path.join(image_folder_path, image_name)
        img = Image.open(img_path)
        img = ImageOps.fit(img, img_size, method=Image.LANCZOS)

        collage.paste((0, 0, 0), (x_offset, y_offset, x_offset + img_size[0] + border, y_offset + img_size[1] + border))
        collage.paste(img, (x_offset + border // 2, y_offset + border // 2))

        x_offset += img_size[0] + border
        if (i + 1) % grid_size == 0:
            x_offset = 0
            y_offset += img_size[1] + border

    draw = ImageDraw.Draw(collage)
    title_bbox = draw.textbbox((0, 0), collage_title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((collage_width - title_width) // 2, 10), collage_title, font=title_font, fill=(0, 0, 0))

    collage.save(output_file, save_collage(output_file))
    print(f"Коллаж сохранен как '{output_file}'")

def main():
    collage_title_text = input("Введите заголовок для коллажа: ")
    output_file_name = "C:/path_to_save_collage/collage"  # Укажите путь без расширения

    selected_images = get_image_selection(image_folder_path)
    
    custom_size = set_image_size()
    generate_collage(selected_images, collage_title_text, f"{output_file_name}.jpg", img_size=custom_size)

if __name__ == "__main__":
=======
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageOps

# Задайте путь к папке с изображениями
image_folder_path = "C:/Collage"  # Укажите сюда ваш путь
allowed_extensions = ('.jpg', '.jpeg', '.png')

def get_image_selection(image_folder):
    images = [f for f in os.listdir(image_folder) if f.lower().endswith(allowed_extensions)]

    if not images:
        print("Ошибка: В указанной папке нет изображений с выбранными расширениями.")
        return []

    print("Доступные изображения:")
    for i, image_name in enumerate(images):
        print(f"{i + 1}: {image_name}")

    selected_images = []
    while True:
        user_input = input("Введите номера изображений, которые вы хотите выбрать (через запятую), 'r' для случайного выбора, или 'q' для выхода: ")
        if user_input.lower() == 'q':
            break
        elif user_input.lower() == 'r':
            count = int(input("Сколько изображений случайно выбрать? (max {}): ".format(len(images))))
            if 0 < count <= len(images):
                selected_images = random.sample(images, count)
                print("Выбранные изображения:", selected_images)
                return selected_images
            else:
                print("Некорректное число.")
        else:
            try:
                indices = [int(x.strip()) - 1 for x in user_input.split(',')]
                selected_images = [images[i] for i in indices if 0 <= i < len(images)]
                if selected_images:
                    print("Выбранные изображения:", selected_images)
                    return selected_images
                else:
                    print("Не выбрано ни одного изображения.")
            except ValueError:
                print("Некорректный ввод. Попробуйте снова.")

def set_image_size():
    while True:
        user_input = input("Введите размер изображений в формате 'ширина,высота' (например, 200,200) или 'q' для выхода: ")
        if user_input.lower() == 'q':
            return (200, 200)  # Вернуть размер по умолчанию
        try:
            width, height = map(int, user_input.split(','))
            return (width, height)
        except ValueError:
            print("Некорректный ввод. Пожалуйста, попробуйте снова.")

def save_collage(output_file):
    valid_formats = ['JPEG', 'PNG', 'BMP']
    while True:
        user_input = input("Выберите формат для сохранения ({}): ".format(', '.join(valid_formats))).upper()
        if user_input in valid_formats:
            return user_input
        else:
            print("Некорректный формат. Пожалуйста, попробуйте снова.")

def generate_collage(selected_images, collage_title, output_file, img_size=(200, 200), border=10):
    if not selected_images:
        print("Ошибка: Не выбрано ни одного изображения для коллажа.")
        return

    try:
        title_font = ImageFont.truetype("Arial.ttf", 20)
    except IOError:
        title_font = ImageFont.load_default()

    n_images = len(selected_images)
    grid_size = int(n_images ** 0.5) + 1
    collage_width = grid_size * (img_size[0] + border) - border
    collage_height = collage_width + 50

    collage = Image.new('RGB', (collage_width, collage_height), color=(220, 220, 220))
    x_offset = 0
    y_offset = 50

    for i, image_name in enumerate(selected_images):
        img_path = os.path.join(image_folder_path, image_name)
        img = Image.open(img_path)
        img = ImageOps.fit(img, img_size, method=Image.LANCZOS)

        collage.paste((0, 0, 0), (x_offset, y_offset, x_offset + img_size[0] + border, y_offset + img_size[1] + border))
        collage.paste(img, (x_offset + border // 2, y_offset + border // 2))

        x_offset += img_size[0] + border
        if (i + 1) % grid_size == 0:
            x_offset = 0
            y_offset += img_size[1] + border

    draw = ImageDraw.Draw(collage)
    title_bbox = draw.textbbox((0, 0), collage_title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((collage_width - title_width) // 2, 10), collage_title, font=title_font, fill=(0, 0, 0))

    collage.save(output_file, save_collage(output_file))
    print(f"Коллаж сохранен как '{output_file}'")

def main():
    collage_title_text = input("Введите заголовок для коллажа: ")
    output_file_name = "C:/path_to_save_collage/collage"  # Укажите путь без расширения

    selected_images = get_image_selection(image_folder_path)
    
    custom_size = set_image_size()
    generate_collage(selected_images, collage_title_text, f"{output_file_name}.jpg", img_size=custom_size)

if __name__ == "__main__":
>>>>>>> 8181b77b8f34c71da2caa6f3c2d44060d042c6ac
    main()