from flask import request, jsonify, send_from_directory, render_template
from app import app
from extract import *
import joblib
import os
import numpy as np

# Répertoire de quarantaine
QUARANTAINE_DIR = 'quarantaine'

@app.route('/')
def accueil():
    return render_template("index.html")

@app.route('/malware_test', methods=['POST'])
def malware_test():
    if 'file' not in request.files:
        return {"message": "No file part"}
    file = request.files['file']
    
    if file.filename == '':
        return  {"message": "Aucun fichier selectionné"}
    if file.filename != '':
        filename = file.filename
        filepath = os.path.join(QUARANTAINE_DIR, filename)
        file.save(os.path.join(filepath))
        features = extract_malware_features(filepath)
        
        model = joblib.load('model.pkl')
        y_pred = model.predict(np.array(list(features.values())) .reshape(1, -1))
        if(y_pred[0] == 0):
            return  {"y_pred": "0"}
        else:
            return {"y_pred": "1"}
    
    return {"message": "Type de fichier invalide"}


@app.route('/*')
def index_route():
    return render_template("index.html")