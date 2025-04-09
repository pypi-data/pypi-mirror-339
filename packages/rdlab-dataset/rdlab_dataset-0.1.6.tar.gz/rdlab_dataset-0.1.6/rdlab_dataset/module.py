import io
import json
import os
import pickle
import random
import matplotlib
import pkg_resources
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


class KhmerWordLoader:
    def __init__(self, filepath=None):
        if filepath is None:
            self.filepath = pkg_resources.resource_filename('rdlab_dataset', 'data/wild_khmer_data.pkl')
        else:
            self.filepath = filepath
        self.words = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.filepath):
            print(f"Word file not found: {self.filepath}")
            return ["No Data Here!"]
        with open(self.filepath, 'rb') as f:
            data = pickle.load(f)
        return data if data else ["No Data Here!"]

    def get_all_words(self):
        return self.words

    def __len__(self):
        return len(self.words)

    def get_first_word(self):
        return self.words[0] if self.words else None

    def get_n_first_words(self, n=5):
        return self.words[:n]

    def find_word(self, word):
        return word in self.words


class KhmerAddressLoader:
    def __init__(self, filepath=None):
        if filepath is None:
            self.filepath = pkg_resources.resource_filename('rdlab_dataset', 'data/address_kh_data.pkl')
        else:
            self.filepath = filepath
        self.addresses = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.filepath):
            print(f"Address file not found: {self.filepath}")
            return ["No Data Here!"]
        with open(self.filepath, 'rb') as f:
            data = pickle.load(f)
        return data if data else ["No Data Here!"]

    def get_all_addresses(self):
        return self.addresses

    def __len__(self):
        return len(self.addresses)

    def get_first_address(self):
        return self.addresses[0] if self.addresses else None

    def get_n_first_addresses(self, n=5):
        return self.addresses[:n]

    def find_address(self, address):
        return address in self.addresses


class KhmerSentencesLoader:
    def __init__(self, filepath=None):
        if filepath is None:
            self.filepath = pkg_resources.resource_filename('rdlab_dataset', 'data/wild_khmer_sentences.pkl')
        else:
            self.filepath = filepath
        self.sentences = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.filepath):
            print(f"Sentence file not found: {self.filepath}")
            return ["No Data Here!"]
        with open(self.filepath, 'rb') as f:
            data = pickle.load(f)
        return data if data else ["No Data Here!"]

    def get_all_sentences(self):
        return self.sentences

    def __len__(self):
        return len(self.sentences)

    def get_first_sentence(self):
        return self.sentences[0] if self.sentences else None

    def get_n_first_sentences(self, n=5):
        return self.sentences[:n]

    def find_sentence(self, sentence):
        return sentence in self.sentences


