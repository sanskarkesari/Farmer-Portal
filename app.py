from flask import Flask, request, render_template
import numpy as np
import pickle
import sklearn

app = Flask(__name__)

# Load models
dtr = pickle.load(open('dtr.pkl', 'rb'))
preprocessor = pickle.load(open('preprocesser.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))
sc = pickle.load(open('standscaler.pkl', 'rb'))
mx = pickle.load(open('minmaxscaler.pkl', 'rb'))

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Government Schemes Page
@app.route('/schemes')
def schemes():
    # Sample data for government schemes (can be replaced with a database or API call)
    schemes_data = [
        {
            "name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
            "description": "Financial support of Rs. 6,000 per year to small and marginal farmers.",
            "link": "https://pmkisan.gov.in"
        },
        {
            "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
            "description": "Crop insurance scheme to protect farmers against crop losses.",
            "link": "https://pmfby.gov.in"
        },
        {
            "name": "Kisan Credit Card (KCC)",
            "description": "Provides farmers with timely access to credit for agricultural needs.",
            "link": "https://kcc.org.in"
        },
        {
            "name": "National Mission for Sustainable Agriculture (NMSA)",
            "description": "Promotes sustainable agriculture practices to increase productivity.",
            "link": "https://nmsa.gov.in"
        }
    ]
    return render_template('schemes.html', schemes=schemes_data)

# Yield prediction page
@app.route('/yield', methods=['GET', 'POST'])
def predictyield():
    if request.method == 'POST':
        Year = request.form['Year']
        average_rain_fall_mm_per_year = request.form['average_rain_fall_mm_per_year']
        pesticides_tonnes = request.form['pesticides_tonnes']
        avg_temp = request.form['avg_temp']
        Area = request.form['Area']
        Item = request.form['Item']

        features = np.array([[Year, average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp, Area, Item]], dtype=object)
        transformed_features = preprocessor.transform(features)
        prediction = dtr.predict(transformed_features).reshape(1, -1)

        return render_template('yield.html', prediction=prediction[0][0])
    return render_template('yield.html')

# Crop prediction page
@app.route('/crop', methods=['GET', 'POST'])
def predictcrop():
    if request.method == 'POST':
        N = request.form['Nitrogen']
        P = request.form['Phosporus']
        K = request.form['Potassium']
        temp = request.form['Temperature']
        humidity = request.form['Humidity']
        ph = request.form['pH']
        rainfall = request.form['Rainfall']

        feature_list = [N, P, K, temp, humidity, ph, rainfall]
        single_pred = np.array(feature_list).reshape(1, -1)

        mx_features = mx.transform(single_pred)
        sc_mx_features = sc.transform(mx_features)
        prediction = model.predict(sc_mx_features)

        crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                     8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                     14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                     19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}

        if prediction[0] in crop_dict:
            crop = crop_dict[prediction[0]]
            result = "{} is the best crop to be cultivated right there".format(crop)
        else:
            result = "Sorry, we could not determine the best crop to be cultivated with the provided data."
        return render_template('crop.html', result=result)
    return render_template('crop.html')

if __name__ == "__main__":
    app.run(debug=True)