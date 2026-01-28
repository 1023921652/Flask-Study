from flask import Flask,request,redirect,render_template
app = Flask(__name__)
app.config.from_object('config')

class User:
    def __init__(self,name,age):
        self.name=name
        self.age=age

# 快捷路由装饰器
# 相当于@app.route('/',methods=['GET'])
@app.get('/')
def index():
    hobby = "游戏"
    person = {
        'name':'zhangsan'
    }
    user = User(name='华三', age=18)
    context = {
        'hobby':hobby,
        'person':person,
        'user':user
    }
    return render_template('control.html',**context)


@app.route('/profile',methods=['GET'])
def profile():
    name = request.args.get('name','')
    if not name:
        return redirect('/login')
    return f'name {name}'


if __name__ == '__main__':
    app.run(debug=True)

