from flask import session, render_template, Flask, request, redirect, url_for, current_app, Blueprint, flash
from utils.DBUtils import UseDatabase
from module.member import Member
from module.checker import check_logged_in

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/list', methods=['GET'])
@check_logged_in
def to_list() -> 'html':
    return render_template('user/user.html')