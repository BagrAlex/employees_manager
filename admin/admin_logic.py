from flask import current_app
from werkzeug.utils import secure_filename

from employees_manager.database.models import Employee, PositionDuration, db, EmployeeFieldValue, EmployeeField, SystemSettings
import os


def add_employee(form):
    """Добавление нового сотрудника."""
    photo_path = None
    if form.photo.data:
        photo_file = form.photo.data
        photo_filename = secure_filename(photo_file.filename)
        photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], photo_filename)
        photo_file.save(photo_path)

    new_employee = Employee(
        full_name=form.full_name.data,
        birth_date=form.birth_date.data,
        personal_number=form.personal_number.data,
        position=form.position.data,
        workplace=form.workplace.data,
        contract_start_date=form.contract_start_date.data,
        contacts=form.contacts.data,
        photo=photo_path
    )
    db.session.add(new_employee)
    db.session.commit()
    return new_employee


def update_employee(employee, form):
    """Обновление данных сотрудника."""
    employee.full_name = form.full_name.data
    employee.birth_date = form.birth_date.data
    employee.personal_number = form.personal_number.data
    employee.position = form.position.data
    employee.workplace = form.workplace.data
    employee.contract_start_date = form.contract_start_date.data
    employee.contacts = form.contacts.data

    if form.photo.data:
        photo_file = form.photo.data
        photo_filename = secure_filename(photo_file.filename)
        photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], photo_filename)
        photo_file.save(photo_path)
        employee.photo = photo_path

    db.session.commit()
    return employee


def delete_employee(employee_id):
    """Удаление сотрудника."""
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()


def get_all_employees():
    """Получение списка всех сотрудников."""
    return Employee.query.all()


def add_position_duration(form):
    """Добавление нового соответствия должность/время."""
    position = form.position.data
    duration_months = form.duration_months.data

    # Проверяем, существует ли уже такая должность
    existing_position = PositionDuration.query.filter_by(position=position).first()
    if existing_position:
        existing_position.duration_months = duration_months
    else:
        new_position = PositionDuration(position=position, duration_months=duration_months)
        db.session.add(new_position)

    db.session.commit()
    return True


def update_position_duration(position_id, form):
    """Обновление существующего соответствия должность/время."""
    position = PositionDuration.query.get_or_404(position_id)
    position.position = form.position.data
    position.duration_months = form.duration_months.data
    db.session.commit()
    return position


def delete_position_duration(position_id):
    """Удаление соответствия должность/время."""
    position = PositionDuration.query.get_or_404(position_id)
    db.session.delete(position)
    db.session.commit()


def get_all_position_durations():
    """Получение всех соотношений должность/длительность."""
    return PositionDuration.query.all()


def update_system_settings(form):
    """Обновление системных настроек."""
    registration_enabled = 'True' if form.registration_enabled.data else 'False'
    SystemSettings.set_setting('registration_enabled', registration_enabled)
    return True


def add_employee_field(name, field_type):
    """Добавление нового поля."""
    new_field = EmployeeField(name=name, field_type=field_type)
    db.session.add(new_field)
    db.session.commit()
    return new_field


def update_employee_field(field_id, name=None, field_type=None):
    """Обновление существующего поля."""
    field = EmployeeField.query.get_or_404(field_id)
    if name:
        field.name = name
    if field_type:
        field.field_type = field_type
    db.session.commit()
    return field


def delete_employee_field(field_id):
    """Удаление поля."""
    field = EmployeeField.query.get_or_404(field_id)
    db.session.delete(field)
    db.session.commit()


def get_all_employee_fields():
    """Получение всех полей."""
    return EmployeeField.query.all()


def set_employee_field_value(employee_id, field_id, value):
    """Установка значения поля для сотрудника."""
    field_value = EmployeeFieldValue.query.filter_by(employee_id=employee_id, field_id=field_id).first()
    if field_value:
        field_value.value = value
    else:
        field_value = EmployeeFieldValue(employee_id=employee_id, field_id=field_id, value=value)
        db.session.add(field_value)
    db.session.commit()
    return field_value
