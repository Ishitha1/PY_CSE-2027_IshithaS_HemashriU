# ✈️ Airline Ticket Booking System (CLI)

A robust, console-based application built entirely using Python's standard library for managing flight schedules and passenger bookings. This system features distinct administrative and user workflows with persistent data storage via JSON files.

---

## ✨ Key Features

- **Dual Access:** Separate menus for Admin (managing flights) and Users (booking/feedback).  
- **Data Persistence:** Uses local JSON files (`flights.txt`, `passengers.txt`, `users.txt`) for data storage.  
- **Robustness:** Implements extensive input validation and handles critical file access errors (like empty files or non-numeric input) without crashing.  
- **Clear Feedback:** Employs visual indicators (✅ Success, ❌ Failure, ⚠ Warning) for an intuitive command-line experience.  

---

## 🛠️ Setup & Run

### Prerequisites
You only need **Python 3.x** installed. The project uses only the standard library (`os`, `json`, `time`).  

### Running the Application
1. **Save the Code:** Save the Python code as `airline_system.py`.  
2. **Execute:** Open your terminal or command prompt, navigate to the file's location, and run:  

```bash
python3 airline_system.py
````

The application will start, display the main menu, and automatically create the necessary data files upon its first run.

---

## 🚀 Usage

### Default Credentials

| Role  | Username | Password |
| ----- | -------- | -------- |
| Admin | admin    | admin    |

### Workflow Overview

| Role  | Main Actions                                                              | Purpose                                                                |
| ----- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Admin | Add, View, Modify, Delete Flight, View All Passengers                     | Manages the available flight inventory and monitors bookings/feedback. |
| User  | Register/Login, Book Flight, View Booking, Cancel Booking, Leave Feedback | Allows registered users to interact with the flight system.            |

---

## 💾 Data Structure

The system uses three main files to store data in a human-readable JSON format.

| File Name      | Purpose                                     | Example Key Fields                         |
| -------------- | ------------------------------------------- | ------------------------------------------ |
| flights.txt    | Stores all available flight details.        | FLIGHT_NO, DEPARTURE, DESTINATION, CHARGES |
| users.txt      | Stores registration details for all users.  | NAME, EMAIL_ADDRESS, PHONE                 |
| passengers.txt | Stores a record for each completed booking. | FLIGHT_NO, EMAIL, PASSPORT, FEEDBACK       |

---

## 🛡️ Hackathon Disclosure

This project's core Python logic was written originally by me (the developer). No templates or starter code were used.

I utilized an AI assistant for project refinement and documentation:

* **Comprehensive Testing and Robustness:** The AI was used to simulate all possible human inputs and edge cases (e.g., non-numeric input, empty files, missing data) to ensure the code's stability and to confirm that all errors were gracefully handled without crashing the application. This process directly addressed a critical `JSONDecodeError` on empty data files.

* **UI/UX:** The AI suggested implementing consistent status emojis (✅, ❌, ⚠) for better command-line user experience.

* **Documentation:** The AI assisted in structuring and writing this README file.
