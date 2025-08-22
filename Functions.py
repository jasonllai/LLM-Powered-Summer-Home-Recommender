# Importing libraries
import uuid
import pandas as pd
from collections import UserString
import json
import datetime

# Classes
class Property:
    def __init__(self, property_id, location, p_type, price_per_night, features, tags, guest_capacity, unavailable_dates):
        self.property_id = property_id
        self.location = location
        self.p_type = p_type
        self.price_per_night = price_per_night
        self.features = features
        self.tags = tags
        self.guest_capacity = guest_capacity
        self.unavailable_dates = unavailable_dates

    def to_dict(self):
        return {
            "property_id": self.property_id,
            "location": self.location,
            "type": self.p_type,
            "price_per_night": self.price_per_night,
            "features": self.features,
            "tags": self.tags,
            "guest_capacity": self.guest_capacity,
            "unavailable_dates": self.unavailable_dates
        }

    @classmethod
    def from_dict(cls, d): 
         return cls(
                property_id=d.get("property_id"),
                location=d.get("location"),
                p_type=d.get("type"),
                price_per_night=d.get("price_per_night", 0),
                features=d.get("features", []),
                tags=d.get("tags", []),
                guest_capacity=d.get("guest_capacity", 0),
                unavailable_dates=d.get("unavailable_dates", [])
            )

class User:
    def __init__(self, user_id, name, password, booking_history, group_size, preferred_environment, budget_range):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.booking_history = booking_history if booking_history else []
        self.group_size = group_size
        self.preferred_environment = preferred_environment
        self.budget_range = budget_range

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "password": self.password,
            "booking_history": self.booking_history,
            "group_size": self.group_size,
            "preferred_environment": self.preferred_environment,
            "budget_range": self.budget_range,
        }

    @classmethod
    def from_dict(cls, d): 
        return cls(
            user_id=d.get("user_id"),
            name=d.get("name"),
            password=d.get("password"),
            booking_history=d.get("booking_history", []),
            group_size=d.get("group_size"),
            preferred_environment=d.get("preferred_environment"),
            budget_range=d.get("budget_range")
        )


class Admin:
    def __init__(self, admin_id, password):
        self.admin_id = admin_id
        self.password = password
    
    def to_dict(self):
        return {
            "admin_id": self.admin_id,
            "password": self.password
        }
    
    @classmethod
    def from_dict(cls, d):
        return cls(
            admin_id=d["admin_id"],
            password=d["password"]
        )
    
    def admin_display_profile(self):
        print(f"""
        Admin ID: {self.admin_id}
        Password: {self.password}
        """)
    

# Functions
def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_data_to_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def generate_property_id():
    return str(uuid.uuid4())

def property_display(file_path="data/Properties.json"):
    properties_data = load_data_from_json(file_path)

    if not properties_data:
        print("No properties found in the JSON file.")
        return None

    df = pd.DataFrame(properties_data).drop(columns=['property_id'], errors='ignore')

    print("Properties:")
    print(df)
    return df

def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def view_properties(index, file_path="data/Properties.json"):
    properties_data = load_data_from_json(file_path)
    df = pd.DataFrame(properties_data).drop(columns=['property_id'], errors='ignore')
    if df is not None:
        if 0 <= index < len(df):
            print( df.iloc[[index]] ) 
        else:
            print(f"No property found at index {index}")
            return None
    else:
        print("Failed to load properties.")
        return None


def add_properties(location, p_type, price_per_night, features, tags, guest_capacity, unavailable_dates):
    property_obj_list = [Property.from_dict(d) for d in load_data_from_json("data/Properties.json")]
    property_id = generate_property_id()

    new_property = Property(
        property_id, location, p_type, price_per_night,
        features, tags, guest_capacity, unavailable_dates
    )
    property_obj_list.append(new_property)
    properties_data = [p.to_dict() for p in property_obj_list]
    save_data_to_json("data/Properties.json", properties_data)
    print(f"Property added successfully!")
    return new_property


# Old version of add properties (ask user for input version)
# def add_properties():
#     property_obj_list = [Property.from_dict(d) for d in load_data_from_json("data/Properties.json")]
#     property_id = generate_property_id()
#     while True:
#         location = input("Enter location: ").strip()
#         if location:
#             break
#         print("Location cannot be empty")

