from app import db

class AnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String(50))
    area = db.Column(db.Float)
    # 他の必要なフィールドもここに追加
