from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    # You can even add HTML code
    return "<h1>Hello world</h1>"

if __name__ == "__main__":
    app.run()
