from flask import Flask 

app = Flask(__name__)

@app.route('/getdata', methods=['GET'])
def get_data():
    return  "Hello, this is your data!"

if __name__ == '__main__':
    app.run(debug=True)