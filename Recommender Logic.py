'''import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'test'))

from Testing import users_obj_list, property_obj_list
'''

from datetime import datetime, timedelta
listing_1 = {
    
        "property_id": 1,
        "location": "Blue Mountain, Ontario",
        "type": "cabin",
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
    'unavailable_dates': ['2025-08-09', '2025-08-14', '2025-09-20', '2025-10-01']
}

listing_3 = {
    "property_id": 3,
    "location": "Niagara-on-the-Lake, Ontario",
    "type": "guesthouse",
    "price_per_night": 95,
    "features": ["wine country view", "garden", "wifi", "bike rentals"],
    "tags": ["romantic", "wine", "culture"],
    'guest_capacity': 2,
    'unavailable_dates': ['2025-09-30', '2025-09-15', '2025-12-20', '2025-12-03']
}

listing_4 = {
    "property_id": 4,
    "location": "Tobermory, Ontario",
    "type": "cottage",
    "price_per_night": 125,
    "features": ["lake view", "kayak included", "fire pit", "wifi"],
    "tags": ["nature", "waterfront", "hiking"],
    'guest_capacity': 3,
    'unavailable_dates': ['2025-10-11', '2025-10-12', '2025-10-13', '2025-12-24', '2025-12-25', '2025-12-26']
}

listing_5 = {
    "property_id": 5,
    "location": "Toronto, Ontario",
    "type": "apartment",
    "price_per_night": 180,
    "features": ["central location", "gym access", "rooftop view", "wifi"],
    "tags": ["city", "nightlife", "foodie"],
    'guest_capacity': 4,
    'unavailable_dates': ['2025-11-19', '2025-11-20', '2025-11-21', '2025-11-27', '2025-11-28']
}
listing_6 = {
        "property_id": 6,
        "location": "Blue Mountain, Ontario",
        "type": "loft",
        "price_per_night": 660,
        "features": ["mountain view", "balcony", "wifi", "hot tub"],
        "tags": ["mountains", "luxury", "ski"],
        'guest_capacity': 8,
        'unavailable_dates': ['2025-10-05']
    }
listing_7 = {
        "property_id": 7,
        "location": "Wasaga Beach, Ontario",
        "type": "villa",
        "price_per_night": 200,
        "features": ["private pool", "beachfront", "AC", "wifi"],
        "tags": ["beach", "luxury", "family"],
        'guest_capacity': 4,
        'unavailable_dates': ['2025-10-17', '2025-10-18', '2025-12-19', '2025-12-20']
    }
listing_8 = {
        "property_id": 8,
        "location": "Niagara-on-the-Lake, Ontario",
        "type": "cottage",
        "price_per_night": 350,
        "features": ["garden", "bike rentals", "fire pit", "wifi"],
        "tags": ["romantic", "nature", "wine"],
        'guest_capacity': 2,
        'unavailable_dates': ['2025-09-12', '2025-09-13', '2026-01-01', '2026-01-02', '2026-01-26']
    }
listing_9 = {
        "property_id": 9,
        "location": "Tobermory, Ontario",
        "type": "tiny house",
        "price_per_night": 90,
        "features": ["lake view", "hiking trails nearby", "BBQ", "wifi"],
        "tags": ["budget", "nature", "waterfront"],
        'guest_capacity': 3,
        'unavailable_dates': ['2025-12-03', '2025-12-19', '2025-12-31', '2026-02-02']
    }
listing_10 = {
        "property_id": 10,
        "location": "Toronto, Ontario",
        "type": "studio",
        "price_per_night": 150,
        "features": ["central location", "AC", "wifi", "workspace"],
        "tags": ["city", "business", "solo travel"],
        'guest_capacity': 2,
        'unavailable_dates': ['2025-11-11', '2025-11-20', '2025-12-04']

    }
listing_11 = {
        "property_id": 11,
        "location": "Muskoka, Ontario",
        "type": "cottage",
        "price_per_night": 770,
        "features": ["lakefront", "canoe included", "fire pit", "wifi"],
        "tags": ["nature", "waterfront", "family"],
        'guest_capacity': 10,
        'unavailable_dates': ['2025-12-12', '2025-12-23', '2025-12-24', '2025-12-28']
    }
listing_12 = {
        "property_id": 12,
        "location": "Prince Edward County, Ontario",
        "type": "guesthouse",
        "price_per_night": 130,
        "features": ["wine country view", "garden", "wifi", "pet friendly"],
        "tags": ["romantic", "wine", "pet friendly"],
        'guest_capacity': 2,
        'unavailable_dates': ['2026-03-01', '2026-03-10', '2025-12-11']
    }
listing_13 = {
        "property_id": 13,
        "location": "Ottawa, Ontario",
        "type": "apartment",
        "price_per_night": 120,
        "features": ["central location", "balcony", "wifi", "parking"],
        "tags": ["city", "history", "budget"],
        'guest_capacity': 3,
        'unavailable_dates':['2025-10-09', '2025-10-11','2025-11-14' ]
    }
listing_14 = {
    "property_id": 14,
    "location": "Algonquin Park, Ontario",
    "type": "cabin",
    "price_per_night": 110,
    "features": ["forest view", "canoe included", "fire pit", "wifi"],
    "tags": ["nature", "hiking", "remote"],
    'guest_capacity': 2,
    'unavailable_dates': ['2025-10-18', '2025-10-19', '2025-11-29']
}

