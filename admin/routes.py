from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from employees_manager.database.models import Employee, EmployeeField, SystemSettings, PositionDuration
from .forms import EmployeeForm, PositionDurationForm, SystemSettingsForm, EmployeeFieldValueForm, EmployeeFieldForm
from .admin_logic import (
    add_employee, update_employee, delete_employee, get_all_employees,
    add_position_duration, update_position_duration, delete_position_duration, get_all_position_durations,
    update_system_settings,
    add_employee_field, update_employee_field, delete_employee_field,
    get_all_employee_fields, set_employee_field_value
)

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    employees = get_all_employees()
    return render_template('admin/dashboard.html', employees=employees)


@admin_bp.route('/employee/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        add_employee(form)
        flash('Employee added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/employee_form.html', form=form, action='Add')


@admin_bp.route('/employee/edit/<int:employee_id>', methods=['GET', 'POST'])
@login_required
def edit_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    form = EmployeeForm(obj=employee)
    if form.validate_on_submit():
        update_employee(employee, form)
        flash('Employee updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/employee_form.html', form=form, action='Edit')


@admin_bp.route('/employee/delete/<int:employee_id>')
@login_required
def delete_employee_route(employee_id):
    delete_employee(employee_id)
    flash('Employee deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/fields', methods=['GET', 'POST'])
@login_required
def manage_fields():
    form = EmployeeFieldForm()
    if form.validate_on_submit():
        add_employee_field(form.name.data, form.field_type.data)
        flash('Field added successfully!', 'success')
        return redirect(url_for('admin.manage_fields'))
    fields = get_all_employee_fields()
    return render_template('admin/manage_fields.html', form=form, fields=fields)


@admin_bp.route('/fields/edit/<int:field_id>', methods=['GET', 'POST'])
@login_required
def edit_field(field_id):
    field = EmployeeField.query.get_or_404(field_id)
    form = EmployeeFieldForm(obj=field)
    if form.validate_on_submit():
        update_employee_field(field_id, name=form.name.data, field_type=form.field_type.data)
        flash('Field updated successfully!', 'success')
        return redirect(url_for('admin.manage_fields'))
    return render_template('admin/edit_field.html', form=form, field=field)


@admin_bp.route('/fields/delete/<int:field_id>')
@login_required
def delete_field(field_id):
    delete_employee_field(field_id)
    flash('Field deleted successfully!', 'success')
    return redirect(url_for('admin.manage_fields'))


@admin_bp.route('/employee/<int:employee_id>/set-field/<int:field_id>', methods=['GET', 'POST'])
@login_required
def set_field_value(employee_id, field_id):
    form = EmployeeFieldValueForm()
    if form.validate_on_submit():
        set_employee_field_value(employee_id, field_id, form.value.data)
        flash('Field value updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/set_field_value.html', form=form)


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = PositionDurationForm()
    if form.validate_on_submit():
        add_position_duration(form)
        flash('Position added successfully!', 'success')
        return redirect(url_for('admin.settings'))

    positions = get_all_position_durations()
    return render_template('admin/settings.html', form=form, positions=positions)


@admin_bp.route('/settings/edit/<int:position_id>', methods=['GET', 'POST'])
@login_required
def edit_position(position_id):
    """Редактирование существующего соответствия должность/время."""
    position = PositionDuration.query.get_or_404(position_id)
    form = PositionDurationForm(obj=position)
    if form.validate_on_submit():
        update_position_duration(position_id, form)
        flash('Position updated successfully!', 'success')
        return redirect(url_for('admin.settings'))
    return render_template('admin/edit_position.html', form=form, position=position)


@admin_bp.route('/settings/delete/<int:position_id>')
@login_required
def delete_position(position_id):
    """Удаление соответствия должность/время."""
    delete_position_duration(position_id)
    flash('Position deleted successfully!', 'success')
    return redirect(url_for('admin.settings'))

@admin_bp.route('/system-settings', methods=['GET', 'POST'])
@login_required
def system_settings():
    form = SystemSettingsForm()
    current_settings = {
        'registration_enabled': SystemSettings.get_setting('registration_enabled', 'True') == 'True'
    }
    form.registration_enabled.data = current_settings['registration_enabled']

    if form.validate_on_submit():
        update_system_settings(form)
        flash('System settings updated successfully!', 'success')
        return redirect(url_for('admin.system_settings'))

    return render_template('admin/system_settings.html', form=form)
