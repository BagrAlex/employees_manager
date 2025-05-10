from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def get_id(self):
        return str(self.id)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    personal_number = db.Column(db.String(50), unique=True, nullable=False)
    position = db.Column(db.String(100), nullable=False)
    workplace = db.Column(db.String(255), nullable=False)
    contract_start_date = db.Column(db.Date, nullable=False)
    contacts = db.Column(db.String(255))
    photo = db.Column(db.String(255))  # Путь к фото
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PositionDuration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(100), unique=True, nullable=False)
    duration_months = db.Column(db.Integer, nullable=False)
    
    
class SystemSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=False)

    @staticmethod
    def get_setting(key, default=None):
        setting = SystemSettings.query.filter_by(key=key).first()
        return setting.value if setting else default

    @staticmethod
    def set_setting(key, value):
        setting = SystemSettings.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = SystemSettings(key=key, value=value)
            db.session.add(setting)
        db.session.commit()


class EmployeeField(db.Model):
    """Модель для хранения дополнительных полей."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)  # Название поля
    field_type = db.Column(db.String(50), nullable=False)  # Тип поля (текст, число, дата и т.д.)

    def __repr__(self):
        return f"<EmployeeField {self.name} ({self.field_type})>"


class EmployeeFieldValue(db.Model):
    """Модель для хранения значений дополнительных полей для сотрудников."""
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey('employee_field.id'), nullable=False)
    value = db.Column(db.String(255))  # Значение поля

    # Связи
    employee = db.relationship('Employee', backref=db.backref('field_values', lazy=True))
    field = db.relationship('EmployeeField', backref=db.backref('values', lazy=True))

    def __repr__(self):
        return f"<EmployeeFieldValue {self.field.name}={self.value}>"