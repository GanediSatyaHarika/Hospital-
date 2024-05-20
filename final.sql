drop table Bill;
drop table appointment;
DROP TABLE ROOM;
drop table prescription;
drop table insurance;
drop table medicine;
DROP TABLE Emergency_Contact;
DROP TABLE DOCTOR;
DROP TABLE Nurse;
drop table staff;
drop table department;
drop table patient ;

CREATE TABLE Patient (
    Patient_ID INT NOT NULL ,
    Patient_FName VARCHAR(20) NOT NULL,
    Patient_LName VARCHAR(20) NOT NULL,
    Phone BIGINT NOT NULL,
	Address VARCHAR(50) ,
	Age int not NULL,
    Blood_Type  VARCHAR(5) NOT NULL,
    Gender  VARCHAR(10),
    Admission_Date DATE,
    Discharge_Date DATE,
    PRIMARY KEY (Patient_ID),
	CONSTRAINT age_check CHECK (100>age and age> 0) 
    );
insert into Patient(Patient_ID,Patient_FName,Patient_LName,
    Phone,Address,Age,Blood_Type,Gender,Admission_Date,Discharge_Date)
values
(1,'Jahnavi','Sethupathi',9874102589,'Kakinada',25,'A+','Female','2022-02-14','2022-02-22'),
(2,'Sam','Williams',8971002587,'Kadapa',28,'AB-','Bisexual','2022-02-18','2022-05-12'),
(3,'Madhu','Dhaggubati',9870024980,'Vizag',12,'O+','Female','2022-03-12','2022-03-12'),
(4,'Revi','Allu',8874003640,'Kurnool',20,'B-','Male','2022-03-28',NULL),
(5,'Subbayya','Naidu',9974002102,'Kochi',66,'B+','Male','2022-04-23','2022-05-9'),
(6,'Dan','Miller',7878789900,'vijayawada',49,'O-','Gay','2022-05-19','2022-06-20'),
(7,'Emma','Granger',9987410020,'Kochi',33,'A+','Female','2024-06-12',NULL);

select * from patient;

CREATE TABLE Department (
    Dept_ID INT NOT NULL,
    Dept_Head VARCHAR(20) NOT NULL,
    Dept_Name VARCHAR(15) NOT NULL,
    Emp_Count INT,
    PRIMARY  KEY (Dept_ID) 
  );
insert into Department(Dept_ID,Dept_Head,Dept_Name,Emp_Count)
values
(1,'Lavanya Mogili','Cardiology',2),
(2,'Sai Praneeth','Emergency',2),
(3,'Satya Harika','Diagnosis',2),
(4,'Pragnya M','Neurology',2),
(5,'Tom Felton','Oncology',1),
(6,'Ron Grint','ENT',1);
select * from department;


CREATE TABLE Staff (
    Emp_ID INT  NOT NULL,
    Emp_FName  VARCHAR(20) NOT NULL,
    Emp_LName  VARCHAR(20) NOT NULL,
    Emp_Type VARCHAR(15) NOT NULL,
    Address  VARCHAR(50) NOT NULL,
    Dept_ID  INT,
    PRIMARY KEY (Emp_ID),
    FOREIGN KEY (Dept_ID) REFERENCES Department  (Dept_ID),
	CONSTRAINT check_type check(Emp_Type IN ('Doctor','Nurse','Receptionist','Billing Staff')),
	CONSTRAINT check_dept_id_for_doctor_nurse CHECK (
        (Emp_Type IN ('Doctor', 'Nurse') AND Dept_ID IS NOT NULL) OR
        (Emp_Type NOT IN ('Doctor', 'Nurse')))
);
insert into Staff(Emp_ID,Emp_FName,Emp_LName,Emp_Type,Address,Dept_ID)
values
(1,'Sai','Praneeth','Doctor','Ananth',2),
(2,'Satya','Harika','Doctor','Hyderabad',3),
(3,'Lavanya','Mogili','Doctor','Guntur',1),
(4,'Pavani','Aalla','Nurse','Kadapa',2),
(5,'Pragnya','M','Doctor','VZM',4),
(6,'Sai','Sreehas','Nurse','Hyderabad',3),
(7,'Vishnu','Priya','Nurse','Kochi',1),
(8,'Nikitha','Allari','Nurse','Tirupati',4),
(9,'Tom','Felton','Doctor','VZM',5),
(10,'Ron','Grint','Doctor','Kadapa',6),
(11,'Harry','R','Receptionist','Kakinada',NULL),
(12,'Arjun','Sama','Billing Staff','Ananth',NULL);
select * from staff;


