import numpy as np
from keras.models import load_model
from PIL import Image


model = load_model("saved_models/facegenerator.h5")
random_noise_dimension = 100
noise = np.random.normal(0, 1, (1, random_noise_dimension))
generated_image = model.predict(noise)
# Normalized (-1 to 1) pixel values to the real (0 to 256) pixel values.
generated_image = (generated_image+1)*127.5
print(generated_image)
# Drop the batch dimension. From (1,w,h,c) to (w,h,c)
generated_image = np.reshape(generated_image, (128, 128, 3))

image = Image.fromarray(generated_image, "RGB")
image.save("prediction.png")