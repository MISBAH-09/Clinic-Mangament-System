create database DB_HMS
use DB_HMS;

-- 1. Create Table for Patients
CREATE TABLE TblPatients (
    PatientID INT PRIMARY KEY IDENTITY(1,1), -- Unique patient identifier
    FirstName VARCHAR(100), -- Patient's first name
    LastName VARCHAR(100), -- Patient's last name
	CNIC VARCHAR(20) unique, -- National Identification number
    DateOfBirth DATE, -- Patient's date of birth
    Gender VARCHAR(10), -- Patient's gender
    ContactNumber VARCHAR(15), -- Patient's contact number
    Email VARCHAR(100) unique, -- Patient's email address
    Address VARCHAR(255), -- Patient's home address
	DateRegistered DATETIME2 DEFAULT CURRENT_TIMESTAMP -- Date and time patient regidtered
);

-- 2. Create Table for Roles (For doctors, staff, etc.)
CREATE TABLE TblRoles (
    RoleID INT PRIMARY KEY IDENTITY(1,1), -- Unique role identifier (e.g., doctor, staff)
    RoleName VARCHAR(100) unique -- Name of the role (doctor, nurse, admin, etc.)
);

-- 3. Create Table for Credentials
CREATE TABLE TblCredentials (
    CredentialID int PRIMARY KEY IDENTITY(1,1), -- Unique credential ID for each user
    Username VARCHAR(100) NOT NULL unique, -- Username for login
    PasswordHash VARCHAR(255) NOT NULL, -- Hashed password for security
    RoleID INT NOT NULL, -- Link to role assigned to the user (Doctor, Staff, etc.)
    FOREIGN KEY (RoleID) REFERENCES TblRoles(RoleID) -- Foreign key reference to TblRoles to identify user role
);

-- 4. Create Table for Salary (Stores salary records)
CREATE TABLE TblSalary (
    SalaryID INT PRIMARY KEY IDENTITY(1,1), -- Unique salary record identifier
    Amount DECIMAL(10, 2), -- Salary amount
   -- EffectiveFrom DATE, -- Start date of this salary amount
    --EffectiveTo DATE -- End date of this salary amount
);

--5 Create Table for Address
CREATE TABLE TblAddress (
    AddressID INT PRIMARY KEY IDENTITY(1,1), -- Unique identifier for each address
    city VARCHAR(20), -- Name of the city
    street VARCHAR(50), -- Street address details
    state VARCHAR(50), -- Name of the state or region
    postal_code VARCHAR(40), -- Postal or ZIP code for the address
    country VARCHAR(50), -- Name of the country
);
-- 6. Create Table for Doctors
CREATE TABLE TblDoctors (
    DoctorID INT PRIMARY KEY IDENTITY(1,1), -- Unique doctor identifier
    FirstName VARCHAR(100), -- Doctor's first name
    LastName VARCHAR(100), -- Doctor's last name
    CNIC VARCHAR(20) unique, -- National Identification number
    LicenseNo VARCHAR(50), -- Medical license number
    JoiningDate DATE, -- Date when the doctor joined the hospital
    JobStatus VARCHAR(20) DEFAULT 'active', -- Job status with default value 'active'
    SalaryID INT, -- Link to the salary record of the doctor
    CredentialID INT, -- Link to the doctor's login credentials
    AddressID INT, -- Link to the address of the staff member
    FOREIGN KEY (SalaryID) REFERENCES TblSalary(SalaryID), -- Foreign key linking to the salary record in TblSalary
    FOREIGN KEY (AddressID) REFERENCES TblAddress(AddressID), -- Foreign key linking to the address record in TblAddress
    FOREIGN KEY (CredentialID) REFERENCES TblCredentials(CredentialID) -- Foreign key linking to login credentials in TblCredentials
);


--insert data into Table Roles
insert into TblRoles values('Admin'),('Receptionist'),('Doctor')

--7 Create Table For Medicines
CREATE TABLE TblMedicines (
    MedicineID INT PRIMARY KEY IDENTITY(1,1), -- Unique identifier for the medicine
    MedicineName VARCHAR(255) NOT NULL, -- Name of the medicine
    ActiveIngredient VARCHAR(255) NOT NULL, -- Active ingredient(s) in the medicine
    Dosage VARCHAR(100), -- Dosage information
    DrugType VARCHAR(50) -- Type of drug (e.g., tablet, syrup, injection)
);

--insert data into TblMedicines