CREATE TABLE Doctor (
    Doctor_ID INT NOT NULL ,
    Qualifications VARCHAR(15) NOT NULL,
    Emp_ID INT NOT NULL,
    Specialization VARCHAR(20) NOT NULL,
    Dept_ID INT NOT NULL,
    PRIMARY KEY (Doctor_ID),
    FOREIGN KEY (Emp_ID) REFERENCES Staff (Emp_ID),
    FOREIGN KEY (Dept_ID) REFERENCES Department (Dept_ID)
);
insert into  Doctor(Doctor_ID,Qualifications,Emp_ID,Specialization,Dept_ID)
values
(11,'MD',2,'Cadriology',1),
(12,'MD',5,'Neurology',4),
(13,'MD',1,'Genomics',3),
(14,'MD',3,'Emergency Medicine',2),
(15,'MD',9,'Medical Oncology',5),
(16,'MS',10,'ENT',6);
select * from doctor;


CREATE TABLE Nurse (
    Nurse_ID INT  NOT NULL,
    Patient_ID  INT  NOT NULL,
    Emp_ID  INT NOT NULL,
    Dept_ID INT NOT NULL,
    PRIMARY KEY(Nurse_ID,Patient_ID),
    FOREIGN KEY (Patient_ID) REFERENCES Patient (Patient_ID),
    FOREIGN KEY (Emp_ID) REFERENCES Staff  (Emp_ID),
    FOREIGN KEY (Dept_ID) REFERENCES Department (Dept_ID)
);
insert into  Nurse(Nurse_ID,Patient_ID,Emp_ID,Dept_ID)
values
(1,2,4,2),
(2,1,6,3),
(3,3,7,1),
(4,5,8,4),
(2,4,6,3),
(3,4,7,1);
select * from Nurse;

CREATE TABLE Emergency_Contact(
    Contact_ID int  NOT NULL,
    Contact_Name VARCHAR(25) NOT NULL,
    Phone bigint NOT NULL,
    Relation VARCHAR(20) NOT NULL,
    Patient_ID  int NOT NULL,
    PRIMARY KEY (Contact_ID),
    FOREIGN KEY (Patient_ID) REFERENCES Patient (Patient_ID)
);
insert into Emergency_Contact(Contact_ID,Contact_Name,Phone,Relation,Patient_ID)
values
(1,'Jay',9365465685,'Sibling',1),
(2,'Reetu',7536535236,'Sister',2),
(3,'Meena',8543653654,'Parent',4),
(4,'Arun',9364535411,'Brother',6),
(5,'Divya',7543652325,'Parent',5),
(6,'Sushma',8354654512,'Sibling',7);
select * from Emergency_Contact;

create table Insurance (
    Policy_Number VARCHAR(20) NOT NULL,
    Patient_ID int NOT NULL,
    Ins_Code VARCHAR(20) NOT NULL,
    End_Date date,
    Provider VARCHAR(20),
    PRIMARY  KEY (Policy_Number),
    FOREIGN KEY (Patient_ID) REFERENCES Patient (Patient_ID)
);
insert into Insurance(Policy_Number,Patient_ID,Ins_Code,end_Date,Provider)
values
('B5436',1,'INS365','2024-12-31','FGH Insurance'),
('D5432',2,'INS865','2024-10-31','KHD Insurance'),
('H5465',4,'INS683','2030-09-30','YFC Insurance'),
('J6543',5,'INS678','2025-05-31','JGT Insurance'),
('L8756',6,'INS345','2026-06-30','DHF Insurance'),
('F3542',7,'INS465','2029-11-30','ADH Insurance');
select * from Insurance;

CREATE TABLE Medicine (
    Medicine_ID int  NOT NULL,
    M_Name VARCHAR(20) NOT NULL,
    M_Quantity INT NOT NULL,
    M_Cost int NOT NULL,
    PRIMARY KEY (Medicine_ID)
    );
INSERT INTO Medicine (Medicine_ID,M_Name, M_Quantity ,M_Cost)
VALUES
(1,'Aspirin', 150,6),
(2,'Ibuprofen',100,8),
(3,'Amoxicillin',125,13),
(4,'Lisinopril',80,10),
(5,'Atorvastatin',100,22),
(6,'Erbitux',200,5);
SELECT * FROM Medicine;

CREATE TABLE Prescription (
    Prescription_ID INT  NOT NULL,
    Patient_ID  INT  NOT NULL,
    Medicine_ID  INT  NOT NULL,
    Date  DATE,
    Dosage  int,
    Doctor_ID INT NOT NULL,
    PRIMARY KEY (Prescription_ID),
    FOREIGN KEY (Patient_ID) REFERENCES Patient (Patient_ID),
    FOREIGN KEY (Doctor_ID) REFERENCES Doctor (Doctor_ID),
    FOREIGN KEY (Medicine_ID) REFERENCES Medicine (Medicine_ID)
);
INSERT INTO Prescription(prescription_id,Patient_ID, Medicine_ID,Date,Dosage,Doctor_ID)
values
(1,1,1,'2022-12-03',3,11),
(2,2,3,'2023-11-06',2,12),
(3,3,2,'2024-03-14',2,13),
(4,6,5,'2024-04-23',3,14),
(5,5,4,'2023-05-08',3,12),
(6,7,2,'2024-08-10',2,13);
select * from Prescription;

