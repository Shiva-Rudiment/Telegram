from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

def prediction(file_name):
    np.set_printoptions(suppress=True)
    model = load_model("keras_model.h5", compile=False)
    
    # Читаем метки и убираем пробелы и переносы
    class_names = [line.strip() for line in open("labels.txt", "r", encoding='utf-8')]

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(file_name).convert("RGB")
    image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array

    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]  # Метка уже без \n
    confidence = prediction[0][index]

    # Проверяем индекс или часть строки
    if index in [0, 2]:  # 0 - спелые бананы, 2 - спелые яблоки
        class_pr = 'Это спелый фрукт, вы можете его приобрести'
    else:  # Все остальные случаи (1 - гнилые бананы, 3 - неспелые яблоки)
        class_pr = "Это гнилой/неспелый фрукт, нежелательно его приобретать"
    
    return f"{class_name}: {class_pr} (Уверенность: {confidence:.2f})"