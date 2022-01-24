from flask import session, render_template, Flask, request, redirect, url_for, current_app, Blueprint, flash
from utils.DBUtils import UseDatabase
from module.member import Member

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/hello', methods=['GET'])
def to_regist() -> 'html':
    """到注册页面，如果已经注册过了直接到登录页面"""
    return render_template('base/regist.html')