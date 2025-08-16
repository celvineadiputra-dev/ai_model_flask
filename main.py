import joblib
from flask import Flask, request, jsonify
import numpy as np
import keras
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from PIL import Image
import io

app = Flask(__name__)

model_diabetes = joblib.load('model/diabetes-76.plk')
model_gunting_batu_kertas = keras.models.load_model('model/model-gunting-batu-kertas.keras')

@app.route('/predict/diabetes', methods=['POST'])
def predict_diabetes():
    data = request.get_json()

    pregnancies = data.get('pregnancies')
    glucose = data.get('glucose')
    blood_pressure = data.get('blood_pressure')
    skin_thickness = data.get('skin_thickness')
    insulin = data.get('insulin')
    diabetes_pedigree_function = data.get('diabetes_pedigree_function')
    bmi = data.get('bmi')
    age = data.get('age')

    raw_data = [pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age]
    input_data = np.array(raw_data).reshape(1, -1)

    prediction = model_diabetes.predict(input_data)

    if prediction[0] == 1:
        result = "Positive Diabetes"
    else:
        result = "Negative Diabetes"

    return jsonify({
        'meta': {
            "status": "success",
            'message': "Prediction successful",
        },
        "data": {
            "prediction": result,
        }
    })


@app.route('/predict/gunting-batu-kertas', methods=['POST'])
def predict_gunting_batu_kertas():
    class_labels = ['paper', 'rock', 'scissors']

    if "file" not in request.files:
        return jsonify({
            'meta': {
                "status": "failure",
                "message": "No file found",
            },
            "data": {}
        })

    file = request.files['file']

    if file.filename == '':
        return jsonify({
            'meta': {
                "status": "failure",
                "message": "No file found",
            },
            "data": {}
        })

    try:
        image_bytes = file.read()
        img = Image.open(io.BytesIO(image_bytes))
        img = img.resize((200, 200))

        image_array = image.img_to_array(img)
        image_array = np.expand_dims(image_array, axis=0)

        image_preprocess = tf.keras.applications.efficientnet.preprocess_input(image_array)

        classes = model_gunting_batu_kertas.predict(image_preprocess)
        class_index = np.argmax(classes)

        predicted_label = class_labels[class_index]
        return jsonify({
            'meta': {
                "status": "success",
                "message": "Prediction successful",
            },
            "data": {
                "prediction": predicted_label,
            }
        })
    except Exception as e:
        return jsonify({
            'meta': {
                "status": "failure",
                "message": str(e),
            },
            "data": {}
        })


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
