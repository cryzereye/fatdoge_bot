from flask import Flask

#packages
app = Flask(__name__)

if __name__ == '__main__':
    app.run(host='localhost', port=5001)

@app.route("/")
def index():
    return "To be updated for FatDoge bot dashboard"