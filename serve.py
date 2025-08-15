import joblib
from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

model = joblib.load('model/diabetes-76.plk')

@app.route('/predict', methods=['POST'])
def predict():
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

    prediction = model.predict(input_data)

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


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