--set identity_insert TblMedicines on
INSERT INTO TblMedicines (MedicineID, MedicineName, ActiveIngredient, Dosage, DrugType)
VALUES
(1, 'Glipizide and Metformin HCl', 'Glipizide, Metformin HCl', 'Unknown', 'Tablet'),
(2, 'Ceftriaxone Sodium', 'Ceftriaxone', 'Unknown', 'Injection'),
(3, 'Anti-Bacterial Hand Gel Mango Madness', 'Alcohol, Fragrance', 'Unknown', 'Gel'),
(4, 'Kinray Vitamin A D', 'Vitamin A, Vitamin D', 'Unknown', 'Tablet'),
(5, 'Facilipro', 'Unknown', 'Unknown', 'Unknown'),
(6, 'Benzonatate', 'Benzonatate', '100mg', 'Capsule'),
(7, 'Medicated Pain Relief', 'Unknown', 'Unknown', 'Cream'),
(8, 'MAXITROL', 'Neomycin, Polymyxin B, Dexamethasone', 'Unknown', 'Ointment'),
(9, 'Denavir', 'Penciclovir', 'Unknown', 'Cream'),
(10, 'METHYLPHENIDATE', 'Methylphenidate', 'Unknown', 'Tablet'),
(11, 'Zinc Oxide and Dimethicone', 'Zinc Oxide, Dimethicone', 'Unknown', 'Cream'),
(12, 'METHADONE HYDROCHLORIDE', 'Methadone', 'Unknown', 'Tablet'),
(13, 'Naproxen', 'Naproxen', '250mg', 'Tablet'),
(14, 'TINTED MOISTURIZER', 'Unknown', 'Unknown', 'Moisturizer'),
(15, 'KETOROLAC TROMETHAMINE', 'Ketorolac', '10mg', 'Injection'),
(16, 'VITALUMIERE AQUA', 'Unknown', 'Unknown', 'Foundation'),
(17, 'PROSTIN', 'Alprostadil', 'Unknown', 'Injection'),
(18, 'ZAFIRLUKAST', 'Zafirlukast', '10mg', 'Tablet'),
(19, 'ALSUMA', 'Unknown', 'Unknown', 'Injection'),
(20, 'Dextroamphetamine Saccharate, Amphetamine Aspartate, Dextroamphetamine Sulfate and Amphetamine Sulfate', 'Dextroamphetamine, Amphetamine', 'Unknown', 'Tablet'),
(21, 'Lidocaine and Prilocaine', 'Lidocaine, Prilocaine', 'Unknown', 'Topical Cream'),
(22, 'KLEENFOAM', 'Unknown', 'Unknown', 'Gel'),
(23, 'Biobron', 'Unknown', 'Unknown', 'Syrup'),
(24, 'Cetirizine Hydrochloride', 'Cetirizine', '10mg', 'Tablet'),
(25, 'Neomycin Polymyxin B Sulfates and Dexamethasone', 'Neomycin, Polymyxin B, Dexamethasone', 'Unknown', 'Ointment'),
(26, 'Vigoril for Men', 'Unknown', 'Unknown', 'Tablet'),
(27, 'Up and Up First Aid Antibiotic', 'Unknown', 'Unknown', 'Ointment'),
(28, 'Clindamycin Hydrochloride', 'Clindamycin', '300mg', 'Capsule'),
(29, 'ADSOL Red Cell Preservation Solution System in Plastic Container (PL 146 Plastic)', 'Unknown', 'Unknown', 'Solution'),
(30, 'Tandem - F', 'Unknown', 'Unknown', 'Injection'),
(31, 'Lidocaine Hydrochloride', 'Lidocaine', 'Unknown', 'Injection'),
(32, 'LANEIGE BB Cushion Dark', 'Unknown', 'Unknown', 'Cosmetic'),
(33, 'Malin and Goetz', 'Unknown', 'Unknown', 'Cream'),
(34, 'Oxy Daily Defense Exfoliating Face Scrub', 'Unknown', 'Unknown', 'Scrub'),
(35, 'Banana Boat Ultra Defense', 'Unknown', 'Unknown', 'Sunscreen'),
(36, 'Eastern Sycamore Pollen', 'Pollen', 'Unknown', 'Allergy Medication'),
(37, 'Oxygen Helium Mixture 30/70', 'Oxygen, Helium', 'Unknown', 'Gas'),
(38, 'Cleocin', 'Clindamycin', '150mg', 'Capsule'),
(39, 'Capture Totale Radiance Restoring Serum Foundation SPF 15 012', 'Unknown', 'Unknown', 'Cosmetic'),
(40, 'Propranolol', 'Propranolol', '10mg', 'Tablet'),
(41, 'LANSOPRAZOLE', 'Lansoprazole', '30mg', 'Capsule'),
(42, 'Aplenzin', 'Bupropion', '174mg', 'Tablet'),
(43, 'CLE DE PEAU BEAUTE PW FOUNDATION s', 'Unknown', 'Unknown', 'Cosmetic'),
(44, 'Butrans', 'Buprenorphine', 'Unknown', 'Patch'),
(45, 'Yat Tip Xiao', 'Unknown', 'Unknown', 'Unknown'),
(46, 'Arbonne Revelage', 'Unknown', 'Unknown', 'Cosmetic'),
(47, 'Vitamin H Velvet Mask', 'Unknown', 'Unknown', 'Mask'),
(48, '60-Second Fluoride', 'Fluoride', 'Unknown', 'Gel'),
(49, 'Burkhart', 'Unknown', 'Unknown', 'Tablet'),
(50, 'Pyrazinamide', 'Pyrazinamide', 'Unknown', 'Tablet'),
(51, 'MUPIROCIN', 'Mupirocin', '2%', 'Ointment'),
(52, 'KOMBIGLYZE', 'Metformin, Saxagliptin', 'Unknown', 'Tablet'),
(53, 'BETHANECHOL CHLORIDE', 'Bethanechol', '10mg', 'Tablet'),
(54, 'Clonidine', 'Clonidine Hydrochloride', '0.1 mg', 'Antihypertensive'),
(55, 'Nicotine Transdermal System', 'Nicotine', '21 mg', 'Smoking Cessation'),
(56, 'ANTIBACTERIAL HAND', 'Triclosan', '1% solution', 'Antiseptic'),
(57, 'LEVOXYL', 'Levothyroxine Sodium', '0.1 mg', 'Thyroid Hormone Replacement'),
(58, 'Super Aqua Night', 'Water, Glycerin', '50 ml', 'Moisturizer'),
(59, 'BETULA LENTA POLLEN', 'Birch Pollen', 'Extract', 'Allergy Relief'),
(60, 'Mucinex', 'Guaifenesin', '600 mg', 'Expectorant'),
(61, 'DentiCare Pro-Foam', 'Fluoride', '40 mg', 'Oral Care'),
(62, 'QueaseX Anti Nausea Drops', 'Meclizine', '25 mg', 'Anti-nausea'),
(63, 'Walgreens Urinary Pain Relief Maximum Strength', 'Phenazopyridine', '95 mg', 'Urinary Analgesic'),
(64, 'In Control Nicotine', 'Nicotine', '21 mg', 'Smoking Cessation'),
(65, 'Cilostazol', 'Cilostazol', '100 mg', 'Antiplatelet'),
(66, 'PRAX', 'N/A', 'N/A', 'N/A'),
(67, 'Cyclafem 1/35', 'Ethinyl Estradiol, Norgestimate', '1 mg, 0.035 mg', 'Oral Contraceptive'),
(68, 'Cimetidine', 'Cimetidine', '200 mg', 'Antacid'),
(69, 'Glipizide and Metformin Hydrochloride', 'Glipizide, Metformin', '5 mg, 500 mg', 'Antidiabetic'),
(70, 'Aurum Metallicum', 'Gold', '30C', 'Homeopathic Remedy'),
(71, 'Mycoplasma Remedy', 'N/A', 'N/A', 'Antimicrobial'),
(72, 'Red Oak', 'Quercus rubra', 'Extract', 'Herbal Remedy'),
(73, 'Dove IS Fresh', 'Water, Glycerin', '50 ml', 'Personal Care'),
(74, 'CLINIMIX', 'Amino Acids, Dextrose', 'Various', 'Parenteral Nutrition'),
(75, 'Atropine Sulfate', 'Atropine', '0.6 mg', 'Antimuscarinic'),
(76, 'Theophylline in Dextrose', 'Theophylline', '100 mg', 'Bronchodilator'),
(77, 'IvyMed', 'Ivy Leaf Extract', '25 mg', 'Herbal Medicine'),
(78, 'FERROUS SULFATE', 'Ferrous Sulfate', '325 mg', 'Iron Supplement'),
(79, 'Medicated', 'N/A', 'N/A', 'Various'),
(80, 'Tekturna', 'Aliskiren', '150 mg', 'Antihypertensive'),
(81, 'Oxymorphone Hydrochloride', 'Oxymorphone', '10 mg', 'Opioid Analgesic'),
(82, 'ELCURE C Serum', 'Vitamin C', '500 mg', 'Supplement'),
(83, 'No7 Dual Action Tinted Moisturiser Medium', 'N/A', 'N/A', 'Cosmetic'),
(84, 'Anti-bacterial Strawberry Kiss Hand', 'Triclosan', '1% solution', 'Antiseptic'),
(85, 'Sertraline', 'Sertraline Hydrochloride', '50 mg', 'Antidepressant'),
(86, 'EIGHT HOUR CREAM SKIN PROTECTANT FRAGRANCE FREE', 'Petrolatum', '50 ml', 'Skin Protectant'),
(87, 'NOEVIR N5', 'N/A', 'N/A', 'Anti-inflammatory'),
(88, 'Orajel Instant Relief for Teething Pain', 'Benzocaine', '10% solution', 'Analgesic'),
(89, 'Topcare Milk of Magnesia', 'Magnesium Hydroxide', '400 mg', 'Laxative'),
(90, 'Arthritis Pain and Joint Relief / Soulagement De La Douleur Arthritique Et Articulaire', 'Menthol', '5% gel', 'Topical Analgesic'),
(91, 'Diltiazem Hydrochloride', 'Diltiazem', '30 mg', 'Calcium Channel Blocker'),
(92, 'Oxygen', 'Oxygen', 'Various', 'Respiratory Support'),
(93, 'NARS FOUNDATION', 'N/A', 'N/A', 'Cosmetic'),
(94, 'EMEND', 'Aprepitant', '125 mg', 'Antiemetic'),
(95, 'Doxycycline', 'Doxycycline Hyclate', '100 mg', 'Antibiotic'),
(96, 'the Balm BalmShelter tinted moisturizer SPF 18 broad spectrum dark', 'Zinc Oxide', '50 ml', 'Sunscreen'),
(97, 'Sodium Bicarbonate', 'Sodium Bicarbonate', '325 mg', 'Antacid'),
(98, 'Azithromycin', 'Azithromycin', '250 mg', 'Antibiotic'),
(99, 'care one all day pain relief', 'Acetaminophen', '500 mg', 'Analgesic'),
(100, 'Azor', 'Amlodipine, Olmesartan', '5 mg, 40 mg', 'Antihypertensive'),
(101, 'Bedwetting', 'Desmopressin', '0.2 mg', 'Antidiuretic'),
(102, 'FIRMAGON', 'Degarelix', '80 mg', 'GnRH Antagonist'),
(103, 'Beyond BB Perfecting Foundation Broad Spectrum SPF 15 Sunscreen', 'N/A', 'N/A', 'Cosmetic'),
(104, 'Medique Sugar Free Medikoff Drops', 'Diphenhydramine', '12.5 mg', 'Cough Suppressant'),
(105, 'BLATELLA GERMANICA', 'German Cockroach', 'Extract', 'Pest Control'),
(106, 'Estradiol', 'Estradiol', '1 mg', 'Estrogen Replacement'),
(107, 'Chlorhexidine Gluconate', 'Chlorhexidine', '0.12% solution', 'Antiseptic'),
(108, 'Lil Drug Store Anti-Diarrheal', 'Loperamide', '2 mg', 'Anti-diarrheal'),
(109, 'Cyanocobalamin', 'Vitamin B12', '1000 mcg', 'Supplement'),
(110, 'Rhizopus oryzae', 'Rhizopus Oryzae', 'Extract', 'Probiotic'),
(111, 'LBEL HYDRATESS', 'N/A', 'N/A', 'Cosmetic'),
(112, 'Sanafitil', 'N/A', 'N/A', 'Health Supplement'),
(113, 'sunmark', 'N/A', 'N/A', 'Varied'),
(114, 'Gatifloxacin', 'Gatifloxacin', '400 mg', 'Antibiotic'),
(115, 'Unagel', 'N/A', 'N/A', 'Topical Gel'),
(116, 'Lomedia 24 Fe', 'Ethinyl Estradiol, Ferrous Fumarate', '0.03 mg, 75 mg', 'Oral Contraceptive'),
(117, 'Elliotts B', 'Vitamin B Complex', 'Various', 'Supplement'),
(118, 'ALNUS INCANA SSP RUGOSA POLLEN', 'Alder Pollen', 'Extract', 'Allergy Relief'),
(119, 'Steiro', 'N/A', 'N/A', 'Steroid'),
(120, 'Citalopram', 'Citalopram', '20 mg', 'Antidepressant'),
(121, 'Derma-Glove', 'N/A', 'N/A', 'Glove'),
(122, 'clarithromycin', 'Clarithromycin', '500 mg', 'Antibiotic'),
(123, 'Endure 300 Cida Rinse Gel', 'N/A', 'N/A', 'Oral Care'),
(124, 'Calloused', 'N/A', 'N/A', 'Skin Care'),
(125, 'HYDROCORTISONE ACETATE', 'Hydrocortisone', '25 mg', 'Corticosteroid'),
(126, 'SUN Solar Defense Organic SPF30', 'Zinc Oxide', '50 ml', 'Sunscreen'),
(127, 'Ketoconazole', 'Ketoconazole', '200 mg', 'Antifungal'),
(128, 'Enalapril Maleate', 'Enalapril', '10 mg', 'Antihypertensive'),
(129, 'ISOVUE', 'Iopamidol', '300 mg', 'Contrast Agent'),
(130, 'Papaverine Hydrochloride', 'Papaverine', '30 mg', 'Vasodilator'),
(131, 'Metadate CD', 'Methylphenidate', '20 mg', 'Stimulant'),
(132, 'Medi First Plus Non-Aspirin', 'Acetaminophen', '500 mg', 'Analgesic'),
(133, 'NIFEDIPINE', 'Nifedipine', '10 mg', 'Calcium Channel Blocker'),
(134, 'ISOPROPYL WINTER GREEN RUBBING ALCOHOL', 'Isopropyl Alcohol', '70%', 'Topical Antiseptic'),
(135, 'VP-PNV-DHA', 'Prenatal Vitamins', 'Various', 'Vitamin Supplement');

