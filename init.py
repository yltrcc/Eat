# -*- coding: utf-8 -*-
from flask import Flask
from route import food_controller, login_controller, comment_controller, user_controller

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
app.register_blueprint(user_controller.bp)
app.add_url_rule('/', endpoint='to_list', view_func=food_controller.to_list)

if __name__ == '__main__':
    app.run(debug=True)
