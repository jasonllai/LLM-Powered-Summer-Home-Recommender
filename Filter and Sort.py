import json
from datetime import datetime, timedelta
from Functions import Property

# function that takes in a json file of properties and filters them according to user inputted attributes and returns a subset of the original 
# properties that meets the filtering criteria as a list of Property objects
def filter_properties(props_json, group_size=None, min_price=None, max_price=None, features=None, tags=None, prop_type=None, location=None, 
                      start_date=None, end_date=None):
    # reads properties from json as list of dictionaries
    with open(props_json, "r") as f:
        loaded_properties = json.load(f)

    # checking for properties that are an exact match for the user provided filters
    filtered = loaded_properties
    if group_size is not None: 
        filtered = [p for p in filtered if p["Guest Capacity"] >= group_size]
    if min_price is not None:
        filtered = [p for p in filtered if p["Price per Night"] >= min_price]
    if max_price is not None:
        filtered = [p for p in filtered if p["Price per Night"] <= max_price]
    if features is not None:
        filtered = [p for p in filtered if set(features).issubset(p["Features"])]
    if tags is not None:
        filtered = [p for p in filtered if set(tags).issubset(p["Tags"])]
    if prop_type is not None:
        filtered = [p for p in filtered if p["Property Type"] == prop_type]
    if location is not None:
        filtered = [p for p in filtered if p["Property Location"] == location]
    # filter on the provided dates if the user enters at least one date to filter on
    if ((start_date or end_date) != None): 
        if start_date: 
            start_date = start_date = datetime.strptime(start_date, "%Y-%m-%d").date() # convert user's start date into date type
        if end_date: 
            end_date = end_date = datetime.strptime(end_date, "%Y-%m-%d").date() # convert user's end date into date type
        # if no end date was provided, automatically set end date to be a week after the start date
        else:
            end_date = start_date + timedelta(days=7) 
        # if no start date was provided, automatically set start date to be a week before the end date
        if end_date and not start_date:
            start_date = end_date - timedelta(days=7) 
        # creating a list of all dates between start and end date
        date_range = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end_date - start_date).days + 1)] 
        filtered = [p for p in filtered if not set(p["Unavailable Dates"]).issubset(date_range)]

    # convert properties that meet all filter attributes to a list of Property objects to be returned
    filtered_props = [Property.from_dict(prop) for prop in filtered]
    return filtered_props


# function that sorts a given list of Property objects based on a user inputed sorting attribute and returns the 
# list of Property objects, now sorted, the sorting attribute must be formatted to be lowercase with underscores (i.e. 'guest_capacity'), 
# also have the option to put into descending order using ascending parameter
def sort_properties_aslist(props_list, attribute, asc=True):
    return sorted(props_list, key=lambda x: getattr(x, attribute), reverse=not asc)


# similarly, this function sorts a given json file containing properties as dictionaries based on a user inputed sorting attribute and
# returns a list of dictionaries, the sorting attribute must be formatted to be capitalized with spaces (i.e. "Property Location"), also 
# have the option to put into descending order using ascending parameter
def sort_properties_asjson(props_json, attribute, asc=True):
    with open(props_json, "r") as f:
        loaded_properties = json.load(f) # reads props from json file as list of dicts 
    sorted_properties = sorted(loaded_properties, key=lambda x: x[attribute], reverse=not(asc)) # sort the list of dictionaries
    return sorted_properties