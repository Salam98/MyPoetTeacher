from flask import Flask
from views import bp  # استيراد الـBlueprint
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app,)
app.config['CORS_HEADERS'] = 'application/json'

# تسجيل الـBlueprint في التطبيق
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)