CREATE TABLE Appointment (
    Appt_ID INT  NOT NULL ,
    Scheduled_On  timestamp default CURRENT_TIMESTAMP,
    Date  DATE,
    Time TIME,
    Doctor_ID INT NOT NULL,
    Patient_ID  INT NOT NULL,
    PRIMARY KEY (Appt_ID),
    FOREIGN KEY (Doctor_ID) REFERENCES Doctor (Doctor_ID), 
    FOREIGN KEY (Patient_ID) REFERENCES Patient (Patient_ID)
);
INSERT INTO Appointment(Appt_ID,Scheduled_On,Date,Time,Doctor_ID,Patient_ID)
values 
(1,'2022-02-14 1:00:00','2022-02-14','6:00:00',11,1),
(2,'2022-02-14 6:00:00','2022-02-15','12:00:00',11,1),
(3,'2022-02-17 22:00:00','2022-02-18','1:00:00',12,2),
(4,'2022-03-12 19:00:00','2022-03-12','19:15:00',13,3),
(5,'2022-03-28 12:00:00','2022-03-28','17:00:00',14,4),
(6,'2022-03-28 17:00:00','2022-03-26','10:00:00',14,4),
(7,'2022-04-23 14:00:00','2022-04-23','16:00:00',12,5),
(8,'2022-05-19 6:00:00','2022-05-19','7:00:00',13,6),
(9,'2022-05-19 7:00:00','2022-06-19','20:00:00',13,6);
select * from appointment;

CREATE TABLE  Room (
    Room_ID INT NOT NULL GENERATED BY DEFAULT AS IDENTITY (START WITH 1 INCREMENT BY 1),
    Room_Type VARCHAR(50) NOT NULL,
    Patient_ID  int ,
    Room_Cost  int,
    PRIMARY KEY (Room_ID),
    FOREIGN KEY (Patient_ID) REFERENCES Patient (Patient_ID)
    );
insert into Room(Room_Type,Room_Cost)
VALUES
('General',200),
('General',200),
('General',200),
('General',200),
('General',200),
('Non-AC',500),
('Non-AC',500),
('Non-AC',500),
('Non-AC',500),
('AC',1000),
('AC',1000),
('AC',1000),
('AC',1000),
('Deluxe',1500),
('Deluxe',1500),
('Deluxe',1500),
('Non-AC',500),
('Non-AC',500),
('Non-AC',500),
('AC',1000);
update room
set patient_id = 7 where room_id = 6;
update room
set patient_id = 4 where room_id = 1;
select * from Room order by room_id;

CREATE TABLE Bill (
    Bill_ID INT NOT NULL ,
    Date  DATE,
    Room_Cost int,
    Test_Cost  int NOT NULL DEFAULT 100,
    Med_Cost int,
    Total  int,
    Patient_ID INT NOT NULL,
    Policy_Number VARCHAR(20),
    PRIMARY KEY (Bill_ID),
    FOREIGN KEY (Patient_ID) REFERENCES Patient (Patient_ID),
    FOREIGN KEY (Policy_Number) REFERENCES Insurance (Policy_Number)
);
insert into Bill(Bill_ID,Date,Room_Cost ,Test_Cost,Med_Cost,Total,Patient_ID,Policy_Number)
values
(101,'2022-02-22',200,175,6,381,1,'B5436'),
(102,'2022-2-18',1000,250,13,1263,2,'D5432'),
(103,'2022-03-12',500,180,8,688,3,'F3542'),
(104,now(),1500,300,22,1822,6,'L8756'),
(105,'2022-04-23',1000,270,10,1280,5,'J6543');
select * from bill;

-------------------------Queries--------------------------------------------------
SELECT p.patient_id, p.Patient_FName||' '|| p.Patient_LName as patient,d.Doctor_ID, d.Qualifications,
d.Specialization
FROM Patient p
INNER JOIN Appointment a ON p.Patient_ID = a.Patient_ID
INNER JOIN Doctor d ON a.Doctor_ID = d.Doctor_ID
WHERE a.Date = '2022-02-18';

SELECT 
    p.Patient_ID, p.Patient_FName||' '|| p.Patient_LName AS Patient,
    d.Doctor_ID, s.Emp_FName||' '||s.Emp_LName AS Doctor,
    a.Date AS Appointment_Date
