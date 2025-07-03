from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta, date
from src.database import db
from src.models import TimeLog, Employee

class GetEmpDetailsByMonth:
    def __init__(self):
        self.session = db.session()

    def emp_details_month(self, request):
        try:
            if not request:
                return {
                    "status": False,
                    "message": "Request data is required",
                    "data": None
                }, 400

            body = request.json
            start_date_str = body.get("start_date")
            end_date_str = body.get("end_date")

            if not start_date_str or not end_date_str:
                return {
                    "status": False,
                    "message": "Both start_date and end_date are required",
                    "data": None
                }, 400

            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            except ValueError as e:
                return {
                    "status": False,
                    "message": f"Invalid date format: {str(e)}. Use YYYY-MM-DD",
                    "data": None
                }, 400

            if end_date < start_date:
                return {
                    "status": False,
                    "message": "end_date must be after start_date",
                    "data": None
                }, 400

            # Get today's date to determine future dates
            today = date.today()

            # Generate all dates in the range
            date_range = []
            current_date = start_date
            while current_date <= end_date:
                date_range.append(current_date)
                current_date += timedelta(days=1)

            employees = db.session.query(Employee).all()
            if not employees:
                return {
                    "status": False,
                    "message": "No employees found",
                    "data": None
                }, 404

            logs = db.session.query(TimeLog).filter(
                TimeLog.date.between(start_date, end_date)
            ).all()

            # Create a dictionary to organize logs by employee and date
            logs_dict = {}
            for log in logs:
                if log.employee_id not in logs_dict:
                    logs_dict[log.employee_id] = {}
                date_str = log.date.strftime("%Y-%m-%d")
                
                if log.clock_in:
                    hours = log.total_hours.strftime("%H:%M") if log.total_hours else "00:00"
                    logs_dict[log.employee_id][date_str] = f"Present ({hours})"
                else:
                    logs_dict[log.employee_id][date_str] = "Absent"

            # Prepare the response data
            employees_data = []
            for emp in employees:
                attendance = {}
                present_days = 0
                
                for date_obj in date_range:
                    date_str = date_obj.strftime("%Y-%m-%d")
                    # Skip weekends (Saturday=5, Sunday=6)
                    if date_obj.weekday() >= 5:
                        attendance[date_str] = "Weekend"
                        continue
                        
                    # For future dates (after today), mark as "-"
                    if date_obj > today:
                        attendance[date_str] = "-"
                        continue
                        
                    # Check if employee has log for this date
                    if emp.employee_id in logs_dict and date_str in logs_dict[emp.employee_id]:
                        status = logs_dict[emp.employee_id][date_str]
                        attendance[date_str] = status
                        if "Present" in status:
                            present_days += 1
                    else:
                        attendance[date_str] = "Absent"

                employees_data.append({
                    "employee_name": emp.name,
                    "employee_id": emp.employee_id,
                    "attendance": attendance,
                    "present_days": present_days
                })

            # Format date range for frontend
            formatted_date_range = [
                {
                    "date": date_obj.strftime("%Y-%m-%d"),
                    "day_name": date_obj.strftime("%a"),
                    "day_number": date_obj.strftime("%d"),
                    "month": date_obj.strftime("%b"),
                    "is_weekend": date_obj.weekday() >= 5,
                    "is_future": date_obj > today
                }
                for date_obj in date_range
            ]

            return {
                "status": True,
                "message": "Employee attendance data fetched successfully",
                "data": {
                    "date_range": formatted_date_range,
                    "employees": employees_data,
                    "start_date": start_date_str,
                    "end_date": end_date_str,
                    "today": today.strftime("%Y-%m-%d")
                }
            }, 200

        except Exception as e:
            db.session.rollback()
            return {
                "status": False,
                "message": f"Server error: {str(e)}",
                "data": None
            }, 500