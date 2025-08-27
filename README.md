# LLM-Powered Summer Home Recommender

A Python-based recommendation system for summer home rentals. It matches users with properties based on preferences, budget, and group size, enhanced with AI-powered suggestions.

## Table of Contents
- [Features](#-features)
- [Property Recommendation Logic](#-property-recommendation-logic)
- [Installation](#-installation)
- [Usage (run locally)](#-usage-run-locally)
- [Project Structure](#-project-structure)
- [Key Components](#-key-components)
- [Development](#-development)
- [API Overview](#-api-overview)
- [How it works](#-how-it-works)
- [Notes](#-notes)
- [License](#-license)
- [Support](#-support)

## 🏠 Features
**Admin Portal**
  - Property Management: add, edit, or delete property listings.

**User Portal**
  - **User Profile Management**: sign in, set your preferences (budget, group size, preferred environment) and password, and update user profile anytime.
  - **Property Recommendations**: view your top 20 suggested properties, further filter by price, group size, location, tags, or dates, and book a property.
  - **AI Travel Guide**: get fun, AI-generated suggested activities, e.g., "Perfect mountain cabin trip for 4 friends under $200/night."

## 🔍 Property Recommendation Logic

Each property is scored based on the user's profile — whether the price is within the user's budget, if the property's guest capacity matches the user's group size, and whether the property matches the user's preferred environment. 

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

## 💻 Usage (run locally)

### 1) Create and activate a virtual env
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 2) Set your AI key (required for server to start)
Set this if you want to use the AI assistant or auto‑generate properties. The backend imports the AI module at startup and requires a key.
```bash
export OPENROUTER_API_KEY="your_api_key_here"
```
If you don’t have a key yet, you can still run the backend and frontend by temporarily removing AI usage, but by default the backend expects the key to be set.

### 3) Start the backend (Flask API)
```bash
python server.py
# Server runs at http://127.0.0.1:5050
```

### 4) Open the frontend
Open the static files via a simple HTTP server
```bash
python -m http.server -d GUI 8080
# Then open http://127.0.0.1:8080 in your browser
```
The application will:
1. Start the web server
2. Provide access to the user and admin portals
3. Enable property recommendations and management

Notes:
- Ensure `GUI/assets/app.js` has `API_BASE = "http://127.0.0.1:5050"`.
- Admin/user credentials are stored in `data/Admin.json` and `data/Users.json`.
- `Main.py` is CLI-only; it is not used to run the web app.


### CLI demo (optional)
```bash
python Main.py
```

## 🏗️ Project Structure

```
LLM-Powered-Summer-Home-Recommender/
├── server.py                   # Flask API server (all endpoints: auth, profile, search, bookings, admin, assistant)
├── LLM_functions.py            # LLM prompts + OpenRouter client + data generation helpers
├── Recommender_Logic.py        # Recommendation scoring logic (top-20, etc.)
├── rental_management.py        # Domain: users/properties/bookings CRUD + JSON persistence
├── filter.py                   # Search filtering functions (and sorting as JSON)
├── utils.py                    # Misc utility helpers
├── Main.py                     # CLI utilities/demos (not the web server entry point)
├── requirements.txt            # Python dependencies
├── README.md                   # Project docs
├── .gitignore
│
├── data/                       # App data (JSON stores)
│   ├── Properties.json
│   ├── Users.json
│   └── Admin.json
│
├── GUI/                        # Frontend (static HTML/CSS/JS)
│   ├── index.html              # Landing page (hero carousel)
│   ├── login.html              # User login
│   ├── register.html           # User registration
│   ├── dashboard.html          # User dashboard
│   ├── search.html             # Search + recommendations + AI assistant
│   ├── profile.html            # User profile + booking history
│   ├── admin-login.html        # Admin login
│   └── admin.html              # Admin dashboard (users/properties/LLM generate)
│
├── GUI/assets/
│   ├── app.js                  # Frontend logic (routing/init, UI handlers, AI modal, search rendering)
│   ├── style.css               # Global styles (includes AI assistant and hero carousel)
│   └── img/                    # Landing page carousel images
│       ├── img1.png
│       ├── img2.png
│       ├── img3.png
│       ├── img4.png
│       └── img5.png
│
└── test/
    └── test_llm_functions.py   # Unit tests for LLM helper(s)
```

## 🔧 Key Components

### Core Application
- **Main.py**: Application entry point and initialization
- **server.py**: Flask web server with REST API endpoints
- **rental_management.py**: Property CRUD operations and rental logic
- **Recommender_Logic.py**: Main recommendation scoring algorithms
- **LLM_functions.py**: AI-powered features and suggestions
- **filter.py**: Advanced property filtering capabilities
- **utils.py**: Helper functions and utilities

### Data Layer
- **Properties.json**: Comprehensive property database with details, price, and availability
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




---

## API Overview
Base URL: `http://127.0.0.1:5050`

### Auth & Profile

| Method | Path              | Purpose        |
|--------|-------------------|----------------|
| POST   | `/login`          | User login     |
| POST   | `/register`       | Create user    |
| POST   | `/profile`        | Get profile    |
| POST   | `/profile/update` | Update profile |
| POST   | `/account/delete` | Delete account |

Request/response details remain the same as listed below in your original bullets.

### Recommendations & Search

| Method | Path         | Purpose                 |
|--------|--------------|-------------------------|
| POST   | `/recommend` | Recommended properties  |
| POST   | `/search`    | Filtered property search|

### Booking

| Method | Path              | Purpose        |
|--------|-------------------|----------------|
| POST   | `/booking/create` | Create booking |
| POST   | `/booking/delete` | Delete booking |

### Admin

| Method      | Path                         | Purpose                   |
|-------------|------------------------------|---------------------------|
| POST        | `/admin/login`               | Admin login               |
| GET or POST | `/admin/users`               | Users + recent bookings   |
| POST        | `/admin/properties`          | List properties           |
| POST        | `/admin/property/create`     | Create property           |
| POST        | `/admin/property/update`     | Update property           |
| POST        | `/admin/property/delete`     | Delete property           |
| POST        | `/admin/properties/generate` | Generate properties (LLM) |

### AI Assistant

| Method | Path         | Purpose             |
|--------|--------------|---------------------|
| POST   | `/assistant` | Travel suggestions  |

> Note: All endpoints support `OPTIONS` (CORS preflight). Errors return `{ "error": "message" }` with appropriate HTTP status.

---


## How it works

- Recommender (`backend/domain/recommender.py`):
  - Scores listings by how closely the properties' attributes match the user’s preferred environment, budget, and group size, then returns top 20.
- Filters (`backend/domain/filters.py`):
  - Checks for properties that are an exact match to the user's selected filters.
- Domain (`backend/domain/rental_management.py`):
  - Users/properties/bookings CRUD and date consistency; saves into JSON files in `data/`.
- AI (`backend/ai/service.py`):
  - Uses OpenRouter for both chat suggestions and property generation.

---

## Notes
- Data is stored in `data/*.json` for simplicity. For production, consider a database and proper auth.
- CORS is enabled in the backend for local development.
- The frontend points to `http://127.0.0.1:5050`; change `API_BASE` in `frontend/assets/app.js` if needed.




## 📞 Support

If you have any questions or need help, please open an issue on GitHub.