from datetime import datetime, timedelta, date
import pandas as pd
from difflib import get_close_matches, SequenceMatcher
import json 

class ListingRecommender():
    def __init__(self):
        with open('data/Properties.json', 'r') as properties:
            self.property_list = json.load(properties)
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
        self.corr_df = corr_df

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
        for prop in self.property_list:
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
                "features": ", ".join(prop.get("features", [])),
                "total_score": round(tag_score + group_size_score + price_score,2)
        })
        # Sorting by descending order and choose top 20
        recommender_output = sorted(rows, key = lambda x: x['total_score'],reverse = True)[:20]
        return recommender_output



#Example usage
with open('data/Users.json', 'r') as users:
    users_list = json.load(users)

active_user_id = 1
for user in users_list:
    if user["user_id"] == active_user_id:
        active_user = user
        break
    
recommender = ListingRecommender()
property_listing_calculated_scores = recommender.calculate_total_score(active_user)
print('#' * 50)
# print(property_listing_calculated_scores)
print('#' * 50)

properties_df = pd.DataFrame(property_listing_calculated_scores)
properties_df["tags"] = properties_df["tags"].apply(lambda x: [tag.strip() for tag in x.split(",")])
properties_df = properties_df.drop(columns=["total_score"])
properties_df["property_index"] = properties_df.index
print(properties_df[["location", "type", "price_per_night", "guest_capacity", "tags"]])