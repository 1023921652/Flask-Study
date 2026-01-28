from flask import Flask,request,redirect,render_template
app = Flask(__name__)
app.config.from_object('config')


# 快捷路由装饰器
# 相当于@app.route('/',methods=['GET'])
@app.get('/')
def index():
    return render_template('extend.html')



if __name__ == '__main__':
    app.run(debug=True)