FROM Patient p
INNER JOIN Appointment a ON p.Patient_ID = a.Patient_ID
INNER JOIN Doctor d ON a.Doctor_ID = d.Doctor_ID
INNER JOIN Staff s on d.Emp_ID = s.Emp_ID;

SELECT 
    p.Patient_ID, p.Patient_FName || ' '|| p.Patient_LName as patient,
    r.Room_Type
FROM Patient p
INNER JOIN Room r ON p.Patient_ID = r.Patient_ID;

SELECT 
    p.Patient_ID,
	p.Patient_FName || ' '|| p.Patient_LName as patient,
    a.Date ||' , '||a.Time AS Appointment_Date_Time
FROM Patient p
INNER JOIN Appointment a ON p.Patient_ID = a.Patient_ID
WHERE a.Doctor_ID = 13;

SELECT 
    d.Doctor_ID,
    s.Emp_FName|| ' '|| s.Emp_LName AS Doctor,
    COUNT(a.Appt_ID) AS Total_Appointments
FROM Doctor d
LEFT JOIN staff s ON d.Emp_ID = s.Emp_ID
LEFT JOIN Appointment a ON d.Doctor_ID = a.Doctor_ID
GROUP BY d.Doctor_ID, s.Emp_FName, s.Emp_LName;
------------------------------------FUNCTIONS-----------------------------------------------

CREATE or replace FUNCTION UpdatePatientInfoFunction(p_id INT,
    new_phone bigint default NULL,
	new_address varchar default NULL
)
RETURNS TEXT
language plpgsql AS $$
BEGIN
	if(new_phone is not NULL and new_address is not null) then begin
		UPDATE Patient 	SET Phone = new_phone ,Address = new_address WHERE Patient_ID = p_id;
		return 'Updated';
	end; end if;
	if(new_phone is NULL and new_address is not NULL) then  begin
		UPDATE Patient 	SET Address = new_address WHERE Patient_ID = p_id;
		return 'Updated'; 
	end; end if;
	IF(new_address is NULL and new_phone is not NULL) then  begin
		UPDATE Patient
    	SET Phone = new_phone WHERE Patient_ID = p_id;
		return 'Updated'; end;
	else RETURN 'Give valid changes';
	end if;
END;
$$;
select UpdatePatientInfoFunction(7,'8041002369');
select * from patient where patient_id = 7;

CREATE or REPLACE FUNCTION AddPatientFunction(
	p_fname VARCHAR,
    p_lname VARCHAR,
    p_phone BIGINT,
	p_address VARCHAR,
    p_age INT,
    p_blood_type VARCHAR(5),
    p_gender VARCHAR,
    p_admission_date DATE DEFAULT CURRENT_DATE,
    p_discharge_date DATE DEFAULT NULL 
)
RETURNS INT
language plpgsql AS $$
DECLARE new_patient_id INT;
BEGIN
-- Insert patient record into Patient table
	select max(patient_id) into new_patient_id from patient;
	new_patient_id = new_patient_id + 1;
    INSERT into Patient(Patient_ID,Patient_FName, Patient_LName, Phone,Address, Age, Blood_Type, Gender, Admission_Date, Discharge_Date)
    VALUES (new_patient_id,p_fname, p_lname, p_phone,p_address, p_age, p_blood_type, p_gender, p_admission_date, p_discharge_date);
	select patient_id into new_patient_id from patient where Patient_LName = p_Lname and Patient_LName= p_Lname;
    -- Get the ID of the newly inserted patient
   RETURN new_patient_id;
END;
$$;
select AddPatientFunction('Manas','Bairstow',8974005898,'Banglore',27,'A-','Male');
select * from patient where patient_id = 8;

CREATE OR REPLACE FUNCTION CheckDoctorAvailability(DoctorID INT, AppointmentDate DATE, AppointmentTime TIME)
RETURNS INT
LANGUAGE plpgsql AS $$
DECLARE
    isAvailable INT;
BEGIN
    SELECT COUNT(*) INTO isAvailable FROM Appointment
    WHERE Doctor_ID = DoctorID AND Date = AppointmentDate AND Time = AppointmentTime;

    IF isAvailable > 0 THEN
        RETURN 0; -- Doctor is not available
    ELSE
        RETURN 1; -- Doctor is available
    END IF;
END;
$$;
SELECT CheckDoctorAvailability(11, '2022-02-15', '06:00:00');

