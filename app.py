import time
import os
import json

# ---------------- FILE PATHS ----------------
FLIGHTS_FILE = "flights.txt"
PASSENGERS_FILE = "passengers.txt"
USERS_FILE = "users.txt" 

# ---------------- r&w FILE FUNCTIONS ----------------
def read_file(file):
    if not os.path.exists(file) or os.path.getsize(file) == 0:
        return []
    try:
        with open(file, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"⚠ Warning: Could not decode JSON from {file}. Returning empty list.")
        return []

def write_file(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- WELCOME PAGE ----------------
def out():
    print('*'*100)
    print("✈ WELCOME TO AIRLINE TICKET BOOKING SYSTEM ✈".center(100))
    print('*'*100)
    print("1) Admin\n2) User\n3) Exit")

# ---------------- ADMIN FUNCTIONS ----------------
def view_flights():
    flights = read_file(FLIGHTS_FILE)
    if not flights:
        print("No flights available.")
        return
    print("-"*100)
    print(f"{'S_NO':<6}{'Flight No':<12}{'Airline':<12}{'From':<10}{'To':<10}{'Departure':<20}{'Arrival':<20}{'Price':<8}")
    print("-"*100)
    for f in flights:
        print(f"{f.get('S_NO', ''):<6}{f.get('FLIGHT_NO', ''):<12}{f.get('AIRLINES_NAME', ''):<12}{f.get('DEPARTURE', ''):<10}{f.get('DESTINATION', ''):<10}{f.get('TIME_OF_DEPARTURE', ''):<20}{f.get('TIME_OF_ARRIVAL', ''):<20}{f.get('CHARGES', ''):<8}")
    print("-"*100)

def add_flight():
    flights = read_file(FLIGHTS_FILE)
    try:
        sno = input("Enter S_NO: ").strip()
        if not sno.isdigit():
            raise ValueError
        sno = int(sno)
    except ValueError:
        print("❌ Invalid input! S_NO must be a number.")
        return
    if any(str(f.get("S_NO")) == str(sno) for f in flights):
        print("❌ Invalid! This S_NO already exists.")
        return

    airline = input("Enter Airline Name: ").strip()
    departure = input("Enter Departure: ").strip().upper()
    destination = input("Enter Destination: ").strip().upper()
    flight_no = input("Enter Flight No: ").strip().upper()
    dep_time = input("Enter Departure Time (YYYY-MM-DD HH:MM): ").strip()
    arr_time = input("Enter Arrival Time (YYYY-MM-DD HH:MM): ").strip()
    try:
        charges = input("Enter Charges: ").strip()
        if not charges.isdigit():
            raise ValueError
        charges = int(charges)
    except ValueError:
        print("❌ Invalid input! Charges must be a number.")
        return

    if not all([airline, departure, destination, flight_no, dep_time, arr_time]):
        print("❌ Invalid input! All fields are required.")
        return

    if any(f.get("FLIGHT_NO", "").upper() == flight_no and f.get("TIME_OF_DEPARTURE", "") == dep_time and f.get("TIME_OF_ARRIVAL", "") == arr_time for f in flights):
        print("❌ Invalid! A flight with this number and timings already exists.")
        return

    new_flight = {
        "S_NO": str(sno),
        "AIRLINES_NAME": airline,
        "DEPARTURE": departure,
        "DESTINATION": destination,
        "FLIGHT_NO": flight_no,
        "TIME_OF_DEPARTURE": dep_time,
        "TIME_OF_ARRIVAL": arr_time,
        "CHARGES": charges
    }
    flights.append(new_flight)
    write_file(FLIGHTS_FILE, flights)
    print(f"✅ Flight {flight_no} added successfully!")

def modify_flight():
    flights = read_file(FLIGHTS_FILE)
    fno = input("Enter Flight No to modify: ").upper().strip()
    flight_to_modify = next((f for f in flights if f.get("FLIGHT_NO", "").upper() == fno), None)
    
    if not flight_to_modify:
        print("❌ Flight not found.")
        return

    while True:
        print("\nModify Options:\n1) Airline Name\n2) Departure\n3) Destination\n4) Departure Time\n5) Arrival Time\n6) Charges\n7) Exit")
        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("❌ Invalid input! Enter a number between 1-7.")
            continue

        if choice == 1:
            flight_to_modify["AIRLINES_NAME"] = input("Enter new Airline Name: ").strip()
        elif choice == 2:
            flight_to_modify["DEPARTURE"] = input("Enter new Departure: ").strip().upper()
        elif choice == 3:
            flight_to_modify["DESTINATION"] = input("Enter new Destination: ").strip().upper()
        elif choice == 4:
            flight_to_modify["TIME_OF_DEPARTURE"] = input("Enter new Departure Time (YYYY-MM-DD HH:MM): ").strip()
        elif choice == 5:
            flight_to_modify["TIME_OF_ARRIVAL"] = input("Enter new Arrival Time (YYYY-MM-DD HH:MM): ").strip()
        elif choice == 6:
            try:
                new_charges = input("Enter new Charges: ").strip()
                if not new_charges.isdigit():
                    raise ValueError
                flight_to_modify["CHARGES"] = int(new_charges)
            except ValueError:
                print("❌ Charges must be a number.")
                continue
        elif choice == 7:
            break
        else:
            print("❌ Invalid choice!")
            continue

        write_file(FLIGHTS_FILE, flights)
        print("✅ Flight modified successfully!")
        
def delete_flight():
    flights = read_file(FLIGHTS_FILE)
    passengers = read_file(PASSENGERS_FILE)
    
    fno = input("Enter Flight No to delete: ").upper().strip()
    dep_time = input("Enter Departure Time (YYYY-MM-DD HH:MM): ").strip()
    arr_time = input("Enter Arrival Time (YYYY-MM-DD HH:MM): ").strip()
    
    original_flight_count = len(flights)
    
    flights_to_keep = [
        f for f in flights 
        if not (
            f.get("FLIGHT_NO", "").upper() == fno and 
            f.get("TIME_OF_DEPARTURE", "") == dep_time and 
            f.get("TIME_OF_ARRIVAL", "") == arr_time
        )
    ]

    if len(flights_to_keep) < original_flight_count:
        passengers_to_keep = [
            p for p in passengers 
            if p.get("FLIGHT_NO", "").upper() != fno or 
               (p.get("FLIGHT_NO", "").upper() == fno and fno not in [f['FLIGHT_NO'] for f in flights_to_keep]
               ) 
        ]
        deleted_flight_data = {
            "FLIGHT_NO": fno,
            "TIME_OF_DEPARTURE": dep_time,
            "TIME_OF_ARRIVAL": arr_time
        }
        
        passengers_to_keep = [
            p for p in passengers
            if p.get("FLIGHT_NO", "").upper() != fno 
        ]        
        passengers = [
            p for p in passengers 
            if p.get("FLIGHT_NO", "").upper() != fno
        ]
        write_file(FLIGHTS_FILE, flights_to_keep)
        write_file(PASSENGERS_FILE, passengers)
        
        print(f"✅ Flight {fno} deleted successfully!")
        print("✅ All corresponding passenger bookings have also been removed.")
    else:
        print(f"❌ Flight {fno} with specified timings not found.")

def view_passengers():
    passengers = read_file(PASSENGERS_FILE)
    if not passengers:
        print("No passenger records.")
        return
    print("-"*100)
    print(f"{'Name':<15}{'Phone':<15}{'Email':<25}{'Flight No':<10}{'Amount':<8}{'Passport':<15}{'Feedback':<20}")
    print("-"*100)
    for p in passengers:
        print(f"{p.get('NAME', ''):<15}{p.get('PHONE', ''):<15}{p.get('EMAIL', ''):<25}{p.get('FLIGHT_NO', ''):<10}{p.get('AMOUNT', ''):<8}{p.get('PASSPORT', ''):<15}{p.get('FEEDBACK', ''):<20}")
    print("-"*100)

# ---------------- USER FUNCTIONS ----------------
def register_user():
    users = read_file(USERS_FILE)
    email = input("Enter your Email: ").strip().lower()
    existing_user = next((u for u in users if u.get("EMAIL_ADDRESS", "").lower() == email), None)
    if existing_user:
        print("⚠ User already exists. Logging you in...")
        return existing_user
    name = input("Enter your Name: ").strip()
    phone = input("Enter your Phone Number: ").strip()
    new_user = {"NAME": name, "EMAIL_ADDRESS": email, "PHONE": phone}
    users.append(new_user)
    write_file(USERS_FILE, users)
    print(f"✅ User {name} registered successfully!")
    return new_user

def book_flight(current_user):
    flights = read_file(FLIGHTS_FILE)
    if not flights:
        print("❌ No flights available.")
        return
    
    # Display Flights
    print("-"*100)
    print(f"{'S_NO':<6}{'Flight No':<12}{'Airline':<12}{'From':<10}{'To':<10}{'Departure':<20}{'Arrival':<20}{'Price':<8}")
    print("-"*100)
    for f in flights:
        print(f"{f.get('S_NO', ''):<6}{f.get('FLIGHT_NO', ''):<12}{f.get('AIRLINES_NAME', ''):<12}{f.get('DEPARTURE', ''):<10}{f.get('DESTINATION', ''):<10}{f.get('TIME_OF_DEPARTURE', ''):<20}{f.get('TIME_OF_ARRIVAL', ''):<20}{f.get('CHARGES', ''):<8}")
    print("-"*100)

    fno = input("Enter Flight No to book: ").upper().strip()
    flight = next((f for f in flights if f.get("FLIGHT_NO", "").upper() == fno), None)
    if not flight:
        print("❌ Flight not found.")
        return

    passengers = read_file(PASSENGERS_FILE)
    current_email = current_user.get("EMAIL_ADDRESS", "").lower()
    if any(p.get("EMAIL", "").lower() == current_email and p.get("FLIGHT_NO", "") == fno for p in passengers):
        print("⚠ You have already booked this flight.")
        return

    passport = input("Enter your Passport No: ").strip()
    amount = flight.get("CHARGES", 0)
    
    new_passenger = {
        "NAME": current_user.get("NAME", ""),
        "PHONE": current_user.get("PHONE", ""),
        "EMAIL": current_user.get("EMAIL_ADDRESS", ""),
        "FLIGHT_NO": flight.get("FLIGHT_NO", ""),
        "AMOUNT": amount,
        "PASSPORT": passport,
        "FEEDBACK": ""
    }
    passengers.append(new_passenger)
    write_file(PASSENGERS_FILE, passengers)
    print(f"✅ Flight {fno} booked successfully for {current_user.get('NAME', 'User')}!")

def view_booking(current_user):
    passengers = read_file(PASSENGERS_FILE)
    current_email = current_user.get("EMAIL_ADDRESS", "").lower()
    booking_list = [p for p in passengers if p.get("EMAIL", "").lower() == current_email]
    
    if not booking_list:
        print("❌ No booking found.")
        return
        
    print("-"*100)
    print(f"{'Name':<15}{'Phone':<12}{'Email':<25}{'Flight No':<12}{'Amount':<8}{'Passport':<15}{'Feedback':<20}")
    print("-"*100)
    for b in booking_list:
        print(f"{b.get('NAME', ''):<15}{b.get('PHONE', ''):<12}{b.get('EMAIL', ''):<25}{b.get('FLIGHT_NO', ''):<12}{b.get('AMOUNT', ''):<8}{b.get('PASSPORT', ''):<15}{b.get('FEEDBACK', ''):<20}")
    print("-"*100)

def cancel_booking(current_user):
    passengers = read_file(PASSENGERS_FILE)
    booking_list = [p for p in passengers if p.get("EMAIL", "").lower() == current_user.get("EMAIL_ADDRESS", "").lower()]
    if not booking_list:
        print("❌ No booking found for your account.")
        return

    print("\n— Your Current Bookings —")
    print(f"{'Flight No':<12}{'Price':<8}")
    print("-"*100)
    for b in booking_list:
        print(f"{b.get('FLIGHT_NO', ''):<12}{b.get('AMOUNT', ''):<8}")
    print("-" *100)

    fno_to_cancel = input("Enter the Flight No to cancel: ").upper().strip()
    
    original_count = len(passengers)
    current_email = current_user.get("EMAIL_ADDRESS", "").lower()
    
    passengers = [
        p for p in passengers
        if not (
            p.get("EMAIL", "").lower() == current_email and 
            p.get("FLIGHT_NO", "").upper() == fno_to_cancel
        )
    ]
    
    if len(passengers) < original_count:
        write_file(PASSENGERS_FILE, passengers)
        print(f"✅ Booking for Flight {fno_to_cancel} cancelled successfully!")
    else:
        print(f"❌ Booking for Flight {fno_to_cancel} not found for your account.")

def feedback(current_user):
    passengers = read_file(PASSENGERS_FILE)
    found = False
    current_email = current_user.get("EMAIL_ADDRESS", "").lower()
    
    for p in passengers:
        if p.get("EMAIL", "").lower() == current_email:
            p["FEEDBACK"] = input("Enter Feedback: ").strip()
            found = True
            
    if found:
        write_file(PASSENGERS_FILE, passengers)
        print("✅ Feedback saved.")
    else:
        print("❌ No booking found for your account.")

# ---------------- MAIN MENU ----------------
current_user = None

while True:
    out()
    try:
        choice = int(input("Enter choice: "))
        print('—'*100)
    except ValueError:
        print("❌ Invalid input! Please enter a number.")
        continue

    if choice == 1:  # Admin
        username = input("Enter Admin Username: ")
        password = input("Enter Admin Password: ")
        print('—'*100)
        if username == "admin" and password == "admin":
            while True:
                print('*'*100)
                print("✈ ADMIN MENU ✈".center(100))
                print('*'*100)
                print("\n\n1)View Flights\n2)Add Flight\n3)Modify Flight\n4)Delete Flight\n5)View Passengers\n6)Exit\n")
                try:
                    c = int(input("Enter choice: "))
                except ValueError:
                    print("❌ Invalid input!")
                    continue
                if c == 1: view_flights()
                elif c == 2: add_flight()
                elif c == 3: modify_flight()
                elif c == 4: delete_flight()
                elif c == 5: view_passengers()
                elif c == 6: break
                else: print("❌ Invalid choice!")
                print('—'*100)
        else:
            print("❌ Access Denied!")

    elif choice == 2:  # User
        users = read_file(USERS_FILE)
        print('*'*100)
        print("✈ USER MENU ✈".center(100))
        print('*'*100)
        print("\nUser Authentication:\n1) Login\n2) Register\n3) Back\n")
        try:
            auth_choice = int(input("Enter choice: "))
        except ValueError:
            print("❌ Invalid input!")
            continue

        if auth_choice == 1:  # Login
            email = input("Enter your Email: ").lower().strip()
            user = next((u for u in users if u.get("EMAIL_ADDRESS", "").lower() == email), None)
            if user:
                print(f"✅ Welcome back, {user.get('NAME', 'User')}!")
                current_user = user
            else:
                print("❌ No user found with this email. Please register first.")
                continue

        elif auth_choice == 2:  # Register
            current_user = register_user()
        elif auth_choice == 3:
            continue
        else:
            print("❌ Invalid choice!")
            continue
        while current_user:
            print('*'*100)
            print("✈ USER MENU ✈".center(100))
            print('*'*100)
            print("\n\n1)Book Flight\n2)View Booking\n3)Cancel Booking\n4)Feedback\n5)Logout\n")
            try:
                c = int(input("Enter choice: "))
            except ValueError:
                print("❌ Invalid input!")
                continue

            if c == 1: book_flight(current_user)
            elif c == 2: view_booking(current_user)
            elif c == 3: cancel_booking(current_user)
            elif c == 4: feedback(current_user)
            elif c == 5: 
                print(f"Goodbye, {current_user.get('NAME', 'User')}!")
                current_user = None
                break
            else:
                print("❌ Invalid choice!")
            print('—'*100)

    elif choice == 3:
        print("Exiting... Goodbye!\n", "Have a great day!".center(100))
        break
    else:
        print("❌ Invalid selection!")
    print('—'*100)
