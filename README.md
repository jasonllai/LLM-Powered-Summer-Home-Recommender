# LLM-Powered Summer Home Recommender

A Python-based recommendation system for summer home rentals that matches users with properties based on their preferences, budget, and group size.

## 🏠 Features

- **Property Management**: Comprehensive property listings with detailed information including location, type, price, features, and tags
- **User Profiles**: User management system with preferences, budget constraints, and group size requirements
- **Smart Matching**: Algorithm to match users with suitable properties based on budget and preferences
- **Ontario Focus**: Specialized in Ontario summer destinations including Blue Mountain, Niagara-on-the-Lake, Tobermory, and more

## 📋 Property Types Available

- Cabins
- Apartments
- Guesthouses
- Cottages
- Lofts
- Villas
- Tiny Houses
- Studios

## 🏖️ Destinations Covered

- Blue Mountain, Ontario
- Niagara-on-the-Lake, Ontario
- Tobermory, Ontario
- Toronto, Ontario
- Wasaga Beach, Ontario
- Muskoka, Ontario
- Prince Edward County, Ontario
- Ottawa, Ontario
- Algonquin Park, Ontario
- Kingston, Ontario

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/LLM-Powered-Summer-Home-Recommender.git
cd LLM-Powered-Summer-Home-Recommender
```

2. Install dependencies (if any):
```bash
pip install -r requirements.txt
```

## 💻 Usage

Run the main application:
```bash
python Testing.py
```

The application will:
1. Display all available properties
2. Show user profiles
3. Demonstrate the matching algorithm

## 🏗️ Project Structure

```
LLM-Powered-Summer-Home-Recommender/
├── Testing.py          # Main application with property listings and user matching
├── Users.py            # User management module
├── README.md           # Project documentation
├── requirements.txt    # Python dependencies
└── .gitignore         # Git ignore rules
```

## 🧩 Core Classes

### Property Class
- `property_id`: Unique identifier
- `location`: Property location
- `type`: Type of accommodation
- `price_per_night`: Nightly rate
- `features`: List of amenities
- `tags`: Property characteristics

### User Class
- `user_id`: Unique identifier
- `name`: User's name
- `group_size`: Number of travelers
- `preferred_environment`: Preferred setting (beach, mountains, city, etc.)
- `budget`: Maximum budget per night

## 🔍 Matching Algorithm

The system matches users with properties based on:
- Budget compatibility (`property.price_per_night <= user.budget`)
- Future enhancements can include environment preferences and group size considerations

## 🛠️ Development

This project is designed to be easily extensible. You can:
- Add more properties to the `property_listings` array
- Create new user profiles in the `users_list` array
- Enhance the matching algorithm in the `User.matches()` method
- Add new features and tags to properties

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you have any questions or need help, please open an issue on GitHub.
