# 🚖 Taxi Booking Application

## 📌 Project Overview

This project is a **Taxi Booking System** developed as part of an internship task.
It simulates a real-world **call taxi service**, where taxis are allocated to customers based on availability, distance, and earnings.

The system efficiently assigns taxis and tracks bookings while ensuring optimal allocation.

---

## 🎯 Features

* 📍 Multiple taxi support (scalable for any number of taxis)
* 📍 Location-based taxi allocation (Points A–F)
* 📍 Nearest taxi assignment logic
* 📍 Earnings-based taxi prioritization
* 📍 Booking rejection if no taxi available
* 📍 Revenue tracking for each taxi
* 📍 Detailed booking history

---

## ⚙️ Problem Logic

### 🚕 Taxi Allocation Rules

* All taxis are initially at point **A**
* When a customer books:

  * Taxi at the same pickup point is preferred
  * Else, nearest available taxi is assigned
  * If multiple taxis are available → choose taxi with **lowest earnings**
* If no taxi is available → booking is rejected

---

### ⏱️ Time & Distance Rules

* Points: **A, B, C, D, E, F**
* Distance between adjacent points = **15 km**
* Travel time between points = **1 hour**
* Taxi becomes free only after completing trip

---

### 💰 Fare Calculation

* ₹100 for first 5 km
* ₹10 per km after 5 km
* Only charged from **pickup to drop point**

---

## 🧠 Concepts Used

* Object-Oriented Programming (OOP)
* Greedy Algorithm (optimal taxi allocation)
* List and Data Handling
* Simulation-based problem solving

---

## 🏗️ Project Structure

```id="p1m92x"
Taxi_app/
│
├── main.py            # Main program execution
├── taxi.py            # Taxi class definition
├── booking.py         # Booking logic
├── service.py         # Core allocation logic
└── README.md
```

---

## ▶️ How to Run

### 1. Clone the repository

```id="q6l19x"
git clone https://github.com/puneethrajtr/Ethnotech_intern.git
cd Taxi_app
```

---

### 2. Run the program

```id="9n4o2f"
python main.py
```

---

## 🧪 Sample Input

```id="3d7k2x"
Customer ID: 1
Pickup Point: A
Drop Point: B
Pickup Time: 9
```

---

## ✅ Sample Output

```id="y3l2xp"
Taxi can be allotted.
Taxi-1 is allotted
```

---

## 📊 Sample Taxi Details

```id="a8x4m2"
Taxi-1 Total Earnings: Rs. 400

BookingID CustomerID From To PickupTime DropTime Amount
1         1          A    B    9          10        200
3         3          B    C    12         13        200
```

---

## 🚀 Future Enhancements

* Web-based UI using Flask/Django
* Real-time taxi tracking
* Database integration (MySQL)
* Map-based distance calculation
* User authentication system

---

## 👨‍💻 Author

**Puneeth Raj T R**

---

⭐ If you found this project useful, give it a star!