CREATE OR REPLACE FUNCTION ScheduleAppointment(p_id INT, d_id INT ,app_date date default null, app_time time default null)
RETURNS text
LANGUAGE plpgsql AS $$
DECLARE A_DATE DATE;
A_TIME TIME;
A_ID INT;
BEGIN
LOOP
	SELECT MAX(APPT_ID) INTO A_ID FROM Appointment;
	A_ID = A_ID + 1;
	A_DATE = app_date; A_TIME = app_time;
	if(A_DATE is NULL) then	SELECT CURRENT_DATE + cast(floor(RANDOM()*(5- 1) + 1 )as int) INTO A_DATE; end if;
	if(A_TIME is NULL) then	SELECT CAST(FLOOR(RANDOM()*24) || ' hours' AS INTERVAL) INTO A_TIME; end if;
	if (select CheckDoctorAvailability(d_id,A_DATE,A_TIME)) then
	begin
		INSERT INTO Appointment (APPT_ID,Scheduled_on,Date,time,doctor_id,patient_id)
		VALUES (A_ID,CURRENT_DATE,A_DATE,A_TIME,d_id,p_id);
		return 'Scheduled at'||' '||A_DATE::text|| ','||A_Time::TEXT|| ' and appointment id =' ||A_ID::TEXT;
	end; 
	end if;
end LOOP;
END;
$$;
select ScheduleAppointment(7,11);
select * from appointment where appt_id = 10;

CREATE OR REPLACE FUNCTION AddPrescription(
    patient_id INT,
    medicine_id INT,
    dosage INT,
    doctor_id INT,
	a_date date default NULL
)
RETURNS TEXT
LANGUAGE plpgsql AS $$
DECLARE pres_id int;
BEGIN
	SELECT MAX(Prescription_ID) + 1 INTO pres_ID FROM prescription;
	IF(a_date is NULL) then a_date = CURRENT_DATE ; end if;
    INSERT INTO Prescription (prescription_id, Patient_ID, Medicine_ID, Date, Dosage, Doctor_ID)
    VALUES (pres_id ,patient_id, medicine_id, a_date, dosage, doctor_id);
    RETURN 'Prescription added';
END;
$$;
select AddPrescription(8,2,5,11);
select * from prescription;

CREATE OR REPLACE FUNCTION DoctorsAppointmentFunction(
    d_id INT
)
RETURNS TABLE (
    Appt_ID INT,
    Scheduled_On TIMESTAMP,
    Date DATE,
    ime TIME,
    Patient_ID INT
)
language plpgsql AS $$
BEGIN
    -- Return appointments for the input doctor id
    RETURN QUERY(
        SELECT Appointment.Appt_ID, Appointment.Scheduled_On, Appointment.Date, appointment.Time, Appointment.Patient_ID
        FROM Appointment
        WHERE Doctor_ID = d_id
    );
END;
$$;
SELECT DoctorsAppointmentFunction(13);

CREATE OR REPLACE FUNCTION DischargePatient(p_id INT)
RETURNS text
LANGUAGE plpgsql as $$
DECLARE D_DATE DATE;
	ret_text text;
BEGIN
	select discharge_date into d_date from patient where patient_id = p_id;
	IF (d_date is NULL) then
	begin 
	UPDATE Patient 
	SET Discharge_Date = CURRENT_DATE WHERE Patient_ID = p_id;
	return 'Discharged';
	end ;
	else raise notice 'Already discharged' ;
	end if;
end;
$$;
select DischargePatient(7);
select * from patient where patient_id = 7;

CREATE OR REPLACE FUNCTION AllotRoom(r_type VARCHAR(50), p_id INT
)
RETURNS TEXT
LANGUAGE plpgsql AS $$
DECLARE r_count int ;
	r_id int;
BEGIN
	select count(*)into r_count from room where room_type = r_type and patient_id is NULL group by room_type,patient_id;
	if(p_id in (select patient_id from room )) then  
		return 'Already alloted ';
	end if;
	if (r_count != 0) then
	begin
		select room_id into r_id from room where room_type = r_type and patient_id is NULL order by room_id limit 1;
		update room
		set patient_id = p_id where room_id = r_id;
		RETURN r_id::text||' '||'Room alloted';
	end;
	else return 'Room unavailable';
	end if; 
END;
$$;
select AllotRoom('AC',8);
select * from room order by room_id ;

CREATE OR REPLACE  FUNCTION GetTotalPatientsByBloodType()
RETURNS TABLE (BloodType VARCHAR(5), TotalPatients bigINT)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT Blood_Type, COUNT(*) AS TotalPatients
    FROM Patient INNER JOIN room on room.patient_id = Patient.patient_id
    GROUP BY Blood_Type;
END; $$;
SELECT * FROM GetTotalPatientsByBloodType();

CREATE OR REPLACE  FUNCTION GetPatientAgeGroupCount()
RETURNS TABLE (AgeGroup TEXT, Count bigINT)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT
        CASE
            WHEN Age < 18 THEN 'Children'
            WHEN Age >= 18 AND Age < 60 THEN 'Adults'
            ELSE 'Seniors'
        END AS AgeGroup,
        COUNT(*) AS Count
    FROM Patient
    GROUP BY AgeGroup;
