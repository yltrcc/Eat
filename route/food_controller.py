from flask import session, render_template, Flask, request, app, redirect, url_for, current_app, Blueprint, jsonify
import json
import math
from utils.DBUtils import UseDatabase
from module.checker import check_logged_in

bp = Blueprint('food', __name__, url_prefix='/food')


@bp.route('/list', methods=['GET'])
@check_logged_in
def to_list() -> 'html':
    """
    跳转到列表页面
    :return:
    """
    # print('to_list ...')
    keywords = request.args.get('keywords', '')
    keywords = keywords.rstrip().lstrip()
    page_num = request.args.get("page_num", type=str, default=1)
    page_num = int(page_num)
    page_size = request.args.get("page_size", type=str, default=5)
    page_size = int(page_size)
    _SQL = "SELECT food_id, food_name, food_cal, taste, location, recorde, add_time FROM tb_food "
    params = []
    if len(keywords) > 0:
        _SQL += " WHERE food_name LIKE %s OR food_id = %s"
        params.append("%%%s%%" % keywords)
        params.append(keywords)
    _SQL += """LIMIT %s, %s """
    params.append((page_num - 1) * page_size)
    params.append(page_size)
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute(_SQL, tuple(params))
        rows = cursor.fetchall()
        column_name_list = [i[0] for i in cursor.description]
    objs = []
    for r in rows:
        obj = {}
        for i, item in enumerate(r):
            obj[column_name_list[i]] = item
        objs.append(obj)
    # print(objs)
    # 查询总记录数
    params = []
    _SQL = 'select count(food_id) as num from tb_food '
    params = []
    if len(keywords) > 0:
        _SQL += " WHERE food_name LIKE %s OR food_id = %s"
        params.append("%%%s%%" % keywords)
        params.append(keywords)
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute(_SQL, tuple(params))
        datas = cursor.fetchall()
    # print('datas=' + str(datas))
    total_count = datas[0][0]
    # print('total_count=' + str(total_count))
    total_page = total_count / page_size
    total_page = math.floor(total_page)
    if total_count % page_size != 0:
        total_page += 1
        total_page = math.ceil(total_page)
    page = {'current_page': page_num, 'page_size': page_size, 'total_page': total_page, 'total_count': total_count,
            'content': objs}
    page_data = {
        "keywords": keywords,
        "page": page
    }
    # print(page_data)
    return render_template('food/food.html', **page_data)


@bp.route('/add', methods=['GET'])
def to_add() -> 'html':
    """
    跳转到新增页面
    :return:
    """
    return render_template('food/food_add.html')


@bp.route('/add', methods=['POST'])
@check_logged_in
def do_add() -> 'html':
    """
    新增操作
    :return:
    """
    # 获取参数
    food_name = request.form.get('food_name')
    food_cal = request.form.get('food_cal')
    taste = request.form.get('taste')
    location = request.form.get('location')

    # TODO 保存数据
    _SQL = """INSERT INTO tb_food
         (food_name, food_cal, taste, location, recorde, add_time)
         values
         (%s, %s, %s, %s, 0, NOW())
         """
    params = (food_name, food_cal, taste, location)
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute(_SQL, params)
    return redirect(url_for("food.to_list"))


@bp.route('/update', methods=['GET'])
def to_update() -> 'html':
    """
    跳转到修改页面
    :return:
    """
    # 获取参数
    food_id = request.args.get('id', '')
    # print('food_id=', food_id)
    # 通过ID去数据库里查询出详细信息，把数据传给页面-仿to_list方法
    _SQL = """SELECT food_id, food_name, food_cal, taste, location, recorde, add_time
               FROM tb_food
               WHERE food_id = %s
               """
    params = (food_id, )
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute(_SQL, params)
        rows = cursor.fetchall()
        column_name_list = [i[0] for i in cursor.description]
    objs = []
    for r in rows:
        obj = {}
        for i, item in enumerate(r):
            obj[column_name_list[i]] = item
        objs.append(obj)
    food = objs[0]
    # print(food)
    return render_template('food/food_update.html', food=food)


@bp.route('/update', methods=['POST'])
def do_update() -> 'json':
    """
    修改操作-仿删除操作接收JSON格式的参数
    :return: 返回JSON-仿删除操作
    """
    # 获取参数
    """
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    food_id = json_data.get('food_id')
    food_name = json_data.get('food_name')
    food_cal = json_data.get('food_cal')
    taste = json_data.get('taste')
    location = json_data.get('location')
    """
    food_id = request.form.get('food_id')
    food_name = request.form.get('food_name')
    food_cal = request.form.get('food_cal')
    taste = request.form.get('taste')
    location = request.form.get('location')

    _SQL = """UPDATE tb_food SET food_name = %s, food_cal = %s, taste = %s, location = %s
               WHERE food_id = %s
               """
    params = (food_name, food_cal, taste, location, food_id)
    print(params)
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute(_SQL, params)
    return redirect(url_for("food.to_list"))


@bp.route('/delete', methods=['POST'])
def do_delete() -> 'json':
    """
    删除操作
    :return: 返回JSON
    """
    # 获取参数
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    food_id = json_data.get('id')
    print('food_id=', food_id)
    r = {'success': 'true', 'errormsg': ''}
    _SQL = "DELETE FROM tb_food WHERE food_id = %s"
    params = (food_id, )
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute(_SQL, params)
    return jsonify(r)


@bp.route('/detail', methods=['GET'])
def to_detail() -> 'html':
    """
    跳转到详情页面
    :return:
    """
    food_id = request.args.get('id', '')
    _SQL = """SELECT food_id, food_name, food_cal, taste, location, recorde, add_time
                   FROM tb_food
                   WHERE food_id = %s
                   """
    params = (food_id, )
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute(_SQL, params)
        rows = cursor.fetchall()
        column_name_list = [i[0] for i in cursor.description]
    objs = []
    for r in rows:
        obj = {}
        for i, item in enumerate(r):
            obj[column_name_list[i]] = item
        objs.append(obj)
    food = objs[0]
    return render_template('food/food_detail.html', food=food)


@bp.route('/select', methods=['GET'])
def to_select() -> 'html':
    """
    跳转到详情页面
    :return:
    """
    render_template('select_random.html')

