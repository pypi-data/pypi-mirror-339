HOLIDYAS = {"2025-01-01": {"date": "2025-01-01", "name": "元旦", "isOffDay": True},
            "2025-01-26": {"date": "2025-01-26", "name": "春节", "isOffDay": False},
            "2025-01-28": {"date": "2025-01-28", "name": "春节", "isOffDay": True},
            "2025-01-29": {"date": "2025-01-29", "name": "春节", "isOffDay": True},
            "2025-01-30": {"date": "2025-01-30", "name": "春节", "isOffDay": True},
            "2025-01-31": {"date": "2025-01-31", "name": "春节", "isOffDay": True},
            "2025-02-01": {"date": "2025-02-01", "name": "春节", "isOffDay": True},
            "2025-02-02": {"date": "2025-02-02", "name": "春节", "isOffDay": True},
            "2025-02-03": {"date": "2025-02-03", "name": "春节", "isOffDay": True},
            "2025-02-04": {"date": "2025-02-04", "name": "春节", "isOffDay": True},
            "2025-02-08": {"date": "2025-02-08", "name": "春节", "isOffDay": False},
            "2025-04-04": {"date": "2025-04-04", "name": "清明节", "isOffDay": True},
            "2025-04-05": {"date": "2025-04-05", "name": "清明节", "isOffDay": True},
            "2025-04-06": {"date": "2025-04-06", "name": "清明节", "isOffDay": True},
            "2025-04-27": {"date": "2025-04-27", "name": "劳动节", "isOffDay": False},
            "2025-05-01": {"date": "2025-05-01", "name": "劳动节", "isOffDay": True},
            "2025-05-02": {"date": "2025-05-02", "name": "劳动节", "isOffDay": True},
            "2025-05-03": {"date": "2025-05-03", "name": "劳动节", "isOffDay": True},
            "2025-05-04": {"date": "2025-05-04", "name": "劳动节", "isOffDay": True},
            "2025-05-05": {"date": "2025-05-05", "name": "劳动节", "isOffDay": True},
            "2025-05-31": {"date": "2025-05-31", "name": "端午节", "isOffDay": True},
            "2025-06-01": {"date": "2025-06-01", "name": "端午节", "isOffDay": True},
            "2025-06-02": {"date": "2025-06-02", "name": "端午节", "isOffDay": True},
            "2025-09-28": {"date": "2025-09-28", "name": "国庆节、中秋节", "isOffDay": False},
            "2025-10-01": {"date": "2025-10-01", "name": "国庆节、中秋节", "isOffDay": True},
            "2025-10-02": {"date": "2025-10-02", "name": "国庆节、中秋节", "isOffDay": True}, "2025-10-03": {"date": "2025-10-03", "name": "国庆节、中秋节", "isOffDay": True}, "2025-10-04": {"date": "2025-10-04", "name": "国庆节、中秋节", "isOffDay": True}, "2025-10-05": {"date": "2025-10-05", "name": "国庆节、中秋节", "isOffDay": True}, "2025-10-06": {"date": "2025-10-06", "name": "国庆节、中秋节", "isOffDay": True}, "2025-10-07": {"date": "2025-10-07", "name": "国庆节、中秋节", "isOffDay": True}, "2025-10-08": {"date": "2025-10-08", "name": "国庆节、中秋节", "isOffDay": True}, "2025-10-11": {"date": "2025-10-11", "name": "国庆节、中秋节", "isOffDay": False}}


def is_holiday() -> bool:
    """
    Check if today is a holiday
    Returns:
        bool: True if today is a holiday (weekend or official holiday), False otherwise
    """
    from datetime import datetime

    today = datetime.now().strftime('%Y-%m-%d')

    # Check if it's weekend
    weekday = datetime.now().weekday()
    if weekday >= 5:  # 5 is Saturday, 6 is Sunday
        return True

    # Check if it's in holiday list
    if today in HOLIDYAS:
        return HOLIDYAS[today]['isOffDay']

    return False


if __name__ == "__main__":
    print(is_holiday())
