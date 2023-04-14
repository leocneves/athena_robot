from flask import Flask, render_template
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
PEOPLE_FOLDER = os.path.join('static')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/')
def index():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'eyes.gif')
    return render_template('index2.html', user_image = full_filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
