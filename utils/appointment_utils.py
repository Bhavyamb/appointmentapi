from datetime import datetime

def get_current_time():
    """
    Get the current time.
    """
    return datetime.now().strftime('%H:%M:%S') 

def get_current_date():
    """
    Get the current date.
    """
    return datetime.now().date()
