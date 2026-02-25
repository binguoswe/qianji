from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/test')
def test():
    return jsonify({'message': 'working'})

@app.route('/chat', methods=['POST'])
def chat():
    return jsonify({'response': 'AI response'})

if __name__ == '__main__':
    app.run(port=8083)