INSERT INTO TblMedicines (MedicineID, MedicineName, ActiveIngredient, Dosage, DrugType) 
VALUES
(136, 'Paracetamol', 'Paracetamol', '500mg', 'Tablet'),
(137, 'Ibuprofen', 'Ibuprofen', '200mg', 'Tablet'),
(138, 'Aspirin', 'Acetylsalicylic acid', '325mg', 'Tablet'),
(139, 'Amoxicillin', 'Amoxicillin', '500mg', 'Capsule'),
(140, 'Metformin', 'Metformin', '500mg', 'Tablet'),
(141, 'Lisinopril', 'Lisinopril', '10mg', 'Tablet'),
(142, 'Atorvastatin', 'Atorvastatin', '20mg', 'Tablet'),
(143, 'Simvastatin', 'Simvastatin', '20mg', 'Tablet'),
(144, 'Omeprazole', 'Omeprazole', '20mg', 'Capsule'),
(145, 'Prednisone', 'Prednisone', '10mg', 'Tablet'),
(146, 'Losartan', 'Losartan', '50mg', 'Tablet'),
(147, 'Levothyroxine', 'Levothyroxine', '50mcg', 'Tablet'),
(148, 'Hydrochlorothiazide', 'Hydrochlorothiazide', '25mg', 'Tablet'),
(149, 'Diphenhydramine', 'Diphenhydramine', '25mg', 'Tablet'),
(150, 'Ciprofloxacin', 'Ciprofloxacin', '500mg', 'Tablet'),
(151, 'Salbutamol', 'Salbutamol', '100mcg', 'Inhaler'),
(152, 'Cetirizine', 'Cetirizine', '10mg', 'Tablet'),
(153, 'Codeine', 'Codeine', '30mg', 'Tablet'),
(154, 'Tramadol', 'Tramadol', '50mg', 'Tablet'),
(155, 'Furosemide', 'Furosemide', '20mg', 'Tablet');

