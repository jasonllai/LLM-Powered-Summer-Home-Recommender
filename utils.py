# Helper functions for main()

def check_login_validity(username, password, user_list):
    for user in user_list:
        if user.user_id == username and user.password == password:
            return user
    print("Username or password is incorrect.")
    return None

def validate_booking_input(user_input, prop_df, id_column="indexes"):
    try:
        # 1. Try converting to integer
        input_index = int(user_input)
    except ValueError:
        return False, None  # not convertible to int

    # 2. Check if this integer exists in the DataFrame column
    if input_index in prop_df[id_column].values:
        return True, input_index
    else:
        return False, None

