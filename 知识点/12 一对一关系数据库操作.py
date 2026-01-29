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

# 一对一主要用在存储其他的信息,不想把一些额外的数据存储在User表中
# 防止User表字段过多
# 假设现在我们要存储用户的一些额外信息，比如生日，毕业院校，但是这些数据又不是常用的，这时候就可以创建一个UserExtension表，用来存储用户的一些不常用的冗余信息，那么User和UserExtension之间就是一对一的关系，也就是一个User只能有一个Extension，一个UserExtension只能被一个User所使用。User和UserExtension之间的一对一关系模型
# 一对一关系在数据库层面是不存在的,只能在ORM中做约束

# ● User模型中的user_extension约束的类型为UserExtension，所以SQLAlchemy在处理类似user.user_extension时，会返回一个UserExtension对象，而不是一个UserExtension的列表，这样就确保了一对一的关系。另外在定义user_extension的relationship时，还显示的传入了一个uselist=False参数，更进一步约束了user_extension是一个对象，而不是一个列表。
# ● 在UserExtension模型中，设置了user_id字段的unique=True，也就是user_id在UserExtension中只能是唯一，也保证了一对一的关系。
class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=True)
    # uselist表示user_extension不是一个list,这样就实现了一对一的关系
    user_extension: Mapped["UserExtension"] = relationship(
        "UserExtension",
        back_populates="user",
        uselist=False)
class UserExtension(db.Model):
    __tablename__ = "user_extension"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    university: Mapped[str] = mapped_column(String(50), nullable=False)
    # 表示user_id必须是唯一的,反向实现了一对一的关系
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), unique=True)
    user: Mapped["User"] = relationship("User", back_populates="user_extension")

@app.route("/one2one")
def one2one():
    user = db.session.scalar(db.select(User).where(User.id==1))
    user.user_extension = UserExtension(university='北京大学')
    db.session.commit()

    return "success"
if __name__ == '__main__':
    app.run()
