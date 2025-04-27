
# CEMA Health Infomation System - 24/04/2025

The CEMA Health Information System is a lightweight and efficient backend API built using Python Flask and SQLite.
It helps manage essential healthcare operations like clients, programs, doctors, and enrollments for a small healthcare facility or NGO.

This backend system provides secure and structured access to health data, making it easy to register clients, enroll them into health programs, manage doctors, and track services offered.

## Author

By:
- Mark Mwangi


## Table of Contents

- [Project Description](#project-description)
- [Key Features/MVP](#key-featuresmvp)
- [Setup/Installation Requirements](#setupinstallation-requirements)
- [API Endpoints](#api-endpoints)
- [Known Bugs](#known-bugs)
- [Technologies Used](#technologies-used)
- [Future Improvements](#future-improvements)
- [Support and contact details](#support-and-contact-details)
- [License](#license)

## Project Description

This project is designed to:

- Register and manage clients receiving health services

- Create and manage health programs (e.g., HIV Care, Maternal Health, Nutrition)

- Enroll and unenroll clients into specific health programs

- Register and manage doctors providing care

- Secure the system with JWT authentication (only logged-in users can access/manage resources)

- Perform CRUD operations (Create, Read, Update, Delete) on clients, doctors, and programs

- Search clients easily by name

## Key Features/MVP

### A user can:


1. Manage Clients (Register, Update, Delete, Search)
2. Manage Doctors (Create, View All, Update, Delete)
3. Manage Programs (Create, View, Update, Delete)
4. Enroll clients into one or more programs
5. Unenroll clients from a program
6. Delete a program (automatically remove all enrolled clients)

### JWT Authentication (Login and Protect Routes)


## Setup/Installation Requirements

1. Clone the repository to any desired folder in your computer.
2. Open the folder with Visual Studio Code or any editor of your choice.
3. There is one folder in the root directory, the `server` folder.
4. Initialize the database by running:

```sh
flask db init
flask db migrate
flask db upgrade
```

4. To download the dependencies for the backend, on a different terminal, run:

```sh
pipenv install && pipenv shell 
```

You can run your Flask API(server) on [`localhost:5000`](http://localhost:5000) by navigating to the `server` folder and run:

```sh
python3 app.py
```

6. And your backend is up and running successfully.

## API Endpoints

---

###  Clients

- Endpoints related to client management. You can register, update, search, enroll, or remove clients from programs.

| Method | Endpoint | Description |
| :---- | :---- | :---- |
| POST | `/clients/register` | Register a new client |
| GET | `/clients/search?q=<query>` | Search for clients by name |
| PUT | `/clients/<int:client_id>` | Update client details |
| DELETE | `/clients/<int:client_id>` | Delete a client |
| POST | `/clients/enroll` | Enroll a client into one or more programs |
| DELETE | `/clients/<int:client_id>/programs/<int:program_id>` | Unenroll a client from a program |

---

###  Doctors

- Endpoints related to doctor management. You can register a new doctor retrieve, update, and delete doctor records.

| Method | Endpoint | Description |
| :---- | :---- | :---- |
| POST | `/doctors/register` | Register a new doctor |
| GET | `/doctors` | Get all doctors |
| PUT | `/doctors/<int:doctor_id>` | Update doctor details |
| DELETE | `/doctors/<int:doctor_id>` | Delete a doctor |

---

###  Programs

- Endpoints related to health program management. You can create, update, fetch, or delete programs.

| Method | Endpoint | Description |
| :---- | :---- | :---- |
| POST | `/programs` | Create a new health program |
| GET | `/programs` | Get all health programs |
| PUT | `/programs/<int:program_id>` | Update program details |
| DELETE | `/programs/<int:program_id>` | Delete a program and automatically remove enrollments |

---

###  Authentication

- Endpoints related to user authentication using JWT. Secure your requests with access tokens.

| Method | Endpoint | Description |
| :---- | :---- | :---- |
| POST | `/login` | Log in and get JWT access token |
| GET | `/user` | Getting an authenticated user |
| DELETE | `/logout` | Log out a user |

---

## Known Bugs

- The application runs successfully.

## Technologies used

- Python
- Flask
- SQLite: Database
- SQLAlchemy ORM
- Postman: for API Testing
- Terminal

## Future Improvements

- Admin dashboard (web frontend)

- Advanced reporting (e.g., client enrollments summary)

- Bulk client registration via excel/spreadsheet file

- Role-based user access (Admin, Staff)

- SMS or Email notifications (for appointments, follow-up)

## Support and contact details

1. Mark Mwangi
- email :: mwangimark57@gmail.com
- phone :: +254770614345

## License

MIT License

Copyright (c) 2024 BRIAN CHERUS, MARK MWANGI, ARNOLD JUMA

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.```