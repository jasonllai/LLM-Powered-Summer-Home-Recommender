from numpy import False_
import pandas as pd
from Functions import User, Admin, Property
from Functions import create_user_profile, edit_user_profile, view_user_profile
from Functions import users_obj_list, property_obj_list
from Recommender_Logic import ListingRecommender
from Filter_And_Sort import filter_properties
from utils import check_login_validity, validate_booking_input
from LLM_functions import generate_suggestions




def main():
    app_status = True
    is_user = False
    is_admin = False
    search_status = False
    filter_status = False
    ai_consultant_status = False
    booking_status = False

    user_logged_in = False
    admin_logged_in = False

    user_username = ""
    user_password = ""

    curr_user = None

    environment_pool = ["beach", "lake", "forest", "mountains", "nightlife", "remote", "glamping", "city", "modern", "historic"]


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
                    curr_user = check_login_validity(user_username, user_password, users_obj_list)
                    
                    if curr_user:
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
                            view_user_profile(curr_user.user_id)
                            

                        elif choice_3 == "u":
                             while True:
                                print(f"\n=== EDITING USIER PROFILE ===")
                                print("Current profile:")
                                view_user_profile(curr_user.user_id)

                                new_name = curr_user.name
                                new_password = curr_user.password
                                new_group_size = curr_user.group_size
                                new_preferred_environment = curr_user.preferred_environment
                                new_budget_range = curr_user.budget_range

                                print("\nWhat would you like to edit?")
                                print("[1] Name")
                                print("[2] Password")
                                print("[3] Create Booking")
                                print("[4] Delete Booking")
                                print("[5] Group Size")
                                print("[6] Preferred Environment")
                                print("[7] Budget Range")
                                print("[8] Exit")

                                try:
                                    edit_choice = int(input("Enter your choice (1-8): ").strip())
                                    if edit_choice < 1 or edit_choice > 8:
                                        print("Please enter a number between 1 and 8")
                                        continue

                                except ValueError:
                                    print("Please enter a number")
                                    continue

                                if edit_choice == 8:
                                    print("Edit session completed")
                                    return curr_user

                                elif edit_choice == 1:
                                    new_name = input("New name: ").strip()
                                    edit_user_profile(curr_user.user_id, edit_choice, new_name)
                                    
                                elif edit_choice == 2:
                                    new_password = input("New password: ").strip()
                                    edit_user_profile(curr_user.user_id, edit_choice, new_password)
                                    
                                elif edit_choice == 3:
                                    edit_user_profile(curr_user.user_id, edit_choice)

                                elif edit_choice == 4:
                                    edit_user_profile(curr_user.user_id, edit_choice)

                                elif edit_choice == 5:
                                    new_group_size = input("New group size: ")
                                    edit_user_profile(curr_user.user_id, edit_choice, new_group_size)

                                elif edit_choice == 6:
                                    environment_pool = ["beach", "lake", "forest", "mountains", "nightlife", "remote", "glamping", "city", "modern", "historic"]
                                    print("Please enter your preferred environment from the list below")
                                    print("If you would like to check multiple preferred environments, please separate each tags by comma")
                                    print(environment_pool)
                                    environment_input = input("New preferred environment: ")
                                    # Split by comma and strip whitespace
                                    new_preferred_environment = [tag.strip() for tag in environment_input.split(",") if tag.strip()]
                                    # Optional: validate against available tags
                                    new_preferred_environment = [tag for tag in new_preferred_environment if tag in environment_pool]

                                    edit_user_profile(curr_user.user_id, edit_choice, new_preferred_environment)

                                elif edit_choice == 7:
                                    new_min_budget = input("New minimum budget is: ")
                                    new_max_budget = input("New maximum budget is: ")
                                    new_budget_range = (new_min_budget, new_max_budget)
                                    edit_user_profile(curr_user.user_id, edit_choice, new_budget_range)
                                                    

                        elif choice_3 == "s":
                            search_status = True

                            while search_status:
                                # Call recommender logic function here
                                recommender = ListingRecommender(property_obj_list)
                                property_listing_calculated_scores = recommender.calculate_total_score(curr_user)
                                properties_df = pd.DataFrame(property_listing_calculated_scores)
                                properties_df["tags"] = properties_df["tags"].apply(lambda x: [tag.strip() for tag in x.split(",")])
                                properties_df = properties_df.drop(columns=["total_score"])
                                properties_df["property_index"] = properties_df.index
                                print(properties_df[["location", "type", "price_per_night", "guest_capacity", "tags"]])

                                print("You can choose to: ")
                                print("[1] Filter properties")
                                print("[2] Ask our AI assistant")
                                print("[3] Go back to home page")
                                choice_4 = input("Please select: ")

                                if choice_4 == "1":
                                    filter_status = True

                                    while filter_status:
                                        # Call filter function
                                        properties_df.to_json("data/properties.json", orient="records", indent=4)


                                        print("Please enter your preferences: ")
                                        print("...")  # Display the properties from filter function
                                        # Store the returned data frame from filter function: df = ...
                                        # Add index to the data frame: df["indexes"] = df.index + 1
                                        print("Have you find an ideal place to stay?")
                                        print("[b] Make a booking")
                                        print("[r] Return to the previous page")
                                        choice_5 = input()

                                        if choice_5 == "b":
                                            book_index = input("Please enter the index of the property you want to book: ")
                                            is_valid, row_index = validate_booking_input(book_index, properties_df, id_column="indexes")

                                            if is_valid:
                                                book_prop_id = properties_df.loc[row_index, "property_id"]
                                                # book_property(book_prop_id); Need to implement a booking function
                                                print("Make a booking")
                                                print("Booking successful!")
                                                direct_search_status = False
                                                search_status = False

                                            else:
                                                print("Invalid id!")


                                        elif choice_5 == "r":
                                            filter_status = False

                                        else:
                                            print("Invalid choice!")


                                elif choice_4 == "2":
                                    ai_consultant_status = True
                                    
                                    while ai_consultant_status:
                                        generate_suggestions()
                                        ai_consultant_status = False

                                elif choice_4 == "3":
                                    search_status = False

                                else:
                                    print("Invalid choice!")
                        
                        elif choice_3 == "b":
                            # Need to print current booking list
                            print("Here are your current booking: ")

                        elif choice_3 == "e":
                            print("Log out successfully!")
                            user_logged_in = False
                            break

                        else:
                            print("Invalid choice!")


                elif choice_2 == "2":
                    # create_user_profile()
                    print("\n=== CREATE NEW PROFILE ===")
                    new_user_name = input("Enter your name: ")
                    new_user_password = input("Enter your password: ")
                    new_user_group_size = input("Enter your group size: ")

                    print("Please enter your preferred environment from the list below")
                    print("If you would like to check multiple preferred environments, please separate each tags by comma")
                    print(environment_pool)
                    new_environment_input = input("New preferred environment: ")
                    # Split by comma and strip whitespace
                    new_user_preferred_environment = [tag.strip() for tag in new_environment_input.split(",") if tag.strip()]
                    # Optional: validate against available tags
                    new_user_preferred_environment = [tag for tag in new_user_preferred_environment if tag in environment_pool]

                    new_user_min_budget = int(input("Enter your minimum budget: "))
                    new_user_max_budget = int(input("Enter your maximum budget: "))
                    new_user_budget_range = (new_user_min_budget, new_user_max_budget)

                    create_user_profile(new_user_name, new_user_password, new_user_group_size, new_user_preferred_environment, new_user_budget_range)
                    
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
                    admin_logged_in = check_login_validity(admin_username, admin_password, users_obj_list)

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