END;
$$;
SELECT * FROM GetPatientAgeGroupCount();

CREATE OR REPLACE FUNCTION GetTotalBillsByPatient()
RETURNS TABLE (PatientName text, TotalBills bigINT)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT CONCAT(P.Patient_FName, ' ', P.Patient_LName) AS PatientName, COUNT(*) AS TotalBills
    FROM Patient P
    JOIN Bill B ON P.Patient_ID = B.Patient_ID
    GROUP BY P.Patient_ID;
END;
$$;

SELECT * FROM GetTotalBillsByPatient();

--------------------TRIGGER--------------------
CREATE OR REPLACE FUNCTION RemovePatientFromRoomTrigger()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if the patient is discharged or discharge date is set
    IF NEW.Discharge_Date = CURRENT_DATE or NEW.Discharge_date < CURRENT_DATE THEN
        -- Update the room to remove the patient
        UPDATE Room
        SET Patient_ID = NULL WHERE Patient_ID = NEW.Patient_ID;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER RemovePatientFromRoom
AFTER UPDATE OF Discharge_Date ON Patient
FOR EACH ROW
EXECUTE FUNCTION RemovePatientFromRoomTrigger();
select Dischargepatient(8);
select * from room order by room_id;

CREATE OR REPLACE FUNCTION update_medicine_quantity()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    UPDATE Medicine
    SET M_Quantity = M_Quantity - NEW.Dosage
    WHERE Medicine_ID = NEW.Medicine_ID;
    RETURN NEW;
END;
$$ ;
CREATE TRIGGER update_medicine_trigger 
AFTER INSERT ON Prescription
FOR EACH ROW
EXECUTE FUNCTION update_medicine_quantity();
select * from medicine;
select addprescription(5,1,10,11);
select * from medicine order by medicine_id;

CREATE OR REPLACE FUNCTION CheckPatientAndDoctorExistenceTrigger()
RETURNS TRIGGER
LANGUAGE plpgsql as $$
BEGIN
    -- Check if the patient exists in the Patient table
    IF NOT EXISTS (SELECT 1 FROM Patient WHERE Patient_ID = NEW.Patient_ID) THEN
        RAISE EXCEPTION 'Patient does not exist';
    END IF;
    -- Check if the doctor exists in the Doctor table
    IF NOT EXISTS (SELECT 1 FROM Doctor WHERE Doctor_ID = NEW.Doctor_ID) THEN
        RAISE EXCEPTION 'Doctor does not exist';
    END IF;
	IF NOT EXISTS(select 1 FROM appointment where Doctor_ID = NEW.Doctor_ID and  Patient_ID = NEW.Patient_ID) then
		RAISE EXCEPTION 'No appointement between doctor and patient';
	END if;
    RETURN NEW;
END;
$$ ;
CREATE TRIGGER EnsurePatientAndDoctorExistence
BEFORE INSERT ON Prescription
FOR EACH ROW
EXECUTE FUNCTION CheckPatientAndDoctorExistenceTrigger();
select addprescription(5,1,10,13);
select * from prescription;

CREATE OR REPLACE FUNCTION update_dept_emp_count()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE Department
        SET Emp_Count = Emp_Count + 1 WHERE Dept_ID = NEW.Dept_ID;
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE Department
        SET Emp_Count = Emp_Count - 1 WHERE Dept_ID = OLD.Dept_ID;
        RETURN OLD;
    END IF;
END;
$$;
CREATE TRIGGER update_dept_emp_count_t
AFTER INSERT OR DELETE ON Staff FOR EACH ROW
EXECUTE FUNCTION update_dept_emp_count();
INSERT INTO STAFF(emp_id,emp_fname,emp_lname,emp_type,address,dept_id)
VALUES (13,'Son','Vals','Nurse','Kochi',6);
select * from department where dept_id = 6;

CREATE OR REPLACE FUNCTION PreventDoubleBooking()
RETURNS TRIGGER AS $$
DECLARE
    existingAppointmentCount INT;
BEGIN
    -- Count existing appointments for the doctor at the given time
    SELECT COUNT(*) INTO existingAppointmentCount FROM Appointment
    WHERE Doctor_ID = NEW.Doctor_ID AND Date = NEW.Date  AND Time = NEW.Time;
    -- Check if the doctor is already scheduled at the same time
    IF existingAppointmentCount > 0 THEN
        RAISE EXCEPTION 'Doctor is already scheduled for an appointment at this time';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER CheckDoubleBooking
BEFORE INSERT ON Appointment
FOR EACH ROW
EXECUTE FUNCTION PreventDoubleBooking();
select* from appointment;
insert into appointment values(11,now(),'2024-05-04','03:50:00',11,5)