INSERT INTO TblMedicines (MedicineID, MedicineName, ActiveIngredient, Dosage, DrugType) 
VALUES
(156, 'Doxycycline', 'Doxycycline', '100mg', 'Capsule'),
(157, 'Lorazepam', 'Lorazepam', '1mg', 'Tablet'),
(158, 'Clopidogrel', 'Clopidogrel', '75mg', 'Tablet'),
(159, 'Alprazolam', 'Alprazolam', '0.5mg', 'Tablet'),
(160, 'Gabapentin', 'Gabapentin', '300mg', 'Capsule'),
(161, 'Citalopram', 'Citalopram', '20mg', 'Tablet'),
(162, 'Fluoxetine', 'Fluoxetine', '20mg', 'Tablet'),
(163, 'Metoprolol', 'Metoprolol', '50mg', 'Tablet'),
(164, 'Diazepam', 'Diazepam', '10mg', 'Tablet'),
(165, 'Loratadine', 'Loratadine', '10mg', 'Tablet'),
(166, 'Fexofenadine', 'Fexofenadine', '180mg', 'Tablet'),
(167, 'Prednisolone', 'Prednisolone', '5mg', 'Tablet'),
(168, 'Ranitidine', 'Ranitidine', '150mg', 'Tablet'),
(169, 'Tamsulosin', 'Tamsulosin', '0.4mg', 'Capsule'),
(170, 'Zolpidem', 'Zolpidem', '10mg', 'Tablet'),
(171, 'Nitroglycerin', 'Nitroglycerin', '0.6mg', 'Tablet'),
(172, 'Verapamil', 'Verapamil', '80mg', 'Tablet'),
(173, 'Bupropion', 'Bupropion', '150mg', 'Tablet'),
(174, 'Chloroquine', 'Chloroquine', '250mg', 'Tablet'),
(175, 'Hydroxychloroquine', 'Hydroxychloroquine', '200mg', 'Tablet');

