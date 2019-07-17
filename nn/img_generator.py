from keras.models import load_model
import numpy as np
from PIL import Image

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