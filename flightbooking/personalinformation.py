def personalinfovalidation(rs,name, phonenumber, id):
    import re
    phone_regex = re.compile("[7-9][0-9]{9}")
    id_regex = re.compile("[0-9]{12}")
    if phone_regex.match(phonenumber):
        if id_regex.match(id):
            return "success"
        else:
            return '{"text": "Entered id is not valid,Please give me the aadhar card number", "options":[]}'

    else:
        return '{"text": "Entered phonenumber is not valid,Please give me your phone number", "options":[]}'
