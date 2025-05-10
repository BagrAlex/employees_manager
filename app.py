from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from employees_manager.config import Config
from employees_manager.database.models import db, SystemSettings

app = Flask(__name__)
app.config.from_object(Config)

# Инициализация расширений
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# Импорт и регистрация блюпринтов
from employees_manager.auth.routes import auth_bp
from employees_manager.admin.routes import admin_bp
#from father.employees.routes import employees_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
#app.register_blueprint(employees_bp, url_prefix='/employees')


@login_manager.user_loader
def load_user(user_id):
    from employees_manager.database.models import User
    return User.query.get(int(user_id))


# Инициализация приложения
def initialize_app():
    with app.app_context():
        db.create_all()

        # Инициализация системных настроек
        if not SystemSettings.query.filter_by(key='registration_enabled').first():
            settings = SystemSettings(key='registration_enabled', value='True')
            db.session.add(settings)
            db.session.commit()


initialize_app()

if __name__ == '__main__':
    app.run(debug=True)