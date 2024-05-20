from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry 

import sqlalchemy
#Database Utility Class
from sqlalchemy.engine import create_engine
# Provides executable SQL expression construct
from sqlalchemy.sql import text
sqlalchemy.__version__


class PostgresqlDB:
    def __init__(self,user_name,password,host,port,db_name):
        """
        class to implement DDL, DQL and DML commands,
        user_name:- username
        password:- password of the user
        host
        port:- port number
        db_name:- database name
        """
        self.user_name = user_name
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.engine = self.create_db_engine()

    def create_db_engine(self):
        """
        Method to establish a connection to the database, will return an instance of Engine
        which can used to communicate with the database
        """
        try:
            db_uri = f"postgresql+psycopg2://{self.user_name}:{self.password}@{self.host}:{self.port}/{self.db_name}"
            return create_engine(db_uri)
        except Exception as err:
            raise RuntimeError(f'Failed to establish connection -- {err}') from err

    def execute_dql_commands(self,stmnt,values=None):
        """
        DQL - Data Query Language
        SQLAlchemy execute query by default as

        BEGIN
        ....
        ROLLBACK

        BEGIN will be added implicitly everytime but if we don't mention commit or rollback explicitly
        then rollback will be appended at the end.
        We can execute only retrieval query with above transaction block.If we try to insert or update data
        it will be rolled back.That's why it is necessary to use commit when we are executing
        Data Manipulation Langiage(DML) or Data Definition Language(DDL) Query.
        """
        try:
            with self.engine.connect() as conn:
                if values is not None:
                    result = conn.execute(text(stmnt),values)
                else:
                    result = conn.execute(text(stmnt))
            return result
        except Exception as err:
            print(f'Failed to execute dql commands -- {err}')

    def execute_ddl_and_dml_commands(self,stmnt,values=None):
        """
        Method to execute DDL and DML commands
        here we have followed another approach without using the "with" clause
        """
        connection = self.engine.connect()
        trans = connection.begin()
        try:
            if values is not None:

                result = connection.execute(text(stmnt),values)
            else:
                result = connection.execute(text(stmnt))
            trans.commit()
            connection.close()
            print('Command executed successfully.')
        except Exception as err:
            trans.rollback()
            print(f'Failed to execute ddl and dml commands -- {err}')
#db_uri = host=localhost,username=postgres,password=postgres,database=pshl_hosp,port = 5432

# Create the engine for database connection
#Defining Db Credentials
USER_NAME = 'postgres'
PASSWORD = 'postgres'
PORT = 5432
DATABASE_NAME = 'project'
HOST = 'localhost'

#Note - Database should be created before executing below operation
#Initializing SqlAlchemy Postgresql Db Instance
db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
engine = db.engine


win = Tk()
win.state('iconic')
win.config(bg='sky blue')
admission_date_entry = DateEntry(win)
discharge_date_entry = DateEntry(win)

admission_date = StringVar()
discharge_date = StringVar()

admission_date_entry.config(textvariable=admission_date)
discharge_date_entry.config(textvariable=discharge_date)


def save():
    if e1.get() == "" or e4.get() == "":
        messagebox.showerror("Error", "All fields are required")
    else:
        # Create the engine for database connection
        db_uri = f"postgresql+psycopg2://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
        engine = create_engine(db_uri)

        try:
            with engine.connect() as conn:
                conn.execute(
                    text("INSERT INTO patient(patient_id, patient_fname, patient_lname, phone, address, age, blood_type, gender, admission_date, discharge_date) VALUES (:p_id, :p_fn, :p_ln, :ph, :add, :age, :b_t, :gen, :adm_d, :dis_d)"),
                    {
                        'p_id': patient_id.get(),
                        'p_fn': patient_fname.get(),
                        'p_ln': patient_lname.get(),
                        'ph': phone.get(),
                        'add': address.get(),
                        'age': age.get(),
                        'b_t': blood_type.get(),
                        'gen': gender.get(),
                        'adm_d': admission_date.get(),  # Assuming admission_date is associated with an entry widget for date input
                        'dis_d': discharge_date.get(),  # Assuming discharge_date is associated with an entry widget for date input
                    }
                )
                conn.commit()  # Commit the transaction
                fetch_data()  # Update the displayed data after insertion
                messagebox.showinfo("SUCCESS", "Record has been inserted")
        except Exception as err:
            messagebox.showerror("Error", f"Failed to insert record: {err}")

def fetch_data():
    try:
        # Create the engine for database connection
        db_uri = f"postgresql+psycopg2://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
        engine = create_engine(db_uri)

        with engine.connect() as conn:
            result = conn.execute(text('SELECT * FROM patient'))
            rows = result.fetchall()

            # Clear existing data in the table widget
            table.delete(*table.get_children())

            # Insert fetched data into the table widget
            for item in rows:
                item = list(item)  # Convert tuple to list for modification
                item[8] = item[8].strftime('%Y-%m-%d ')  # Format scheduled_on
                table.insert('', END, values=item)
    except Exception as err:
        messagebox.showerror('Error', f'Failed to fetch data: {err}')
        print(f'Failed to fetch data -- {err}')



def get_data(event=''):
     cursor_row = table.focus()
     data = table.item(cursor_row)
     row = data['values']
     patient_id.set(row[0])
     patient_fname.set(row[1])
     patient_lname.set(row[2]) 
     phone.set(row[3])
     address.set(row[4])
     age.set(row[5])
     blood_type.set(row[6])
     gender.set(row[7])
     admission_date.set(row[8])
     discharge_date.set(row[9])
   
        



