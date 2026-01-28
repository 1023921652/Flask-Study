from flask import Flask,request
app = Flask(__name__)
app.config.from_object('config')
@app.route('/')
def hello_world():
    return 'Hello World!'

# url需要这样传
# http://127.0.0.1:8080/blog?blog_id=2
@app.route('/blog')
def blog():
    # type 转换为int类型
    blog_id = request.args.get('blog_id',1,type=int)
    return f'Blog {blog_id}'


if __name__ == '__main__':
    app.run(debug=True)

