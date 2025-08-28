import json
import pandas as pd

from rental_management import User, Property
from rental_management import load_data_from_json, validate_date
from rental_management import validate_user, validate_admin
from rental_management import create_user_profile, view_user_profile, delete_profile, edit_user_profile, create_booking, delete_booking
from rental_management import view_users, view_properties, add_properties, delete_property, update_property

from Recommender_Logic import ListingRecommender
from filter import filter_properties
from LLM_functions import generate_properties, generate_suggestions
from utils import get_int_input, get_string_input, get_string_list_input



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

    curr_user = None

    environment_pool = ["beach", "lake", "forest", "mountains", "nightlife", "remote", "glamping", "city", "modern", "historic"]

    location_pool = ["Vancouver", "Toronto", "Montreal", "Calgary", "Edmonton", "Winnipeg", "Halifax", "Victoria", "Quebec City", "Fredericton"]

    type_pool = ["cabin", "apartment", "cottage", "loft", "villa", "tiny house", "studio"]

    feature_pool = ["mountain view", "city skyline view", "lakefront", "riverfront",
                "oceanfront", "beach access", "balcony or patio", "rooftop terrace",
                "private hot tub", "sauna", "private pool", "fireplace", "houskeeper service",
                "BBQ grill", "full kitchen", "chef's kitchen", "EV charger", "free parking",
                "garage", "air conditioning", "heating", "washer and dryer", "fast wifi",
                "dedicated workspace", "smart TV with streaming", "game room", "fitness room",
                "ski-in/ski-out", "wheelchair accessible", "pet-friendly"]

    tag_pool = ["mountains", "remote", "adventure", "beach", "city", "lake", 
                "river", "ocean", "forest", "park", "national park", "state park", 
                "national forest", "state forest", "modern","rustic","historic",
                "family-friendly","kid-friendly","pet-friendly","romantic","business-travel",
                "nightlife","eco-friendly","spa","golf","foodie","farm-stay","glamping","long-term"]

    user_data = load_data_from_json("data/Users.json")


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
                    user_id_input = input("Please enter your user id: ")
                    password_input = input("Please enter your password: ")

                    if validate_user(user_id_input, password_input):
                        print("Log in successful!")
                        user_logged_in = True
                    
                    else:
                        print("User id and password do not match!")

                    while user_logged_in:
                        curr_user_dict = next((a for a in user_data if a.get("user_id") == user_id_input and a.get("password") == password_input), None)
                        curr_user = User.from_dict(curr_user_dict)
                        print("How can we help you today?")
                        print("[v] View my profile")
                        print("[u] Update my profile")
                        print("[s] Search and book a property")
                        print("[b] Check my booking")
                        print("[d] Delete my profile and exit")
                        print("[e] Exit")
                        choice_3 = input("Please enter the corresponding letter: ")

                        if choice_3 == "v":
                            print(f"\n=== VIEWING USER PROFILE ===")
                            user_profile = view_user_profile(curr_user.user_id)
                            user_profile_df = pd.DataFrame([user_profile]).drop(columns = "booking_history")
                            user_booking_df = pd.DataFrame(user_profile["booking_history"])

                            print("\nUser Profile: ")
                            print(user_profile_df)
                            print("\nBooking Profile: ")
                            print(user_booking_df)
                            
                        elif choice_3 == "u":
                             while True:
                                print(f"\n=== EDITING USER PROFILE ===")
                                new_user_id = curr_user.user_id
                                new_name = curr_user.name
                                new_password = curr_user.password
                                new_booking_history = curr_user.booking_history
                                new_group_size = curr_user.group_size
                                new_preferred_environment = curr_user.preferred_environment
                                new_budget_range = curr_user.budget_range

                                print("\nWhat would you like to edit?")
                                print("[1] Username")
                                print("[2] Password")
                                print("[3] Delete Booking")
                                print("[4] Group Size")
                                print("[5] Preferred Environment")
                                print("[6] Budget Range")
                                print("[7] Exit")

                                user_edit_choice = input("Enter your choice (1-7): ").strip()

                                if user_edit_choice == "1":
                                    new_name = input("New name: ").strip()
                                    new_user_dict = User(new_user_id, new_name, new_password, new_booking_history, new_group_size, new_preferred_environment, new_budget_range).to_dict()
                                    edit_user_profile(new_user_dict)
           
                                elif user_edit_choice == "2":
                                    new_password = input("New password: ").strip()
                                    new_user_dict = User(new_user_id, new_name, new_password, new_booking_history, new_group_size, new_preferred_environment, new_budget_range).to_dict()
                                    edit_user_profile(new_user_dict)
                                    
                                elif user_edit_choice == "3":
                                    print("Here are your current booking(s): ")
                                    user_profile = view_user_profile(curr_user.user_id)
                                    user_booking_df = pd.DataFrame(user_profile["booking_history"])

                                    if user_booking_df.empty:
                                        print("There's currently no booking history for this user.")

                                    else:
                                        print(user_booking_df)
                                        print("Please enter the row index of the booking that you want to delete: ")
                                        delete_booking_index = input("Or enter [c] to cancel delete booking: ").strip()

                                        if delete_booking_index == "c":
                                            continue

                                        elif int(delete_booking_index) in user_booking_df.index:
                                            delete_prop_id = user_booking_df.loc[int(delete_booking_index)]["property_id"]
                                            delete_start_date = user_booking_df.loc[int(delete_booking_index)]["start_date"]
                                            delete_end_date = user_booking_df.loc[int(delete_booking_index)]["end_date"]

                                            delete_booking(new_user_id, delete_prop_id, delete_start_date, delete_end_date)

                                        else:
                                            print("Invalid index!") 

                                elif user_edit_choice == "4":
                                    new_group_size = int(input("New group size: ").strip())
                                    new_user_dict = User(new_user_id, new_name, new_password, new_booking_history, new_group_size, new_preferred_environment, new_budget_range).to_dict()
                                    edit_user_profile(new_user_dict)

                                elif user_edit_choice == "5":
                                    print("Please enter your preferred environment from the list below: ")
                                    print(environment_pool)
                                    new_preferred_environment = get_string_input("New preferred environment: ", environment_pool)
                                    new_user_dict = User(new_user_id, new_name, new_password, new_booking_history, new_group_size, new_preferred_environment, new_budget_range).to_dict()
                                    edit_user_profile(new_user_dict)

                                elif user_edit_choice == "6":
                                    while True:
                                        new_min_budget = get_int_input("New minimum budget: ")
                                        new_max_budget = get_int_input("New maximum budget: ")
                                        if new_max_budget >= new_min_budget:
                                            new_budget_range = [new_min_budget, new_max_budget]
                                            break

                                        else:
                                            print("Invalid budget range! The maximum budget should be greater than or equal to minimum budget.")

                                    new_user_dict = User(new_user_id, new_name, new_password, new_booking_history, new_group_size, new_preferred_environment, new_budget_range).to_dict()
                                    edit_user_profile(new_user_dict)
                                            
                                elif user_edit_choice == "7":
                                    print("Edit session completed!")
                                    break

                                else:
                                    print("Invalid choice!")

                                                    
                        elif choice_3 == "s":
                            search_status = True

                            while search_status:
                                recommender = ListingRecommender()
                                recommended_properties = recommender.calculate_total_score(curr_user.user_id)
                                recommended_properties_df = pd.DataFrame(recommended_properties)
                                recommended_properties_df = recommended_properties_df.drop(columns=["total_score"])
                                recommended_properties_df["property_index"] = recommended_properties_df.index
                                print("Check out these properties that may be of your interest!")
                                print(recommended_properties_df[["location", "type", "price_per_night", "guest_capacity", "tags"]])

                                print("You can choose to: ")
                                print("[1] Filter properties")
                                print("[2] Ask our AI assistant")
                                print("[3] Make a booking")
                                print("[4] Go back to home page")
                                choice_4 = input("Please select: ")

                                if choice_4 == "1":
                                    filter_status = True

                                    filter_group_size = None
                                    filter_min_price = None
                                    filter_max_price = None
                                    filter_features = None
                                    filter_tags = None
                                    filter_type = None
                                    filter_location = None
                                    filter_start_date = None
                                    filter_end_date = None

                                    while filter_status:
                                        print("\nPlease select the attribute you want to filter on and enter your preferences")
                                        print("[1] Group size")
                                        print("[2] Minimum price per night")
                                        print("[3] Maximum price per night")
                                        print("[4] Features")
                                        print("[5] Tags")
                                        print("[6] Property type")
                                        print("[7] Location")
                                        print("[8] Start date")
                                        print("[9] End date")
                                        print("[f] Filter properties based on the preferences input")
                                        print("[b] Go back to the previous page")

                                        filter_choice = input("Enter your choice: ").strip()

                                        if filter_choice == "1":
                                            filter_group_size = get_int_input("Please enter the group size you want to filter on: ")
                                            
                                        elif filter_choice == "2":
                                            filter_min_price = get_int_input("Please enter the min price you want to filter on: ")

                                        elif filter_choice == "3":
                                            filter_max_price = get_int_input("Please enter the max price you want to filter on: ")

                                        elif filter_choice == "4":
                                            filter_features = get_string_list_input("Please enter the features you want to filter on; If you have multiple features, please separate by comma: ", feature_pool)
                                            if not filter_features:
                                             filter_features = None

                                        elif filter_choice == "5":
                                            filter_tags = get_string_list_input("Please enter the tags you want to filter on; If you have multiple tags, please separate by comma: ", tag_pool)
                                            if not filter_tags:
                                                filter_tags = None

                                        elif filter_choice == "6":
                                            filter_type = get_string_input("Please enter the property type you want to filter on: ", type_pool)

                                        elif filter_choice == "7":
                                            filter_location = get_string_input("Please enter the location you want to filter on: ", location_pool)

                                        elif filter_choice == "8":
                                            input_start_date = input("Please enter the start date (yyyy-mm-dd): ")
                                            if validate_date(input_start_date):
                                                filter_start_date = input_start_date
                                            else:
                                                print("Invalid format for start date!")

                                        elif filter_choice == "9":
                                            input_end_date = input("Please enter the end date (yyyy-mm-dd): ")
                                            if validate_date(input_end_date):
                                                filter_end_date = input_end_date
                                            else:
                                                print("Invalid format for end date!")

                                        elif filter_choice == "f":
                                            filtered_properties = filter_properties(group_size=filter_group_size, min_price=filter_min_price, max_price=filter_max_price, features=filter_features, tags=filter_tags, prop_type=filter_type, location=filter_location, start_date=filter_start_date, end_date=filter_end_date)
                                            filtered_properties_df = pd.DataFrame(filtered_properties)
                                            print(filtered_properties_df.drop(columns = "property_id"))
                                            booking_status = True

                                            while booking_status:
                                                print("\nHave you find an ideal property?")
                                                print("[b] Make a booking")
                                                print("[r] Return to the previous page")
                                                choice_5 = input("Please select an option: ").strip()

                                                if choice_5 == "b":
                                                    booking_index = get_int_input("Please enter the index of the property you want to book: ")

                                                    if booking_index in filtered_properties_df.index:
                                                        booking_user_id = curr_user.user_id
                                                        booking_prop_id = filtered_properties_df.loc[booking_index]["property_id"]
                                                        booking_start_date = input("Please enter the start date of your booking (yyyy-mm-dd): ")
                                                        booking_end_date = input("Please enter the end date of your booking (yyyy-mm-dd): ")
                                                        if create_booking(booking_user_id, booking_prop_id, booking_start_date, booking_end_date):
                                                            booking_status = False
                                                            filter_status = False
                                                        else:
                                                            booking_status = False
                                                    
                                                    else:
                                                        print("Invalid index!")

                                                elif choice_5 == "r":
                                                    booking_status = False

                                        elif filter_choice == "b":
                                            filter_status = False

                                        else:
                                            print("Invalid choice!")


                                elif choice_4 == "2":
                                    ai_consultant_status = True
                                    
                                    while ai_consultant_status:
                                        generate_suggestions()
                                        print("Are you satisfied with AI suggestions?")
                                        exit_ai_choice = input("If yes, you can enter [e] to exit: ").strip()

                                        if exit_ai_choice == "e":
                                            ai_consultant_status = False


                                elif choice_4 == "3":
                                    booking_status = True

                                    while booking_status:
                                        booking_index = get_int_input("Please enter the index of the property you want to book: ")

                                        if booking_index in recommended_properties_df.index:
                                            booking_user_id = curr_user.user_id
                                            booking_prop_id = recommended_properties_df.loc[booking_index]["property_id"]
                                            booking_start_date = input("Please enter the start date of your booking (yyyy-mm-dd): ")
                                            booking_end_date = input("Please enter the end date of your booking (yyyy-mm-dd): ")
                                            create_booking(booking_user_id, booking_prop_id, booking_start_date, booking_end_date)
                                            booking_status = False

                                        else:
                                            print("Invalid index!")


                                elif choice_4 == "4":
                                    search_status = False


                                else:
                                    print("Invalid choice!")

                        
                        elif choice_3 == "b":
                            booking = view_user_profile(curr_user.user_id)
                            print(pd.DataFrame(booking["booking_history"]))


                        elif choice_3 == "d":
                            print("Are you sure you want to delete your current user profile?")
                            delete_profile_choice = input("[y] Yes; [n] No")
                            
                            if delete_profile_choice == "y":
                                print("User profile deleted. See you next time!")
                                delete_profile(curr_user.user_id)
                                user_logged_in = False

                            elif delete_profile_choice == "n":
                                continue

                        elif choice_3 == "e":
                            print("Log out successfully!")
                            user_logged_in = False
                            break

                        else:
                            print("Invalid choice!")


                elif choice_2 == "2":
                    print("\n=== CREATE NEW PROFILE ===")
                    new_user_id = input("Enter your user id: ").strip()
                    new_user_name = input("Enter your username: ").strip()
                    new_user_password = input("Enter your password: ").strip()
                    new_user_group_size = get_int_input("Enter your group size: ")

                    print("Please enter your preferred environment from the list below")
                    print(environment_pool)
                    new_user_preferred_environment = get_string_input("Enter your preferred environment: ", environment_pool)

                    while True:
                        new_user_min_budget = get_int_input("Enter your minimum budget: ")
                        new_user_max_budget = get_int_input("Enter your maximum budget: ")
                        
                        if new_user_max_budget >= new_user_min_budget:
                            new_user_budget_range = [new_user_min_budget, new_user_max_budget]
                            break
                        else:
                            print("Invalid budget range! The maximum budget should be greater than or equal to minimum budget.")

                    create_user_profile(new_user_id, new_user_name, new_user_password, new_user_group_size, new_user_preferred_environment, new_user_budget_range)
                    

                elif choice_2 == "3":
                    print("Thanks for using!")
                    is_user = False
                    app_status = False
                    
                else:
                    print("Invalid choice!")
                    
                        
        elif choice_1 == "a":
            is_admin = True

            while is_admin:
                print("Welcome administrator!")
                print("[1] Sign in")
                print("[2] Exit")
                choice_6 = input("Please enter [1]/[2]: ")

                if choice_6 == "1":
                    admin_id_input = input("Please enter your username: ")
                    admin_password_input = input("Please enter your password: ")

                    if validate_admin(admin_id_input, admin_password_input):
                        print("Log in successful!")
                        admin_logged_in = True
                    
                    else:
                        print("Admin id and password do not match!")

                    while admin_logged_in:
                        print("Welcome Administrator! Please select from the following options: ")
                        print("[u] View users in the app")
                        print("[p] View properties in the app")
                        print("[a] Add a new property")
                        print("[e] Update a property")
                        print("[d] Delete a property")
                        print("[g] AI generate properties")
                        print("[x] Exit")
                        choice_7 = input("Please enter your choice: ")

                        if choice_7 == "u":
                            print("Here are the registered users in our app: ")
                            pd.set_option("display.max_colwidth", 30)
                            print(pd.DataFrame(view_users()))

                        elif choice_7 == "p":
                            print("Here are the properties listed in our app: ")
                            pd.set_option("display.max_colwidth", 20)
                            print(pd.DataFrame(view_properties()).drop(columns = "property_id"))

                        elif choice_7 == "a":
                            print("\n===Adding A New Property ===")
                            print("Please enter the location from the list below: ")
                            print(location_pool)
                            prop_location = get_string_input("Location: ", location_pool)

                            print("Please enter the property type from the list below: ")
                            print(type_pool)
                            prop_type = get_string_input("Property type: ", type_pool)

                            prop_price = get_int_input("Price per night (integer): ")

                            print("Please enter the features from the list below: ")
                            print("If the property has multiple features, please separate each feature by comma.")
                            print(feature_pool)
                            prop_features = get_string_list_input("Features: ", feature_pool)

                            print("Please enter the tags from the list below: ")
                            print("If the property has multiple tags, please separate each tag by comma.")
                            prop_tags = get_string_list_input("Tags: ", tag_pool)

                            prop_guest_capacity = get_int_input("Guest capacity (integer): ")

                            add_properties(prop_location, prop_type, prop_price, prop_features, prop_tags, prop_guest_capacity)

                        elif choice_7 == "e":
                            
                            while True:
                                print(f"\n=== Editing Property ===")
                                property_obj_list = [Property.from_dict(d) for d in load_data_from_json("data/Properties.json")]

                                pd.set_option("display.max_colwidth", 20)
                                properties_dict = view_properties()
                                properties_df = pd.DataFrame(properties_dict)
                                print(properties_df.drop(columns = "property_id"))

                                edit_prop_index = get_int_input("Enter the index of the property you want to update: ")

                                if edit_prop_index in properties_df.index:
                                    edit_prop_id = properties_df.loc[edit_prop_index]["property_id"]
                                    edit_prop = next((p for p in property_obj_list if p.property_id == edit_prop_id), None)
                                
                                    new_property_id = edit_prop.property_id
                                    new_location = edit_prop.location
                                    new_p_type = edit_prop.p_type
                                    new_price = edit_prop.price_per_night
                                    new_features = edit_prop.features
                                    new_tags = edit_prop.tags
                                    new_guest_capacity = edit_prop.guest_capacity
                                    new_unavailable_dates = edit_prop.unavailable_dates

                                    print("\nWhat would you like to edit?")
                                    print("[1] Location")
                                    print("[2] Property type")
                                    print("[3] Price per night")
                                    print("[4] Features")
                                    print("[5] Tags")
                                    print("[6] Guest capacity")
                                    print("[7] Exit")

                                    prop_edit_choice = input("Enter your choice (1-7): ").strip()

                                    if prop_edit_choice == "1":
                                        print("Please enter the new location from the list below: ")
                                        print(location_pool)
                                        new_location = get_string_input("New location: ", location_pool)
                                        new_prop_dict = Property(new_property_id, new_location, new_p_type, new_price, new_features, new_tags, new_guest_capacity, new_unavailable_dates).to_dict()
                                        update_property(new_prop_dict)
            
                                    elif prop_edit_choice == "2":
                                        print("Please enter the new property type from the list below: ")
                                        print(type_pool)
                                        new_p_type = get_string_input("New property type: ", type_pool)
                                        new_prop_dict = Property(new_property_id, new_location, new_p_type, new_price, new_features, new_tags, new_guest_capacity, new_unavailable_dates).to_dict()
                                        update_property(new_prop_dict)
                                        
                                    elif prop_edit_choice == "3":
                                        new_price = get_int_input("New price per night (integer): ")
                                        new_prop_dict = Property(new_property_id, new_location, new_p_type, new_price, new_features, new_tags, new_guest_capacity, new_unavailable_dates).to_dict()
                                        update_property(new_prop_dict)

                                    elif prop_edit_choice == "4":
                                        print("Please enter the new features from the list below: ")
                                        print("If the property has multiple features, please separate each feature by comma.")
                                        print(feature_pool)
                                        new_features = get_string_list_input("New property features: ", feature_pool)
                                        new_prop_dict = Property(new_property_id, new_location, new_p_type, new_price, new_features, new_tags, new_guest_capacity, new_unavailable_dates).to_dict()
                                        update_property(new_prop_dict)

                                    elif prop_edit_choice == "5":
                                        print("Please enter the new tags from the list below: ")
                                        print("If the property has multiple tags, please separate each tag by comma.")
                                        print(tag_pool)
                                        new_tags = get_string_list_input("New property tags: ", tag_pool)
                                        new_prop_dict = Property(new_property_id, new_location, new_p_type, new_price, new_features, new_tags, new_guest_capacity, new_unavailable_dates).to_dict()
                                        update_property(new_prop_dict)

                                    elif prop_edit_choice == "6":
                                        new_guest_capacity = get_int_input("New guest capacity (integer): ")
                                        new_prop_dict = Property(new_property_id, new_location, new_p_type, new_price, new_features, new_tags, new_guest_capacity, new_unavailable_dates).to_dict()
                                        update_property(new_prop_dict)
                                                
                                    elif prop_edit_choice == "7":
                                        print("Edit session completed!")
                                        break

                                    else:
                                        print("Invalid choice!")

                                else:
                                    print("Invalid index!")


                        elif choice_7 == "d":
                            while True:
                                pd.set_option("display.max_colwidth", 20)
                                properties_dict = view_properties()
                                properties_df = pd.DataFrame(properties_dict)
                                print(properties_df.drop(columns = "property_id"))
                                delete_prop_index = get_int_input("Enter the index of the property you want to delete: ")

                                if delete_prop_index in properties_df.index:
                                    delete_prop_id = properties_df.loc[delete_prop_index]["property_id"]
                                    delete_property(delete_prop_id)

                                else:
                                    print("Invalid index!")


                        elif choice_7 == "g":
                            n = get_int_input("Enter the number of properties you want to generate: ")
                            generate_properties(n)

                        elif choice_7 == "x":
                            print("Log out successfully!")
                            admin_logged_in = False

                        else:
                            print("Invalid choice!")

                elif choice_6 == "2":
                    print("Thanks for using!")
                    is_admin = False
                    app_status = False
                    
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
    