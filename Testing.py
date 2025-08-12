listing_1 = {
    
        "property_id": 1,
        "location": "Blue Mountain, Ontario",
        "type": "cabin",
        "price_per_night": 140,
        "features": ["mountain view", "fireplace", "ski-in/ski-out", "wifi"],
        "tags": ["mountains", "remote", "adventure"]
    }


listing_2 = {
    "property_id": 2,
    "location": "103 Ocean Street West",
    "type" : "Apartment",
    "price_per_night": 65,
    "features" : ["furnished", "on the beach", "open concept"],
    "tags" : ["cozy", "seaside"]
}

listing_3 = {
    "property_id": 3,
    "location": "Niagara-on-the-Lake, Ontario",
    "type": "guesthouse",
    "price_per_night": 95,
    "features": ["wine country view", "garden", "wifi", "bike rentals"],
    "tags": ["romantic", "wine", "culture"]
}

listing_4 = {
    "property_id": 4,
    "location": "Tobermory, Ontario",
    "type": "cottage",
    "price_per_night": 125,
    "features": ["lake view", "kayak included", "fire pit", "wifi"],
    "tags": ["nature", "waterfront", "hiking"]
}

listing_5 = {
    "property_id": 5,
    "location": "Toronto, Ontario",
    "type": "apartment",
    "price_per_night": 180,
    "features": ["central location", "gym access", "rooftop view", "wifi"],
    "tags": ["city", "nightlife", "foodie"]
}
listing_6 = {
        "property_id": 6,
        "location": "Blue Mountain, Ontario",
        "type": "loft",
        "price_per_night": 160,
        "features": ["mountain view", "balcony", "wifi", "hot tub"],
        "tags": ["mountains", "luxury", "ski"]
    }
listing_7 = {
        "property_id": 7,
        "location": "Wasaga Beach, Ontario",
        "type": "villa",
        "price_per_night": 200,
        "features": ["private pool", "beachfront", "AC", "wifi"],
        "tags": ["beach", "luxury", "family"]
    }
listing_8 = {
        "property_id": 8,
        "location": "Niagara-on-the-Lake, Ontario",
        "type": "cottage",
        "price_per_night": 105,
        "features": ["garden", "bike rentals", "fire pit", "wifi"],
        "tags": ["romantic", "nature", "wine"]
    }
listing_9 = {
        "property_id": 9,
        "location": "Tobermory, Ontario",
        "type": "tiny house",
        "price_per_night": 90,
        "features": ["lake view", "hiking trails nearby", "BBQ", "wifi"],
        "tags": ["budget", "nature", "waterfront"]
    }
listing_10 = {
        "property_id": 10,
        "location": "Toronto, Ontario",
        "type": "studio",
        "price_per_night": 150,
        "features": ["central location", "AC", "wifi", "workspace"],
        "tags": ["city", "business", "solo travel"]
    }
listing_11 = {
        "property_id": 11,
        "location": "Muskoka, Ontario",
        "type": "cottage",
        "price_per_night": 170,
        "features": ["lakefront", "canoe included", "fire pit", "wifi"],
        "tags": ["nature", "waterfront", "family"]
    }
listing_12 = {
        "property_id": 12,
        "location": "Prince Edward County, Ontario",
        "type": "guesthouse",
        "price_per_night": 130,
        "features": ["wine country view", "garden", "wifi", "pet friendly"],
        "tags": ["romantic", "wine", "pet friendly"]
    }
listing_13 = {
        "property_id": 13,
        "location": "Ottawa, Ontario",
        "type": "apartment",
        "price_per_night": 120,
        "features": ["central location", "balcony", "wifi", "parking"],
        "tags": ["city", "history", "budget"]
    }
listing_14 = {
    "property_id": 14,
    "location": "Algonquin Park, Ontario",
    "type": "cabin",
    "price_per_night": 110,
    "features": ["forest view", "canoe included", "fire pit", "wifi"],
    "tags": ["nature", "hiking", "remote"]
}

listing_15 = {
    "property_id": 15,
    "location": "Kingston, Ontario",
    "type": "loft",
    "price_per_night": 140,
    "features": ["waterfront view", "balcony", "wifi", "downtown access"],
    "tags": ["city", "romantic", "history"]
}


class Property:
    def __init__(self, property_id, location, p_type, price_per_night,features,tags):
        self.property_id = property_id
        self.location = location
        self.type = p_type
        self.price_per_night = price_per_night
        self.features = features
        self.tags = tags
    def property_display(self):
        print(f"""
        Property ID: {self.property_id} 
        Property Location: {self.location}
        Property Type: {self.type}
        Price per Night: {self.price_per_night}
        Features: {self.features}
        Tags: {self.tags}""")

property_listings = [listing_1, listing_2, listing_3, listing_4, listing_5, listing_6, listing_7, listing_8, listing_9, listing_10, listing_11, listing_12, listing_13, listing_14, listing_15]


property_obj_list = []  
for listings in property_listings:
    property_obj_list.append(Property(listings.get('property_id'),listings.get('location'),listings.get('type'),listings.get('price_per_night'),listings.get('features'),listings.get('tags')))



class User:
    def __init__(self,user_id, name, group_size, preferred_environment, budget_range, travel_dates):
        self.user_id = user_id
        self.name = name
        self.group_size = group_size
        self.preferred_environment = preferred_environment
        self.budget_range = budget_range
        self.travel_dates = travel_dates
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "group_size": self.group_size,
            "preferred_environment": self.preferred_environment,
            "budget_range": self.budget_range,
            "travel_dates": self.travel_dates
        }
    
    @classmethod
    def from_dict(cls, d): # Use value in d (which is a dictionary) to create an instance
        return cls(
            user_id=d["user_id"],
            name=d["name"],
            group_size=d["group_size"],
            preferred_environment=d["preferred_environment"],
            budget_range=d["budget_range"],
            travel_dates=d["travel_dates"]
        )

    def matches(self, property_obj):
        return property_obj.price_per_night <= self.budget

    def user_display_profile(self):
        print(f"""
        User ID: {self.user_id}
        User Name: {self.name}
        Group Size: {self.group_size}
        Preferred Environment: {self.preferred_environment}
        Budget: {self.budget_range}
        Travel Dates: {self.travel_dates}""")


