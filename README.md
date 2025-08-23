# LLM-Powered Summer Home Recommender

A Python-based recommendation system for summer home rentals. It matches users with properties based on travel dates, preferences, budget, and group size, enhanced with AI-powered suggestions.


## 🏠 Features
-**Admin Portal**: 

  Property Management: add, edit, or delete property listings.


-**User Portal**:  

  **User Profile Management**: sign in, set your preferences (budget, group size, preferred environment) and password, and update user profile anytime.  

  **Property Recommendations**: see your top 20 suggested properties, further filter by price, group size, location, tags, or dates, and book a property.

  **AI Travel Guide**: get fun, AI-generated suggested activities, e.g., “Perfect mountain cabin trip for 4 friends under $200/night.”

## 🔍 Property Recommendation Logic

Each property is scored based on the user's profile — how close the price is to the user’s budget, how well the property’s guest capacity matches the user’s group size, and whether the property matches the user’s preferred environment. 

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/jasonllai/LLM-Powered-Summer-Home-Recommender.git
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
