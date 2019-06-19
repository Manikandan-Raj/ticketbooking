def personalinfophone(phone):
    import re
    phone_regex = re.compile("[7-9][0-9]{9}")
    if phone_regex.match(phone):
        return "success"
    else:
        return "failure"

def personalinfoid(aadhar):
    import re
    id_regex = re.compile("[0-9]{12}")
    if id_regex.match(aadhar):
        return "success"
    else:
        return "failure"