#     while True:
#         p_type = input("Enter type: ").strip()
#         if p_type:
#             break
#         print("Type cannot be empty")

#     while True:
#         try:
#             v = float(input("Enter price per night (whole number): ").strip())
#             if v != int(v):
#                 print("Please enter a whole number")
#                 continue
#             price_per_night = int(v)
#             if price_per_night <= 0:
#                 print("Price must be positive")
#                 continue
#             break
#         except ValueError:
#             print("Please enter a whole number")

#     while True:
#         try:
#             guest_capacity = int(input("Enter guest capacity: ").strip())
#             if guest_capacity > 0:
#                 break
#             print("Guest capacity must be positive")
#         except ValueError:
#             print("Please enter a whole number")

#     print("Enter features (at least one). Press Enter on an empty line to finish.")
#     features = []
#     while True:
#         f = input("Add feature: ").strip().lower()
#         if not f:
#             if not features:
#                 print("Please enter at least one feature")
#                 continue
#             break
#         features.append(f)

#     print("Enter tags (at least one). Press Enter on an empty line to finish.")
#     tags = []
#     while True:
#         t = input("Add tag: ").strip().lower()
#         if not t:
#             if not tags:
#                 print("Please enter at least one tag")
#                 continue
#             break
#         tags.append(t)

#     print("Enter unavailable dates (YYYY-MM-DD). Press Enter on an empty line to finish.")
#     unavailable_dates = []
#     while True:
#         d = input("Date: ").strip()
#         if not d:
#             break
#         if validate_date(d):
#             unavailable_dates.append(d)
#         else:
#             print("Invalid format. Use YYYY-MM-DD")

#     new_property = Property(
#         property_id, location, p_type, price_per_night,
#         features, tags, guest_capacity, unavailable_dates
#     )
#     property_obj_list.append(new_property)
#     properties_data = [p.to_dict() for p in property_obj_list]
#     save_data_to_json("data/Properties.json", properties_data)
#     print(f"Property added successfully!")
#     return new_property



def delete_property(index, file_path="data/Properties.json"):
    df = property_display(file_path)
    if 0 <= index < len(df):
        df = df.drop(index).reset_index(drop=True)
        print(f"Property at index {index} deleted successfully!")

        updated_properties_data = df.to_dict(orient='records')

        save_data_to_json(file_path, updated_properties_data)
    else:
        print(f"No property found at index {index}")

    print(len(df))


def update_property(index, number, new_value, file_path="data/Properties.json"):
    properties_data = load_data_from_json(file_path)
    df = pd.DataFrame(properties_data)
    df_display = df.drop(columns=['property_id'], errors='ignore')
    
    if 0 <= index < len(df):
        if number == 1:
            df.at[index, 'location'] = new_value
            print("Location updated!")
        
        elif number == 2:
            df.at[index, 'type'] = new_value
            print("Type updated!")
        
        elif number == 3:
            if isinstance(new_value, (int, float)) and new_value > 0:
                df.at[index, 'price_per_night'] = int(new_value)
                print("Price updated!")
            else:
                print("Invalid price value. Must be a positive whole number.")
                return
        
        elif number == 4:
            if isinstance(new_value, list) and all(isinstance(f, str) for f in new_value):
                df.at[index, 'features'] = new_value
                print("Features updated!")
            else:
                print("Invalid features value. Must be a list of strings.")
                return
        
        elif number == 5:
            if isinstance(new_value, list) and all(isinstance(t, str) for t in new_value):
                df.at[index, 'tags'] = new_value
                print("Tags updated!")
            else:
                print("Invalid tags value. Must be a list of strings.")
                return
        
        elif number == 6:
            if isinstance(new_value, int) and new_value > 0:
                df.at[index, 'guest_capacity'] = new_value
                print("Guest capacity updated!")
            else:
                print("Invalid guest capacity value. Must be a positive integer.")
                return
        
        elif number == 7:
            if isinstance(new_value, list) and all(validate_date(d) for d in new_value):
                df.at[index, 'unavailable_dates'] = new_value
                print("Unavailable dates updated!")
            else:
                print("Invalid dates value. Must be a list of valid date strings (YYYY-MM-DD).")
                return
        
        else:
            print("Invalid number. Please enter a valid option.")
            return

        updated_properties_data = df.to_dict(orient='records')
        save_data_to_json(file_path, updated_properties_data)
        print("\nUpdated Property Details:")
        print(df_display.iloc[index])
    else:
        print(f"No property found at index {index}")


