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

    def property_display(self):
        print(f"""
        Property ID: {self.property_id} 
        Property Location: {self.location}
        Property Type: {self.type}
        Price per Night: {self.price_per_night}
        Features: {self.features}
        Tags: {self.tags}
        Guest Capacity: {self.guest_capacity}
        Unavailable Dates: {self.unavailable_dates}""")

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
            property_id=d["property_id"],
            location=d["location"],  
            p_type=d["type"],        
            price_per_night=d["price_per_night"],
            features=d["features"],
            tags=d["tags"],
            guest_capacity=d["guest_capacity"],
            unavailable_dates=d["unavailable_dates"]    
        )

class User:
    def __init__(self, user_id, name, password, booking_history):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.booking_history = booking_history if booking_history else []
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "password": self.password,
            "booking_history": self.booking_history
        }
    
    @classmethod
    def from_dict(cls, d): 
        return cls(
            user_id=d["user_id"],
            name=d["name"],
            password=d["password"],
            booking_history=d.get("booking_history", [])
        )

    def user_display_profile(self):
        print(f"""
        User ID: {self.user_id}
        Name: {self.name}
        Password: {self.password}
        Booking History:""")

        if not self.booking_history:
            print("    No booking yet")
        col_widths = {
            "index": 5,
            "property_id": 15,
            "start_date": 12,
            "end_date": 12
        }

        # Calculate the starting position for booking details
        indent = " " * 4  # Adjust this to match the indentation of the password line

        # Print header with consistent indentation
        print(f"{indent}{'Index':<{col_widths['index']}} {'Property ID':<{col_widths['property_id']}} "
              f"{'Start Date':<{col_widths['start_date']}} {'End Date':<{col_widths['end_date']}}")

        # Print each booking with consistent indentation
        for i, booking in enumerate(self.booking_history, 1):
            print(f"{indent}{i:<{col_widths['index']}} {booking['property_id']:<{col_widths['property_id']}} "
                  f"{booking['start_date']:<{col_widths['start_date']}} {booking['end_date']:<{col_widths['end_date']}}")


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
from collections import UserString
import json
def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_data_to_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


import datetime
def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def view_properties(property_id):
    property_obj_list = [Property.from_dict(d) for d in load_data_from_json("data/Properties.json")]

    for property in property_obj_list:
        if property.property_id == property_id:
            property.property_display()
            return property
    print(f"No property found with ID {property_id}")
    return None


def add_properties():
    property_obj_list = [Property.from_dict(d) for d in load_data_from_json("data/Properties.json")]
    property_id = len(property_obj_list) + 1

    while True:
        location = input("Enter location: ").strip()
        if location:
            break
        print("Location cannot be empty")

    while True:
        p_type = input("Enter type: ").strip()
        if p_type:
            break
        print("Type cannot be empty")

    while True:
        try:
            v = float(input("Enter price per night (whole number): ").strip())
            if v != int(v):
                print("Please enter a whole number")
                continue
            price_per_night = int(v)
            if price_per_night <= 0:
                print("Price must be positive")
                continue
            break
        except ValueError:
            print("Please enter a whole number")

    while True:
        try:
            guest_capacity = int(input("Enter guest capacity: ").strip())
            if guest_capacity > 0:
                break
            print("Guest capacity must be positive")
        except ValueError:
            print("Please enter a whole number")

    print("Enter features (at least one). Press Enter on an empty line to finish.")
    features = []
    while True:
        f = input("Add feature: ").strip().lower()
        if not f:
            if not features:
                print("Please enter at least one feature")
                continue
            break
        features.append(f)

    print("Enter tags (at least one). Press Enter on an empty line to finish.")
    tags = []
    while True:
        t = input("Add tag: ").strip().lower()
        if not t:
            if not tags:
                print("Please enter at least one tag")
                continue
            break
        tags.append(t)

    print("Enter unavailable dates (YYYY-MM-DD). Press Enter on an empty line to finish.")
    unavailable_dates = []
    while True:
        d = input("Date: ").strip()
        if not d:
            break
        if validate_date(d):
            unavailable_dates.append(d)
        else:
            print("Invalid format. Use YYYY-MM-DD")

    new_property = Property(
        property_id, location, p_type, price_per_night,
        features, tags, guest_capacity, unavailable_dates
    )
    property_obj_list.append(new_property)
    properties_data = [p.to_dict() for p in property_obj_list]
    save_data_to_json("data/Properties.json", properties_data)
    print(f"Property added successfully! Property ID: {property_id}")
    return new_property



def delete_properties(property_id):
    property_obj_list = [Property.from_dict(d) for d in load_data_from_json("data/Properties.json")]
    for i, property in enumerate(property_obj_list):
        if property.property_id == property_id:
            property_obj_list.pop(i)
            print(f"Property deleted successfully! Property ID: {property_id}")
            
    properties_data = [p.to_dict() for p in property_obj_list]
    save_data_to_json("data/Properties.json", properties_data)
    print(f"No property found with ID {property_id}")
    return


def update_property(property_id):
    property_obj_list = [Property.from_dict(d) for d in load_data_from_json("data/Properties.json")]
    target = None
    for p in property_obj_list:
        if p.property_id == property_id:
            target = p
            break
    if not target:
        print(f"No property found with ID {property_id}")
        return None

    while True:
        print(f"\n=== EDITING PROPERTY {property_id} ===")
        target.property_display()
        print("\nWhat would you like to edit?")
        print("1. Location")
        print("2. Type")
        print("3. Price per Night")
        print("4. Features")
        print("5. Tags")
        print("6. Guest Capacity")
        print("7. Unavailable Dates")
        print("8. Done (Exit)")

        try:
            choice = int(input("Enter your choice (1-8): ").strip())
            if choice < 1 or choice > 8:
                print("Please enter a number between 1 and 8")
                continue
        except ValueError:
            print("Please enter a number")
            continue

        if choice == 8:
            print("Edit session completed")
            break

        if choice == 1:
            while True:
                new_loc = input("New location: ").strip()
                if new_loc:
                    target.location = new_loc
                    print("Location updated!")
                    break
                print("Location cannot be empty")

        elif choice == 2:
            while True:
                new_type = input("New type: ").strip()
                if new_type:
                    target.type = new_type
                    print("Type updated!")
                    break
                print("Type cannot be empty")

        elif choice == 3:
            while True:
                try:
                    v = float(input("New price per night (whole number): ").strip())
                    if v != int(v):
                        print("Please enter a whole number")
                        continue
                    v = int(v)
                    if v <= 0:
                        print("Price must be positive")
                        continue
                    target.price_per_night = v
                    print("Price updated!")
                    break
                except ValueError:
                    print("Please enter a whole number")

        elif choice == 4:
            print("Enter features (at least one). Press Enter with empty input to finish.")
            new_features = []
            while True:
                f = input("Add feature: ").strip().lower()
                if not f:
                    if not new_features:
                        print("Please enter at least one feature")
                        continue
                    break
                new_features.append(f)
            target.features = new_features
            print("Features updated!")

        elif choice == 5:
            print("Enter tags (at least one). Press Enter with empty input to finish.")
            new_tags = []
            while True:
                t = input("Add tag: ").strip().lower()
                if not t:
                    if not new_tags:
                        print("Please enter at least one tag")
                        continue
                    break
                new_tags.append(t)
            target.tags = new_tags
            print("Tags updated!")

        elif choice == 6:
            while True:
                try:
                    cap = int(input("New guest capacity: ").strip())
                    if cap <= 0:
                        print("Capacity must be positive")
                        continue
                    target.guest_capacity = cap
                    print("Guest capacity updated!")
                    break
                except ValueError:
                    print("Please enter a whole number")

        elif choice == 7:
            print("Re-enter ALL unavailable dates (YYYY-MM-DD). Press Enter on an empty line to finish.")
            new_dates = []
            while True:
                d = input("Date: ").strip()
                if not d:
                    break
                if validate_date(d):
                    new_dates.append(d)
                else:
                    print("Invalid format. Use YYYY-MM-DD")
            target.unavailable_dates = new_dates
            print("Unavailable dates updated!")

        print("\nUpdated property:")
        target.property_display()
    properties_data = [p.to_dict() for p in property_obj_list]
    save_data_to_json("data/Properties.json", properties_data)
    return target

def _find_user(user_id):
    users_obj_list = [User.from_dict(d) for d in load_data_from_json("data/Users.json")]
    for u in users_obj_list:
        if u.user_id == user_id:
            return u
    return None

def _find_property(property_id):
    property_obj_list = [Property.from_dict(d) for d in load_data_from_json("data/Properties.json")]
    for p in property_obj_list:
        if p.property_id == property_id:
            return p
    return None


def create_booking_history(user, users_obj_list):
    print(f"\n=== Booking FOR USER {user.user_id} ===")
    
    if not user:
        print(f"No user found with ID {user.user_id}")
        return None

    while True:
        try:
            pid = int(input("Property ID to book: ").strip())
            prop = _find_property(pid)
            if prop:
                break
            print("Property not found")
        except ValueError:
            print("Please enter a whole number")

    while True:
        start_date = input("Start date (YYYY-MM-DD): ").strip()
        if not start_date:
            print("Start date is required")
            continue
        if validate_date(start_date):
            break
        print("Invalid format. Use YYYY-MM-DD")

    while True:
        end_date = input("End date (YYYY-MM-DD): ").strip()
        if not end_date:
            print("End date is required")
            continue
        if validate_date(end_date):
            if datetime.datetime.strptime(end_date, "%Y-%m-%d") <= datetime.datetime.strptime(start_date, "%Y-%m-%d"):
                print("End date must be after start date")
                continue
            break
        print("Invalid format. Use YYYY-MM-DD")

    user.booking_history.append({
        "property_id": prop.property_id,
        "start_date": start_date,
        "end_date": end_date
    })

    for i, u in enumerate(users_obj_list):
        if u.user_id == user.user_id:
            users_obj_list[i] = user
            break

    print("Booking created successfully!")
    print("Current bookings:", user.booking_history)



