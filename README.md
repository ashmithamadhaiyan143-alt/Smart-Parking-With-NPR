Smart Parking System with Number Plate Recognition Using EasyOCR: An intelligent “Smart Parking Management System” that automates vehicle entry, parking slot allocation, and exit management using “Number Plate Recognition (NPR)” powered by “EasyOCR. The system includes a “Flask-based web application” with a real-time dashboard for monitoring parking slot availability.

Project Overview: Traditional parking systems require manual record maintenance, which is time-consuming and prone to errors. This project automates the parking process by recognizing vehicle number plates, assigning available parking slots, storing parking records, and displaying real-time parking status on a web dashboard.

Features:

Automatic Number Plate Recognition using EasyOCR
Vehicle image upload for plate detection -Automatic parking slot allocation
Real-time parking dashboard
Available slots displayed in Green
Occupied slots displayed in Red
Entry and Exit time recording
SQLite database for parking records
Admin login authentication
Fast and lightweight Flask application
Tech Stack: Frontend - HTML - CSS - JavaScript Backend -Python - Flask Database - SQLite3 OCR Library - EasyOCR

How It Works:

Upload or capture a vehicle image.
EasyOCR extracts the vehicle number plate.
Flask validates the vehicle details.
The next available parking slot is assigned.
Details are stored in SQLite.
Dashboard updates instantly.
On vehicle exit, exit time is recorded and the slot becomes available again.
AUTHOR: Ashmitha M|Engineering Student