# Old version of update property (ask user for input version)
# def update_property(index, file_path="data/Properties.json"):
#     properties_data = load_data_from_json(file_path)
#     df = pd.DataFrame(properties_data)
#     df_display = df.drop(columns=['property_id'], errors='ignore')
#     if 0 <= index < len(df):
#         while True:
#             print(f"\n=== EDITING PROPERTY AT INDEX {index} ===")
#             print(df_display.iloc[index]) 
#             print("\nWhat would you like to edit?")
#             print("1. Location")
#             print("2. Type")
#             print("3. Price per Night")
#             print("4. Features")
#             print("5. Tags")
#             print("6. Guest Capacity")
#             print("7. Unavailable Dates")
#             print("8. Done (Exit)")

#             try:
#                 choice = int(input("Enter your choice (1-8): ").strip())
#                 if choice < 1 or choice > 8:
#                     print("Please enter a number between 1 and 8")
#                     continue
#             except ValueError:
#                 print("Please enter a number")
#                 continue

#             if choice == 8:
#                 print("Edit session completed")
#                 break

#             if choice == 1:
#                 new_loc = input("New location: ").strip()
#                 if new_loc:
#                     df.at[index, 'location'] = new_loc
#                     print("Location updated!")

#             elif choice == 2:
#                 new_type = input("New type: ").strip()
#                 if new_type:
#                     df.at[index, 'type'] = new_type
#                     print("Type updated!")

#             elif choice == 3:
#                 try:
#                     v = float(input("New price per night (whole number): ").strip())
#                     if v != int(v):
#                         print("Please enter a whole number")
#                         continue
#                     v = int(v)
#                     if v <= 0:
#                         print("Price must be positive")
#                         continue
#                     df.at[index, 'price_per_night'] = v
#                     print("Price updated!")
#                 except ValueError:
#                     print("Please enter a whole number")

#             elif choice == 4:
#                 print("Enter features (at least one). Press Enter with empty input to finish.")
#                 new_features = []
#                 while True:
#                     f = input("Add feature: ").strip().lower()
#                     if not f:
#                         if not new_features:
#                             print("Please enter at least one feature")
#                             continue
#                         break
#                     new_features.append(f)
#                 df.at[index, 'features'] = new_features
#                 print("Features updated!")

#             elif choice == 5:
#                 print("Enter tags (at least one). Press Enter with empty input to finish.")
#                 new_tags = []
#                 while True:
#                     t = input("Add tag: ").strip().lower()
#                     if not t:
#                         if not new_tags:
#                             print("Please enter at least one tag")
#                             continue
#                         break
#                     new_tags.append(t)
#                 df.at[index, 'tags'] = new_tags
#                 print("Tags updated!")

#             elif choice == 6:
#                 try:
#                     cap = int(input("New guest capacity: ").strip())
#                     if cap <= 0:
#                         print("Capacity must be positive")
#                         continue
#                     df.at[index, 'guest_capacity'] = cap
#                     print("Guest capacity updated!")
#                 except ValueError:
#                     print("Please enter a whole number")

#             elif choice == 7:
#                 print("Re-enter ALL unavailable dates (YYYY-MM-DD). Press Enter on an empty line to finish.")
#                 new_dates = []
#                 while True:
#                     d = input("Date: ").strip()
#                     if not d:
#                         break
#                     if validate_date(d):
#                         new_dates.append(d)
#                     else:
#                         print("Invalid format. Use YYYY-MM-DD")
#                 df.at[index, 'unavailable_dates'] = new_dates
#                 print("Unavailable dates updated!")

#         print("\nUpdated Property Details:")
#         print(df_display.iloc[index])

#         updated_properties_data = df.to_dict(orient='records')

