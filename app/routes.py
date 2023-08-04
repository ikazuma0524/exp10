from flask import render_template, request, redirect, url_for
from app import app
import pandas as pd
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

    # ファイル解析と画像生成のコード（前述のコードと同じ）

    return render_template('result.html', image_path=image_path)
