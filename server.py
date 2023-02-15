import pymysql
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 连接数据库
conn = pymysql.connect(
    host='localhost',  # 数据库主机名
    user='root',  # 数据库用户名
    password='dingbin123',  # 数据库密码
    db='fixed_assets',  # 数据库名称
    charset='utf8mb4'  # 数据库编码
)

# 获取游标
cursor = conn.cursor()

# 登录页面
@app.route('/')
def login():
    return render_template('login.html')

# 处理登录请求
@app.route('/login', methods=['POST'])
def do_login():
    # 获取用户名和密码
    username = request.form['username']
    password = request.form['password']

    # 查询用户表是否存在该用户
    sql = 'SELECT * FROM users WHERE username=%s AND password=%s'
    cursor.execute(sql, (username, password))
    user = cursor.fetchone()

    if user:
        # 登录成功，保存用户名到session中
        session['username'] = username
        return redirect(url_for('index'))
    else:
        # 登录失败，返回错误信息
        return render_template('login.html', error='用户名或密码错误')

# 资产管理主页面
@app.route('/index')
def index():
    return render_template('index.html')

# 固定资产页面
@app.route('/assets')
def assets():
    # 查询所有固定资产
    sql = 'SELECT * FROM assets'
    cursor.execute(sql)
    assets = cursor.fetchall()

    return render_template('assets.html', assets=assets)

# 盘点页面
@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

# 关闭数据库连接
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()
