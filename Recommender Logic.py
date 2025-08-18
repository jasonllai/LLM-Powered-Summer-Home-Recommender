from datetime import datetime, timedelta, date
import pandas as pd
from difflib import get_close_matches, SequenceMatcher
# Tags correlation table
tags_pool = ["Luxury stay", "Budget-friendly", 'Family-friendly', 'Pet-friendly', 'City center', 'Beachfront', 'Mountain view', 'Lake view', 'River view', 'Ocean view']

data = {
    "Luxury stay": [1, 0.2, 0.1, 0.1, 0.1, 0.3, 0.2, 0.2, 0.1, 0.3],
    "Budget-friendly": [0.2, 1, 0.3, 0.2, 0.3, 0.1, 0.1, 0.1, 0.1, 0.1],
    "Family-friendly": [0.1, 0.3, 1, 0.5, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1],
    "Pet-friendly": [0.1, 0.2, 0.5, 1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
    "City center": [0.1, 0.3, 0.2, 0.1, 1, 0.1, 0.1, 0.1, 0.1, 0.1],
    "Beachfront": [0.3, 0.1, 0.1, 0.1, 0.1, 1, 0.2, 0.3, 0.2, 0.4],
    "Mountain view": [0.2, 0.1, 0.1, 0.1, 0.1, 0.2, 1, 0.3, 0.3, 0.2],
    "Lake view": [0.2, 0.1, 0.1, 0.1, 0.1, 0.3, 0.3, 1, 0.4, 0.2],
    "River view": [0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.3, 0.4, 1, 0.2],
    "Ocean view": [0.3, 0.1, 0.1, 0.1, 0.1, 0.4, 0.2, 0.2, 0.2, 1]
}

corr_df = pd.DataFrame(data, index=tags_pool)

class ListingRecommender():
    def __init__(self, listing_lst):
        self.listing_lst = listing_lst
        self.calculated_scores = {}
        for listing in listing_lst:
            self.calculated_scores[listing.property_id] = 0

        self.selected_group_size = 0
        self.selected_minimum_budget = 0
        self.selected_maximum_budget = 0
        self.selected_tag = ""
        self.selected_start_date = ""
        self.selected_end_date = ""

        self.budget_score = 0
        self.tag_score = 0
        self.group_size_score = 0
        self.date_score = 0
    def reset_all(self):
        for listing in self.listing_lst:
            self.calculated_scores[listing.property_id] = 0 

        self.selected_group_size = 0
        self.selected_minimum_budget = 0
        self.selected_maximum_budget = 0
        self.selected_tag = ""
        self.selected_start_date = ""
        self.selected_end_date = ""

    def reset_selection(self):
        self.selected_group_size = 0
        self.selected_minimum_budget = 0
        self.selected_maximum_budget = 0
        self.selected_tag = ""
        self.selected_start_date = ""
        self.selected_end_date = ""
    
    def reset_scores(self):
        for listing in self.listing_lst:
            self.calculated_scores[listing.property_id] = 0 

    def prompt_tag(self):
        while True:
            self.selected_tag = input("What are you searching for: ").strip().lower()
            if not self.selected_tag:
                if self.selected_tag or len(self.selected_tag) == 0:
                    print("Please enter at least one tag.")
                    # continue
            break

    def prompt_group_size(self):
        while True:
            try:
                self.selected_group_size = int(input("Group Size: "))
                if self.selected_group_size > 0: break
                print("Must be positive number")
            except ValueError:
                print("Please enter a whole number")
    
    def prompt_budget(self):
        while True:
            try:
                self.selected_minimum_budget = float(input("Minimum Budget ($) - whole number only: "))
                if self.selected_minimum_budget != int(self.selected_minimum_budget):
                    print("Please enter a whole number (no decimals)")
                    continue
                self.selected_minimum_budget = int(self.selected_minimum_budget)
                if self.selected_minimum_budget <= 0:
                    print("Minimum budget must be positive")
                    continue
                break
            except ValueError:
                print("Please enter a whole number")
    
        while True:
            try:
                self.selected_maximum_budget = float(input("Maximum Budget ($) - whole number only: "))
                if self.selected_maximum_budget != int(self.selected_maximum_budget):
                    print("Please enter a whole number (no decimals)")
                    continue
                self.selected_maximum_budget = int(self.selected_maximum_budget)
                if self.selected_maximum_budget <= 0:
                    print("Maximum budget must be positive")
                    continue
                if self.selected_maximum_budget < self.selected_minimum_budget:
                    print("Maximum budget must be greater than or equal to minimum budget")
                    continue
                break
            except ValueError:
                print("Please enter a whole number")

    def prompt_dates(self):
        print("Enter Start Date of Travel (YYYY-MM-DD format): ")
    
        while True:
            self.selected_start_date = input("Start date: ").strip()
            if not self.selected_start_date:
                print("Start date is required")
                continue
            if self.validate_date(self.selected_start_date):
                break
            else:
                print("Invalid format. Use YYYY-MM-DD")
        
        while True:
            self.selected_end_date = input("End date (YYYY-MM-DD format): ").strip()
            if not self.selected_end_date:
                print("End date is required")
                continue
            if self.validate_date(self.selected_end_date):
                if datetime.strptime(self.selected_end_date, '%Y-%m-%d') <= datetime.strptime(self.selected_start_date, '%Y-%m-%d'):
                    print("End date must be after start date")
                    continue
                break
            else:
                print("Invalid format. Use YYYY-MM-DD")

    def calculate_tag_score(self):
        tag_score = 0
        for listing in self.listing_lst:
        # Exact match kontrolü
            if self.selected_tag in tags_pool:
                tag_score = 1
                # Diğerleri korelasyona göre 0-1 arası
                for tag in tags_pool:
                    if tag != self.selected_tag:
                        tag_score = round(corr_df.loc[tag_score, tag], 2)
            
            # Exact match yoksa en yakın tag'ı bul
            matches = get_close_matches(self.selected_tag, tags_pool, n=1, cutoff=0.1)
            if matches:
                closest_tag = matches[0]
            else:
                closest_tag = min(
                    tags_pool,
                    key=lambda x: sum(1 for a, b in zip(x.lower(), self.selected_tag.lower()) if a != b) + abs(len(x)-len(self.selected_tag))
                )
            
            # Skorları hesapla: benzerlik × korelasyon
            similarity = SequenceMatcher(None, self.selected_tag.lower(), closest_tag.lower()).ratio()
            for tag in tags_pool:
                corr = corr_df.loc[closest_tag, tag]
                tag_score = round(similarity * corr, 2)
            
            print(f"Property {listing.property_id} ({listing.location}) prop tags: {listing.tags} your tag {self.selected_tag} score: {tag_score}")
            self.calculated_scores[listing.property_id] = self.calculated_scores[listing.property_id] + tag_score


    def calculate_budget_score(self):
        price_score = 0 
        for listing in self.listing_lst:
            if listing.price_per_night in range(self.selected_minimum_budget, self.selected_maximum_budget):
                price_score = 3 # if the property price per night is within the user's budget return the highest score which is 3
            elif listing.price_per_night < self.selected_minimum_budget:
                price_difference = 1 - ((self.selected_minimum_budget - listing.price_per_night) / self.selected_minimum_budget )
                price_score = max(0, round(price_difference * 3, 2))
            else: # if the property price per night is higher than the user's budget
                price_difference = 1 - ((listing.price_per_night - self.selected_maximum_budget) / self.selected_maximum_budget)
                price_score = max(0, round(price_difference * 3, 2))
            
            print(f"Property {listing.property_id} ({listing.location}) prop price: {listing.price_per_night} budget {self.selected_maximum_budget} . Price Score: {round(price_score, 2)}")
            self.calculated_scores[listing.property_id] = self.calculated_scores[listing.property_id] + price_score

    def calculate_date_score(self):
        date_score = 0
        travel_start = datetime.strptime(self.selected_start_date, '%Y-%m-%d').date()
        travel_end = datetime.strptime(self.selected_end_date, '%Y-%m-%d').date()
        days_of_stay = (travel_end - travel_start).days + 1
        total_overlap = 0
        for listing in self.listing_lst:
            total_overlap = 0 
            for booking_start_date, booking_end_date in listing.unavailable_dates:
                overlap_start = max(travel_start, booking_start_date)
                overlap_end = min(travel_end, booking_end_date)
                if overlap_start <= overlap_end:
                    total_overlap = total_overlap + (overlap_end - overlap_start).days + 1
            if total_overlap == 0:
                date_score = 2
            elif total_overlap >= days_of_stay:
                date_score = 0
            else:
                available_days = days_of_stay - total_overlap
                date_score = round((available_days/days_of_stay) * 2, 2)

            print(f"Property {listing.property_id} ({listing.location}) Property_unavail dates: {listing.unavailable_dates} your travel dates {self.selected_start_date} {self.selected_end_date}. date Score: {date_score}")
            self.calculated_scores[listing.property_id] = self.calculated_scores[listing.property_id] + date_score

    def calculate_group_size_score(self):
        group_size_score = 0
        for listing in self.listing_lst:
            if self.selected_group_size == listing.guest_capacity:
                group_size_score = 3
            elif self.selected_group_size > listing.guest_capacity:
                group_size_score = 0
            else:
                group_size_score = round(3 - ((3 / listing.guest_capacity) * (listing.guest_capacity - self.selected_group_size)), 2)
            print(f"Property {listing.property_id} ({listing.location}) prop capacity: {listing.guest_capacity} your group size {self.selected_group_size} score: {group_size_score}")
            self.calculated_scores[listing.property_id] = self.calculated_scores[listing.property_id] + group_size_score

        

    #HELPER METHODS
    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False



listing_1 = {
    
        "property_id": 1,
        "location": "Blue Mountain, Ontario",
        "type": "cabin",
        "price_per_night": 230,
        "features": ["mountain view", "fireplace", "ski-in/ski-out", "wifi"],
        "tags": ["mountains", "remote", "adventure"],
        "guest_capacity": 4,
        'unavailable_dates': [
            (date(2025, 8, 15), date(2025, 8, 20)), 
            (date(2025, 10 ,21), date(2025, 10, 23))
            ]


    }


listing_2 = {
    "property_id": 2,
    "location": "103 Ocean Street West",
    "type": "Apartment",
    "price_per_night": 65,
    "features": ["furnished", "on the beach", "open concept"],
    "tags": ["cozy", "seaside"],
    'guest_capacity': 2,
    'unavailable_dates': [
        (date(2025, 8, 16), date(2025, 8, 17)),
        (date(2025, 8, 14), date(2025, 8, 14)),
        (date(2025, 9, 20), date(2025, 9, 20)),
        (date(2025, 10, 1), date(2025, 10, 1))
    ]
}

listing_3 = {
    "property_id": 3,
    "location": "Niagara-on-the-Lake, Ontario",
    "type": "guesthouse",
    "price_per_night": 95,
    "features": ["wine country view", "garden", "wifi", "bike rentals"],
    "tags": ["romantic", "wine", "culture"],
    'guest_capacity': 2,
    'unavailable_dates': [
        (date(2025, 9, 15), date(2025, 9, 15)),
        (date(2025, 9, 30), date(2025, 9, 30)),
        (date(2025, 12, 3), date(2025, 12, 3)),
        (date(2025, 12, 20), date(2025, 12, 20))
    ]
}

listing_4 = {
    "property_id": 4,
    "location": "Tobermory, Ontario",
    "type": "cottage",
    "price_per_night": 125,
    "features": ["lake view", "kayak included", "fire pit", "wifi"],
    "tags": ["nature", "waterfront", "hiking"],
    'guest_capacity': 3,
    'unavailable_dates': [
        (date(2025, 10, 11), date(2025, 10, 13)),
        (date(2025, 12, 24), date(2025, 12, 26))
    ]
}

listing_5 = {
    "property_id": 5,
    "location": "Toronto, Ontario",
    "type": "apartment",
    "price_per_night": 180,
    "features": ["central location", "gym access", "rooftop view", "wifi"],
    "tags": ["city", "nightlife", "foodie"],
    'guest_capacity': 4,
    'unavailable_dates': [
        (date(2025, 11, 19), date(2025, 11, 21)),
        (date(2025, 11, 27), date(2025, 11, 28))
    ]
}

listing_6 = {
    "property_id": 6,
    "location": "Blue Mountain, Ontario",
    "type": "loft",
    "price_per_night": 660,
    "features": ["mountain view", "balcony", "wifi", "hot tub"],
    "tags": ["mountains", "luxury", "ski"],
    'guest_capacity': 8,
    'unavailable_dates': [
        (date(2025, 10, 5), date(2025, 10, 5))
    ]
}

listing_7 = {
    "property_id": 7,
    "location": "Wasaga Beach, Ontario",
    "type": "villa",
    "price_per_night": 200,
    "features": ["private pool", "beachfront", "AC", "wifi"],
    "tags": ["beach", "luxury", "family"],
    'guest_capacity': 4,
    'unavailable_dates': [
        (date(2025, 10, 17), date(2025, 10, 18)),
        (date(2025, 12, 19), date(2025, 12, 20))
    ]
}

listing_8 = {
    "property_id": 8,
    "location": "Niagara-on-the-Lake, Ontario",
    "type": "cottage",
    "price_per_night": 350,
    "features": ["garden", "bike rentals", "fire pit", "wifi"],
    "tags": ["romantic", "nature", "wine"],
    'guest_capacity': 2,
    'unavailable_dates': [
        (date(2025, 9, 12), date(2025, 9, 13)),
        (date(2026, 1, 1), date(2026, 1, 2)),
        (date(2026, 1, 26), date(2026, 1, 26))
    ]
}

listing_9 = {
    "property_id": 9,
    "location": "Tobermory, Ontario",
    "type": "tiny house",
    "price_per_night": 90,
    "features": ["lake view", "hiking trails nearby", "BBQ", "wifi"],
    "tags": ["budget", "nature", "waterfront"],
    'guest_capacity': 3,
    'unavailable_dates': [
        (date(2025, 12, 3), date(2025, 12, 3)),
        (date(2025, 12, 19), date(2025, 12, 19)),
        (date(2025, 12, 31), date(2025, 12, 31)),
        (date(2026, 2, 2), date(2026, 2, 2))
    ]
}

listing_10 = {
    "property_id": 10,
    "location": "Toronto, Ontario",
    "type": "studio",
    "price_per_night": 150,
    "features": ["central location", "AC", "wifi", "workspace"],
    "tags": ["city", "business", "solo travel"],
    'guest_capacity': 2,
    'unavailable_dates': [
        (date(2025, 11, 11), date(2025, 11, 11)),
        (date(2025, 11, 20), date(2025, 11, 20)),
        (date(2025, 12, 4), date(2025, 12, 4))
    ]
}

listing_11 = {
    "property_id": 11,
    "location": "Muskoka, Ontario",
    "type": "cottage",
    "price_per_night": 770,
    "features": ["lakefront", "canoe included", "fire pit", "wifi"],
    "tags": ["nature", "waterfront", "family"],
    'guest_capacity': 10,
    'unavailable_dates': [
        (date(2025, 12, 12), date(2025, 12, 12)),
        (date(2025, 12, 23), date(2025, 12, 24)),
        (date(2025, 12, 28), date(2025, 12, 28))
    ]
}

listing_12 = {
    "property_id": 12,
    "location": "Prince Edward County, Ontario",
    "type": "guesthouse",
    "price_per_night": 130,
    "features": ["wine country view", "garden", "wifi", "pet friendly"],
    "tags": ["romantic", "wine", "pet friendly"],
    'guest_capacity': 2,
    'unavailable_dates': [
        (date(2025, 12, 11), date(2025, 12, 11)),
        (date(2026, 3, 1), date(2026, 3, 1)),
        (date(2026, 3, 10), date(2026, 3, 10))
    ]
}

listing_13 = {
    "property_id": 13,
    "location": "Ottawa, Ontario",
    "type": "apartment",
    "price_per_night": 120,
    "features": ["central location", "balcony", "wifi", "parking"],
    "tags": ["city", "history", "budget"],
    'guest_capacity': 3,
    'unavailable_dates': [
        (date(2025, 10, 9), date(2025, 10, 9)),
        (date(2025, 10, 11), date(2025, 10, 11)),
        (date(2025, 11, 14), date(2025, 11, 14))
    ]
}

listing_14 = {
    "property_id": 14,
    "location": "Algonquin Park, Ontario",
    "type": "cabin",
    "price_per_night": 110,
    "features": ["forest view", "canoe included", "fire pit", "wifi"],
    "tags": ["nature", "hiking", "remote"],
    'guest_capacity': 2,
    'unavailable_dates': [
        (date(2025, 10, 18), date(2025, 10, 19)),
        (date(2025, 11, 29), date(2025, 11, 29))
    ]
}

listing_15 = {
    "property_id": 15,
    "location": "Kingston, Ontario",
    "type": "loft",
    "price_per_night": 540,
    "features": ["waterfront view", "balcony", "wifi", "downtown access"],
    "tags": ["city", "romantic", "history"],
    'guest_capacity': 6,
    'unavailable_dates': [
        (date(2025, 12, 3), date(2025, 12, 5)),
        (date(2025, 12, 8), date(2025, 12, 9)),
        (date(2025, 12, 31), date(2025, 12, 31))
    ]
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

recommender = ListingRecommender(property_obj_list)
recommender.prompt_tag()
print('TESTING -----------', recommender.selected_tag)
recommender.calculate_tag_score()
print('TESTING -----------', recommender.calculated_scores)
recommender.reset_selection()
print('resetted -----------', recommender.selected_group_size)
recommender.reset_scores()
print('resetted -----------', recommender.calculated_scores)



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

# bunlar kaliyor
# trial_user_input_tag = input('What are you searching for?')
# trial_user_input_group_size = int(input('What is your group size?'))
# trial_start_date = input('When is your check-in date?')
# trial_end_date = input('When is your check-out date?')
#ask for the flex. dates 

# trial_start_date = datetime.strptime(trial_start_date, "%Y-%m-%d").date()
# trial_end_date = datetime.strptime(trial_end_date, "%Y-%m-%d").date()

print("-"*50)

# Calculate weighted Tag Score --> for now no matches score 0 but we need to define correlations in our tags pool

# Calculate weighted Price Score --> in the range fixed score out of the range 


# Calculate weighted group size


# Calculate weighted date availability score