#         save_data_to_json(file_path, updated_properties_data)
#     else:
#         print(f"No property found at index {index}")





def _find_property(property_id):
    property_obj_list = [Property.from_dict(d) for d in load_data_from_json("data/Properties.json")]
    for p in property_obj_list:
        if p.property_id == property_id:
            return p
    return None


# def create_booking_history(user_id, current_list, property_index, start_date, end_date, users_file_path="data/Users.json"):
#     print(f"\n=== Booking FOR USER {user_id} ===")
    
#     # Load users data from JSON
#     users_data = load_data_from_json(users_file_path)
    
#     # Find the user by user_id
#     user = next((u for u in users_data if u['user_id'] == user_id), None)
    
#     if not user:
#         print(f"No user found with ID {user_id}")
#         return None

#     # Convert properties_list to DataFrame
#     properties_df = pd.DataFrame(current_list)

#     # Debugging: Print DataFrame columns and head
#     print("DataFrame Columns:", properties_df.columns)
#     print("DataFrame Head:")
#     print(properties_df.head())

#     # Check if the property index is valid
#     if 0 <= property_index < len(properties_df):
#         prop = properties_df.iloc[property_index]
#     else:
#         print(f"No property found at index {property_index}")
#         return None

#     # Validate the start and end dates
#     if not validate_date(start_date):
#         print("Invalid start date format. Use YYYY-MM-DD")
#         return None

#     if not validate_date(end_date):
#         print("Invalid end date format. Use YYYY-MM-DD")
#         return None

#     if datetime.datetime.strptime(end_date, "%Y-%m-%d") <= datetime.datetime.strptime(start_date, "%Y-%m-%d"):
#         print("End date must be after start date")
#         return None

#     # Append the booking to the user's booking history
#     if 'booking_history' not in user:
#         user['booking_history'] = []
    
#     user['booking_history'].append({
#         "property_id": prop['property_id'],
#         "start_date": start_date,
#         "end_date": end_date
#     })

#     # Save the updated users data back to JSON
#     save_data_to_json(users_file_path, users_data)

#     print("Booking created successfully!")
#     print("Current bookings:", user['booking_history'])


# Book a property for a user if dates are available.
# Updates user's booking history and property's unavailable dates.
def create_booking(user_dict, property_dict,
                   start_date, end_date,
                   users_file_path="data/Users.json",
                   properties_file_path="data/Properties.json"):

    user_id = user_dict.get("user_id")
    property_id = property_dict.get("property_id")
    users = load_data_from_json(users_file_path)
    properties = load_data_from_json(properties_file_path)

    # Debugging: Print properties data
    print("Properties data loaded:", properties)

    # Debugging: Print properties data with index
    for idx, p in enumerate(properties):
        if 'property_id' not in p:
            print(f"Missing 'property_id' in property at index {idx}: {p}")
        else:
            print(f"Property at index {idx} has property_id: {p['property_id']}")

    user = next((u for u in users if u['user_id'] == user_id), None)
    prop = next((p for p in properties if p['property_id'] == property_id), None)

    if not user:
        print(f"No user found with ID {user_id}")
        return
    if not prop:
        print(f"No property found with ID {property_id}")
        return

    try:
        date_range = pd.date_range(start=start_date, end=end_date).strftime("%Y-%m-%d").tolist()
    except Exception as e:
        print(f"Invalid date input: {e}")
        return

    if any(date in prop['unavailable_dates'] for date in date_range):
        print(f"Property '{prop.get('property_type', property_id)}' is not available for the requested dates.")
        return

    prop['unavailable_dates'].extend(date_range)

    if 'booking_history' not in user:
        user['booking_history'] = []

    user['booking_history'].append({
        "property_id": property_id,
        "start_date": start_date,
        "end_date": end_date
    })

    for idx, p in enumerate(properties):
        if p['property_id'] == property_id:
            properties[idx] = prop
            break
    save_data_to_json(properties_file_path, properties)

    for idx, u in enumerate(users):
        if u['user_id'] == user_id:
            users[idx] = user
            break
    save_data_to_json(users_file_path, users)

    print(f"Booking successful!")
    print(f"User '{user.get('name', user_id)}' booked property '{prop.get('property_type', property_id)}' "
          f"from {start_date} to {end_date}.")
    print(f"Updated booking history for user: {user['booking_history']}")

