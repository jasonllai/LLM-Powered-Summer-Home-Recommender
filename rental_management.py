import uuid
import json
import datetime
import pandas as pd


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
    

# Utility Functions
def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_data_to_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def generate_property_id():
    return str(uuid.uuid4())


def validate_date(date_str):
    try:
        dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%Y-%m-%d') == date_str  # enforce zero-padding
    except ValueError:
        return False



# Functions for Admin and User

# return all properties in the json file
def view_properties(file_path="data/Properties.json"):
    properties_data = load_data_from_json(file_path)
    if not properties_data:
        print("No properties found in the JSON file.")
        return None
    return properties_data


# return all users in the json file
def view_users(file_path="data/Users.json"):
    users_data = load_data_from_json(file_path)
    if not users_data:
        print("No users found in the JSON file.")
        return None
    return users_data

# takes new property's location, type, price, features, tags, guest capacity, and add to the json file
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


# takes property id, delete the property with the id from the json file, 
# also the booking history of the property from all users
def delete_property(prop_id, file_path="data/Properties.json", users_file_path="data/Users.json"):
    properties_data = load_data_from_json(file_path)
    users_data = load_data_from_json(users_file_path)

    # Remove the property
    new_properties = [p for p in properties_data if p.get('property_id') != prop_id]
    if len(new_properties) == len(properties_data):
        print(f"No property found with ID {prop_id}")
        return

    # Remove bookings referencing this property across all users
    updated_users = False
    for u in users_data:
        bookings = u.get('booking_history', [])
        new_bookings = [b for b in bookings if b.get('property_id') != prop_id]
        if len(new_bookings) != len(bookings):
            u['booking_history'] = new_bookings
            updated_users = True

    save_data_to_json(file_path, new_properties)
    if updated_users:
        save_data_to_json(users_file_path, users_data)

    print("Property deleted successfully!")
    


# takes a new property in dictionary format, update the property in the json file
def update_property(new_property, file_path="data/Properties.json"):
    properties_data = load_data_from_json(file_path)
    updated_property = False
    for idx, p in enumerate(properties_data):
        if p['property_id'] == new_property['property_id']:
            properties_data[idx] = new_property
            updated_property = True
            break
    if updated_property:
        save_data_to_json(file_path, properties_data)
        print(f"Property updated successfully!")
    else:
        print(f"No property found with ID {new_property['property_id']}")
    

# create a new user profile with username, name, password, group_size, preferred_environment, budget_range
def create_user_profile(username, name, password, group_size, preferred_environment, budget_range, file_path="data/Users.json"):
    users_obj_list = [User.from_dict(d) for d in load_data_from_json(file_path)]
    
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



# return a user's profile in dictionary format
def view_user_profile(user_id, file_path="data/Users.json"):
    users_data = load_data_from_json(file_path)
    user = next((u for u in users_data if u['user_id'] == user_id), None)
    if user:
        return user
    else:
        print(f"No user found with ID {user_id}")


# delete a user profile with user id, also delete the booking of property by the user
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
    


# edit a user's profile with a new user in dictionary format
def edit_user_profile(new_user, users_file_path="data/Users.json"):
    users_data = load_data_from_json(users_file_path)
    user = next((u for u in users_data if u.get('user_id') == new_user.get('user_id')), None)
    if not user:
        print(f"No user found with ID {new_user.get('user_id')}")
        return

    # Update only provided fields
    for key in ('name', 'password', 'group_size', 'preferred_environment', 'budget_range'):
        if key in new_user and new_user[key] is not None:
            user[key] = new_user[key]

    save_data_to_json(users_file_path, users_data)
    print("User profile updated successfully!")



# create a booking for a user with a property, and add the booking to the user's booking history
def create_booking(user_id, property_id,
                   start_date, end_date,
                   users_file_path="data/Users.json",
                   properties_file_path="data/Properties.json"):

    # Validate dates
    if not validate_date(start_date) or not validate_date(end_date):
        print("Invalid date format. Use YYYY-MM-DD.")
        return False

    # Load data
    users = load_data_from_json(users_file_path)
    properties = load_data_from_json(properties_file_path)

    # Find user and property
    user = next((u for u in users if u.get('user_id') == user_id), None)
    prop = next((p for p in properties if p.get('property_id') == property_id), None)

    if not user:
        print(f"No user found with ID {user_id}")
        return False
    if not prop:
        print(f"No property found with ID {property_id}")
        return False

    # Build inclusive date range as ISO strings
    try:
        date_range = pd.date_range(start=start_date, end=end_date).strftime("%Y-%m-%d").tolist()
    except Exception as e:
        print(f"Invalid date input: {e}")
        return False

    # Check availability
    existing = set(prop.get('unavailable_dates', []))
    conflict = existing.intersection(date_range)
    if conflict:
        print("Property is not available for the requested dates.")
        return False

    # Update property unavailable dates
    prop['unavailable_dates'] = sorted(existing.union(date_range))

    # Update user's booking history
    user['booking_history'].append({
        "property_id": property_id,
        "start_date": start_date,
        "end_date": end_date
    })

    # Persist updates
    for idx, p in enumerate(properties):
        if p.get('property_id') == property_id:
            properties[idx] = prop
            break
    save_data_to_json(properties_file_path, properties)

    for idx, u in enumerate(users):
        if u.get('user_id') == user_id:
            users[idx] = user
            break
    save_data_to_json(users_file_path, users)

    print("Booking successful!")
    print(f"User '{user.get('name', user_id)}' booked property '{prop.get('type', property_id)}' "
          f"from {start_date} to {end_date}.")
    return True



# delete a booking for a user with a property, and remove the booking from the user's booking history
def delete_booking(user_id, property_id, start_date, end_date,
                   users_file_path="data/Users.json",
                   properties_file_path="data/Properties.json"):
    # Validate dates
    if not validate_date(start_date) or not validate_date(end_date):
        print("Invalid date format. Use YYYY-MM-DD.")
        return
    
    # Load data
    users = load_data_from_json(users_file_path)
    properties = load_data_from_json(properties_file_path)

    # Find user and property
    user = next((u for u in users if u.get('user_id') == user_id), None)
    if not user:
        print(f"No user found with ID {user_id}")
        return
    prop = next((p for p in properties if p.get('property_id') == property_id), None)
    if not prop:
        print(f"No property found with ID {property_id}")
        return

    # Locate the exact booking
    bookings = user.get('booking_history', [])
    idx = next((i for i, b in enumerate(bookings)
                if b.get('property_id') == property_id
                and b.get('start_date') == start_date
                and b.get('end_date') == end_date), None)
    if idx is None:
        print("Booking not found for given user/property/dates.")
        return

    # Remove the booking from the user
    bookings.pop(idx)

    # Recompute property's unavailable_dates from ALL users' bookings for this property
    all_dates = set()
    for u in users:
        for b in u.get('booking_history', []):
            if b.get('property_id') == property_id:
                try:
                    dr = pd.date_range(start=b['start_date'], end=b['end_date']).strftime("%Y-%m-%d").tolist()
                    all_dates.update(dr)
                except Exception:
                    pass
    prop['unavailable_dates'] = sorted(all_dates)

    # Persist updates
    for i, u in enumerate(users):
        if u.get('user_id') == user_id:
            users[i] = user
            break
    save_data_to_json(users_file_path, users)

    for i, p in enumerate(properties):
        if p.get('property_id') == property_id:
            properties[i] = prop
            break
    save_data_to_json(properties_file_path, properties)

    print("Booking deleted successfully.")