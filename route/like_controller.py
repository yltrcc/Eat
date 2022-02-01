from flask import session, render_template, Flask, request, app, redirect, url_for, current_app, Blueprint, jsonify
import json
import math
from utils.DBUtils import UseDatabase
from module.checker import check_logged_in

bp = Blueprint('like', __name__, url_prefix='/like')


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
    return render_template('like/like.html', **page_data)



