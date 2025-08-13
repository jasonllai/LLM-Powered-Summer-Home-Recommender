from Testing import users_obj_list, property_obj_list

print("-"*100)


import numpy as np
# print(np.__version__)

deneme = np.array([[3,0],[4,0]])
#print(np.vectorize(deneme))
distance = np.linalg.norm(deneme[0]-deneme[1])

print(distance)

print("-"*50)

# Defining weights for each feature


# Defining a function that gives scores to properties according to user information

def score_property_for_user(user, prop):
    score_for_budget = 0
    score_for_preferred_environment = 0
    score_for_group_size = 0
    score_for_avail_dates = 0
    
    # Match preferred environment with tags
    if user.preferred_environment.lower() in [tag.lower() for tag in prop.tags]:
        score_for_preferred_environment = 3
    
    # Check if the property price fits user's budget range
    if user.budget_range[0] <= prop.price_per_night <= user.budget_range[1]:
        score_for_budget = 2
    
    # Check if the group size fits the property's capacity so we need to DEFINE CAPACITY IN PROPERTY CLASS
    
    '''
     if user.group_size <= prop.capacity:
        score_for_group_size = 2
    '''
    # Check availability based on travel dates so we need to DEFINE AVAIL DATES IN PROPERTY CLASS
    '''
    if user.travel_dates[0] <= prop.available_date
        score_for_avail_dates = 2
    '''
    
    return score_for_budget, score_for_preferred_environment, score_for_group_size, score_for_avail_dates


# Scoring all user-property combinations
'''
for user in users_obj_list:
    print(f"\nUser: {user.name}")
    for prop in property_obj_list:
        print(f"Property {prop.property_id}: {score_property_for_user(user, prop)} points")
'''
'''
for x in users_obj_list:
    print(x.preferred_environment)

# Checking if the preferred environment is in the tag list in properties

for user in users_obj_list:
    for prop in property_obj_list:
        # Checking for a match between preferred_environment and the tags list
        if user.preferred_environment.lower() in [tag.lower() for tag in prop.tags]:
            print(f"{user.name} ({user.preferred_environment}) -> Property {prop.property_id} ({prop.location}) eşleşti")
'''

