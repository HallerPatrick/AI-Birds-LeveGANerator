from keras.models import load_model
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def generate_single_image(model_path, image_save_path, random_noise_dimension=100):
    noise = np.random.normal(0, 1, (1, random_noise_dimension))
    model = load_model(model_path)
    generated_image = model.predict(noise)
    # Normalized (-1 to 1) pixel values to the real (0 to 256) pixel values.
    generated_image = (generated_image+1)*127.5
    
    # Drop the batch dimension. From (1,w,h,c) to (w,h,c)
    generated_image = np.reshape(generated_image, (64, 64, 3))

    image = Image.fromarray(generated_image, "RGB")
    image.save("tmp/" + image_save_path)
    return "tmp/" + image_save_path

def generate_25_images(generator_model, folder_path):
    rows, columns = 5, 5
    noise = np.random.normal(
        0, 1, (rows * columns, 100))

    generator = load_model(generator_model)
    generator.compile(loss="binary_crossentropy", optimizer="SGD")

    generated_images = generator.predict(noise)

    generated_images = 0.5 * generated_images + 0.5

    image_count = 0

    for _ in range(rows):
        for _ in range(columns):
            img = generated_images[image_count, :]
            print(len(img))
            plt.imsave(folder_path + '/' + '{}.png'.format(image_count), img, cmap="spring")
            image_count += 1