user_dict = {
    "user_id": 1,
    "name": "Alice",
    "booking_history": [] 
}
property_dict = {
    "property_id": "b2c3d4e5-f6a7-4890-9123-4567890abcde",
    "name": "Downtown Apartment",
    "location": "Toronto",
    "price_per_night": 120,
    "unavailable_dates": ["2025-08-21", "2025-08-22"]
}
create_booking(user_dict, property_dict, '2021-01-01', '2021-01-02')

### Old version of create booking history (ask user for input version)
# def create_booking_history(user, users_obj_list, current_list):
#     print(f"\n=== Booking FOR USER {user.user_id} ===")
    
#     if not user:
#         print(f"No user found with ID {user.user_id}")
#         return None

#     while True:
#         try:
#             pid = int(input("Property ID to book: ").strip())
#             prop = _find_property(pid, current_list)
#             if prop:
#                 break
#             print("Property not found")
#         except ValueError:
#             print("Please enter a whole number")

#     while True:
#         start_date = input("Start date (YYYY-MM-DD): ").strip()
#         if not start_date:
#             print("Start date is required")
#             continue
#         if validate_date(start_date):
#             break
#         print("Invalid format. Use YYYY-MM-DD")

#     while True:
#         end_date = input("End date (YYYY-MM-DD): ").strip()
#         if not end_date:
#             print("End date is required")
#             continue
#         if validate_date(end_date):
#             if datetime.datetime.strptime(end_date, "%Y-%m-%d") <= datetime.datetime.strptime(start_date, "%Y-%m-%d"):
#                 print("End date must be after start date")
#                 continue
#             break
#         print("Invalid format. Use YYYY-MM-DD")

#     user.booking_history.append({
#         "property_id": prop.property_id,
#         "start_date": start_date,
#         "end_date": end_date
#     })

#     for i, u in enumerate(users_obj_list):
#         if u.user_id == user.user_id:
#             users_obj_list[i] = user
#             break

#     print("Booking created successfully!")
#     print("Current bookings:", user.booking_history)


def delete_booking(user_id, booking_index, users_file_path="data/Users.json"):
    users_data = load_data_from_json(users_file_path)
    user = next((u for u in users_data if u['user_id'] == user_id), None)
    
    if not user:
        print(f"No user found with ID {user_id}")
        return None

    if not user.get('booking_history'):
        print("No booking to delete")
        return None

    if 1 <= booking_index <= len(user['booking_history']):
        removed = user['booking_history'].pop(booking_index - 1)
        print(f"Booking {booking_index} deleted")
    else:
        print(f"Invalid booking index. Please enter a number between 1 and {len(user['booking_history'])}")
        return None

    save_data_to_json(users_file_path, users_data)

# Old version of delete booking (ask user for input version)
# def delete_booking(user, users_obj_list):
#     if not user:
#         print(f"No user found with ID {user.user_id}")
#         return None
#     if not user.booking_history:
#         print("No booking to delete")
#         return None

#     print("\nYour bookings:")
#     for i, b in enumerate(user.booking_history, 1):
#         print(f"{i}. Booking {i}:  Property {b['property_id']} | from {b['start_date']} to {b['end_date']}")

#     while True:
#         try:
#             idx_f = float(input("Enter booking index to delete: ").strip())
#             if idx_f != int(idx_f):
#                 print("Please enter a whole number")
#                 continue
#             idx = int(idx_f)
#             if 1 <= idx <= len(user.booking_history):
#                 break
#             print(f"Please enter a number between 1 and {len(user.booking_history)}")
#         except ValueError:
#             print("Please enter a whole number")

#     confirm = input(f"Delete booking {idx} (yes/no)? ").strip().lower()
#     if confirm != "yes":
#         print("Cancelled")
#         return None

#     if idx < 1 or idx > len(user.booking_history):
#         print("That booking no longer exists")
#         return None

#     try:
#         removed = user.booking_history.pop(idx - 1)
#     except IndexError:
#         print("That booking no longer exists")
#         return None