CREATE OR REPLACE FUNCTION update_room_cost()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.Room_Type = 'AC' THEN
        NEW.Room_Cost := 1000;
    ELSIF NEW.Room_Type = 'Non-AC' THEN
        NEW.Room_Cost := 500;
    ELSIF NEW.Room_Type = 'Deluxe' THEN
        NEW.Room_Cost := 1500;
    ELSIF NEW.Room_Type = 'General' THEN
        NEW.Room_Cost := 200;
	ELSE 
		raise notice 'Not a valid room type';
    END IF;
    RETURN NEW;
END;
$$;
CREATE TRIGGER update_room_cost_trigger
BEFORE INSERT ON Room FOR EACH ROW
EXECUTE FUNCTION update_room_cost();
insert into room(room_type) values ('Deluxe');
select * from room order by room_id;
---role-1-----  reset role drop role admin
CREATE ROLE admin;
GRANT ALL ON DATABASE pshl_hosp to admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON DATABASE pshl_hosp TO admin;
----role-2---
CREATE ROLE doctor;
GRANT SELECT ON Patient, Prescription, Appointment,Doctor,Medicine TO doctor;
GRANT INSERT ON Prescription TO Doctor;
---role-3--
CREATE ROLE nurse;
GRANT SELECT ON Patient, Room, Nurse,Prescription TO nurse;
---role-4---
CREATE ROLE receptionists;
GRANT SELECT, INSERT, UPDATE ON Appointment,Emergency_Contact,Patient TO receptionists;
GRANT SELECT,UPDATE ON room to receptionists;
---role-5---
CREATE ROLE  billing_staff;
GRANT SELECT, INSERT, UPDATE ON Bill TO billing_staff;
GRANT SELECT, UPDATE ON medicine TO billing_staff;
GRANT SELECT ON prescription,room,insurance TO billing_staff;

--------------------------------------------
select addpatientfunction('Jack','Wang',9988665500,'Kurnool',35,'O+','Gender');
select scheduleappointment(9,15);
select addprescription(9,4,10,15,'2024-04-30');
select allotroom('Deluxe',9);
select scheduleappointment(9,15);
select updatepatientinfofunction(9, NULL, 'Kochi');
select * from patient;
-----VIEW-1---
CREATE VIEW Insurance_Details AS
SELECT pa.Patient_FName||' '||pa.Patient_LName AS Patient_name,i.*
FROM Insurance i
JOIN Patient pa ON i.Patient_ID = pa.Patient_ID;
SELECT * FROM INSURANCE_DETAILS;
---view-2---
CREATE VIEW Room_Occupancy AS
SELECT r.*, pa.Patient_FName||'  '||pa.Patient_LName as Patient_name
FROM Room r
JOIN Patient pa ON r.Patient_ID = pa.Patient_ID;
select * from room_occupancy;
-------view-3---
CREATE or REPLACE VIEW Nurse_Assignments AS
SELECT nurse_id,n.dept_id,s.emp_fname||' '||s.emp_lname as nurse, 
pa.patient_id,pa.Patient_FName||' '|| pa.Patient_LName as patient
FROM Nurse n
JOIN Patient pa ON n.Patient_ID = pa.Patient_ID
LEFT JOIN Staff s ON n.Emp_ID = s.Emp_ID;
SELECT * FROM NURSE_ASSIGNMENTS;
---view-4--
CREATE or replace VIEW Emergency_Contacts AS
SELECT contact_name as relative,e.phone,relation, pa.Patient_FName||' '|| pa.Patient_LName as patient
FROM Emergency_Contact e
JOIN Patient pa ON e.Patient_ID = pa.Patient_ID;
select * from emergency_contacts;
----view-5---
CREATE VIEW Department_Overview AS
SELECT d.*, Emp_ID,emp_lname||' '||emp_fname as Employee_name
FROM Department d
LEFT JOIN Staff s ON d.Dept_ID = s.Dept_ID WHERE d.dept_head != emp_fname||' '||emp_lname ;
select * from department_overview;



----------------


SET ROLE receptionists;
-- Query to view patient appointments
SELECT P.Patient_ID, P.Patient_FName, P.Patient_LName, A.Appt_ID, A.Scheduled_On, A.Date, A.Time
FROM Patient P
JOIN Appointment A ON P.Patient_ID = A.Patient_ID;

-- Query to view patient emergency contacts // ROLE receptionist
SELECT P.Patient_FName||' '||P.Patient_LName as patient, E.Contact_Name, E.Phone, E.Relation
FROM Patient P
JOIN Emergency_Contact E ON P.Patient_ID = E.Patient_ID;

