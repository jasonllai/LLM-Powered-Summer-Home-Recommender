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


def add_properties(location, p_type, price_per_night, features, tags, guest_capacity):
    property_obj_list = [Property.from_dict(d) for d in load_data_from_json("data/Properties.json")]
    property_id = generate_property_id()

    new_property = Property(
        property_id, location, p_type, price_per_night,
        features, tags, guest_capacity, []
    )
    property_obj_list.append(new_property)
    properties_data = [p.to_dict() for p in property_obj_list]
    save_data_to_json("data/Properties.json", properties_data)
    print(f"Property added successfully!")
    return new_property


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


# takes a new property in dictionary format, update the property in the json file
def update_property(new_property, file_path="data/Properties.json"):
    properties_data = load_data_from_json(file_path)
    for idx, p in enumerate(properties_data):
        if p['property_id'] == new_property.property_id:
            properties_data[idx] = new_property
            break
    save_data_to_json(file_path, properties_data)
    print(f"Property updated successfully!")


def create_booking(user_dict, property_dict,
                   start_date, end_date,
                   users_file_path="data/Users.json",
                   properties_file_path="data/Properties.json"):

    user_id = user_dict.get("user_id")
    property_id = property_dict.get("property_id")
    users = load_data_from_json(users_file_path)
    properties = load_data_from_json(properties_file_path)

    user = next((u for u in users if u['user_id'] == user_id), None)
    prop = next((p for p in properties if p['property_id'] == property_id), None)

    try:
        date_range = pd.date_range(start=start_date, end=end_date).strftime("%Y-%m-%d").tolist()
    except Exception as e:
        print(f"Invalid date input: {e}")
        return

    if any(date in prop['unavailable_dates'] for date in date_range):
        print(f"Property '{prop.get('property_type', property_id)}' is not available for the requested dates.")
        return

    prop['unavailable_dates'].extend(date_range)

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
    "user_id": "alice",
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
create_booking(user_dict, property_dict, '2025-08-21', '2025-08-22')


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


def create_user_profile(username, name, password, group_size, preferred_environment, budget_range, file_path="data/Users.json"):
    users_obj_list = [User.from_dict(d) for d in load_data_from_json(file_path)]
    
    print("\n=== CREATE NEW PROFILE ===")
    while True:
        try:
            usernames = {user.user_id for user in users_obj_list}
            if username not in usernames: break
        except ValueError:
            print("Username used by others, please enter a new username")
    user_id = username

    new_user = User(user_id, name, password, [], group_size,preferred_environment, budget_range)
    users_obj_list.append(new_user)

    # Save the updated users list back to JSON
    users_data = [u.to_dict() for u in users_obj_list]
    save_data_to_json(file_path, users_data)

    print(f"Profile created successfully! User ID: {user_id}")
    return new_user


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