#     for i, u in enumerate(users_obj_list):
#         if u.user_id == user.user_id:
#             users_obj_list[i] = user
#             break

#     print(f"Booking {idx} deleted")



def create_user_profile(name, password, group_size, preferred_environment, budget_range, file_path="data/Users.json"):
    users_obj_list = [User.from_dict(d) for d in load_data_from_json(file_path)]
    
    print("\n=== CREATE NEW PROFILE ===")
    user_id = len(users_obj_list) + 1

    new_user = User(user_id, name, password, [], group_size,preferred_environment, budget_range)
    users_obj_list.append(new_user)

    # Save the updated users list back to JSON
    users_data = [u.to_dict() for u in users_obj_list]
    save_data_to_json(file_path, users_data)

    users_data = [u.to_dict() for u in users_obj_list]
    save_data_to_json(file_path, users_data)

    print(f"Profile created successfully! User ID: {user_id}")
    return new_user


# Old version of create user profile (ask user for input version)
# def create_user_profile(file_path="data/Users.json"):
#     users_obj_list = [User.from_dict(d) for d in load_data_from_json("data/Users.json")]
    
#     print("\n=== CREATE NEW PROFILE ===")
#     user_id = len(users_obj_list) + 1

#     while True:
#         name = input("Full Name: ").strip()
#         if name: break
#         print("Name cannot be empty")

#     while True:
#         password = input("Password: ").strip()
#         if password: break
#         print("Password cannot be empty")
    
#     while True:
#         try:
#             group_size = int(input("Group Size: "))
#             if group_size > 0: break
#             print("Must be positive number")
#         except ValueError:
#             print("Please enter a whole number")
            
#     while True:
#         try:
#             min_budget = float(input("Minimum Budget ($) - whole number only: "))
#             if min_budget != int(min_budget):
#                 print("Please enter a whole number (no decimals)")
#                 continue
#             min_budget = int(min_budget)
#             if min_budget <= 0:
#                 print("Minimum budget must be positive")
#                 continue
#             break
#         except ValueError:
#             print("Please enter a whole number")

#     while True:
#         try:
#             max_budget = float(input("Maximum Budget ($) - whole number only: "))
#             if max_budget != int(max_budget):
#                 print("Please enter a whole number (no decimals)")
#                 continue
#             max_budget = int(max_budget)
#             if max_budget <= 0:
#                 print("Maximum budget must be positive")
#                 continue
#             if max_budget < min_budget:
#                 print("Maximum budget must be greater than or equal to minimum budget")
#                 continue
#             break
#         except ValueError:
#             print("Please enter a whole number")

#     budget_range = (min_budget, max_budget)

#     while True:
#         preferred_environment = input("Preferred Environment: ").strip()
#         if preferred_environment: break
#         print("Preferred environment cannot be empty")

#     new_user = User(user_id, name, group_size,password, [], preferred_environment, budget_range)
#     users_obj_list.append(new_user)

#     users_data = [u.to_dict() for u in users_obj_list]
#     save_data_to_json(file_path, users_data)

#     print(f"Profile created successfully! User ID: {user_id}")
#     return new_user



def user_display_profile(user):
    user_data = {
        "User ID": [user.user_id],
        "Name": [user.name],
        "Group Size": [user.group_size],
        "Password": [user.password],
        "Preferred Environment": [user.preferred_environment],
        "Budget Range": [user.budget_range]
    }
    
    df = pd.DataFrame(user_data)
    
    print("User Profile:")
    print(df)

    if user.booking_history:
        print("\nBooking History:")
        booking_df = pd.DataFrame(user.booking_history)
        print(booking_df)
    else:
        print("\nNo booking history available.")

def view_user_profile(user_id, file_path="data/Users.json"):
    users_data = load_data_from_json(file_path)
    user = next((u for u in users_data if u['user_id'] == user_id), None)
    if user:
        user_display_profile(user)
    else:
        print(f"No user found with ID {user_id}")


def delete_profile(user_id):
    users_obj_list = [User.from_dict(d) for d in load_data_from_json("data/Users.json")]
    for i, user in enumerate(users_obj_list):
        if user.user_id == user_id:
            users_obj_list.pop(i)
            print(f"Deleted user ID {user_id}")
            users_data = [u.to_dict() for u in users_obj_list]
            save_data_to_json("data/Users.json", users_data)
            return
    print(f"No user found with ID {user_id}")


