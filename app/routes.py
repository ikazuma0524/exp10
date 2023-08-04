from flask import render_template, request, redirect, url_for
from app.models import AnalysisResult
from app import app, db
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

@app.route('/upload', methods=['POST'])
def analyze_file():
    material = request.form['material']
    area = float(request.form['area'])
    file = request.files['file']

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # エクセルファイルの読み込み
        data = pd.read_excel(filepath, skiprows=13)
        data.columns = ['Time', 'Voltage_B', 'Voltage_C', 'Voltage_D']

        # 変換
        data['Load_N'] = data['Voltage_B'] * 200
        data['Strain_percentage'] = (data['Voltage_C'] / data['Voltage_C'].median()) * 1
        data['Stroke_mm'] = data['Voltage_D'] * 6

        # 真応力-真歪みの計算
        data['True_Strain'] = np.log(1 + data['Strain_percentage'] / 100)
        data['True_Stress'] = (data['Load_N'] / area) * (1 + data['Strain_percentage'] / 100)

        # グラフの描画
        plt.plot(data['True_Strain'], data['True_Stress'])
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result.png')
        plt.savefig(image_path)

        # データベースに保存
        result = AnalysisResult(material=material, area=area) # 他の情報も保存できます
        db.session.add(result)
        db.session.commit()

        return render_template('result.html', image_path=image_path)

    return redirect(url_for('upload_file'))
