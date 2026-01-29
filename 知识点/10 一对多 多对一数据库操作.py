from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import config
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import MetaData, Integer, String,ForeignKey
from typing import List
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
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey('department.id'), nullable=True)
    # 会自动查找外键department_id对应的Deparment表,将获取到的Deparment对象赋值给deparment
    # 就可以通过user.department.name就可以访问所属的部门
    # 注意此处是一对多的关系
    # back_populates表示反向引用,它的值和Department的users字段对应
    # 我们针对department_id创建了一个属性department（这个属性是ORM层面的属性，并不会在数据库中生成字段）。它引用的是Department类对象
    department: Mapped['Department'] = relationship(back_populates='users')

class Department(db.Model):
    __tablename__ = 'department'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    # 注意此处是多对一的关系,注意这是一个list
    # users中存储的是符合name字段的所有user对象,这是ORM框架内部的实现,新增这种字段不用进行数据表迁移和更新
    users: Mapped[List["User"]] = relationship(back_populates='department')


@app.route('/one2many')
def one2many():
    # 1 通过user添加deparment
    # department = Department(name='技术部')
    # user= User(username = "张三", department = department)
    # db.session.add(user)
    # db.session.commit()
    # 2 通过deparment添加user
    # department = db.session.scalar(db.select(Department).where(Department.id == 1))
    # user = User(username="李四")
    # department.users.append(user)
    # # 此处未使用,因为department已经通过session查出来了,已经在session中
    # db.session.commit()
    # 3 通过user访问deparment
    # user = db.session.scalar(db.select(User).where(User.username == '李四'))
    # print(user.department.name)
    # 4 通过deparment获取所有用户
    department = db.session.scalar(db.select(Department).where(Department.id == 1))
    users = department.users
    for user in users:
        print(user.username)
    return "数据添加成功"

if __name__ == '__main__':
    app.run()