def edit_user_profile(user_id, choice, new_value=None, users_file_path="data/Users.json"):
    users_obj_list = [User.from_dict(d) for d in load_data_from_json(users_file_path)]
    user = next((u for u in users_obj_list if u.user_id == user_id), None)
    if not user:
        print(f"No user found with ID {user_id}")
        return None

    print(f"\n=== EDITING PROFILE FOR USER {user_id} ===")
    print("Current profile:")
    user_display_profile(user)

    if choice == 1:
        if new_value:
            user.name = new_value
            print("Name updated successfully!")
        else:
            print("New name cannot be empty")

    elif choice == 2:
        if new_value:
            user.password = new_value
            print("Password updated successfully!")
        else:
            print("New password cannot be empty")

    elif choice == 3:
        create_booking_history(user, users_obj_list)

    elif choice == 4:
        delete_booking(user, users_obj_list)

    elif choice == 5:
        if isinstance(new_value, int) and new_value > 0:
            user.group_size = new_value
            print("Group size updated successfully!")
        else:
            print("Invalid group size. Must be a positive integer.")

    elif choice == 6:
        if new_value:
            user.preferred_environment = new_value
            print("Preferred environment updated successfully!")
        else:
            print("Preferred environment cannot be empty")

    elif choice == 7:
        if isinstance(new_value, tuple) and len(new_value) == 2:
            min_budget, max_budget = new_value
            if min_budget > 0 and max_budget >= min_budget:
                user.budget_range = new_value
                print("Budget range updated successfully!")
            else:
                print("Invalid budget range. Ensure min budget is positive and max budget is greater than or equal to min budget.")
        else:
            print("Invalid budget range. Must be a tuple with two values.")
    else:
        print("Invalid choice")
        return None

    for i, u in enumerate(users_obj_list):
        if u.user_id == user.user_id:
            users_obj_list[i] = user
            break

    users_data = [u.to_dict() for u in users_obj_list]
    save_data_to_json(users_file_path, users_data)

    print("\nUpdated profile:")
    user_display_profile(user)



# Old version of edit user profile (ask user for input version)
# def edit_user_profile(user_id):
#     users_obj_list = [User.from_dict(d) for d in load_data_from_json("data/Users.json")]
#     user = next((u for u in users_obj_list if u.user_id == user_id), None)
#     if not user:
#         print(f"No user found with ID {user_id}")
#         return None

#     while True:
#         print(f"\n=== EDITING PROFILE FOR USER {user_id} ===")
#         print("Current profile:")
#         user_display_profile()

#         print("\nWhat would you like to edit?")
#         print("1. Name")
#         print("2. Password")
#         print("3. Create Booking")
#         print("4. Delete Booking")
#         print("5. Done (Exit)")

#         try:
#             choice = int(input("Enter your choice (1-5): ").strip())
#             if choice < 1 or choice > 5:
#                 print("Please enter a number between 1 and 5")
#                 continue
#         except ValueError:
#             print("Please enter a number")
#             continue

#         if choice == 5:
#             print("Edit session completed")
#             break

#         if choice == 1:
#             while True:
#                 new_name = input("New name: ").strip()
#                 if new_name:
#                     user.name = new_name
#                     print("Name updated successfully!")
#                     break
#                 print("Name cannot be empty")

#         elif choice == 2:
#             while True:
#                 new_pw = input("New password: ").strip()
#                 if new_pw:
#                     user.password = new_pw
#                     print("Password updated successfully!")
#                     break
#                 print("Password cannot be empty")

#         elif choice == 3:
#             create_booking_history(user, users_obj_list)

#         elif choice == 4:
#             delete_booking(user, users_obj_list)

#         for i, u in enumerate(users_obj_list):
#             if u.user_id == user.user_id:
#                 users_obj_list[i] = user
#                 break

#         users_data = [u.to_dict() for u in users_obj_list]
#         save_data_to_json("data/Users.json", users_data)
#         print("\nUpdated profile:")
#         user.user_display_profile()




