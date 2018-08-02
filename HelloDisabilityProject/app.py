from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/a/<path>')
def goPath(path=None):
    if path:
       return render_template("%s.html" % path)
    else : return 'a'





if __name__ == '__main__':
    app.run()