import datetime

def validate_date(date_str): #Validate if a string is in YYYY-MM-DD format
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def create_user_profile(self):
    print("\n=== CREATE NEW PROFILE ===")
    user_id = len(users_obj_list) + 1
    
    while True:
        name = input("Full Name: ").strip()
        if name: break
        print("Name cannot be empty")
    
    while True:
        try:
            group_size = int(input("Group Size: "))
            if group_size > 0: break
            print("Must be positive number")
        except ValueError:
            print("Please enter a number")
    while True:
        try:
            min_budget = int(input("Minimum Budget ($): "))
            max_budget = int(input("Maximum Budget ($): "))
            if 0 < min_budget <= max_budget: break
            print("Invalid budget range")
        except ValueError:
            print("Please enter numbers only")
    
    env_options = ["beach", "mountains", "city", "countryside", "desert"]
    print("Environment options:", ", ".join(env_options))
    while True:
            preferred_environment = input("Preferred Environment: ").lower().strip()
            if preferred_environment in env_options: break
            print(f"Must be one of: {', '.join(env_options)}")
    
    while True:
            try:
                min_budget = int(input("Minimum Budget ($): "))
                max_budget = int(input("Maximum Budget ($): "))
                if 0 < min_budget <= max_budget: break
                print("Invalid budget range")
            except ValueError:
                print("Please enter numbers only")
    
    travel_dates = []
    print("\nEnter Travel Dates (YYYY-MM-DD format)")
    while True:
        date = input("Add date: ").strip()
        if not date: 
            break
        if validate_date(date):
            travel_dates.append(date)
        else:
            print("Invalid format. Use YYYY-MM-DD")
    
    new_user = User(user_id, name, group_size, preferred_environment, 
                   (min_budget, max_budget), travel_dates)
    users_obj_list.append(new_user)
    print(f"\nProfile created successfully! User ID: {user_id}")
    return new_user

def view_user_profile(user_id):
    for user in users_obj_list:
        if user.user_id == user_id:
            user.display_profile()
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


users_list = [
    {"user_id": 1, "name": "Alice", "group_size": 2, "preferred_environment": "beach", "budget_range": [100,200], 'travel_dates': ['2025-08-15', '2025-08-20']},
    {"user_id": 2, "name": "Bob", "group_size": 4, "preferred_environment": "mountains", "budget_range": [200,350], 'travel_dates': ['2025-10-15', '2025-11-02']},
    {"user_id": 3, "name": "Charlie", "group_size": 1, "preferred_environment": "city", "budget_range": [80, 150], 'travel_dates': ['2026-01-01', '2026-02-01']},
    {"user_id": 4, "name": "Diana", "group_size": 3, "preferred_environment": "countryside", "budget_range": [300,500], 'travel_dates': ['2025-12-05', '2025-12-12']},
    {"user_id": 5, "name": "Ethan", "group_size": 5, "preferred_environment": "beach", "budget_range": [250,400], 'travel_dates': ['2025-12-25', '2026-01-20']},
    {"user_id": 6, "name": "Fiona", "group_size": 2, "preferred_environment": "desert", "budget_range": [140,250], 'travel_dates': ['2025-09-20', '2025-09-25']},
    {"user_id": 7, "name": "George", "group_size": 6, "preferred_environment": "mountains", "budget_range": [300,500], 'travel_dates': ['2025-09-23', '2025-09-26']},
    {"user_id": 8, "name": "Hannah", "group_size": 3, "preferred_environment": "city", "budget_range": [170,300], 'travel_dates': ['2026-03-19', '2025-03-22']},
    {"user_id": 9, "name": "Isaac", "group_size": 4, "preferred_environment": "countryside", "budget_range": [210,350], 'travel_dates': ['2026-04-26', '2026-05-01']},
    {"user_id": 10, "name": "Julia", "group_size": 2, "preferred_environment": "beach", "budget_range": [160,280], 'travel_dates': ['2025-11-25', '2025-11-27']},
    {"user_id": 11, "name": "Kevin", "group_size": 1, "preferred_environment": "desert", "budget_range": [110,200], 'travel_dates': ['2025-09-05', '2025-09-07']},
    {"user_id": 12, "name": "Laura", "group_size": 5, "preferred_environment": "mountains", "budget_range": [260,450], 'travel_dates': ['2025-11-21', '2025-11-30']},
    {"user_id": 13, "name": "Michael", "group_size": 3, "preferred_environment": "city", "budget_range": [190,320], 'travel_dates': ['2025-12-06', '2025-12-16']},
    {"user_id": 14, "name": "Nina", "group_size": 4, "preferred_environment": "countryside", "budget_range": [220,380], 'travel_dates': ['2026-03-15', '2026-03-17']},
    {"user_id": 15, "name": "Oscar", "group_size": 2, "preferred_environment": "beach", "budget_range": [130,230], 'travel_dates': ['2026-01-15', '2026-01-20']}

]

users_obj_list = []  
for users in users_list:
    users_obj_list.append(User(users.get('user_id'),users.get('name'),users.get('group_size'),users.get('preferred_environment'),users.get('budget_range'),users.get('travel_dates')))

for user in users_obj_list:
    user.user_display_profile()

for listing in property_obj_list:
    listing.property_display()
