# ⚽ L7 Football System  

This project is a **football match management web application** that allows users to:  
✅ **View live matches, teams, and players** in a **card-based UI**  
✅ **Filter matches** by **team and month**  
✅ **Manage teams, players, and matches** via an **Admin Panel**  
✅ **Search and select teams using a dropdown with a search bar**

---

## 🚀 **Tech Stack**
### **Backend (Flask)**
- Python 3.x, Flask, Flask-SQLAlchemy  
- Flask-CORS (for frontend-backend communication)  
- SQLite (default) or PostgreSQL (for production)  

### **Frontend (React + TypeScript)**
- React, TypeScript, Vite  
- Axios (for API requests)  
- React Router (for navigation)  
- Tailwind CSS (for styling)  

---

## 📌 **Project Setup Instructions**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/kAbhi/l7-football.git
cd l7-football
```

---

## **2️⃣ Backend Setup (Flask)**
### **🔹 Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

### **🔹 Set Up the Database**
```bash
python app.py
```
🔹 **This will create the database and seed it with**:
- **5 Teams**
- **50 Players (10 per team)**
- **10 Matches in 5 locations**

---

## **3️⃣ Frontend Setup (React)**
### **🔹 Install Dependencies**
```bash
cd frontend
npm install
```

### **🔹 Run the Frontend**
```bash
npm run dev
```
🔹 Open `http://localhost:5173` in your browser.

---

## **📌 API Endpoints**
### **🔹 Matches API**
| Method | Endpoint                   | Description                                |
|--------|----------------------------|--------------------------------------------|
| GET    | `/matches`                  | Get all matches                           |
| GET    | `/matches?team=TeamName`     | Get matches where **TeamName** is playing |
| GET    | `/matches?month=YYYY-MM`     | Get matches in a **specific month**       |
| GET    | `/matches?team=Team&month=YYYY-MM` | Get matches filtered by **team & month** |
| POST   | `/matches`                   | Add a new match                           |

### **🔹 Teams API**
| Method | Endpoint   | Description                     |
|--------|-----------|---------------------------------|
| GET    | `/teams`  | Get all teams                   |
| POST   | `/teams`  | Add a new team (with validation for duplicates) |

### **🔹 Players API**
| Method | Endpoint   | Description                                      |
|--------|-----------|--------------------------------------------------|
| GET    | `/players`  | Get all players                              |
| POST   | `/players`  | Add a new player (checks if team exists) |

### **🔹 Areas API**
| Method | Endpoint   | Description                     |
|--------|-----------|---------------------------------|
| GET    | `/areas`  | Get locations of all matches   |

---

## **📌 Features**
### **🏆 Matches Page**
✅ **Automatically fetches all matches on page load**  
✅ **Filters:**
- Filter matches by **team**
- Filter matches by **month**
- Filter matches by **team & month**

### **🏆 Teams & Players Pages**
✅ **Automatically fetches all teams & players on page load**  
✅ **Displays teams and players in a card-based layout**  
✅ **Searchable dropdowns for team selection**

### **🏆 Admin Panel**
✅ **Centralized page to add**:
- **New Matches**
- **New Teams**
- **New Players**

✅ **Tab-based UI for better navigation**

---

## **📌 Running API Documentation**
### **Swagger API Docs**
1. Start the **backend server**:
   ```bash
   cd backend
   python app.py
   ```
2. Open **Swagger UI**:
   ```
   http://localhost:5000/apidocs/
   ```
3. Test APIs directly in the browser.

---

## **📌 Input Validations**
- **Teams:** Prevents duplicate team names when adding new teams.
- **Players:**
   - Prevents duplicate player names.
   - Ensures the team exists before adding a player.
- **Matches:**
   - Prevents the **same team from having more than one match on the same date**.
   - Prevents the **same location from hosting more than one match on the same date**.
   - Ensures **teams exist before scheduling a match**.
- **Dropdown Enhancements:**
   - **Searchable team selection dropdowns** when adding **players** and **matches**.

---

## **📌 Troubleshooting**
### **🔹 Backend Not Starting?**
1. Ensure **Python 3.x** is installed.
2. Run `pip install -r requirements.txt` to install dependencies.

### **🔹 CORS Error in Console?**
If frontend gets blocked by CORS, ensure Flask CORS is enabled in `app.py`:
```python
from flask_cors import CORS
CORS(app, resources={r"/*": {"origins": "*"}})
```

### **🔹 Database Not Seeding?**
1. Delete `instance/sports.db` file.
2. Restart backend:
   ```bash
   python app.py
   ```

---
## **📌 Future Roadmap**
### **🎯 Planned Enhancements**

✅ **Enhanced Match, Team & Player Insights**
- Enable clickable cards that **redirect to detailed pages** for matches, teams, and players.
- Provide comprehensive statistics and historical data for better user engagement.
- User following a Match or Player can look at the detailed page of the corresponding Matches or Players.

✅ **Integrate Match Status & Filtering**
- Display match results for completed games and indicate **"Yet to Play"** for upcoming fixtures.
- Implement a **result-based filter** to quickly view completed and upcoming matches.

✅ **Real-Time Match Updates**
- Implement **WebSocket-based live updates** to dynamically refresh match scores, player stats, and team performance.

---

## **📌 Contributors**
👨‍💻 **Developer:** Abhishek Sharma

---
