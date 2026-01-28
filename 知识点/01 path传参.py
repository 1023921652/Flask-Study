from flask import Flask
app = Flask(__name__)
app.config.from_object('config')



@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/blog/<int:blog_id>')
def blog(blog_id):
    return 'Blog %d' % blog_id


if __name__ == '__main__':
    app.run(debug=True)

