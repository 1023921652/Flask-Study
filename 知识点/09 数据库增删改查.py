from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import config
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData, Integer, String
from flask_migrate import Migrate
# 上述代码中，字典naming_convention是一个固定的写法，主要是用来给表约束做一些命名约定的，使得后期alembic在生成迁移脚本时，生成的约束名不是随机的，而是有命名规范的。
# 在User模型中，我们使用Mapped[类型名]语法来让开发者和IDE识别该属性的类型，为开发提供便捷性；另外，凡是使用了mapped_column创建的属性都将被映射到表中成为字段，并且该字段有什么配置，都可以在mapped_column中添加相关参数，比如字段类型（db.Integer）、是否可以为空（nullable）、是否为主键（primary_key=True）、是否自增（autoincrement=True）等。
# 之后，我们调用db.create_all()方法，就会将该模型迁移到数据库中生成一张表，这种方式在字段发生改变时无法自动同步到数据库中，所以仅作为一种临时解决方案，后续会使用flask-migrate来实现迁移。
app = Flask(__name__)
app.config.from_object(config)

# 定义命名约定的Base类
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        # ix: index，索引。
        "ix": 'ix_%(column_0_label)s',
        # un：unique，唯一约束
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        # ck：Check，检查约束
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        # fk：Foreign Key，外键约束
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        # pk：Primary Key，主键约束
        "pk": "pk_%(table_name)s"
    })

db = SQLAlchemy(app=app, model_class=Base)
# 用于数据迁移,
# 在创建完迁移对象后,我们需要初始化迁移环境
# 在项目根目录执行flask db init
# 在初始化完迁移环境的前提下，无论是新增了ORM模型，或者是ORM模型中有任何字段信息发生改变，并且想要将这些改变同步到数据库中，那么要做的一件事情就是将当前的修改，生成一个迁移脚本，生成迁移脚本命令如下
# flask db migrate -m "备注信息"
# 执行数据迁移
# flask db upgrade
migrate = Migrate(app, db)
# 每个类对应数据库中的一张表,类属性是表中的字段,类的实例是表中的一条记录
class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=True)
    password: Mapped[str] = mapped_column(String(200), nullable=True)
    email: Mapped[str] = mapped_column(String(200), nullable=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'
# 添加数据
@app.route('/create')
def create():
    # 添加一条记录
    # user = User(username="lili", password="asledfgo")
    # db.session.add(user)
    # 添加多条数据
    user1 = User(username="小王", password="asledfgo")
    user2 = User(username="小张", password="asledfgo")
    db.session.add_all([user1, user2])
    db.session.commit()
    return '数据添加成功'

# 读取数据
@app.route('/read')
def read():
    # 查找多条数据,可以使用db.session.scalars
    # 方式一
    # users = db.session.execute(db.select(User)).scalars().all()
    # 方式二
    # users = db.session.scalars(db.select(User)).all()

    # 查找一条数据,可以使用db.session.scalar
    # 数据筛选 filter_by只能进行相等筛查
    # user = db.session.scalar(db.select(User).filter_by(id=1))
    # where可以进行不等筛查
    # user = db.session.execute(db.select(User).where(User.id == 1)).scalar()
    # user = db.session.scalar(db.select(User).where(User.id == 1))

    # 排序,默认是从小到大排序,如果想从大到小排序,使用User.username.desc()
    users = db.session.scalars(db.select(User).order_by(User.id.desc()))
    print(users)
    return '数据读取成功'

@app.route('/update')
def update():
    # 两次sql操作
    # user = db.session.scalar(db.select(User).where(User.id == 1))
    # user.username = "历史"
    # db.session.commit()
    # 一次sql操作
    db.session.execute(db.update(User).where(User.id == 1).values(username="王五"))
    db.session.commit()
    # print(users)
    return "更新成功"


@app.route('/delete')
def delete():
    # 两次sql操作
    # user = db.session.scalar(db.select(User).where(User.id == 1))
    # db.session.delete(user)
    # db.session.commit()
    # 一次sql操作
    db.session.execute(db.delete(User).where(User.id == 2))
    db.session.commit()
    return "删除成功"
if __name__ == '__main__':
    app.run()
