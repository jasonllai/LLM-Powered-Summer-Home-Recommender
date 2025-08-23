# Helper functions for main()

# Check if the user input is a valid string from the given list of string
def get_string_input(prompt, options_list):
    while True:
        user_input = input(prompt).strip()
        if user_input not in options_list:
            print("Invalid choice!")

        else:
            return user_input

# Check if the user's input is an integer; If true, returns the user input as an integer
def get_int_input(prompt):
    while True:
        user_input = input(prompt).strip()
        try:
            return int(user_input)
        except ValueError:
            print("Invalid input. Please enter an integer.")

# Check if the user input is from a given list of string; While true, returns the comma-separated strings as a list of strings
def get_string_list_input(prompt, options_list):
    """Prompt the user for a comma-separated list of strings from allowed_values (no duplicates)."""
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            return []  # allow empty input if user presses Enter

        # Split and normalize
        items = [item.strip().lower() for item in user_input.split(",")]

        # Remove duplicates while preserving order
        seen = set()
        unique_items = []
        for item in items:
            if item not in seen:
                seen.add(item)
                unique_items.append(item)

        # Check validity
        invalid_items = [item for item in unique_items if item not in options_list]
        if invalid_items:
            print(f"Invalid choices: {', '.join(invalid_items)}. Allowed values are: {', '.join(options_list)}")
        else:
            return unique_items
