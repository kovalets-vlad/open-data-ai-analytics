import os
import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    quality_report = {}
    quality_path = '/app/reports/quality_report.json'
    if os.path.exists(quality_path):
        with open(quality_path, 'r', encoding='utf-8') as f:
            quality_report = json.load(f)

    research_report = {}
    research_path = '/app/reports/research_report.json'
    if os.path.exists(research_path):
        with open(research_path, 'r', encoding='utf-8') as f:
            research_report = json.load(f)

    plots = []
    plots_dir = '/app/static/plots'
    if os.path.exists(plots_dir):
        plots = [f for f in os.listdir(plots_dir) if f.endswith('.png')]

    return render_template('index.html', quality=quality_report, research=research_report, plots=plots)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)