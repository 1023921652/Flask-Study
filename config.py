
#mysqldb 表示使用的驱动为mysqlclient
# root:root用户名和密码
# database_learn数据库
SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:root@127.0.0.1:3306/database_learn?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = False