# Lists for testing
listing_1 = {
    "property_id": 1,
    "location": "Blue Mountain, Ontario","type": "cabin",
    "price_per_night": 140,
    "features": ["mountain view", "fireplace", "ski-in/ski-out", "wifi"],
    "tags": ["mountains", "remote", "adventure"],
    "guest_capacity": 4,
    'unavailable_dates': ['2025-08-15', '2025-08-20', '2025-10-21', '2025-10-22', '2025-10-23']
    }

listing_2 = {
    "property_id": 2,
    "location": "103 Ocean Street West",
    "type" : "Apartment",
    "price_per_night": 65,
    "features" : ["furnished", "on the beach", "open concept"],
    "tags" : ["cozy", "seaside"],
    'guest_capacity': 2,
    'unavailable_dates': ['2025-09-01', '2025-09-02', '2025-09-20', '2025-10-01']
}

property_listings = [listing_1, listing_2]

users_list = [
    {"user_id": 1, "name": "Alice", "password": '123456', 'booking_history': [{"property_id": 1, "start_date": "2025-08-15", "end_date": "2025-08-20"}]},
    {"user_id": 2, "name": "Bob", "password": '8765', 'booking_history':[]}
]

admin_list = [
    {"admin_id": 1, "password": 'admin123'},
    {"admin_id": 2, "password": 'admin456'}
]


# Pool of locations, features, tags, and types
locations_pool = ["Toronto", "Montreal", "Vancouver", "Calgary", "Edmonton", "Winnipeg", "Paris", "Rome", "New York", "Los Angeles", "Chicago", "Miami", "San Francisco", "Seattle", "Boston", "Washington D.C.", "London"]   
features_pool = ["Free wifi", "Fireplace", "Pool", "Air conditioning", 'Gym access', 'Washer/Dryer', 'Sauna', 'Private balcony', 'BBQ grill', "Kitchen with oven and dishwasher", "Hot tub"]
tags_pool = ["Luxury stay", "Budget-friendly", 'Family-friendly', 'Pet-friendly', 'City center', 'Beachfront', 'Mountain view', 'Lake view', 'River view', 'Ocean view']
types_pool = ["Apartment", "House", "Cabin", "Villa", "Condo", "Townhouse", "Bungalow", "Cottage", "Studio", "Loft", "Penthouse", "Chalet", "Farmhouse"]

# Classes
class Property:
    def __init__(self, property_id, location, p_type, price_per_night, features, tags, guest_capacity, unavailable_dates):
        self.property_id = property_id
        self.location = location
        self.type = p_type
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
            "Property Location": self.location,
            "Property Type": self.type,
            "Price per Night": self.price_per_night,
            "Features": self.features,
            "Tags": self.tags,
            "Guest Capacity": self.guest_capacity,
            "Unavailable Dates": self.unavailable_dates
        }

    @classmethod
    def from_dict(cls, d): 
        return cls(
            property_id=d["property_id"],
            location=d["Property Location"],
            p_type=d["Property Type"],
            price_per_night=d["Price per Night"],
            features=d["Features"],
            tags=d["Tags"],
            guest_capacity=d["Guest Capacity"],
            unavailable_dates=d["Unavailable Dates"]    
        )

property_obj_list = [
    Property(
        l["property_id"], l["location"], l["type"], l["price_per_night"],
        l["features"], l["tags"], l["guest_capacity"], l.get("unavailable_dates", [])
    )
    for l in property_listings
]


class User:
    def __init__(self, user_id, name, password, booking_history):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.booking_history = booking_history
    
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
            booking_history=d["booking_history"]
        )

    def user_display_profile(self):
        bh = self.booking_history if self.booking_history else "No booking yet"
        print(f"""
        User ID: {self.user_id}
        Name: {self.name}
        Password: {self.password}
        Booking History: {bh}""")

users_obj_list = [
    User(u["user_id"], u["name"], u["password"], u.get("booking_history", []))
    for u in users_list
]


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
import datetime
def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def view_properties(property_id):
    for property in property_obj_list:
        if property.property_id == property_id:
            property.property_display()
            return property
    print(f"No property found with ID {property_id}")
    return None


def add_properties():
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
    print(f"Property added successfully! Property ID: {property_id}")
    return new_property



def delete_properties(property_id):
    for i, property in enumerate(property_obj_list):
        if property.property_id == property_id:
            property_obj_list.pop(i)
            print(f"Property deleted successfully! Property ID: {property_id}")
            return
    print(f"No property found with ID {property_id}")


def update_property(property_id):
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

    return target

def _find_user(user_id):
    for u in users_obj_list:
        if u.user_id == user_id:
            return u
    return None

def _find_property(property_id):
    for p in property_obj_list:
        if p.property_id == property_id:
            return p
    return None


def create_booking_history(user_id):
    print(f"\n=== Booking FOR USER {user_id} ===")
    user = _find_user(user_id)
    
    if not user:
        print(f"No user found with ID {user_id}")
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
    print("Booking created successfully!")



def delete_booking(user_id):
    user = _find_user(user_id)
    if not user:
        print(f"No user found with ID {user_id}")
        return None
    if not user.booking_history:
        print("No booking to delete")
        return None

    print("\nYour bookings:")
    for i, b in enumerate(user.booking_history, 1):
        print(f"{i}. Property {b['property_id']} | from {b['start_date']} to {b['end_date']}")

    while True:
        try:
            idx_f = float(input("Enter booking number to delete: ").strip())
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

    print(f"Booking {idx} deleted")
    return removed


def create_user_profile():
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
    return new_user


def view_user_profile(user_id):
    for user in users_obj_list:
        if user.user_id == user_id:
            user.user_display_profile()
            return user
    print(f"No user found with ID {user_id}")
    return None

def delete_profile(user_id):
    global users_obj_list
    for i, user in enumerate(users_obj_list):
        if user.user_id == user_id:
            users_obj_list.pop(i)
            print(f"Deleted user ID {user_id}")
            return
    print(f"No user found with ID {user_id}")

def edit_user_profile(user_id):
    user = _find_user(user_id)
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
            return user

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
            create_booking_history(user.user_id)

        elif choice == 4:
            delete_booking(user.user_id)

        print("\nUpdated profile:")
        user.user_display_profile()






# Includes some validations for the things users input
def search_properties():
    while True:
        try:
            group_size = int(input("Group Size: "))
            if group_size > 0: break
            print("Must be positive number")
        except ValueError:
            print("Please enter a whole number")
    while True:
        try:
            min_budget = float(input("Minimum Budget ($) - whole number only: "))
            if min_budget != int(min_budget):
                print("Please enter a whole number (no decimals)")
                continue
            min_budget = int(min_budget)
            if min_budget <= 0:
                print("Minimum budget must be positive")
                continue
            break
        except ValueError:
            print("Please enter a whole number")
    
    while True:
        try:
            max_budget = float(input("Maximum Budget ($) - whole number only: "))
            if max_budget != int(max_budget):
                print("Please enter a whole number (no decimals)")
                continue
            max_budget = int(max_budget)
            if max_budget <= 0:
                print("Maximum budget must be positive")
                continue
            if max_budget < min_budget:
                print("Maximum budget must be greater than or equal to minimum budget")
                continue
            break
        except ValueError:
            print("Please enter a whole number")
    
    # Get preferred features
    print("\nEnter your preferred features (at least one required):")
    print("Examples: wifi, fireplace, pool, beachfront, mountain view, etc.")
    print("Press Enter when you're done adding features")
    preferred_features = []
    while True:
        feature = input("Add feature: ").strip().lower()
        if not feature:
            if not preferred_features:
                print("Please enter at least one feature")
                continue
            else:
                print(f"Features added: {preferred_features}")
                break
        preferred_features.append(feature)
        print(f"Added: {feature}")
    
    print("\nEnter your preferred tags (at least one required):")
    print("Examples: beach, luxury, budget, family, adventure, etc.")
    print("Press Enter when you're done adding tags")
    preferred_tags = []
    while True:
        tag = input("Add tag: ").strip().lower()
        if not tag:
            if not preferred_tags:
                print("Please enter at least one tag")
                continue
            else:
                print(f"Tags added: {preferred_tags}")
                break
        preferred_tags.append(tag)
        print(f"Added: {tag}")
    
    
    travel_dates = []
    print("\nEnter Start Date of Travel (YYYY-MM-DD format): ")
    
    while True:
        start_date = input("Start date: ").strip()
        if not start_date:
            print("Start date is required")
            continue
        if validate_date(start_date):
            break
        else:
            print("Invalid format. Use YYYY-MM-DD")
    
    while True:
        end_date = input("End date (YYYY-MM-DD format): ").strip()
        if not end_date:
            print("End date is required")
            continue
        if validate_date(end_date):
            if datetime.datetime.strptime(end_date, '%Y-%m-%d') <= datetime.datetime.strptime(start_date, '%Y-%m-%d'):
                print("End date must be after start date")
                continue
            break
        else:
            print("Invalid format. Use YYYY-MM-DD")
    
    travel_dates = [start_date, end_date]
