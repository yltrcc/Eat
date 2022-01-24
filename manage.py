# -*- coding: utf-8 -*-
from flask import Flask, render_template, session
import login_controller
import food_controller
import comment_controller

app = Flask(__name__)
app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'root',
                          'password': '12345678',
                          'auth_plugin': 'mysql_native_password',
                          "buffered": True,
                          'database': 'eat_system'}
app.secret_key = 'YouWillNeverGuessMySecretKey'

app.register_blueprint(login_controller.bp)
app.register_blueprint(food_controller.bp)
app.register_blueprint(comment_controller.bp)
app.add_url_rule('/', endpoint='to_list', view_func=food_controller.to_list)

"""
@app.route('/login', methods=['GET'])
def to_login():
    return render_template('login.html')


@app.route('/', methods=['GET'])
def to_login():
    return 'hello'
"""

if __name__ == '__main__':
    app.run(debug=True)