class ATextImageGenerator:
    def __init__(self, font_path="rdlab_dataset/font", background_path="rdlab_dataset/background", output_folder="generated_images", font_size=48, background_color=(255, 255, 255), text_color=(0, 0, 0), margin=20, customize_font=False):
        self.font_path = pkg_resources.resource_filename('rdlab_dataset', font_path)
        self.output_folder = output_folder
        self.background_path = pkg_resources.resource_filename('rdlab_dataset', background_path)
        self.font_size = font_size
        self.background_color = background_color
        self.text_color = text_color
        self.margin = margin
        self.customize_font = customize_font
        self.font = None

    def load_font(self, font_file=None):
        if font_file and os.path.isfile(font_file):
            self.font = ImageFont.truetype(font_file, self.font_size)
        else:
            default_fonts = [f for f in os.listdir(self.font_path) if f.lower().endswith(".ttf")]
            if not default_fonts:
                raise ValueError(f"No TTF font files found in {self.font_path}")
            default_font_path = os.path.join(self.font_path, default_fonts[0])
            self.font = ImageFont.truetype(default_font_path, self.font_size)

    def random_shift_text_left_right_0_to_10_pixels(self):
        return random.randint(0, 10)

    def random_rotate_sentence_minus_5_to_5_degree(self):
        return random.uniform(-3, 3)

    def add_noise(self, image):
        """Randomly apply one of five noise types with random moderate density."""
        noise_type = random.choice(['gaussian', 'salt_pepper', 'speckle', 'poisson', 'blur'])
        img_array = np.array(image)

        if noise_type == 'gaussian':
            mean = 0
            var = random.uniform(10, 30)
            sigma = var ** 0.5
            gaussian = np.random.normal(mean, sigma, img_array.shape)
            noisy_img = img_array + gaussian
            noisy_img = np.clip(noisy_img, 0, 255)
        
        elif noise_type == 'salt_pepper':
            amount = random.uniform(0.01, 0.05)
            noisy_img = np.copy(img_array)
            # Salt mode
            num_salt = np.ceil(amount * img_array.size * 0.5)
            coords = [np.random.randint(0, i - 1, int(num_salt)) for i in img_array.shape]
            noisy_img[tuple(coords)] = 255
            # Pepper mode
            num_pepper = np.ceil(amount * img_array.size * 0.5)
            coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in img_array.shape]
            noisy_img[tuple(coords)] = 0

        elif noise_type == 'speckle':
            speckle = np.random.randn(*img_array.shape)
            noisy_img = img_array + img_array * speckle * random.uniform(0.05, 0.15)
            noisy_img = np.clip(noisy_img, 0, 255)

        elif noise_type == 'poisson':
            vals = len(np.unique(img_array))
            vals = 2 ** np.ceil(np.log2(vals))
            noisy_img = np.random.poisson(img_array * vals) / float(vals)
            noisy_img = np.clip(noisy_img, 0, 255)

        elif noise_type == 'blur':
            # For blur we use PIL
            radius = random.uniform(1, 2)
            return image.filter(ImageFilter.GaussianBlur(radius))

        return Image.fromarray(noisy_img.astype(np.uint8))

    def generate_image(self, text, font_folder=None):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        if self.customize_font and font_folder:
            font_files = [f for f in os.listdir(font_folder) if f.lower().endswith(".ttf")]
            if not font_files:
                raise ValueError(f"No TTF font files found in {font_folder}")
        else:
            font_folder = self.font_path
            font_files = [f for f in os.listdir(font_folder) if f.lower().endswith(".ttf")]
            if not font_files:
                raise ValueError(f"No TTF font files found in {font_folder}")

        background_files = [f for f in os.listdir(self.background_path) if f.lower().endswith(".jpg")]
        if not background_files:
            raise ValueError(f"No JPG background files found in {self.background_path}")

        for font_file in font_files:
            font_path = os.path.join(font_folder, font_file)
            self.load_font(font_path)

            for background_file in background_files:
                background_path = os.path.join(self.background_path, background_file)
                background_image = Image.open(background_path).convert('RGB')

                shift = self.random_shift_text_left_right_0_to_10_pixels()
                rotation = self.random_rotate_sentence_minus_5_to_5_degree()

                temp_image = Image.new('RGBA', (1, 1), (255, 255, 255, 0))
                draw = ImageDraw.Draw(temp_image)

                bbox = draw.textbbox((0, 0), text, font=self.font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                image_width = text_width + self.margin * 2
                image_height = text_height + self.margin * 2

                text_layer = Image.new('RGBA', (image_width, image_height), (255, 255, 255, 0))
                draw = ImageDraw.Draw(text_layer)

                text_x = self.margin + shift
                text_y = self.margin
                draw.text((text_x, text_y), text, font=self.font, fill=self.text_color+(255,))

                # Rotate the text layer
                rotated_text = text_layer.rotate(rotation, expand=True)

                # Resize background to match rotated text size
                bg_width, bg_height = rotated_text.size
                background = background_image.resize((bg_width, bg_height))

                # Composite text onto background
                combined = Image.alpha_composite(background.convert('RGBA'), rotated_text)

                # Randomly crop equally from top and bottom
                crop_amount = random.randint(5, 20)
                width, height = combined.size
                new_top = crop_amount
                new_bottom = height - crop_amount

                if new_bottom <= new_top:
                    cropped_image = combined
                else:
                    cropped_image = combined.crop((0, new_top, width, new_bottom))

                # Convert back to RGB and add random noise
                final_image = cropped_image.convert('RGB')
                final_image_with_noise = self.add_noise(final_image)

                font_name = os.path.splitext(font_file)[0]
                background_name = os.path.splitext(background_file)[0]
                output_filename = f"{font_name}_{background_name}_noisy_output_image.png"
                output_path = os.path.join(self.output_folder, output_filename)
                final_image_with_noise.save(output_path)
                print(f"Image saved to {output_path}")


class TextArrayListImageGenerator:
    def __init__(self, font_path="font", background_path="background", output_folder="generated_images", font_size=48, background_color=(255, 255, 255), text_color=(0, 0, 0), margin=20, customize_font=False):
        self.font_path = pkg_resources.resource_filename('rdlab_dataset', font_path)
        self.output_folder = output_folder
        self.background_path = pkg_resources.resource_filename('rdlab_dataset', background_path)
        self.font_size = font_size
        self.background_color = background_color
        self.text_color = text_color
        self.margin = margin
        self.customize_font = customize_font
        self.font = None
        self.annotations = []
        self.pickle_data = []

    def load_font(self, font_file=None):
        if font_file and os.path.isfile(font_file):
            self.font = ImageFont.truetype(font_file, self.font_size)
        else:
            default_fonts = [f for f in os.listdir(self.font_path) if f.lower().endswith(".ttf")]
            if not default_fonts:
                raise ValueError(f"No TTF font files found in {self.font_path}")
            default_font_path = os.path.join(self.font_path, default_fonts[0])
            self.font = ImageFont.truetype(default_font_path, self.font_size)

    def random_shift_text_left_right_0_to_10_pixels(self):
        return random.randint(0, 10)

    def random_rotate_sentence_minus_5_to_5_degree(self):
        return random.uniform(-3, 3)

    def add_noise(self, image):
        noise_type = random.choice(['gaussian', 'salt_pepper', 'speckle', 'poisson', 'blur'])
        img_array = np.array(image)

        if noise_type == 'gaussian':
            mean = 0
            var = random.uniform(10, 30)
            sigma = var ** 0.5
            gaussian = np.random.normal(mean, sigma, img_array.shape)
            noisy_img = img_array + gaussian
            noisy_img = np.clip(noisy_img, 0, 255)
        elif noise_type == 'salt_pepper':
            amount = random.uniform(0.01, 0.05)
            noisy_img = np.copy(img_array)
            num_salt = np.ceil(amount * img_array.size * 0.5)
            coords = [np.random.randint(0, i - 1, int(num_salt)) for i in img_array.shape]
            noisy_img[tuple(coords)] = 255
            num_pepper = np.ceil(amount * img_array.size * 0.5)
            coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in img_array.shape]
            noisy_img[tuple(coords)] = 0
        elif noise_type == 'speckle':
            speckle = np.random.randn(*img_array.shape)
            noisy_img = img_array + img_array * speckle * random.uniform(0.05, 0.15)
            noisy_img = np.clip(noisy_img, 0, 255)
        elif noise_type == 'poisson':
            vals = len(np.unique(img_array))
            vals = 2 ** np.ceil(np.log2(vals))
            noisy_img = np.random.poisson(img_array * vals) / float(vals)
            noisy_img = np.clip(noisy_img, 0, 255)
        elif noise_type == 'blur':
            radius = random.uniform(1, 2)
            return image.filter(ImageFilter.GaussianBlur(radius))

        return Image.fromarray(noisy_img.astype(np.uint8))

    def generate_images(self, text_list, font_folder=None, save_as_pickle=False):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        if self.customize_font and font_folder:
            font_folder = pkg_resources.resource_filename('rdlab_dataset', font_folder)
            font_files = [f for f in os.listdir(font_folder) if f.lower().endswith(".ttf")]
        else:
            font_files = [f for f in os.listdir(self.font_path) if f.lower().endswith(".ttf")]

        background_files = [f for f in os.listdir(self.background_path) if f.lower().endswith(".jpg")]

        for text in text_list:
            now = datetime.now()
            folder_name = now.strftime("image_folder_date_%d_%m_%y_time_%H_%M_%S_%f")[:-3]
            batch_output_folder = os.path.join(self.output_folder, folder_name)
            if not save_as_pickle:
                os.makedirs(batch_output_folder, exist_ok=True)

            for font_file in font_files:
                font_path = os.path.join(font_folder if self.customize_font else self.font_path, font_file)
                self.load_font(font_path)

                for background_file in background_files:
                    background_path = os.path.join(self.background_path, background_file)
                    background_image = Image.open(background_path).convert('RGB')

                    shift = self.random_shift_text_left_right_0_to_10_pixels()
                    rotation = self.random_rotate_sentence_minus_5_to_5_degree()

                    temp_image = Image.new('RGBA', (1, 1), (255, 255, 255, 0))
                    draw = ImageDraw.Draw(temp_image)
                    bbox = draw.textbbox((0, 0), text, font=self.font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]

                    image_width = text_width + self.margin * 2
                    image_height = text_height + self.margin * 2

                    text_layer = Image.new('RGBA', (image_width, image_height), (255, 255, 255, 0))
                    draw = ImageDraw.Draw(text_layer)
                    text_x = self.margin + shift
                    text_y = self.margin
                    draw.text((text_x, text_y), text, font=self.font, fill=self.text_color+(255,))

                    rotated_text = text_layer.rotate(rotation, expand=True)
                    bg_width, bg_height = rotated_text.size
                    background = background_image.resize((bg_width, bg_height))
                    combined = Image.alpha_composite(background.convert('RGBA'), rotated_text)

                    crop_amount = random.randint(5, 20)
                    width, height = combined.size
                    new_top = crop_amount
                    new_bottom = height - crop_amount
                    if new_bottom <= new_top:
                        cropped_image = combined
                    else:
                        cropped_image = combined.crop((0, new_top, width, new_bottom))

                    final_image = cropped_image.convert('RGB')
                    final_image_with_noise = self.add_noise(final_image)

                    datetime_part = datetime.now().strftime("%d_%m_%y_%H_%M_%S_%f")[:-3]
                    font_name = os.path.splitext(font_file)[0]
                    background_name = os.path.splitext(background_file)[0]
                    filename = f"{font_name}_{background_name}_{datetime_part}_noisy.png"
                    output_path = os.path.join(batch_output_folder, filename)

                    if not save_as_pickle:
                        final_image_with_noise.save(output_path)
                        print(f"Image saved to {output_path}")

                    self.annotations.append({
                        "image_path": output_path.replace("\\", "/"),
                        "label": text
                    })

                    img_byte_arr = io.BytesIO()
                    final_image_with_noise.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()
                    self.pickle_data.append({
                        "image": img_byte_arr,
                        "label": text,
                        "path": output_path.replace("\\", "/")
                    })

        self.save_annotations(save_as_pickle)

    def save_annotations(self, save_as_pickle=False):
        if save_as_pickle:
            annotation_pkl_path = os.path.join(self.output_folder, "annotation.pkl")
            with open(annotation_pkl_path, 'wb') as f:
                pickle.dump(self.pickle_data, f)
            print(f"Annotations with images saved to {annotation_pkl_path}")
        else:
            annotation_txt_path = os.path.join(self.output_folder, "annotation.txt")
            with open(annotation_txt_path, 'w', encoding='utf-8') as f:
                for item in self.annotations:
                    f.write(f"{item['image_path']}\t{item['label']}\n")
            print(f"Annotations saved to {annotation_txt_path}")

