from flask import Blueprint, render_template, request, jsonify, current_app
from utils.DBUtils import UseDatabase
import json
import math
from module.checker import check_logged_in

bp = Blueprint('comment', __name__, url_prefix='/comment')


@bp.route('/list', methods=['GET'])
def to_list() -> 'html':
    """
    评论列表页面
    :return:
    """
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
    return render_template('comment.html', **page_data)



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



