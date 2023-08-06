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
    load0 = float(request.form['load0'])
    distortion0= float(request.form['distortion0'])
    distortiongaugecollection1 = float(request.form['distortiongaugecollection1'])
    file = request.files['file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    data_raw = pd.read_excel(filepath, header=13)
    data = data_raw.iloc[:, :4]
    data.columns = ['time','Analog1','Analog2','Analog3']
    data['Load_N'] = data['Analog1']*200
    data['Strain_percentage']=data['Analog2']/data['Analog2'].median()
    data['Stroke_mm'] = data['Analog3']*6
    data['time_seconds'] =[i * 0.05 for i in range(len(data))]
    
    plt.xlabel('Time (s)')
    plt.ylabel('Analog 1 (V)')
    plt.plot(data['time_seconds'], data['Analog1'])
    plt.show()
    image_filename = 'result.png'
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    image_url = url_for('static', filename=f'images/{image_filename}')
    plt.savefig(image_path)
    
    plt.clf()
    
    plt.xlabel('Time (s)')
    plt.ylabel('Analog 2 (V)')
    plt.plot(data['time_seconds'], data['Analog2'])
    plt.show()
    image_filename_2 = 'result2.png'
    image_path_2 = os.path.join(app.config['UPLOAD_FOLDER'], image_filename_2)
    image_url_2 = url_for('static', filename=f'images/{image_filename_2}')
    plt.savefig(image_path_2)
    
    
    
    return render_template('result.html', image_path=image_url, image_path_2=image_url_2)