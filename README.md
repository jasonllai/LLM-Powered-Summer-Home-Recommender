# LLM-Powered Summer Home Recommender

A Python-based recommendation system for summer home rentals. It matches users with properties based on travel dates, preferences, budget, and group size, enhanced with AI-powered suggestions.

## 🏠 Features
-**Admin Portal**: 

  Property Management: add, edit, or delete property listings.


-**User Portal**:  

  **User Profile Management**: sign in, set your preferences (budget, group size, preferred environment) and password, and update user profile anytime.  

  **Property Recommendations**: see your top 20 suggested properties, further filter by price, group size, location, tags, or dates, and book a property.

  **AI Travel Guide**: get fun, AI-generated suggested activities, e.g., "Perfect mountain cabin trip for 4 friends under $200/night."

## 🔍 Property Recommendation Logic

Each property is scored based on the user's profile — how close the price is to the user's budget, how well the property's guest capacity matches the user's group size, and whether the property matches the user's preferred environment. 

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/jasonllai/LLM-Powered-Summer-Home-Recommender.git
cd LLM-Powered-Summer-Home-Recommender
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

Run the main application:
```bash
python Main.py
```

The application will:
1. Start the web server
2. Provide access to the user and admin portals
3. Enable property recommendations and management

## 🏗️ Project Structure

```
LLM-Powered-Summer-Home-Recommender/
├── 📁 Core Application
│   ├── Main.py                    # Main application entry point
│   ├── server.py                  # Web server and API endpoints
│   ├── rental_management.py       # Property and rental management logic
│   ├── Recommender_Logic.py       # Core recommendation algorithms
│   ├── LLM_functions.py          # AI/LLM integration functions
│   ├── filter.py                  # Property filtering utilities
│   └── utils.py                   # General utility functions
│
├── 📁 Data
│   ├── Properties.json            # Property listings and details
│   ├── Users.json                 # User profiles and preferences
│   └── Admin.json                 # Admin account information
│
├── 📁 Frontend (GUI)
│   ├── index.html                 # Landing page
│   ├── login.html                 # User login page
│   ├── register.html              # User registration page
│   ├── profile.html               # User profile management
│   ├── search.html                # Property search interface
│   ├── dashboard.html             # User dashboard
│   ├── admin-login.html           # Admin login page
│   ├── admin.html                 # Admin dashboard
│   └── 📁 assets/
│       ├── app.js                 # Frontend JavaScript logic
│       ├── style.css              # Styling and CSS
│       └── 📁 img/                # Image assets
│
├── 📁 Testing
│   └── test_llm_functions.py      # Unit tests for LLM functions
│
├── 📄 Configuration
│   ├── requirements.txt           # Python dependencies
│   ├── .gitignore                # Git ignore rules
│   └── README.md                 # Project documentation
```

## 🔧 Key Components

### Core Application
- **Main.py**: Application entry point and initialization
- **server.py**: Flask web server with REST API endpoints
- **rental_management.py**: Property CRUD operations and rental logic
- **Recommender_Logic.py**: Core recommendation scoring algorithms
- **LLM_functions.py**: AI-powered features and suggestions
- **filter.py**: Advanced property filtering capabilities
- **utils.py**: Helper functions and utilities

### Data Layer
- **Properties.json**: Comprehensive property database with details, pricing, and availability
- **Users.json**: User profiles, preferences, and booking history
- **Admin.json**: Administrative accounts and permissions

### Frontend
- **HTML Pages**: Complete user interface for both users and admins
- **JavaScript (app.js)**: Interactive frontend functionality
- **CSS (style.css)**: Modern, responsive styling
- **Images**: Visual assets for the application

## 🛠️ Development

This project is designed to be easily extensible. You can:
- Add more properties to the `data/Properties.json` file
- Create new user profiles in the `data/Users.json` file
- Enhance the matching algorithm in the `Recommender_Logic.py` module
- Add new features and tags to properties
- Extend the LLM functionality in `LLM_functions.py`
- Customize the frontend in the `GUI/` directory

