from flask import session, render_template, Flask, request, redirect, url_for, current_app, Blueprint, flash, jsonify
import math
import json
from utils.DBUtils import UseDatabase
from module.checker import check_logged_in

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/hello', methods=['GET'])
def to_regist() -> 'json':
    """到注册页面，如果已经注册过了直接到登录页面"""
    return render_template('base/regist.html')


@bp.route('/getFood', methods=['GET'])
def do_delete() -> 'json':
    """
    删除操作
    :return: 返回JSON
    """
    # 获取参数
    data = request.get_data()
    # json_data = json.loads(data.decode("utf-8"))
    # food_id = json_data.get('id')
    # _SQL = "SELECT *  FROM tb_food WHERE food_id = %s"
    # params = (food_id, )
    # with UseDatabase(current_app.config['dbconfig']) as cursor:
    #     cursor.execute(_SQL, params)
    return jsonify({
        'success': True,
        'message': '评论成功！',
        # 'data':
    })
