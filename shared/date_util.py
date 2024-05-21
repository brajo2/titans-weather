from datetime import datetime

def convert_date_format(date_str: str) -> str:
    date_as_obj = datetime.strptime(date_str, '%m/%d/%Y')
    return date_as_obj.strftime('%Y-%m-%d')
