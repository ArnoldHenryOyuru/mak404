from flask import Flask, abort, request

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    abort(404)

if __name__ == '__main__':
    app.run()
