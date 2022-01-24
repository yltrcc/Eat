from flask import session, render_template, Flask, request, redirect, url_for, current_app, Blueprint, flash
from DBcm import UseDatabase
from member import Member

bp = Blueprint('login', __name__)


@bp.route('/regist', methods=['GET'])
def to_regist() -> 'html':
    """到注册页面，如果已经注册过了直接到登录页面"""
    return render_template('regist.html')


@bp.route('/regist', methods=['POST'])
def do_regist() -> 'html':
    """
    注册操作
    :return: 这个方法返回json
    """
    username = request.form.get('user_name')
    login_name = request.form.get('login_name')
    password = request.form.get('pwd')
    password2 = request.form.get('pwd2')
    sex = request.form.get('sex')
    tel = request.form.get('tel')
    print("username=%s, login_name=%s, password=%s, password2=%s, sex=%s" % (username, login_name, password, password2,
                                                                             sex))
    if not all([username, password, password, password2, sex]):
        # flash('参数不完整')
        return render_template('regist.html', errormsg='参数不完整', username=username)
    elif password != password2:
        # flash('两次密码不一致，请重新输入')
        return render_template('regist.html', errormsg='两次密码不一致，请重新输入', username=username)
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = "select count(user_id) as num from tb_user where login_name = %s"
        cursor.execute(_SQL, (login_name, ))
        result = cursor.fetchall()
        print(result)
        count = result[0][0]
        print(count)
    if count >= 1:
        return render_template('regist.html', errormsg='用户名重复', username=username)
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = "insert into tb_user (user_name, login_name, pwd, sex, `identity`, `tel`, `state`, `add_time`) " \
               "values (%s, %s, %s, %s, %s, %s, %s, NOW())"
        cursor.execute(_SQL, (username, login_name, password, sex, '学生', tel, 0))
    return redirect(url_for('login.to_login'))


@bp.route('/login', methods=['GET'])
def to_login() -> 'html':
    """到登录页面，如果已经登录过了直接到食物列表页面"""
    if 'logged_in' in session:
        return redirect(url_for('food.to_list'))
    return render_template('login.html')


@bp.route('/login', methods=['POST'])
def do_login() -> 'html':
    """
    登录操作
    :return: 这个方法应该是返回json
    """
    username = request.form.get('user_name')
    password = request.form.get('pwd')
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = "select user_id, user_name, pwd, add_time from tb_user where login_name = %s and pwd = %s"
        cursor.execute(_SQL, (username, password))
        result = cursor.fetchall()
    if len(result) != 1:
        return render_template('login.html', errormsg='用户名或密码错误', username=username, password=password)
    member = Member(*result[0])
    session['logged_in'] = True
    session['login_type'] = 'member'
    session['member_id'] = member.id
    if username == 'zhangsan':
        return redirect(url_for('food.to_list'))
    else:
        return render_template('select_random.html')


@bp.route('/logout', methods=['GET'])
def do_logout() -> 'html':
    """退出登录操作"""
    if 'logged_in' in session:
        session.pop('logged_in')
    if 'login_type' in session:
        session.pop('login_type')
    if 'member_id' in session:
        session.pop('member_id')
    return redirect(url_for('login.do_login'))

