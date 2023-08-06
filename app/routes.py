from flask import render_template, request, redirect, url_for
from app import app
import pandas as pd
import math
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
    length = float(request.form['length'])
    load0 = float(request.form['load0'])
    distortion0= float(request.form['distortion0'])
    distortiongaugecollection1 = float(request.form['distortiongaugecollection1'])
    distortiongaugecollection2 = distortion0+distortiongaugecollection1
    distortiongaugecollection3 = 1/distortiongaugecollection2
    file = request.files['file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    data_raw = pd.read_excel(filepath, header=13)
    data = data_raw.iloc[:, :4]
    data.columns = ['time','Analog1','Analog2','Analog3']
    data['Stroke_mm'] = data['Analog3']*6
    data['time_seconds'] =[i * 0.05 for i in range(len(data))]
    data['Analog1_2']=data['Analog1']+load0
    data['Analog2_2']=data['Analog2']+distortion0
    data['Load_N'] = data['Analog1_2']*2000
    data['Nominal_Stress_(MPa)'] = data['Load_N']/area
    data['Nominal_Strain(gage)_(%)'] = data['Analog2_2']*distortiongaugecollection3
    data['Nominal_Strain(Stroke)_(%)']= (data['Stroke_mm']*100)/length
    data['True_Stress(gage)_(MPa)'] = data['Nominal_Stress_(MPa)']*(1+data['Nominal_Strain(gage)_(%)']/100)
    data['True_Strain(gage)_(%)'] = data["Nominal_Strain(gage)_(%)"].apply(lambda x: math.log(1 + x/100))
    data['True_Stress(Stroke)_(MPa)'] =data['Nominal_Stress_(MPa)']*(1+(data['Nominal_Strain(Stroke)_(%)']/100))
    data['True_Strain(Stroke)_(%)'] = data["Nominal_Strain(Stroke)_(%)"].apply(lambda x: math.log(1 + x/100))
    def safe_log(x):
        if x > 0:
            return math.log(x)
        else:
            return None


    def safe_log_2(x):
        if x > 0:
            return math.log(x/100)
        else:
            return None

    data['log_True_Stress(gage)'] = data['True_Stress(gage)_(MPa)'].apply(safe_log)
    data['log_True_Strain(gage)'] = data['True_Strain(gage)_(%)'].apply(safe_log_2)
    data['log_True_Stress(Stroke)'] = data['True_Stress(Stroke)_(MPa)'].apply(safe_log)
    data['log_True_Strain(Stroke)'] = data['True_Strain(Stroke)_(%)'].apply(safe_log_2)
    
    
    
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
    
    plt.clf()
    
    plt.xlabel('Nominal Strain (gage) (%)')
    plt.ylabel('Nominal Stress_(MPa)')
    plt.plot(data['Nominal_Strain(gage)_(%)'], data['Nominal_Stress_(MPa)'])
    image_filename_3 = 'fig3.png'
    image_path_3 = os.path.join(app.config['UPLOAD_FOLDER'], image_filename_3)
    image_url_3 = url_for('static', filename=f'images/{image_filename_3}')
    plt.savefig(image_path_3)
    
    plt.clf()
    
    plt.xlabel('Nominal Strain (Stroke) (%)')
    plt.ylabel('Nominal Stress (MPa)')
    plt.plot(data['Nominal_Strain(Stroke)_(%)'], data['Nominal_Stress_(MPa)'])
    image_filename_4 = 'fig4.png'
    image_path_4 = os.path.join(app.config['UPLOAD_FOLDER'], image_filename_4)
    image_url_4 = url_for('static', filename=f'images/{image_filename_4}')
    plt.savefig(image_path_4)
    
    plt.clf()
    
    plt.xlabel('True Strain (gage) (%)')
    plt.ylabel('True Stress (gage) (MPa)')
    plt.plot(data['True_Strain(gage)_(%)'], data['True_Stress(gage)_(MPa)'])
    image_filename_5 = 'fig5.png'
    image_path_5 = os.path.join(app.config['UPLOAD_FOLDER'], image_filename_5)
    image_url_5 = url_for('static', filename=f'images/{image_filename_5}')
    plt.savefig(image_path_5)
    
    plt.clf()
    
    plt.xlabel('True Strain (Stroke) (%)')
    plt.ylabel('True Stress (Stroke) (MPa)')
    plt.plot(data['True_Strain(Stroke)_(%)'], data['True_Stress(Stroke)_(MPa)'])
    image_filename_6 = 'fig6.png'
    image_path_6 = os.path.join(app.config['UPLOAD_FOLDER'], image_filename_6)
    image_url_6 = url_for('static', filename=f'images/{image_filename_6}')
    plt.savefig(image_path_6)
    
    plt.clf()
    
    plt.xlabel('log_True_Strain (gage) (%)')
    plt.ylabel('log_True_Stress (gage) (MPa)')
    plt.plot(data['log_True_Strain(gage)'], data['log_True_Stress(gage)'])
    image_filename_7 = 'fig7.png'
    image_path_7 = os.path.join(app.config['UPLOAD_FOLDER'], image_filename_7)
    image_url_7 = url_for('static', filename=f'images/{image_filename_7}')
    plt.savefig(image_path_7)
    
    plt.clf()
    
    plt.xlabel('log_True_Strain (Stroke) (%)')
    plt.ylabel('log_True_Stress (Stroke) (MPa)')
    plt.plot(data['log_True_Strain(Stroke)'], data['log_True_Stress(Stroke)'])
    image_filename_8 = 'fig8.png'
    image_path_8 = os.path.join(app.config['UPLOAD_FOLDER'], image_filename_8)
    image_url_8 = url_for('static', filename=f'images/{image_filename_8}')
    plt.savefig(image_path_8)
    return render_template( 'result.html',image_path=image_url, image_path_2=image_url_2, image_path_3=image_url_3, image_path_4=image_url_4, image_path_5=image_url_5, image_path_6=image_url_6, image_path_7=image_url_7, image_path_8=image_url_8)
    
    
    
    
  