--set identity_insert TblMedicines off
--Drop table TblMedicines

-- 8. Create Table for Tests (Stores details of medical tests)
CREATE TABLE TblTests (
    TestID INT PRIMARY KEY IDENTITY(1,1), -- Unique test identifier
    TestName VARCHAR(255) NOT NULL -- Name of the test (e.g., blood test, X-ray)
);

-- 9. Create Table for Staff
CREATE TABLE TblStaff (
    StaffID INT PRIMARY KEY IDENTITY(1,1), -- Unique doctor identifier
    FirstName VARCHAR(100), -- Doctor's first name
    LastName VARCHAR(100), -- Doctor's last name
    CNIC VARCHAR(20) unique, -- National Identification number
    JoiningDate DATE, -- Date when the doctor joined the hospital
    JobStatus VARCHAR(20) DEFAULT 'active', -- Job status with default value 'active'
    SalaryID INT, -- Link to the salary record of the doctor
    CredentialID INT, -- Link to the doctor's login credentials
    AddressID INT, -- Link to the address of the staff member
    FOREIGN KEY (SalaryID) REFERENCES TblSalary(SalaryID), -- Foreign key linking to the salary record in TblSalary
    FOREIGN KEY (AddressID) REFERENCES TblAddress(AddressID), -- Foreign key linking to the address record in TblAddress
    FOREIGN KEY (CredentialID) REFERENCES TblCredentials(CredentialID) -- Foreign key linking to login credentials in TblCredentials
);

