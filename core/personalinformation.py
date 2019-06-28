import re

def personalinfophone(phone):
    phone_regex = re.compile("[7-9][0-9]{9}")
    if phone_regex.match(phone):
        return True
    return False

def personalinfoid(aadhar):
    id_regex = re.compile("[0-9]{12}")
    if id_regex.match(aadhar):
        return True
    return False

def personalinfoname(name):
    if re.match("[a-zA-Z]*",name).group() != '':
        return True
    return False
