def reset_user_vars(rs):
    all_users = rs.get_uservars(rs.current_user())
    print("ALL user variable--->", all_users)
    return "success"
