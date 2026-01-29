from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import config
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import MetaData, Integer, String, ForeignKey, Table, Column
from flask_migrate import Migrate
from typing import List

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
migrate = Migrate(app, db)
# 多对多的关系需要通过中间表实现
# 此处是直接定义表,没有通过ORM模型实现
department_permission_table = Table(
    # 表在数据库中的名字
    "department_permission",
    # 表的元数据,就是上方Base对象的metadata
    db.metadata,
    # 字段名
    # 这两个字段合起来作为一个主键,称为复合主键
    # 这意味着：唯一性约束不再是针对单独的 department_id，而是针对 (department_id, permission_id) 这个组合。
    # 合起来作为一个主键,示例 : 技术部能够访问主页在此表中   只会存在一条数据   不应该存在两条数据
    Column("department_id", Integer, ForeignKey("department.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permission.id"), primary_key=True)
)
class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=True)

    department_id: Mapped[int] = mapped_column(Integer, ForeignKey("department.id"), nullable=True)
    department: Mapped["Department"] = relationship("Department", back_populates="users")


class Department(db.Model):
    __tablename__ = "department"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    users: Mapped[List[User]] = relationship("User", back_populates="department")

    permissions: Mapped[List["Permission"]] = relationship(
        # 表示引用的模型名
        "Permission",
        # 中间表
        secondary=department_permission_table,
        # 声明别的表反向使用Deparment的时候需要使用deparments属性
        back_populates="departments"
    )


class Permission(db.Model):
    __tablename__ = "permission"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    departments: Mapped[List[Department]] = relationship(
        "Department",
        secondary=department_permission_table,
        back_populates="permissions"
    )



@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/many2many')
def many2many():
    # 1. 通过department来添加permission
    # department = db.session.scalar(db.select(Department).where(Department.id==1))
    # permissions = [
    #     Permission(name="访问首页"),
    #     Permission(name='访问用户')
    # ]
    # # 可以将department.permissions当做一个列表
    # department.permissions.extend(permissions)
    # db.session.commit()
    # 2 通过permission来添加deparment
    # permission = Permission(name="登录页")
    # deparment1 = Department(name="综管部")
    # deparment2 = Department(name="财务部")
    # permission.departments.extend([deparment1, deparment2])
    # db.session.add(permission)
    # db.session.commit()
    # 3 通过permision来获取deparments
    permissin = db.session.scalar(db.select(Permission).where(Permission.name=="登录页"))
    deparments = permissin.departments
    for department in deparments:
        print(department.name)
    db.session.commit()
    # 4. 移除
    # department = db.session.scalar(db.select(Department).where(Department.id == 1))
    # permission = db.session.scalar(db.select(Permission).where(Permission.id == 1))
    # department.permissions.remove(permission)
    # db.session.commit()

    return "多对多操作成功！"

# @app.route("/one2one")
# def one2one():
#     user: User = db.session.scalar(db.select(User).where(User.id == 1))
#     user.user_extension = UserExtension(university="北京大学")
#     db.session.commit()
#     return "一对一操作完成！"

if __name__ == '__main__':
    app.run()
