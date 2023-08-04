from flask import render_template, request, redirect, url_for
from app import app
import pandas as pd
import matplotlib
from datetime import datetime, timedelta
from matplotlib.dates import date2num
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def analyze_file():
    material = request.form['material']
    area = float(request.form['area'])
    file = request.files['file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    data_raw = pd.read_excel(filepath, header=13)
    data = data_raw.iloc[:, :4]
    data.columns = ['time','Analog1','Analog2','Analog3']
    data['Load_N'] = data['Analog1']*200
    data['Strain_percentage']=data['Analog2']/data['Analog2'].median()
    data['Stroke_mm'] = data['Analog3']*6
    def time_to_seconds(time):
       return time.hour*3600 + time.minute*60 + time.second
    data['time_seconds'] = data['time'].apply(time_to_seconds)
    plt.plot(data['time_seconds'], data['Load_N'])
    image_filename = 'result.png'
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    image_url = url_for('static', filename=f'images/{image_filename}')
    plt.savefig(image_path)
    return render_template('result.html', image_path=image_url)