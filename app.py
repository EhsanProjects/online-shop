from flask import Flask



from blueprints.general import app as general
from blueprints.admin import app as admin
from blueprints.user import app as user
import config
import extensions


app = Flask(__name__)
app.register_blueprint(general)
app.register_blueprint(admin)
app.register_blueprint(user)
# db=SQLAlchemy(app)


app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
extensions.db.init_app(app)

with app.app_context():
    extensions.db.create_all()


if __name__ == '__main__':
    app.run()
