
# ASM Clinic Management System

## 📌 Overview

The **ASM Clinic Management System (HMS)** is a desktop-based application developed using **Python (PyQt5)** and **Microsoft SQL Server**. It is designed to enhance the efficiency of clinical operations such as managing patients, appointments, diagnoses, prescriptions, laboratory tests, billing, staff roles, and reporting — all within a unified platform.

---

## 👨‍⚕️ Key Roles and Modules

### 🛎️ Receptionist Features
- Register, update, and delete patient records.
- Manage doctor appointments.
- Generate and track billing for visits, tests, and medications.

### 🩺 Doctor Features
- View complete medical history of patients.
- Add diagnoses, prescribe medicines, and order lab tests.
- Manage personal appointment schedules.

### 🧑‍💼 Administrator Features
- Manage staff information, roles, and salaries.
- Add/update/delete medicines and lab tests.
- Generate detailed reports on operations and finances.
- Monitor overall system usage.

---

## ✅ Functional Requirements

- CRUD operations for Patients, Doctors, Staff, Visits, Prescriptions, and Payments.
- Search by CNIC, contact info, or visit ID.
- Role-Based Access Control (RBAC).
- Data export/import functionality.

---

## 🔒 Non-Functional Requirements

- **Performance:** Handles multiple concurrent users.
- **Usability:** User-friendly PyQt5 GUI.
- **Security:** Encrypted sensitive data and RBAC.
- **Reliability:** Scheduled automatic backups.
- **Portability:** Compatible with Windows, Linux, and macOS.
- **Scalability & Maintainability:** Modular architecture with extendable design.

---

## 🛠️ Technical Stack

| Layer        | Technology             |
|--------------|------------------------|
| Frontend     | Python (PyQt5)         |
| Backend      | Microsoft SQL Server   |
| OS Support   | Windows, Linux, macOS  |
| Development  | Python 3.x, PyQt5, SQL Server Management Studio |

---

## 🗃️ Database Design

### Key Tables:

- `TblPatients`, `TblDoctors`, `TblVisits`, `TblPrescriptions`, `TblMedicines`
- `TblTests`, `TblTestPrescriptions`, `TblPayments`, `TblStaff`, `TblRoles`
- `TblAddress`, `TblSalary`, `TblCredentials`, `TblSymptoms`, `TblDiagnoses`

### Relationships:

- One-to-Many: Patient → Visits, Doctor → Visits, Visit → Prescriptions, etc.
- One-to-One: Staff → Credentials

### Normalization:

- **1NF**: Ensures atomicity and removes repeating groups.
- **2NF**: Removes partial dependencies.
- **3NF**: Eliminates transitive dependencies.

---

## 📈 Denormalization Opportunities

- Embed frequently accessed info like doctor specialization or patient address.
- Precompute and cache visit summaries.
- Combine payment and visit data for faster financial queries.

---

## 📸 GUI Snapshots

- **Login Screen**
- **Admin Panel**
- **Doctor Panel**
- *(Screenshots available in the report or project folder)*

---

## 🧪 Testing & Validation

Each table and field follows strict validation rules:
- Unique IDs, correct formats (e.g., CNIC, email, phone)
- Referential integrity for foreign keys
- Date and numeric validations for fields like salary, payment amount, etc.

---

## 📌 Project Structure

```
├── README.md
├── main.py
├── /ui               # PyQt5 GUI components
├── /db               # SQL Server schema and seed data
├── /modules          # Functional modules: patients, appointments, etc.
└── /assets           # Icons and screenshots
```

---

## 👥 Contributors

- **Malik Muhammad Suleman Saleh**   
- **Muhammad Ali**   
- **Misbah Sehar** 

---

## ✅ Recommendations

- **Training:** Provide onboarding sessions for hospital staff.
- **Integration:** Connect with EHR and external billing systems.
- **Security Compliance:** Ensure HIPAA/GDPR adherence.
- **Continuous Testing:** Conduct trials in real environments for improvement.
- **Scalability:** Keep the architecture ready for future enhancements and online deployments.

---

## 📃 License

This project is developed as part of a university assignment and is for educational purposes.