def delete_booking(user, users_obj_list):
    if not user:
        print(f"No user found with ID {user.user_id}")
        return None
    if not user.booking_history:
        print("No booking to delete")
        return None

    print("\nYour bookings:")
    for i, b in enumerate(user.booking_history, 1):
        print(f"{i}. Booking {i}:  Property {b['property_id']} | from {b['start_date']} to {b['end_date']}")

    while True:
        try:
            idx_f = float(input("Enter booking index to delete: ").strip())
            if idx_f != int(idx_f):
                print("Please enter a whole number")
                continue
            idx = int(idx_f)
            if 1 <= idx <= len(user.booking_history):
                break
            print(f"Please enter a number between 1 and {len(user.booking_history)}")
        except ValueError:
            print("Please enter a whole number")

    confirm = input(f"Delete booking {idx} (yes/no)? ").strip().lower()
    if confirm != "yes":
        print("Cancelled")
        return None

    # final existence check (protects against list changing)
    if idx < 1 or idx > len(user.booking_history):
        print("That booking no longer exists")
        return None

    try:
        removed = user.booking_history.pop(idx - 1)
    except IndexError:
        print("That booking no longer exists")
        return None

    for i, u in enumerate(users_obj_list):
        if u.user_id == user.user_id:
            users_obj_list[i] = user
            break

    print(f"Booking {idx} deleted")



def create_user_profile():
    users_obj_list = []
    print("\n=== CREATE NEW PROFILE ===")
    user_id = len(users_obj_list) + 1
    
    while True:
        name = input("Full Name: ").strip()
        if name: break
        print("Name cannot be empty")
    
    while True:
        password = input("Password: ").strip()
        if password: break
        print("Password cannot be empty")
    
    new_user = User(user_id, name, password, [])
    users_obj_list.append(new_user)
    print(f"\nProfile created successfully! User ID: {user_id}")
    users_data = [u.to_dict() for u in users_obj_list]
    save_data_to_json("data/Users.json", users_data)
    return new_user


def view_user_profile(user_id):
    users_obj_list = [User.from_dict(d) for d in load_data_from_json("data/Users.json")]
    for user in users_obj_list:
        if user.user_id == user_id:
            user.user_display_profile()
            return user
    print(f"No user found with ID {user_id}")
    return None

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


def edit_user_profile(user_id):
    users_obj_list = [User.from_dict(d) for d in load_data_from_json("data/Users.json")]
    user = next((u for u in users_obj_list if u.user_id == user_id), None)
    if not user:
        print(f"No user found with ID {user_id}")
        return None

    while True:
        print(f"\n=== EDITING PROFILE FOR USER {user_id} ===")
        print("Current profile:")
        user.user_display_profile()

        print("\nWhat would you like to edit?")
        print("1. Name")
        print("2. Password")
        print("3. Create Booking")
        print("4. Delete Booking")
        print("5. Done (Exit)")

        try:
            choice = int(input("Enter your choice (1-5): ").strip())
            if choice < 1 or choice > 5:
                print("Please enter a number between 1 and 5")
                continue
        except ValueError:
            print("Please enter a number")
            continue

        if choice == 5:
            print("Edit session completed")
            break

        if choice == 1:
            while True:
                new_name = input("New name: ").strip()
                if new_name:
                    user.name = new_name
                    print("Name updated successfully!")
                    break
                print("Name cannot be empty")

        elif choice == 2:
            while True:
                new_pw = input("New password: ").strip()
                if new_pw:
                    user.password = new_pw
                    print("Password updated successfully!")
                    break
                print("Password cannot be empty")

        elif choice == 3:
            create_booking_history(user, users_obj_list)

        elif choice == 4:
            delete_booking(user, users_obj_list)

        for i, u in enumerate(users_obj_list):
            if u.user_id == user.user_id:
                users_obj_list[i] = user
                break

        users_data = [u.to_dict() for u in users_obj_list]
        save_data_to_json("data/Users.json", users_data)
        print("\nUpdated profile:")
        user.user_display_profile()

view_user_profile(1)
edit_user_profile(1)
view_user_profile(1)



