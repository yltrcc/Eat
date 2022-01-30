from flask import session, render_template, Flask, request, redirect, url_for, current_app, Blueprint, flash, jsonify
import math
import json
from utils.DBUtils import UseDatabase
from datetime import datetime

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/getFood', methods=['GET'])
def getFood() -> 'json':
    page_num = request.args.get("page_num", type=str, default=1)
    page_num = int(page_num)
    page_size = request.args.get("page_size", type=str, default=5)
    page_size = int(page_size)
    canteen = request.args.get("canteen", type=str)
    _SQL = "SELECT food_id, food_name, food_cal, taste, location, recorde, add_time, img, info, canteen FROM tb_food "
    params = []
    if canteen:
        _SQL += "where canteen = %s "
        params.append(canteen)
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
    if canteen:
        _SQL += "where canteen = %s "
        params.append(canteen)
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute(_SQL, tuple(params))
        datas = cursor.fetchall()
    total_count = datas[0][0]
    # print('total_count=' + str(total_count))
    total_page = total_count / page_size
    total_page = math.floor(total_page)
    if total_count % page_size != 0:
        total_page += 1
        total_page = math.ceil(total_page)
    page = {'current_page': page_num, 'page_size': page_size, 'total_page': total_page, 'total_count': total_count,
            'content': objs}

    return jsonify({
        'success': True,
        'data': page,
    })

@bp.route('/getLike', methods=['GET'])
def getLike() -> 'json':
    page_num = request.args.get("page_num", type=str, default=1)
    page_num = int(page_num)
    page_size = request.args.get("page_size", type=str, default=5)
    page_size = int(page_size)
    user_id = request.args.get("user_id", type=str, default=5)
    _SQL = "SELECT food_id, food_name, food_cal, taste, location, recorde, add_time, img, info, canteen FROM tb_food where food_id in ( select DISTINCT food_id from tb_like where user_id = %s)"
    params = []
    params.append(user_id)
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
    _SQL = 'select count(food_id) as num from tb_food where food_id in ( select DISTINCT food_id from tb_like where user_id = %s)'
    params = []
    params.append(user_id)
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute(_SQL, tuple(params))
        datas = cursor.fetchall()
    total_count = datas[0][0]
    # print('total_count=' + str(total_count))
    total_page = total_count / page_size
    total_page = math.floor(total_page)
    if total_count % page_size != 0:
        total_page += 1
        total_page = math.ceil(total_page)
    page = {'current_page': page_num, 'page_size': page_size, 'total_page': total_page, 'total_count': total_count,
            'content': objs}

    return jsonify({
        'success': True,
        'data': page,
    })

@bp.route('/getCollect', methods=['GET'])
def getCollect() -> 'json':
    page_num = request.args.get("page_num", type=str, default=1)
    page_num = int(page_num)
    page_size = request.args.get("page_size", type=str, default=5)
    page_size = int(page_size)
    user_id = request.args.get("user_id", type=str, default=5)
    _SQL = "SELECT food_id, food_name, food_cal, taste, location, recorde, add_time, img, info, canteen FROM tb_food where food_id in ( select DISTINCT food_id from tb_collect where user_id = %s) "
    params = []
    params.append(user_id)
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
    _SQL = 'select count(food_id) as num from tb_food  where food_id in ( select DISTINCT food_id from tb_collect where user_id = %s) '
    params = []
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute(_SQL, tuple(params))
        datas = cursor.fetchall()
    total_count = datas[0][0]
    # print('total_count=' + str(total_count))
    total_page = total_count / page_size
    total_page = math.floor(total_page)
    if total_count % page_size != 0:
        total_page += 1
        total_page = math.ceil(total_page)
    page = {'current_page': page_num, 'page_size': page_size, 'total_page': total_page, 'total_count': total_count,
            'content': objs}

    return jsonify({
        'success': True,
        'data': page,
    })

@bp.route('/getComment', methods=['GET'])
def getComment() -> 'json':
    page_num = request.args.get("page_num", type=str, default=1)
    page_num = int(page_num)
    page_size = request.args.get("page_size", type=str, default=5)
    page_size = int(page_size)
    food_id = request.args.get("food_id", type=str)
    user_id = request.args.get("user_id", type=str)
    _SQL = "SELECT id, comment, user_id, food_id, user_name, avatar_url FROM tb_comment "
    params = []
    if food_id:
        _SQL += "where food_id = %s "
        params.append(food_id)
    if user_id:
        _SQL += "where user_id = %s "
        params.append(user_id)
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
    _SQL = 'select count(food_id) as num from tb_comment '
    params = []
    if food_id:
        _SQL += "where food_id = %s "
        params.append(food_id)
    if user_id:
        _SQL += "where user_id = %s "
        params.append(user_id)
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute(_SQL, tuple(params))
        datas = cursor.fetchall()
    total_count = datas[0][0]
    # print('total_count=' + str(total_count))
    total_page = total_count / page_size
    total_page = math.floor(total_page)
    if total_count % page_size != 0:
        total_page += 1
        total_page = math.ceil(total_page)
    page = {'current_page': page_num, 'page_size': page_size, 'total_page': total_page, 'total_count': total_count,
            'content': objs}

    return jsonify({
        'success': True,
        'data': page,
    })

@bp.route('/getUser', methods=['GET'])
def getUser() -> 'json':
    nickName = request.args.get("nickName", type=str, default=1)
    _SQL = "SELECT user_id, user_name FROM tb_user "
    params = []
    if nickName:
        _SQL += "where wx_nickname = %s "
        params.append(nickName)
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
    page = {'content': objs}

    return jsonify({
        'success': True,
        'data': page,
    })


@bp.route('/saveCollect', methods=['POST'])
def saveCollect() -> 'json':
    userId = request.args.get("userId", type=str)
    foodId = request.args.get("foodId", type=str)
    date = datetime.now()
    _SQL = """INSERT INTO `tb_collect` ( `user_id`, `food_id`, `create_time` ) VALUES( %s, %s, NOW() )"""
    params = []
    params.append(userId)
    params.append(foodId)
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute(_SQL, tuple(params))

    return jsonify({
        'success': True,
    })

@bp.route('/saveLike', methods=['POST'])
def saveLike() -> 'json':
    userId = request.args.get("userId", type=str)
    foodId = request.args.get("foodId", type=str)
    commentId = request.args.get("commentId", type=str)
    date = datetime.now()
    _SQL = """INSERT INTO `tb_like` ( `user_id`, `food_id`, `ltime`, `lcount`, `comment_id` ) VALUES( %s, %s, NOW(), 0, %s )"""
    params = []
    params.append(userId)
    params.append(foodId)
    params.append(commentId)
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute(_SQL, tuple(params))

    return jsonify({
        'success': True,
    })

@bp.route('/saveComment', methods=['POST'])
def saveComment() -> 'json':
    userId = request.args.get("userId", type=str)
    foodId = request.args.get("foodId", type=str)
    comment = request.args.get("comment", type=str)
    user_name = request.args.get("user_name", type=str)
    avatar_url = request.args.get("avatar_url", type=str)
    _SQL = """INSERT INTO `tb_comment` ( `comment`, `user_id`, `food_id`, `create_time`, `user_name`, `avatar_url` ) VALUES( %s, %s, %s, NOW(), %s, %s )"""
    params = []
    params.append(comment)
    params.append(userId)
    params.append(foodId)
    params.append(user_name)
    params.append(avatar_url)
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute(_SQL, tuple(params))

    return jsonify({
        'success': True,
    })