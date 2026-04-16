# Ensf-338-final-project-Group_3- Campus Navigation and Event Management System

## GitHub Repository
GitHub Repository URL: **[https://github.com/07162005/Ensf-338-final-project-]**

---

## Group Members

- **Adesope Ajayi** — **30194173**
- **Shiv Sharma** — **30219086**
- **Ameitesh Saina** — **30244391**
- **Utkarsh Sudhir** — **30240320**
- **Julia Izuogu** — **30242363**
- **Fiemna Ekpombang** — **30253697**

---

## Project Overview

This project is a **Campus Navigation and Event Management System** developed in Python for a ENSF 338. The system supports:
- campus map representation using a graph
- shortest path navigation between campus locations
- route history and undo functionality
- room and event booking management
- priority-based service request handling
- fast building and room lookup
- FIFO incoming request processing
- optional balanced event index for the bonus feature

---

## Requirements

- **Python 3.x**
- No external libraries are required for the core system

---

## How to Run the Application

1. Open **PowerShell**, **Command Prompt**, or the **VS Code terminal**.
2. Navigate to the folder that contains `main.py`.
3. Make sure the `data` folder is inside the same folder as `main.py`.
4. Make sure the `data` folder contains the following files:
   - `buildings.txt`
   - `rooms.txt`
   - `campus_map.txt`
   - `bookings.txt`
   - `service_requests.txt`
   - `incoming_requests.txt`
5. Run the application with:

   ```bash
   python main.py
6. If your system uses `python3`, run:

   ```bash
   python3 main.py
7. Wait for the main menu to appear.
8. Enter the number of the feature you want to use, then press Enter.
9. Follow the prompts shown on the screen.
10. Enter building IDs, room IDs, dates, and times exactly in the format requested by the program.
11. Use dates in the format YYYY-MM-DD.
12. Use times in the format HH:MM.
13. To stop the program, select option 0 from the main menu.
