from datetime import datetime

def validate_date_range(start_date, end_date):
    try: 
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")

        if end_dt < start_dt:
            return False
        return True
    
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD")
        return False
    