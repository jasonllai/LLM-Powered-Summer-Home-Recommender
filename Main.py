def main():
    print("Welcome to the Summer Home Recommender App!")
    print("If you are a user, type [u]")
    print("If you are an administrator, type [a]")
    choice = input("Please select between [u] and [a]: ")

    if choice == "u":
        print("Welcome user!")
    
    elif choice == "a":
        print("Welcome administrator!")

    else:
        print("Invalid choice. Exiting.")
        return

main()