def clear():
    patient_id.set('')
    patient_fname.set('')
    patient_lname.set('')
    phone.set('')
    address.set('')
    age.set('')
    blood_type.set('')
    gender.set('')
    admission_date_entry.set_date(' ')  # Clear admission_date_entry
    discharge_date_entry.set_date(' ')  # Clear discharge_date_entry



    

     
def exit():
     confirm = messagebox.askyesno('confirmation',' ARE YOU SURE YOU WANT TO EXIT')
     if confirm>0:
          win.destroy()
          return
                
     

Label(win,text='PSHL HOSPITAL',font='impack 31 bold',bg='black',fg='white').pack(fill=X)

frame1 = Frame(win,bd=15,relief=RIDGE)
frame1.place(x=0,y=55,width=1535,height=650)

lf1 = LabelFrame(frame1,text='PATIENT',font='ariel 28 bold',bd=10,bg='pink')
lf1.place(x=8,y=0,width=1500,height=600)

Label(lf1,text='patient_id',font='ariel 15',bg='pink').place(x=5,y=50)
Label(lf1,text='patient_fname',font='ariel 15',bg='pink').place(x=5,y=100)
Label(lf1,text='patient_lname',font='ariel 15',bg='pink').place(x=5,y=150)
Label(lf1,text='phone',font='ariel 15',bg='pink').place(x=5,y=200)
Label(lf1,text='address',font='ariel 15',bg='pink').place(x=5,y=250)
Label(lf1,text='age',font='ariel 15',bg='pink').place(x=5,y=300)
Label(lf1,text='blood_type',font='ariel 15',bg='pink').place(x=5,y=350)
Label(lf1,text='gender',font='ariel 15',bg='pink').place(x=500,y=50)
Label(lf1,text='admission_date',font='ariel 15',bg='pink').place(x=500,y=100)
Label(lf1,text='discharge_date',font='ariel 15',bg='pink').place(x=500,y=150)


patient_id = IntVar()
patient_fname = StringVar()
patient_lname = StringVar()
phone= IntVar()
address=StringVar()
age=IntVar()
blood_type=StringVar()
gender=StringVar()
admission_date=DateEntry(lf1)

discharge_date=StringVar()


e1 = Entry(lf1, bd=4)
e1.place(x=200, y=50, width=200)
e1.config(textvariable=patient_id)

e2 = Entry(lf1, bd=4)
e2.place(x=200, y=100, width=200)
e2.config(textvariable=patient_fname)

e3 = Entry(lf1, bd=4)
e3.place(x=200, y=150, width=200)
e3.config(textvariable=patient_lname)

e4 = Entry(lf1, bd=4)
e4.place(x=200, y=200, width=200)
e4.config(textvariable=phone)

e5 = Entry(lf1, bd=4)
e5.place(x=200, y=250, width=200)
e5.config(textvariable=address)

e6 = Entry(lf1, bd=4)
e6.place(x=200, y=300, width=200)
e6.config(textvariable=age)

e7 = Entry(lf1, bd=4)
e7.place(x=200, y=350, width=200)
e7.config(textvariable=blood_type)

e8 = Entry(lf1, bd=4)
e8.place(x=700, y=50, width=200)
e8.config(textvariable=gender)

e9 = Entry(lf1, bd=4)
e9.place(x=700, y=100, width=200)
e9.config(textvariable=admission_date_entry.get())

e10 = Entry(lf1, bd=4)
e10.place(x=700, y=150, width=200)
e10.config(textvariable=discharge_date)



frame2 = Frame(win,bd=15,relief=RIDGE)
frame2.place(x=0,y=500,width=1535,height=240)

s_btn = Button(win,text='Save ',font='ariel 15 bold',bg='green',fg='white',bd=6,cursor='hand2',command=save)
s_btn.place(x=330,y=741,width=290)

c_btn = Button(win,text='Clear',font='ariel 15 bold',bg='blue',fg='white',bd=6,cursor='hand2',command=clear)
c_btn.place(x=650,y=741,width=270)

e_btn = Button(win,text='Exit',font='ariel 15 bold',bg='red',fg='white',bd=6,cursor='hand2',command=exit)
e_btn.place(x=963,y=741,width=270)

scroll_x = ttk.Scrollbar(frame2,orient=HORIZONTAL)
scroll_x.pack(side='bottom',fill='x')

scroll_y = ttk.Scrollbar(frame2,orient=VERTICAL)
scroll_y.pack(side='right',fill='y')

table = ttk.Treeview(frame2, columns=('p_id','p_fn','p_ln','ph','add','age','b_t','gen','adm_d','dis_d'),xscrollcommand=scroll_y.set,yscrollcommand=scroll_x.set )
scroll_x=ttk.Scrollbar(command=table.xview)
scroll_y=ttk.Scrollbar(command=table.yview)

table.heading('p_id',text='patient_id')
table.heading('p_fn',text='patient_fname')
table.heading('p_ln',text='patient_lname')
table.heading('ph',text='phone')
table.heading('add',text='address')
table.heading('age',text='age')
table.heading('b_t',text='blood_type')
table.heading('gen',text='gender')
table.heading('adm_d',text='admission_date')
table.heading('dis_d',text='discharge_date')

table['show'] = 'headings'
table.pack(fill = BOTH,expand=1)

fetch_data()

mainloop()