listing_15 = {
    "property_id": 15,
    "location": "Kingston, Ontario",
    "type": "loft",
    "price_per_night": 540,
    "features": ["waterfront view", "balcony", "wifi", "downtown access"],
    "tags": ["city", "romantic", "history"],
    'guest_capacity': 6,
    'unavailable_dates': ['2025-12-03', '2025-12-04', '2025-12-05', '2025-12-08', '2025-12-09', '2025-12-31']
}

class Property:
    def __init__(self, property_id, location, p_type, price_per_night,features,tags, guest_capacity, unavailable_dates):
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

property_listings = [listing_1, listing_2, listing_3, listing_4, listing_5, listing_6, listing_7, listing_8, listing_9, listing_10, listing_11, listing_12, listing_13, listing_14, listing_15]


property_obj_list = []  
for listings in property_listings:
    property_obj_list.append(Property(listings.get('property_id'),listings.get('location'),listings.get('type'),listings.get('price_per_night'),listings.get('features'),listings.get('tags'),listings.get('guest_capacity'),listings.get('unavailable_dates')))


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


print("-"*100)


import numpy as np
# print(np.__version__)


print("-"*50)

trial_user_input_tag = input('What are you searching for?')
trial_user_input_group_size = int(input('What is your group size?'))
# trial_user_budget_min = input('What is your minimum budget?')
trial_user_budget_max = int(input('What is your maximum budget?'))
trial_start_date = input('When is your check-in date?')
trial_end_date = input('When is your check-out date?')

trial_start_date = datetime.strptime(trial_start_date, "%Y-%m-%d").date()
trial_end_date = datetime.strptime(trial_end_date, "%Y-%m-%d").date()

print("-"*50)

# Calculate weighted Tag Score --> for now no matches score 0 but we need to define correlations in our tags pool
properties_matched_tags_score = 0

for prop in property_obj_list:
    if trial_user_input_tag.lower() in [tag.lower() for tag in prop.tags]:
        properties_matched_tags_score = 10
    else: 
        properties_matched_tags_score = 0
    
    print(f"Property {prop.property_id} ({prop.location}) tag score :{properties_matched_tags_score} prop tags:{prop.tags} user tag: {trial_user_input_tag}")# Calculate weighted Tag Score TODO we need to define correlation btw tags

# Calculate weighted Price Score
price_score = 0 

for prop in property_obj_list:
    if trial_user_budget_max >= prop.price_per_night:
        price_score = 10 - 5 * (prop.price_per_night / trial_user_budget_max)   # 10 at 0 price, 5 at budget
    else:
        price_score = max(0, 5 - 5 * ((prop.price_per_night - trial_user_budget_max) / trial_user_budget_max))
    
    print(f"Property {prop.property_id} ({prop.location}) prop price: {prop.price_per_night} budget {trial_user_budget_max} . Price Score: {round(price_score, 2)}")

# Calculate weighted group size
group_size_score = 0 

for prop in property_obj_list:
    if trial_user_input_group_size > prop.guest_capacity:
        group_size_score = 0 
    else:
        extra_space = prop.guest_capacity - trial_user_input_group_size
        group_size_score = 10 + min(extra_space, 5)

    
    print(f"Property {prop.property_id} ({prop.location}) prop capacity: {prop.guest_capacity} group size: {trial_user_input_group_size} . Capacity Score: {round(group_size_score, 2)}")


# Calculate weighted date availability score
availability_score = 0
total_days = (trial_end_date - trial_start_date).days + 1

for prop in property_obj_list:
    unavailable_dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in prop.unavailable_dates]
    
    # identify available days within the user’s date range
    current_streak = 0
    max_streak = 0
    fully_available = True
    
    for i in range(total_days):
        current_day = trial_start_date + timedelta(days=i)
        if current_day not in unavailable_dates:
            current_streak += 1
            if current_streak > max_streak:
                max_streak = current_streak
        else:
            fully_available = False
            current_streak = 0
    
    
    if fully_available:
        availability_score = 10
    elif max_streak >= total_days:  # not all user days are in a fully available range, but they fit within gaps
        availability_score = 5
    else:
        availability_score = 0
  
    print(f"Property {prop.property_id} ({prop.location}) unavail dates: {prop.unavailable_dates} user dates:{trial_start_date} and {trial_end_date} avail score: {round(availability_score,2)}" )


# Defining a function that gives scores to properties according to user information

'''
def score_property_for_user(user, prop):
    score_for_budget = 0
    score_for_preferred_environment = 0
    score_for_group_size = 0
    score_for_avail_dates = 0
    
    # Match preferred environment with tags
    if trial_user_input.lower() in [tag.lower() for tag in prop.tags]:
        score_for_preferred_environment = 3
    
    # Check if the property price fits user's budget range
    if user.budget_range[0] <= prop.price_per_night <= user.budget_range[1]:
        score_for_budget = 2
    
    # Check if the group size fits the property's capacity so we need to DEFINE CAPACITY IN PROPERTY CLASS
    
    
    if user.group_size <= prop.capacity:
        score_for_group_size = 2
    
    # Check availability based on travel dates so we need to DEFINE AVAIL DATES IN PROPERTY CLASS
    
    if user.travel_dates[0] <= prop.available_date
        score_for_avail_dates = 2
    
    
    return score_for_budget, score_for_preferred_environment, score_for_group_size, score_for_avail_dates
'''

# Checking if the preferred environment is in the tag list in properties
'''
for user in users_obj_list:
    for prop in property_obj_list:
        # Checking for a match between preferred_environment and the tags list
        if user.preferred_environment.lower() in [tag.lower() for tag in prop.tags]:
            print(f"{user.name} ({user.preferred_environment}) -> Property {prop.property_id} ({prop.location}) eşleşti")
'''

