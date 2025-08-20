from datetime import datetime, timedelta, date
import pandas as pd
from difflib import get_close_matches, SequenceMatcher
import json 

class ListingRecommender():
    def __init__(self, property_lst):
        # Tags correlation table
        tags_pool = ["mountains", "remote", "adventure", "beach", "city", "lake", 
                    "river", "ocean", "forest", "park", "national park", "state park", 
                    "national forest", "state forest", "modern","rustic","historic",
                    "family-friendly","kid-friendly","pet-friendly","romantic","business-travel",
                    "nightlife","eco-friendly","spa","golf","foodie","farm-stay","glamping","long-term"]

        correlation_table = {
            "beach": [0.1,0.2,0.3,1.0,0.3,0.2,0.2,0.8,0.1,0.3,0.2,0.2,0.1,0.1,0.2,0.2,0.2,0.1,0.1,0.1,0.4,0.1,0.5,0.3,0.5,0.3,0.2,0.2,0.1,0.2],
            "lake": [0.1,0.1,0.1,0.2,0.2,1.0,0.7,0.3,0.6,0.2,0.3,0.2,0.7,0.6,0.1,0.3,0.4,0.1,0.1,0.1,0.2,0.2,0.1,0.2,0.2,0.1,0.2,0.4,0.3,0.3],
            "forest": [0.9,0.4,0.7,0.1,0.1,0.6,0.5,0.1,1.0,0.4,0.6,0.5,0.9,0.8,0.1,0.5,0.6,0.1,0.1,0.1,0.1,0.1,0.2,0.2,0.2,0.2,0.5,0.4,0.3,0.3],
            "mountains": [1.0,0.2,0.7,0.1,0.1,0.1,0.1,0.1,0.9,0.2,0.3,0.2,0.8,0.7,0.1,0.5,0.6,0.1,0.1,0.1,0.1,0.1,0.2,0.2,0.1,0.2,0.6,0.5,0.3,0.4],
            "nightlife": [0.2,0.1,0.2,0.3,0.1,0.1,0.1,0.3,0.2,0.2,0.2,0.2,0.2,0.2,0.1,0.1,0.1,0.1,0.1,0.1,0.3,0.2,1.0,0.2,0.5,0.3,0.1,0.1,0.2,0.2],
            "remote": [0.2,1.0,0.5,0.2,0.1,0.1,0.1,0.1,0.4,0.2,0.2,0.2,0.4,0.3,0.1,0.3,0.3,0.1,0.1,0.1,0.2,0.1,0.1,0.2,0.1,0.1,0.3,0.2,0.2,0.3],
            "glamping": [0.3,0.3,0.3,0.1,0.1,0.2,0.2,0.1,0.3,0.1,0.2,0.2,0.3,0.3,0.3,0.2,0.2,0.1,0.1,0.1,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,1.0,0.2],
            "city": [0.1,0.1,0.1,0.3,1.0,0.2,0.2,0.2,0.1,0.3,0.1,0.1,0.1,0.1,0.7,0.3,0.2,0.1,0.1,0.1,0.5,0.8,0.6,0.1,0.6,0.6,0.6,0.1,0.1,0.2],
            "modern": [0.1,0.1,0.1,0.2,0.7,0.1,0.1,0.2,0.1,0.2,0.2,0.2,0.1,0.1,1.0,0.4,0.3,0.1,0.1,0.3,0.4,0.6,0.1,0.2,0.5,0.3,0.1,0.1,0.3,0.3],
            "historic": [0.6,0.3,0.5,0.2,0.2,0.4,0.4,0.2,0.6,0.2,0.3,0.3,0.6,0.5,0.3,0.6,1.0,0.1,0.1,0.2,0.3,0.2,0.1,0.2,0.2,0.2,0.3,0.3,0.2,0.3],
        }

        # Creating correlation data frame with zeros
        corr_df = pd.DataFrame(0.0, index=tags_pool, columns=tags_pool)

        # Fill rows from correlation_table (pad/truncate to tags_pool length)

        for tag, row in correlation_table.items():
        # Making sure each row has the same length as our tags_pool. Our rows in correlation_table are shorter than tags_pool, so we pad them with zeros. Truncation is just a safeguard.
        # So actually only row + [0.0] * (len(tags_pool)-len(row)) is running
            if tag in corr_df.index:
                r = (row + [0.0]*(len(tags_pool)-len(row)))[:len(tags_pool)]
                corr_df.loc[tag] = r

        # Set self-correlation = 1 for every tag
        for t in tags_pool:
            corr_df.loc[t, t] = 1.0

        self.property_lst = property_lst
        self.corr_df = corr_df

        self.calculated_scores = {}
        for listing in property_lst:
            self.calculated_scores[listing.get('property_id')] = 0

        self.selected_group_size = 0
        self.selected_minimum_budget = 0
        self.selected_maximum_budget = 0
        self.selected_tag = ""
        #self.selected_start_date = ""
        #self.selected_end_date = ""

        self.budget_score = 0
        self.tag_score = 0
        self.group_size_score = 0
        #self.date_score = 0

    def reset_all(self):
        for listing in self.property_lst:
            self.calculated_scores[listing.get('property_id')] = 0 

        self.selected_group_size = 0
        self.selected_minimum_budget = 0
        self.selected_maximum_budget = 0
        self.selected_tag = ""
        #self.selected_start_date = ""
        #self.selected_end_date = ""

    def reset_selection(self):
        self.selected_group_size = 0
        self.selected_minimum_budget = 0
        self.selected_maximum_budget = 0
        self.selected_tag = ""
        #self.selected_start_date = ""
        #self.selected_end_date = ""
    
    def reset_scores(self):
        for listing in self.property_lst:
            self.calculated_scores[listing.property_id] = 0 
    
    def prompt_tag(self):
        while True:
            self.selected_tag = input("What are you searching for: ").strip().lower()
            if not self.selected_tag:
                if self.selected_tag or len(self.selected_tag) == 0:
                    print("Please enter at least one tag.")
                    continue
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

    def calculate_tag_score(self, active_user, property_tags):
        # If the user has no preferred tag or the listing has no tags, return score 0
        preferred_tag = active_user["preferred_environment"]
        if not preferred_tag or not property_tags:
            return 0.0

        # Normalize the preferred tag (strip spaces, lowercase)
        normalized_preferred = preferred_tag.strip().lower()

        # First checking for exact matches
        for lt in property_tags:
            if normalized_preferred == lt.strip().lower():
                return 1.0

        # If no exact match found, look for correlations. Correlation matrix is asymmetric: row = preferred environment of user, column = listing tag
        best_correlation = 0
        for property_tag in property_tags:
            normalized_property_tag = lt.strip().lower()
            if normalized_preferred in self.corr_df.index and normalized_property_tag in self.corr_df.columns:
                v = float(self.corr_df.loc[normalized_preferred, normalized_property_tag])
                if v > best_correlation:
                    best_correlation = v # Here we keep the maximum correlation score by listing
        # Returning the tag_score            
        return round(best_correlation, 3)

    def calculate_budget_score(self, active_user, price):
        price_score = 0
        budget = active_user.get("budget_range")
        min_budget, max_budget = map(float, budget)
        if min_budget <= price <= max_budget:
            price_score = 3 # if the property price per night is within the user's budget return the highest score which is 3
        elif price < min_budget:
            price_difference = 1 - ((min_budget - price) / min_budget)
            price_score = max(0, round(price_difference * 3, 2))
        else: # if the property price per night is higher than the user's budget
            price_difference = 1 - ((price - max_budget) / max_budget)
            price_score = max(0, round(price_difference * 3, 2))
        return price_score

    def calculate_group_size_score(self, active_user, capacity):
        group_size_score = 0
        group_size = active_user.get("group_size")
        if group_size == capacity:
            group_size_score = 3
        elif group_size > capacity:
            group_size_score = 0
        else:
            group_size_score = round(3 - ((3 / capacity) * (capacity - group_size)), 2)
        return group_size_score

    def calculate_total_score(self, active_user):
        rows = []
        for prop in self.property_lst:
            tag_score = self.calculate_tag_score(active_user, prop.get("tags", []))

            capacity = prop.get("guest_capacity", 0)
            group_size_score = self.calculate_group_size_score(active_user, capacity)

            price = prop.get("price_per_night", 0)
            price_score = self.calculate_budget_score(active_user, price)

            rows.append({
                "property_id": prop["property_id"],
                "location": prop.get("location", ""),
                "type": prop.get("type", ""),
                "price_per_night": price,
                "guest_capacity": prop.get("guest_capacity"),
                "tags": ", ".join(prop.get("tags", [])),
                "total_score": tag_score + group_size_score + price_score
        })
        # Sorting by descending order and choose top 20
        recommender_output = sorted(rows, key = lambda x: x['total_score'],reverse = True)[:20]
        return recommender_output


with open('data/Users.json', 'r') as users:
    users_list = json.load(users)

with open('data/Properties.json', 'r') as properties:
    property_list = json.load(properties)


'''
active_user_id = 1
for user in users_list:
    if user["user_id"] == active_user_id:
        active_user = user
        break
preferred_tag = active_user["preferred_environment"]
print(preferred_tag)
'''

recommender = ListingRecommender(property_list)
property_listing_calculated_scores = recommender.calculate_total_score(active_user)
print('#' * 50)
print(property_listing_calculated_scores)
print('#' * 50)