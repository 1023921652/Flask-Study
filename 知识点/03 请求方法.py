from flask import Flask,request,redirect
app = Flask(__name__)
app.config.from_object('config')

# 快捷路由装饰器
# 相当于@app.route('/',methods=['GET'])
@app.get('/login')
def login():
    return 'login page!'


@app.route('/profile',methods=['GET'])
def profile():
    name = request.args.get('name','')
    if not name:
        return redirect('/login')
    return f'name {name}'


if __name__ == '__main__':
    app.run(debug=True)