--10 Create Table Visit
CREATE TABLE TblVisits (
    VisitID INT PRIMARY KEY IDENTITY(1,1), -- Unique visit record identifier
    PatientID INT NOT NULL, -- Link to the patient who visited
    DoctorID INT NOT NULL, -- Link to the doctor consulted
    VisitDate DATETIME NOT NULL, -- Date and time of the visi
    FOREIGN KEY (PatientID) REFERENCES TblPatients(PatientID), -- Foreign key linking to patient
    FOREIGN KEY (DoctorID) REFERENCES TblDoctors(DoctorID) -- Foreign key linking to doctor
);
--11 create table for payments
CREATE TABLE TblPayments (
    PaymentID INT PRIMARY KEY IDENTITY(1,1),   -- Unique ID for each payment
    PatientID INT,                              -- Foreign key to the patient
    VisitID INT,                                -- Foreign key to the visit
    CheckupFee DECIMAL(10, 2) NOT NULL,         -- The checkup fee charged for the visit
    PaymentMethod VARCHAR(50) DEFAULT 'cash',   -- Method of payment (e.g., cash, credit card)
    PaymentDate DATETIME2 DEFAULT CURRENT_TIMESTAMP, -- Date and time the payment was made
    PaymentStatus VARCHAR(20) DEFAULT 'Paid',   -- Payment status (e.g., Paid, Pending)
    FOREIGN KEY (PatientID) REFERENCES TblPatients (PatientId), -- Link to patient table
    FOREIGN KEY (VisitID) REFERENCES TblVisits (VisitId)         -- Link to visit table
    ON DELETE CASCADE                            -- Delete payment if the visit is deleted
);

-- 12. Create Table for Symptoms (Stores symptoms for visits or diagnoses)
CREATE TABLE TblSymptoms (
    SymptomID INT PRIMARY KEY IDENTITY(1,1), -- Unique symptom identifier
    SymptomName VARCHAR(255) NOT NULL UNIQUE -- Name of the symptom (e.g., fever, headache)
);

-- 13. Create Table for Diagnoses (Stores various diagnoses)
CREATE TABLE TblDiagnoses (
    DiagnosisID INT PRIMARY KEY IDENTITY(1,1), -- Unique diagnosis identifier
    DiagnosisName VARCHAR(255) NOT NULL UNIQUE -- Name of the diagnosis (e.g., pneumonia, diabetes)
);