reset role;
-------
SET ROLE billing_staff;
-- Query using GetTotalBillsByPatient function to calculate total bills for each patient
SELECT PatientName, TotalBills
FROM GetTotalBillsByPatient();

--total no.of bills and total payment done in year 2022
select count(*),sum(total) from bill where extract(year from bill.date) = 2022 ;
reset role;

SET ROLE admin;
-- Query using GetTotalPatientsByBloodType function to calculate total patients by blood type
SELECT BloodType, TotalPatients
FROM GetTotalPatientsByBloodType();
RESET role;

SET ROLE doctor;
-- Query to view patient details along with prescriptions
SELECT P.Patient_ID, P.Patient_FName||' '||P.Patient_LName as patient, P.Phone, P.Address,
       PR.Prescription_ID, PR.Medicine_ID, PR.Date, PR.Dosage
FROM Patient P
JOIN Prescription PR ON P.Patient_ID = PR.Patient_ID;
reset role;
---------------------indexes---------------
--1--
drop index blood_type_count;
CREATE  INDEX blood_type_count ON patient USING HASH(blood_type);
explain analyze SELECT Blood_Type, COUNT(*) AS Count
FROM Patient
WHERE Blood_Type = 'O+' GROUP BY Blood_Type;
explain analyze select * from patient 
WHERE Blood_Type = 'A+' and gender = 'Female';
--2--
drop index prescription_range;
create index prescription_range on prescription(date);
explain analyse SELECT *
FROM Prescription
WHERE Date >= '2023-01-01';
--3--
drop index idx_patient_age;
CREATE INDEX idx_patient_age ON Patient (Age);
explain analyze SELECT r.*, p.Patient_FName, p.Patient_LName,age
FROM Room r
JOIN Patient p ON r.Patient_ID = p.Patient_ID
WHERE p.Age > 50;
--4--
drop index idx_appointment_date
CREATE INDEX idx_appointment_date ON Appointment USING HASH(Date);
explain analyze select * from appointment where date = '2022-02-14'
--5--
drop index idx_room_room_type;
CREATE INDEX idx_room_room_type ON Room (Room_Type);
explain analyze SELECT Room_Type, COUNT(Patient_ID) AS NumberOfPatients
FROM Room
WHERE Room_Type = 'Deluxe'
GROUP BY Room_Type;
select * from room
------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION view_doctor_patient_details(did INT)
RETURNS TABLE (
    doctor_id INT,
    doctor_fname VARCHAR(20),
    doctor_lname VARCHAR(20),
    qualifications VARCHAR(15),
    specialization VARCHAR(20),
    patient_id INT,
    patient_fname VARCHAR(20),
    patient_lname VARCHAR(20),
    phone BIGINT,
    address VARCHAR(50),
    age INT,
    blood_type VARCHAR(5),
    gender VARCHAR(10),
    admission_date DATE,
    discharge_date DATE,
    prescription_id INT,
    medicine_id INT,
    medicine_name VARCHAR(20),
    dosage INT,
    prescription_date DATE,
    bill_id INT,
    bill_date DATE,
    total_cost INT
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT
        D.Doctor_ID ,
        S.Emp_FName,   S.Emp_LName ,
        D.Qualifications,
        D.Specialization ,
        P.Patient_ID ,
        P.Patient_FName , P.Patient_LName ,
        P.Phone ,
        P.Address ,
        P.Age ,
        P.Blood_Type ,
        P.Gender ,
        P.Admission_Date ,
        P.Discharge_Date ,
        Pr.Prescription_ID ,
        Pr.Medicine_ID ,
        M.M_Name ,
        Pr.Dosage ,
        Pr.Date ,
        B.Bill_ID ,
        B.Date ,
        B.Total
    FROM
        Doctor D
    JOIN
        APPOINTMENT A ON A.doctor_id = D.doctor_id
join
   staff S on S.Emp_id = D.Emp_id
    JOIN
        Prescription Pr ON Pr.patient_id = A.patient_id
    JOIN
        Patient P ON Pr.Patient_ID = P.Patient_ID
    JOIN
        Medicine M ON Pr.Medicine_ID = M.Medicine_ID
    JOIN
        Bill B ON P.Patient_ID = B.Patient_ID
    WHERE
        D.doctor_id =did;
END;
$$;
SELECT *  FROM  view_doctor_patient_details(12);

---------------------------------------------------------
create or replace function getbill(p_id int)
returns total int;
language plpgsql as $$;
declare admission date;
	now_d date;
	mul int;
	n int ;
begin
	select admission_date into admission from patient where patient_id = p_id;
	if(now_d is NULL) then begin
		now_d = current_date ;
	end;
	end if;
	total = date(discharge) - date(admission);
	select room_cost into mul from room;
	total = mul * total;
	select  from


