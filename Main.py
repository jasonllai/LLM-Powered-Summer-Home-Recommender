def main():
    app_status = True
    is_user = False
    is_admin = False
    search_status = False
    direct_search_status = False
    ai_consultant_status = False
    filter_status = False
    booking_status = False

    user_logged_in = False
    admin_logged_in = False

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
                    # Need to check if the username and password pair exists
                    # Call check_login_validity(user_username, user_password, user_list)
                    user_logged_in = True

                    while user_logged_in:
                        print("How can we help you today?")
                        print("[v] View my profile")
                        print("[u] Update my profile")
                        print("[s] Search for a property")
                        print("[b] Check my booking")
                        print("[e] Exit")
                        choice_3 = input("Please enter the corresponding letter: ")

                        if choice_3 == "v":
                            print("Here is your profile: ")
                            continue

                        elif choice_3 == "u":
                            print("Please follow the instruction to update your profile")
                            continue

                        elif choice_3 == "s":
                            search_status = True

                            while search_status:
                                print("You can choose to: ")
                                print("[1] Direct search for properties")
                                print("[2] Ask our AI consultant")
                                print("[3] Go back to home page")
                                choice_4 = input("Please select: ")

                                if choice_4 == "1":
                                    direct_search_status = True

                                    while direct_search_status:
                                        # Call recommender function
                                        print("Please enter your preferences: ")
                                        print("...")  # Display the properties from recommender function
                                        # Store the returned data frame from recommender function: df = ...
                                        # Add index to the data frame: df["indexes"] = df.index + 1
                                        print("[f] Filter recommended properties")
                                        print("[2] Make a booking by entering the corresponding index: ")
                                        print("[b] Go back to the previous page")
                                        choice_5 = input()

                                        if choice_5 == "f":
                                            # Call filter function; pass df into the filter function
                                            print("Filtering")
                                            # df = ...
                                            # df = df.reset_index(drop=True)
                                            # df["indexes"] = df.index + 1

                                        elif choice_5 == "2":  # Need to be modified later
                                            # Have to check if the input is an integer between 1 and last index of the df
                                            print("Make a booking")
                                            # Call booking function; should take prop_id and dates as its arguments
                                            print("Booking successful!")
                                            direct_search_status = False
                                            search_status = False

                                        elif choice_5 == "b":
                                            direct_search_status = False

                                        else:
                                            print("Invalid choice!")




                                elif choice_4 == "2":
                                    ai_consultant_status = True
                                    
                                    while ai_consultant_status:
                                        # Call LLM function
                                        print("Let our AI consultant help!")
                                        ai_consultant_status = False

                                elif choice_4 == "3":
                                    search_status = False

                                else:
                                    print("Invalid choice!")
                        
                        elif choice_3 == "b":
                            print("Here are your current booking: ")

                        elif choice_3 == "e":
                            print("Log out successfully!")
                            user_logged_in = False
                            break

                        else:
                            print("Invalid choice!")


                elif choice_2 == "2":
                    # create_user_profile()
                    print("Let's sign up!")
                    
                elif choice_2 == "3":
                    print("Thanks for using!")
                    is_user = False
                    
                else:
                    print("Invalid choice!")
                    
                        
        elif choice_1 == "a":
            is_admin = True

            while is_admin:
                print("Welcome administrator!")
                print("[1] Sign in")
                print("[2] Exit")
                choice_6 = input()

                if choice_6 == "1":
                    admin_username = input("Please enter your username: ")
                    admin_password = input("Please enter your password: ")
                    # Call check_login_validity(admin_username, admin_password, admin_list)
                    admin_logged_in = True

                    while admin_logged_in:
                        print("Welcome Administrator! Please select from the following options: ")
                        print("[u] View users in the app")
                        print("[p] View properties in the app")
                        print("[a] Add a new property")
                        print("[e] Update a property")
                        print("[d] Delete a property")
                        print("[g] AI generate properties")
                        print("[x] Exit")
                        choice_7 = input()

                        if choice_7 == "u":
                            print("Here are the registered users in our app: ")
                            # print users_list

                        elif choice_7 == "p":
                            print("Here are the properties listed in our app: ")
                            # print properties_list

                        elif choice_7 == "a":
                            print("Addding a new property: ")
                            # Call add_properties()

                        elif choice_7 == "e":
                            property_id = input("Enter the property id you want to update: ")
                            # Call update_property(property_id)

                        elif choice_7 == "d":
                            property_id = input("Enter the property id you want to delete: ")
                            # Call delete_properties(property_id)

                        elif choice_7 == "g":
                            n = input("Enter the number of properties you want to generate: ")
                            # Call LLM function that generates n properties

                        elif choice_7 == "x":
                            print("Log out successfully!")
                            admin_logged_in = False

                        else:
                            print("Invalid choice!")

                elif choice_6 == "2":
                    print("Thanks for using!")
                    is_admin = False
                    
                else:
                    print("Invalid choice!")

        
        elif choice_1 == "e":
            app_status = False
            print("Thanks for using!")
            

        else:
            print("Invalid choice. Exiting.")
            return


if __name__ == "__main__":
    main()