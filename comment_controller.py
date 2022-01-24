from flask import Blueprint, render_template, request, session, jsonify, current_app
from DBcm import UseDatabase
import json
from checker import check_logged_in
import os
import time

bp = Blueprint('comment', __name__, url_prefix='/comment')


@bp.route('/list', methods=['GET'])
def to_list() -> 'html':
    """
    评论列表页面
    :return:
    """
    return render_template('comment.html')


@bp.route("/add", methods=['POST'])
@check_logged_in
def do_add() -> 'html':
    """
    添加评论操作
    :return:
    """
    # 获取参数
    comment_id = request.form.get('cid')
    text = request.form.get('comment')
    user_id = request.form.get('u_id')
    """
    # TODO 保存数据
    _SQL = "INSERT INTO tb_comment (cid,comment,u_id,create_time) VALUES (%s, %s, %s, %s)"
    params = (cid, comment, u_id, create_time)
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute(_SQL, params)
        return redirect(url_for("comment"))
    # 获取当前系统时间
    create_time = time.strftime("%Y-%m-%d %H:%M:%S")
    user = User.query.filter(User.username == username).first()
    comment = Comment(text=text, create_time=create_time, cid=cid, u_id=u_id)
    db.session.add(comment)
    db.session.commit();
    """
    return jsonify({
        'success': True,
        'message': '评论成功！',
    })


@bp.route('/all_Comment', methods=['GET'])
@check_logged_in
def do_comment():
    """
    查询用户所有的评论
    :return:
    """
    # login_name = session.get('login_name')
    # user = User.query.filter(User.login_name == login_name).first()
    # order_by按照时间倒序
    # commentList = Comment.query.filter(Comment.user_id == user.id).order_by(Comment.create_time.desc()).all();
    # return render_template("myComment.html", commentList=commentList)
    return render_template("all_comment.html", commentList=[])


@bp.route('/delete', methods=['POST'])
def com_delete() -> 'json':
    """
    删除操作
    :return: 返回JSON
    """
    # 获取参数
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    cid = json_data.get('id')
    print('cid=', cid)
    r = {'success': 'true', 'errormsg': ''}
    _SQL = "DELETE FROM tb_comment WHERE cid = %s"
    params = (cid, )
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute(_SQL, params)
    return jsonify(r)