-- 14. Create Table for Visit Symptoms (Links symptoms to a particular visit)
CREATE TABLE TblVisitSymptoms (
    VisitID INT NOT NULL, -- Link to the visit record
    SymptomID INT NOT NULL, -- Link to the symptom associated with the visit
    FOREIGN KEY (VisitID) REFERENCES TblVisits(VisitID), -- Foreign key linking to the visit
    FOREIGN KEY (SymptomID) REFERENCES TblSymptoms(SymptomID), -- Foreign key linking to the symptom
    PRIMARY KEY (VisitID, SymptomID) -- Composite primary key to ensure each symptom is linked once per visit
);

-- 15. Create Table for Visit Diagnoses (Links diagnoses to a particular visit)
CREATE TABLE TblVisitDiagnoses (
    VisitID INT NOT NULL, -- Link to the visit record
    DiagnosisID INT NOT NULL, -- Link to the diagnosis associated with the visit
    FOREIGN KEY (VisitID) REFERENCES TblVisits(VisitID), -- Foreign key linking to the visit
    FOREIGN KEY (DiagnosisID) REFERENCES TblDiagnoses(DiagnosisID), -- Foreign key linking to the diagnosis
    PRIMARY KEY (VisitID, DiagnosisID) -- Composite primary key to ensure each diagnosis is linked once per visit
);

-- 16. Create Table for Test Prescriptions (Links tests to visits)
CREATE TABLE TblTestPrescriptions (
    TestPrescriptionID INT PRIMARY KEY IDENTITY(1,1), -- Unique test prescription identifier
    VisitID INT NOT NULL, -- Link to the visit for which the test is prescribed
    TestID INT NOT NULL, -- Link to the test prescribed
    TestInstructions TEXT, -- Instructions for the test (e.g., fasting required)
    FOREIGN KEY (VisitID) REFERENCES TblVisits(VisitID), -- Foreign key linking to the visit record
    FOREIGN KEY (TestID) REFERENCES TblTests(TestID) -- Foreign key linking to the prescribed test
);

--17. Create Table for Prescription
CREATE TABLE TblPrescriptions (
    PrescriptionID INT PRIMARY KEY IDENTITY(1,1), -- Unique prescription identifier
    VisitID INT NOT NULL, -- Link to the visit for which the prescription is made
    MedicineID INT NOT NULL, -- Link to the medicine prescribed
    Dosage VARCHAR(255), -- Dosage details (e.g., 500mg twice daily)
    Duration VARCHAR(100), -- Duration for which the medicine is to be taken (e.g., 7 days)
    FOREIGN KEY (VisitID) REFERENCES TblVisits(VisitID), -- Foreign key linking to the visit record
    FOREIGN KEY (MedicineID) REFERENCES TblMedicines(MedicineID) -- Foreign key linking to the prescribed medicine
);

-- Insert data into TblTests
INSERT INTO TblTests (TestName) VALUES 
('Complete Blood Count (CBC)'), 
('X-ray'),
('MRI Scan'),
('CT Scan'),
('Urinalysis'),
('Lipid Profile'),
('Liver Function Test (LFT)'),
('Thyroid Function Test (TFT)'),
('Blood Glucose Test'),
('Electrocardiogram (ECG)');

-- Insert data into TblSymptoms
INSERT INTO TblSymptoms (SymptomName) VALUES 
('Fever'),
('Headache'),
('Cough'),
('Nausea'),
('Vomiting'),
('Fatigue'),
('Abdominal Pain'),
('Shortness of Breath'),
('Chest Pain'),
('Dizziness');

-- Insert data into TblDiagnoses
INSERT INTO TblDiagnoses (DiagnosisName) VALUES 
('Pneumonia'),
('Diabetes Mellitus'),
('Hypertension'),
('Anemia'),
('Tuberculosis'),
('Heart Failure'),
('Asthma'),
('Migraine'),
('Acute Appendicitis'),
('Chronic Kidney Disease');

--Procedures

-- P1  Search Medicine by name
CREATE PROCEDURE search_medicine_by_name
    @medicine_name NVARCHAR(255)
AS
BEGIN
    SELECT * FROM TblMedicines
    WHERE MedicineName LIKE '%' + @medicine_name + '%'
END


-- P2 Search  Test by name
CREATE PROCEDURE search_test_by_name
    @test_name NVARCHAR(255)
AS
BEGIN
    SELECT * FROM TblTests
    WHERE TestName LIKE '%' + @test_name + '%'
END

