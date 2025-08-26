import json
from datetime import datetime, timedelta
from rental_management import Property, validate_date, load_data_from_json

# function that filters all properties from json file according to user inputted attributes and returns a subset of the original 
# properties that meets the filtering criteria fromatted as a list of dictionaries
def filter_properties(group_size=None, min_price=None, max_price=None, features=None, tags=None, prop_type=None, location=None, 
                      start_date=None, end_date=None):
    # reads properties from json as list of dictionaries
    loaded_properties = load_data_from_json("data/Properties.json")

    # checking for properties that are an exact match for the user provided filters
    filtered = loaded_properties
    if group_size is not None: 
        filtered = [p for p in filtered if p["guest_capacity"] >= group_size]
    if min_price is not None:
        filtered = [p for p in filtered if p["price_per_night"] >= min_price]
    if max_price is not None:
        filtered = [p for p in filtered if p["price_per_night"] <= max_price]
    if features is not None:
        filtered = [p for p in filtered if set(features).issubset(p["features"])]
    if tags is not None:
        filtered = [p for p in filtered if set(tags).issubset(p["tags"])]
    if prop_type is not None:
        filtered = [p for p in filtered if p["type"] == prop_type]
    if location is not None:
        filtered = [p for p in filtered if p["location"] == location]
    # filter on the provided dates if the user enters at least one date to filter on
    if start_date or end_date:
        # Validate provided dates
        if start_date and not validate_date(start_date):
            print("Invalid start_date format. Use YYYY-MM-DD.")
            return []
        if end_date and not validate_date(end_date):
            print("Invalid end_date format. Use YYYY-MM-DD.")
            return []

        if start_date and end_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
            if end_dt < start_dt:
                print("end_date must be on or after start_date.")
                return []
        elif start_date and not end_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_dt = start_dt + timedelta(days=7)
        else:  # end_date and not start_date
            end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
            start_dt = end_dt - timedelta(days=7)

        date_range = [(start_dt + timedelta(days=i)).strftime("%Y-%m-%d")
                      for i in range((end_dt - start_dt).days + 1)]
        date_set = set(date_range)

        # Keep properties whose unavailable dates DO NOT intersect requested range
        filtered = [p for p in filtered if set(p.get("unavailable_dates", [])).isdisjoint(date_set)]

    return filtered


# function that sorts a given list of Property objects based on a user inputed sorting attribute and returns the 
# list of Property objects, now sorted, the sorting attribute must be formatted to be lowercase with underscores (i.e. 'guest_capacity'), 
# also have the option to put into descending order using ascending parameter
def sort_properties_aslist(props_list, attribute, asc=True):
    return sorted(props_list, key=lambda x: getattr(x, attribute), reverse=not asc)


# similarly, this function sorts our json file containing properties as dictionaries based on a user inputed sorting attribute and
# returns a list of dictionaries, the sorting attribute must be formatted to be lowercase with underscores (i.e. 'guest_capacity'),  also 
# have the option to put into descending order using ascending parameter
def sort_properties_asjson(attribute, asc=True):
    with open("data/Properties.json", "r") as f:
        loaded_properties = json.load(f) # reads props from json file as list of dicts 
    sorted_properties = sorted(loaded_properties, key=lambda x: x[attribute], reverse=not(asc)) # sort the list of dictionaries
    return sorted_properties