## Setup

### 1) Python environment
```bash
cd /Users/superman/Desktop/UofT/Python/Rental_Project/SummerHome
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 2) Environment variables (LLM features)
Set this if you want to use the AI assistant or auto‑generate properties. The backend imports the AI module at startup and requires a key.
```bash
export OPENROUTER_API_KEY="your_api_key_here"
```

If you don’t have a key yet, you can still run the backend and frontend by temporarily removing AI usage, but by default the backend expects the key to be set.

---

## Run

### Start the backend (Flask API)
```bash
source .venv/bin/activate
python -m backend.app
# Server runs at http://127.0.0.1:5050
```

### Open the frontend (static)
Option A: Open the HTML directly (e.g., `frontend/index.html`).

Option B: Serve statically (recommended):
```bash
python -m http.server -d frontend 8080
# Then open http://127.0.0.1:8080 in your browser
```

The frontend is preconfigured to call the backend at `http://127.0.0.1:5050`.

### CLI demo (optional)
```bash
python -m scripts.cli
```

---

## API Overview

Base URL: `http://127.0.0.1:5050`

### Auth & Profile
- `POST /register` → create user
  - body: `{ userId, name, password, preferredEnv, budgetRange:[min,max], groupSize }`
- `POST /login` → user login
  - body: `{ userId, password }`
- `POST /profile` → get user profile
  - body: `{ userId }`
- `POST /profile/update` → update partial fields
  - body: subset of `{ userId, name, password, preferredEnv, budgetRange:[min,max], groupSize }`
- `POST /account/delete` → delete user and reconcile property availability
  - body: `{ userId }`

### Recommendations & Search
- `POST /recommend` → top‑20 recommended properties for a user
  - body: `{ userId }`
- `POST /search` → filtered properties
  - body (all optional): `{ location, propType, minPrice, maxPrice, groupSize, features:[...], tags:[...], startDate, endDate }`

### Booking
- `POST /booking/create` → create booking
  - body: `{ userId, propertyId, start, end }` with dates `YYYY-MM-DD`
- `POST /booking/delete` → delete a booking
  - body: `{ userId, propertyId, start, end }`

### Admin
- `POST /admin/login` → admin login: `{ userId, password }`
- `POST /admin/users` → list users + bookings
- `POST /admin/properties` → list properties
- `POST /admin/property/create` → create property
  - body: `{ location, type, price_per_night, guest_capacity, features:[...], tags:[...] }`
- `POST /admin/property/update` → update property
  - body: `{ property_id, location, type, price_per_night, guest_capacity, features:[...], tags:[...], [unavailable_dates] }`
- `POST /admin/property/delete` → delete property
  - body: `{ propertyId }`
- `POST /admin/properties/generate` → generate N properties via LLM
  - body: `{ n }`

### AI Assistant
- `POST /assistant` → travel blurb/ideas
  - body: `{ user_input, messages }` (messages optional for chat continuity)

---


## How it works

- Recommender (`backend/domain/recommender.py`):
  - Scores listings by tag affinity to the user’s preferred environment, budget fit, and capacity match, then returns top 20.
- Filters (`backend/domain/filters.py`):
  - Applies field equality/inclusion checks and optional availability window logic.
- Domain (`backend/domain/rental_management.py`):
  - Users/properties/bookings CRUD and date consistency; persists into JSON files in `data/`.
- AI (`backend/ai/service.py`):
  - Uses OpenRouter for both chat suggestions and structured property generation with strict schema and coherence constraints.

---

## Notes
- Data is stored in `data/*.json` for simplicity. For production, consider a database and proper auth.
- CORS is enabled in the backend for local development.
- The frontend points to `http://127.0.0.1:5050`; change `API_BASE` in `frontend/assets/app.js` if needed.



## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you have any questions or need help, please open an issue on GitHub.
