from datetime import datetime, timedelta
from employees_manager.database.models import Employee, PositionDuration, db

def get_expiring_contracts():
    next_month = datetime.now().replace(day=1) + timedelta(days=32)
    start_next_month = next_month.replace(day=1)
    end_next_month = (start_next_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    expiring_employees = []
    for employee in Employee.query.all():
        position_duration = PositionDuration.query.filter_by(position=employee.position).first()
        if position_duration:
            contract_end_date = employee.contract_start_date + timedelta(days=position_duration.duration_months * 30)
            if start_next_month <= contract_end_date <= end_next_month:
                expiring_employees.append(employee)
    return expiring_employees