from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle

# Load the trained model and imputer
model_path = "model.pkl"
imputer_path = "imputer.pkl"

with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

with open(imputer_path, 'rb') as imputer_file:
    imputer = pickle.load(imputer_file)

# Define genre columns
genre_columns = ['Genre_Action', 'Genre_Comedy', 'Genre_Drama', 'Genre_Horror', 'Genre_SciFi']

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form
        year_of_release = float(data['year_of_release'])
        metascore = float(data['metascore'])
        budget = float(data['budget'])
        runtime = float(data['runtime'])
        votes = float(data['votes'])
        imdb_rating = float(data['imdb_rating'])
        selected_genre = data['genre']

        # Initialize genre encoding
        genre_dict = {genre: 0 for genre in genre_columns}
        if selected_genre in genre_dict:
            genre_dict[selected_genre] = 1

        # Create feature array
        user_features = [year_of_release, metascore, budget, runtime, votes, imdb_rating] + list(genre_dict.values())
        user_features = np.array(user_features).reshape(1, -1)
        user_features = imputer.transform(user_features)

        # Predict Gross Revenue
        predicted_gross = model.predict(user_features)[0] * 0.0000001  # Convert to Crores
        return render_template('result.html', prediction=f"₹ {predicted_gross:,.2f} Crs")
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
