<h1 align="center">🏟️ Sports Ticket Reservation Platform</h1>

<p align="center">
  A full-stack web platform for browsing, reserving, and paying for tickets to football, basketball, and volleyball matches.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/Django-5-092E20?logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/MySQL-8-4479A1?logo=mysql&logoColor=white" />
  <img src="https://img.shields.io/badge/Vite-Build-646CFF?logo=vite&logoColor=white" />
</p>

---

<h2>📖 Overview</h2>

<p>
This project is a full-stack sports ticket reservation system built as a university database course project.
Users can search matches by sport, city, and venue, reserve tickets, complete payment, and manage their bookings.
The platform also supports <strong>support</strong> and <strong>admin</strong> roles for handling user reports and managing reservations.
</p>

<h2>🧱 Tech Stack</h2>

<table>
  <tr>
    <th>Layer</th>
    <th>Technology</th>
  </tr>
  <tr>
    <td>Frontend</td>
    <td>React 19, Vite, React Router, Axios, Tailwind CSS</td>
  </tr>
  <tr>
    <td>Backend</td>
    <td>Django 5, Django REST Framework, JWT Auth (PyJWT), PyMySQL</td>
  </tr>
  <tr>
    <td>Database</td>
    <td>MySQL 8 — with Stored Procedures, Functions, and Triggers</td>
  </tr>
</table>

<h2>🏗️ Architecture</h2>

<p>
The backend follows a layered <strong>View → Service → Repository</strong> architecture, separating business logic
from data access for better maintainability and testability. Each domain (users, matches, tickets, payments, reports, locations)
is implemented as an independent Django app.
</p>

<h2>🗄️ Database Design</h2>

<p>
The database (<code>SportsTicketDB</code>) contains 16 core tables covering users, cities, sports, venues, teams, matches,
sport-specific details (football/basketball/volleyball), ticket types, tickets, reservations, payments, and reports.
</p>

<ul>
  <li><strong>Stored Procedures:</strong> GetAllUsers, GetAllMatches, GetAllPayments, GetAllReservations, CountUsers, CountReservations, GetVenueRemainingCapacity, GetUserFullName</li>
  <li><strong>Functions:</strong> GetUserFullName, GetRemainingCapacity, GetUserReservationCount</li>
  <li><strong>Triggers:</strong> <code>BeforeReservationInsert</code> (validates expiry time), <code>AfterPaymentSuccess</code> (auto-updates reservation status on successful payment)</li>
</ul>

<h2>✨ Features</h2>

<ul>
  <li>User registration and login (password-based or OTP)</li>
  <li>Browse and search matches by sport, city, and venue</li>
  <li>Reserve tickets with automatic venue capacity management</li>
  <li>Two-step reservation → payment flow with expiry handling and race-condition-safe payment (row locking)</li>
  <li>Multiple payment methods: Bank Card, Wallet, Crypto</li>
  <li>Cancel reservations (by user or admin) with automatic capacity restore</li>
  <li>Submit and track support reports/complaints</li>
  <li>Admin dashboard for managing reservations and reviewing reports</li>
</ul>

<h2>📂 Project Structure</h2>

<pre>
sports-ticketing-platform/
├── backend/
│   ├── users/          # Auth, registration, OTP, profile
│   ├── locations/      # Cities & venues
│   ├── matches/        # Matches, reservations
│   ├── tickets/        # Ticket search & details
│   ├── payments/       # Payment processing
│   └── reports/        # User reports & support review
├── frontend/
│   └── src/
│       ├── api/        # Axios API clients
│       ├── pages/       # Page components
│       ├── components/  # Shared UI components
│       ├── context/      # Auth context
│       └── routes/       # Protected/support routes
└── database/
    ├── database.sql     # Schema
    ├── procedures.sql   # Stored procedures
    ├── functions.sql    # Functions
    └── triggers.sql      # Triggers
</pre>

<h2>🚀 Getting Started</h2>

<h3>1. Database</h3>
<pre>
mysql -u root -p < database/database.sql
mysql -u root -p SportsTicketDB < database/procedures.sql
mysql -u root -p SportsTicketDB < database/functions.sql
mysql -u root -p SportsTicketDB < database/triggers.sql
</pre>

<h3>2. Backend</h3>
<pre>
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
</pre>

<h3>3. Frontend</h3>
<pre>
cd frontend
npm install
npm run dev
</pre>

<h2>👥 Team</h2>

<ul>
  <li>Mohammad Masoumi</li>
  <li>Parsa Rostami</li>
  <li>Mozhgan Hosseini</li>
</ul>

<h2>🎓 Course</h2>

<p>Database course project — Instructor: Dr. Pishgoo</p>
