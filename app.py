# import the Flask class from the flask module
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import Function
from testing import getdata
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

# create the application object
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
#getdata()
db.init_app(app)

# blueprint for auth routes in our app
from Page_Render import auth as auth_blueprint

app.register_blueprint(auth_blueprint)


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)








def create_app():
    app1 = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)


    return app1
