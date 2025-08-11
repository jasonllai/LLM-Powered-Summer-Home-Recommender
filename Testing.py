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
    def property_pp(self):
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
    def __init__(self,user_id, name, group_size, preferred_environment, budget):
        self.user_id = user_id
        self.name = name
        self.group_size = group_size
        self.preferred_environment = preferred_environment
        self.budget = budget
    
    def matches(self, property_obj):
        return property_obj.price_per_night <= self.budget

    def user_pp(self):
        print(f"""
        User ID: {self.user_id}
        User Name: {self.name}
        Group Size: {self.group_size}
        Preferred Environment: {self.preferred_environment}
        Budget: {self.budget}""")


users_list = [
    {"user_id": 1, "name": "Alice", "group_size": 2, "preferred_environment": "beach", "budget": 150},
    {"user_id": 2, "name": "Bob", "group_size": 4, "preferred_environment": "mountains", "budget": 200},
    {"user_id": 3, "name": "Charlie", "group_size": 1, "preferred_environment": "city", "budget": 120},
    {"user_id": 4, "name": "Diana", "group_size": 3, "preferred_environment": "countryside", "budget": 180},
    {"user_id": 5, "name": "Ethan", "group_size": 5, "preferred_environment": "beach", "budget": 250},
    {"user_id": 6, "name": "Fiona", "group_size": 2, "preferred_environment": "desert", "budget": 140},
    {"user_id": 7, "name": "George", "group_size": 6, "preferred_environment": "mountains", "budget": 300},
    {"user_id": 8, "name": "Hannah", "group_size": 3, "preferred_environment": "city", "budget": 170},
    {"user_id": 9, "name": "Isaac", "group_size": 4, "preferred_environment": "countryside", "budget": 210},
    {"user_id": 10, "name": "Julia", "group_size": 2, "preferred_environment": "beach", "budget": 160},
    {"user_id": 11, "name": "Kevin", "group_size": 1, "preferred_environment": "desert", "budget": 110},
    {"user_id": 12, "name": "Laura", "group_size": 5, "preferred_environment": "mountains", "budget": 260},
    {"user_id": 13, "name": "Michael", "group_size": 3, "preferred_environment": "city", "budget": 190},
    {"user_id": 14, "name": "Nina", "group_size": 4, "preferred_environment": "countryside", "budget": 220},
    {"user_id": 15, "name": "Oscar", "group_size": 2, "preferred_environment": "beach", "budget": 130}

]

users_obj_list = []  
for users in users_list:
    users_obj_list.append(User(users.get('user_id'),users.get('name'),users.get('group_size'),users.get('preferred_environment'),users.get('budget'),))

for user in users_obj_list:
    user.user_pp()

for listing in property_obj_list:
    listing.property_pp()