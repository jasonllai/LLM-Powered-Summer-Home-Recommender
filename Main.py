def main():
    app_status = True
    is_user = False
    is_admin = False
    search_status = False
    logged_in = False

    user_username = ""
    user_password = ""

    while app_status:
        print("Welcome to the Summer Home Recommender App!")
        print("If you are a user, type [u]")
        print("If you are an administrator, type [a]")
        print("If you want to exit, type [e]")
        choice_1 = input("[u]/[a]/[e]: ")
        
        if choice_1 == "u":
            is_user = True
            
            while is_user:
                print("Welcome our user! Please choose between the following options:")
                choice_2 = input("[1]Sign in; [2]Sign up; [3]Exit ")

                if choice_2 == "1":
                    user_username = input("Please enter your username: ")
                    user_password = input("Please enter your password: ")
                    logged_in = True

                elif choice_2 == "2":
                    print("Let's register a new account for you!")
                    user_username = input("Please enter your username: ")
                    user_password = input("Please enter your password: ")
                    
                elif choice_2 == "3":
                    print("Thanks for using!")
                    is_user = False
                    app_status = False
                    break
                    
                else:
                    print("Invalid choice!")
                    
                        
        elif choice_1 == "a":
            is_admin = True
            print("Welcome administrator!")
            
        
        elif choice_1 == "e":
            app_status = False
            print("Thanks for using!")
            

        else:
            print("Invalid choice. Exiting.")
            return


main()