from src.models import TimeLog, Employee
from src.database import db
from datetime import datetime
from sqlalchemy.orm import aliased
from sqlalchemy import func, and_


class GetEmpDetailsByDate:

    def __init__(self):
        self.session = db.session()

    def emp_details_date(self, request):
        try:
            body = request.json
            date_str = body.get("date")
            specific_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Subquery to get the latest clock_in per employee for that date
            latest_clock_in_subq = (
                self.session.query(
                    TimeLog.employee_id,
                    func.max(TimeLog.clock_in).label("latest_clock_in")
                )
                .filter(TimeLog.date == specific_date)
                .group_by(TimeLog.employee_id)
                .subquery()
            )

            TL = aliased(TimeLog)

            # List of employee_ids to exclude
            excluded_ids = ["ELKHGFJJKEHLKJG4102836", "Nischal0001"]

            # Outer join with Employee, filter out excluded employees
            logs = (
                self.session.query(Employee, TL)
                .filter(~Employee.employee_id.in_(excluded_ids))  # Exclude specific employee IDs
                .outerjoin(
                    latest_clock_in_subq,
                    Employee.employee_id == latest_clock_in_subq.c.employee_id
                )
                .outerjoin(
                    TL,
                    and_(
                        Employee.employee_id == TL.employee_id,
                        TL.clock_in == latest_clock_in_subq.c.latest_clock_in,
                        TL.date == specific_date
                    )
                )
                .all()
            )

            # Format final response
            log_list = []
            for emp, tl in logs:
                log_entry = {
                    "employee_id": emp.employee_id,
                    "employee_name": emp.name,
                    "employee_avatar": emp.avatar,
                    "date": str(specific_date),
                    "clock_in": tl.clock_in.strftime('%H:%M') if tl and tl.clock_in else None,
                    "clock_out": tl.clock_out.strftime('%H:%M') if tl and tl.clock_out else None,
                    "total_hours": tl.total_hours.strftime('%H:%M:%S') if tl and tl.total_hours else None,
                    "status": "Present" if tl and tl.clock_in else "Absent"
                }
                log_list.append(log_entry)

            return {
                "status": True,
                "error": 0,
                "message": "Time logs fetched successfully for the given date.",
                "data": {
                    "logs": log_list
                }
            }

        except Exception as e:
            return {
                "status": False,
                "error": 1,
                "message": f"Failed to fetch time logs: {e}",
                "data": {}
            }