-- P3 Get All Distnict Role name (Roles Dropdown) 
CREATE PROCEDURE GetDistinctRoleNames
AS
BEGIN
    SET NOCOUNT ON;
    SELECT DISTINCT RoleName FROM TblRoles;
END;

-- P4 Get role ID of RoleName
CREATE PROCEDURE GetRoleID
    @RoleName NVARCHAR(50),
    @RoleID INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT @RoleID = RoleID
    FROM TblRoles
    WHERE RoleName = @RoleName;

    RETURN @RoleID;
END

-- p5  to get doctors
CREATE PROCEDURE GetDoctors
AS
BEGIN
    SET NOCOUNT ON;
    SELECT FirstName + ' ' + LastName AS FullName FROM TblDoctors;
END;

-- get doctor ID6
CREATE PROCEDURE GetDoctorID
    @FirstName NVARCHAR(50),
    @LastName NVARCHAR(50),
    @DoctorID INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- Retrieve the DoctorID based on FullName (FirstName and LastName)
    SELECT TOP 1 @DoctorID = DoctorID
    FROM TblDoctors
    WHERE FirstName = @FirstName AND LastName = @LastName;

    -- Handle case where no match is found
    IF @DoctorID IS NULL
    BEGIN
        PRINT 'Doctor not found.';
    END
END;

-- p7  Search symptoms by name
CREATE PROCEDURE search_symptoms_by_name
    @symptoms_name NVARCHAR(255)
AS
BEGIN
    SELECT * FROM TblSymptoms
    WHERE SymptomName LIKE '%' + @symptoms_name + '%'
END


-- P8 Search  diagnosis by name
CREATE PROCEDURE search_diagnosis_by_name
    @diagnosis_name NVARCHAR(255)
AS
BEGIN
    SELECT * FROM TblDiagnoses
    WHERE DiagnosisName LIKE '%' + @diagnosis_name + '%'
END

--p9 get Medicine Id
CREATE PROCEDURE GetMedID
    @Medname NVARCHAR(255), -- Input parameter: Medicine name
    @MedID INT OUTPUT       -- Output parameter: Medicine ID
AS
BEGIN
    SET NOCOUNT ON;

    -- Retrieve the MedicineID based on the provided MedicineName
    SELECT @MedID = MedicineID
    FROM TblMedicines
    WHERE MedicineName = @Medname;
END;

--DROP PROCEDURE IF EXISTS GetMedID;

--p10 get Test Id
CREATE PROCEDURE GetTestID
    @Testname NVARCHAR(255), -- Input parameter: Medicine name
    @TestID INT OUTPUT       -- Output parameter: Medicine ID
AS
BEGIN
    SET NOCOUNT ON;

    -- Retrieve the MedicineID based on the provided MedicineName
    SELECT @TestID = TestID
    FROM TblTests
    WHERE TestName = @Testname;
END;

--p11 proc to get Symptoms Id
CREATE PROCEDURE GetSymptomID
    @SymptomName NVARCHAR(255), -- Input parameter: Symptom name
    @SymptomID INT OUTPUT       -- Output parameter: Symptom ID
AS
BEGIN
    SET NOCOUNT ON;

    -- Retrieve the SymptomID based on the provided SymptomName
    SELECT @SymptomID = SymptomID
    FROM TblSymptoms
    WHERE SymptomName = @SymptomName;
END;

--p12 proc to get Diagnosis Id
CREATE PROCEDURE GetDiagnosisID
    @DiagnosisName NVARCHAR(255), -- Input parameter: Diagnosis name
    @DiagnosisID INT OUTPUT       -- Output parameter: Diagnosis ID
AS
BEGIN
    SET NOCOUNT ON;

    -- Retrieve the DiagnosisID based on the provided DiagnosisName
    SELECT @DiagnosisID = DiagnosisID
    FROM TblDiagnoses
    WHERE DiagnosisName = @DiagnosisName;
END;







DECLARE @DoctorID INT;

EXEC GetDoctorID 
    @FirstName = 'Muhammad', 
    @LastName = 'Ahmad', 
    @DoctorID = @DoctorID OUTPUT;

PRINT @DoctorID; -- Prints the DoctorID if found, or NULL if not found



--Testing P4
--DECLARE @RoleID INT;
--EXEC GetRoleID @RoleName = 'Admin', @RoleID = @RoleID OUTPUT;
--PRINT @RoleID;

select *from TblStaff
select *from TblAddress
select *from TblCredentials
select *from TblPatients
select *from TblSalary
select *from TblDoctors
select *from TblVisits