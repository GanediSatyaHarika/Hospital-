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

root = Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)
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
            raise RuntimeError(f'Failed to establish connection -- {err}') from er
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


def display():    
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

    def save():
        if e1.get() == "" or e4.get() == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            try:
                with engine.connect() as conn:
                    conn.execute(
                        text("INSERT INTO room (room_id, room_type, patient_id, room_cost) VALUES (:r_id, :r_t, :p_id, :r_c)"),
                        {
                            'r_id': room_id.get(),
                            'r_t': room_type.get(),
                            'p_id': patient_id.get(),
                            'r_c': room_cost.get()
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
                result = conn.execute(text('SELECT * FROM room'))
                rows = result.fetchall()

                # Clear existing data in the table widget
                table.delete(*table.get_children())

                # Insert fetched data into the table widget
                for item in rows:
                    # Convert room_type to string explicitly to avoid display issues
                    item = list(item)
                    item[1] = str(item[1])  # Assuming room_type is at index 1
                    table.insert('', END, values=item)
        except Exception as err:
            messagebox.showerror('Error', f'Failed to fetch data: {err}')
            print(f'Failed to fetch data -- {err}')


    def get_data(event=''):
        cursor_row = table.focus()
        data = table.item(cursor_row)
        row = data['values']
        room_id.set(row[0])
        room_type.set(row[1])
        patient_id.set(row[2]) 
        room_cost.set(row[3])    
        



    def clear():
        room_id.set('')
        room_type.set('')
        patient_id.set('')
        room_cost.set('')
        

        
    def exit():
        confirm = messagebox.askyesno('confirmation',' ARE YOU SURE YOU WANT TO EXIT')
        if confirm>0:
            win.destroy()
            return
                    
        

    Label(win,text='PSHL HOSPITAL',font='impack 31 bold',bg='black',fg='white').pack(fill=X)

    frame1 = Frame(win,bd=15,relief=RIDGE)
    frame1.place(x=0,y=55,width=1535,height=450)

    lf1 = LabelFrame(frame1,text='ROOM',font='ariel 28 bold',bd=10,bg='pink')
    lf1.place(x=8,y=0,width=1500,height=425)

    Label(lf1,text='room_id',font='ariel 15',bg='pink').place(x=5,y=50)
    Label(lf1,text='room_type',font='ariel 15',bg='pink').place(x=5,y=100)
    Label(lf1,text='patient_id',font='ariel 15',bg='pink').place(x=5,y=150)
    Label(lf1,text='room_cost',font='ariel 15',bg='pink').place(x=5,y=200)


    room_id = IntVar()
    room_type = StringVar()
    patient_id = IntVar()
    room_cost= IntVar()


    e1 = Entry(lf1, bd=4)
    e1.place(x=200, y=50, width=200)
    e1.config(textvariable=room_id)

    e2 = Entry(lf1, bd=4)
    e2.place(x=200, y=100, width=200)
    e2.config(textvariable=room_type)

    e3 = Entry(lf1, bd=4)
    e3.place(x=200, y=150, width=200)
    e3.config(textvariable=patient_id)

    e4 = Entry(lf1, bd=4)
    e4.place(x=200, y=200, width=200)
    e4.config(textvariable=room_cost)


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

    table = ttk.Treeview(frame2, columns=('r_id','r_t','p_id','r_c'),xscrollcommand=scroll_y.set,yscrollcommand=scroll_x.set )
    scroll_x=ttk.Scrollbar(command=table.xview)
    scroll_y=ttk.Scrollbar(command=table.yview)

    table.heading('r_id',text='room_id')
    table.heading('r_t',text='room_type')
    table.heading('p_id',text='patient_id')
    table.heading('r_c',text='room_cost')


    table['show'] = 'headings'
    table.pack(fill = BOTH,expand=1)

    fetch_data()

    mainloop()

def display1():
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

    def save():
        if e1.get() == "" or e3.get() == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            # Create the engine for database connection
            db_uri = f"postgresql+psycopg2://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
            engine = create_engine(db_uri)

            try:
                with engine.connect() as conn:
                    conn.execute(
                        text("INSERT INTO emergency_contact (contact_id, contact_name, phone, relation, patient_id) VALUES (:c_id, :c_n, :ph, :rel, :p_id)"),
                        {
                            'c_id': contact_id.get(),
                            'c_n': contact_name.get(),
                            'ph': phone.get(),
                            'rel': relation.get(),
                            'p_id': patient_id.get(),
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
                result = conn.execute(text('SELECT * FROM emergency_contact'))
                rows = result.fetchall()

                # Clear existing data in the table widget
                table.delete(*table.get_children())

                # Insert fetched data into the table widget
                for item in rows:
                    table.insert('', END, values=item)
        except Exception as err:
            messagebox.showerror('Error', f'Failed to fetch data: {err}')
            print(f'Failed to fetch data -- {err}')

    def get_data(event=''):
        cursor_row = table.focus()
        data = table.item(cursor_row)
        row = data['values']
        contact_id.set(row[0])
        contact_name.set(row[1])
        phone.set(row[2]) 
        relation.set(row[3])
        patient_id.set(row[4])
        
        
        
            




    def clear():
        contact_id.set('')
        contact_name.set('')
        phone.set('')
        relation.set('')
        patient_id.set('')

        

        
    def exit():
        confirm = messagebox.askyesno('confirmation',' ARE YOU SURE YOU WANT TO EXIT')
        if confirm>0:
            win.destroy()
            return
                    
        

    Label(win,text='PSHL HOSPITAL',font='impack 31 bold',bg='black',fg='white').pack(fill=X)

    frame1 = Frame(win,bd=15,relief=RIDGE)
    frame1.place(x=0,y=55,width=1535,height=450)

    lf1 = LabelFrame(frame1,text='EMERGENCY_CONTACT',font='ariel 28 bold',bd=10,bg='pink')
    lf1.place(x=8,y=0,width=1500,height=425)

    Label(lf1,text='contact_id',font='ariel 15',bg='pink').place(x=5,y=50)
    Label(lf1,text='contact_name',font='ariel 15',bg='pink').place(x=5,y=100)
    Label(lf1,text='phone',font='ariel 15',bg='pink').place(x=5,y=150)
    Label(lf1,text='relation',font='ariel 15',bg='pink').place(x=5,y=200)
    Label(lf1,text='patient_id',font='ariel 15',bg='pink').place(x=5,y=250)


    contact_id = IntVar()
    contact_name = StringVar()
    phone = IntVar()
    relation= StringVar()
    patient_id=IntVar()


    e1 = Entry(lf1, bd=4)
    e1.place(x=200, y=50, width=200)
    e1.config(textvariable=contact_id)

    e2 = Entry(lf1, bd=4)
    e2.place(x=200, y=100, width=200)
    e2.config(textvariable=contact_name)

    e3 = Entry(lf1, bd=4)
    e3.place(x=200, y=150, width=200)
    e3.config(textvariable=phone)

    e4 = Entry(lf1, bd=4)
    e4.place(x=200, y=200, width=200)
    e4.config(textvariable=relation)

    e5 = Entry(lf1, bd=4)
    e5.place(x=200, y=250, width=200)
    e5.config(textvariable=patient_id)



    frame2 = Frame(win,bd=15,relief=RIDGE)
    frame2.place(x=0,y=500,width=1535,height=240)

    ss_btn = Button(win,text='Save ',font='ariel 15 bold',bg='green',fg='white',bd=6,cursor='hand2',command=save)
    ss_btn.place(x=330,y=741,width=290)

    c_btn = Button(win,text='Clear',font='ariel 15 bold',bg='blue',fg='white',bd=6,cursor='hand2',command=clear)
    c_btn.place(x=650,y=741,width=270)

    e_btn = Button(win,text='Exit',font='ariel 15 bold',bg='red',fg='white',bd=6,cursor='hand2',command=exit)
    e_btn.place(x=963,y=741,width=270)

    scroll_x = ttk.Scrollbar(frame2,orient=HORIZONTAL)
    scroll_x.pack(side='bottom',fill='x')

    scroll_y = ttk.Scrollbar(frame2,orient=VERTICAL)
    scroll_y.pack(side='right',fill='y')

    table = ttk.Treeview(frame2, columns=('c_id','c_n','ph','rel','p_id'),xscrollcommand=scroll_y.set,yscrollcommand=scroll_x.set )
    scroll_x=ttk.Scrollbar(command=table.xview)
    scroll_y=ttk.Scrollbar(command=table.yview)

    table.heading('c_id',text='contact_id')
    table.heading('c_n',text='contact_name')
    table.heading('ph',text='phone')
    table.heading('rel',text='relation')
    table.heading('p_id',text='patient_id')


    table['show'] = 'headings'
    table.pack(fill = BOTH,expand=1)


    fetch_data()
    mainloop()
        

def display2():
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

    def save():
        if e1.get() == "" or e6.get() == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            try:
                with engine.connect() as conn:
                    conn.execute(
                        text("INSERT INTO staff (emp_id, emp_fname, emp_lname, emp_type, address, dept_id) VALUES (:e_id, :e_fn, :e_ln, :e_t, :add, :d_id)"),
                        {
                            'e_id': emp_id.get(),
                            'e_fn': emp_fname.get(),
                            'e_ln': emp_lname.get(),
                            'e_t': emp_type.get(),
                            'add': address.get(),
                            'd_id': dept_id.get(),
                        }
                    )
                    conn.commit()
                fetch_data()  # Update the displayed data after insertion
                messagebox.showinfo("SUCCESS", "Record has been inserted")
            except Exception as err:
                print(f'Failed to insert record -- {err}')



    def fetch_data():
        try:
            # Create the engine for database connection
            db_uri = f"postgresql+psycopg2://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
            engine = create_engine(db_uri)

            with engine.connect() as conn:
                result = conn.execute(text('SELECT * FROM staff'))
                rows = result.fetchall()

                # Clear existing data in the table widget
                table.delete(*table.get_children())

                # Insert fetched data into the table widget
                for item in rows:
                    table.insert('', END, values=item)
        except Exception as err:
            messagebox.showerror('Error', f'Failed to fetch data: {err}')
            print(f'Failed to fetch data -- {err}')

    def get_data(event=''):
        cursor_row = table.focus()
        data = table.item(cursor_row)
        row = data['values']
        emp_id.set(row[0])
        emp_fname.set(row[1])
        emp_lname.set(row[2]) 
        emp_type.set(row[3])
        address.set(row[4])
        dept_id.set(row[5])
        
            



    def clear():
        emp_id.set('')
        emp_fname.set('')
        emp_lname.set('')
        emp_type.set('')
        address.set('')
        dept_id.set('')
        
        

        
    def exit():
        confirm = messagebox.askyesno('confirmation',' ARE YOU SURE YOU WANT TO EXIT')
        if confirm>0:
            win.destroy()
            return
                    
        

    Label(win,text='PSHL HOSPITAL',font='impack 31 bold',bg='black',fg='white').pack(fill=X)

    frame1 = Frame(win,bd=15,relief=RIDGE)
    frame1.place(x=0,y=55,width=1535,height=450)

    lf1 = LabelFrame(frame1,text='STAFF',font='ariel 28 bold',bd=10,bg='pink')
    lf1.place(x=8,y=0,width=1500,height=425)

    Label(lf1,text='emp_id',font='ariel 15',bg='pink').place(x=5,y=50)
    Label(lf1,text='emp_fname',font='ariel 15',bg='pink').place(x=5,y=100)
    Label(lf1,text='emp_lname',font='ariel 15',bg='pink').place(x=5,y=150)
    Label(lf1,text='emp_type',font='ariel 15',bg='pink').place(x=5,y=200)
    Label(lf1,text='address',font='ariel 15',bg='pink').place(x=5,y=250)
    Label(lf1,text='dept_id',font='ariel 15',bg='pink').place(x=5,y=300)


    emp_id = IntVar()
    emp_fname = StringVar()
    emp_lname = StringVar()
    emp_type= StringVar()
    address =StringVar()
    dept_id=IntVar()

    e1 = Entry(lf1, bd=4)
    e1.place(x=200, y=50, width=200)
    e1.config(textvariable=emp_id)

    e2 = Entry(lf1, bd=4)
    e2.place(x=200, y=100, width=200)
    e2.config(textvariable=emp_fname)

    e3 = Entry(lf1, bd=4)
    e3.place(x=200, y=150, width=200)
    e3.config(textvariable=emp_lname)

    e4 = Entry(lf1, bd=4)
    e4.place(x=200, y=200, width=200)
    e4.config(textvariable=emp_type)

    e5 = Entry(lf1, bd=4)
    e5.place(x=200, y=250, width=200)
    e5.config(textvariable=address)

    e6 = Entry(lf1, bd=4)
    e6.place(x=200, y=300, width=200)
    e6.config(textvariable=dept_id)


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

    table = ttk.Treeview(frame2, columns=('e_id','e_fn','e_ln','e_t','add','d_id'),xscrollcommand=scroll_y.set,yscrollcommand=scroll_x.set )
    scroll_x=ttk.Scrollbar(command=table.xview)
    scroll_y=ttk.Scrollbar(command=table.yview)

    table.heading('e_id',text='emp_id')
    table.heading('e_fn',text='emp_fname')
    table.heading('e_ln',text='emp_lname')
    table.heading('e_t',text='emp_type')
    table.heading('add',text='address')
    table.heading('d_id',text='dept_id')

    table['show'] = 'headings'
    table.pack(fill = BOTH,expand=1)


    fetch_data()
    mainloop()
                    
        

    Label(win,text='PSHL HOSPITAL',font='impack 31 bold',bg='black',fg='white').pack(fill=X)

    frame1 = Frame(win,bd=15,relief=RIDGE)
    frame1.place(x=0,y=55,width=1535,height=450)

    lf1 = LabelFrame(frame1,text='EMERGENCY_CONTACT',font='ariel 28 bold',bd=10,bg='pink')
    lf1.place(x=8,y=0,width=1500,height=425)

    Label(lf1,text='contact_id',font='ariel 15',bg='pink').place(x=5,y=50)
    Label(lf1,text='contact_name',font='ariel 15',bg='pink').place(x=5,y=100)
    Label(lf1,text='phone',font='ariel 15',bg='pink').place(x=5,y=150)
    Label(lf1,text='relation',font='ariel 15',bg='pink').place(x=5,y=200)
    Label(lf1,text='patient_id',font='ariel 15',bg='pink').place(x=5,y=250)


    contact_id = IntVar()
    contact_name = StringVar()
    phone = IntVar()
    relation= StringVar()
    patient_id=IntVar()


    e1 = Entry(lf1, bd=4)
    e1.place(x=200, y=50, width=200)
    e1.config(textvariable=contact_id)

    e2 = Entry(lf1, bd=4)
    e2.place(x=200, y=100, width=200)
    e2.config(textvariable=contact_name)

    e3 = Entry(lf1, bd=4)
    e3.place(x=200, y=150, width=200)
    e3.config(textvariable=phone)

    e4 = Entry(lf1, bd=4)
    e4.place(x=200, y=200, width=200)
    e4.config(textvariable=relation)

    e5 = Entry(lf1, bd=4)
    e5.place(x=200, y=250, width=200)
    e5.config(textvariable=patient_id)



    frame2 = Frame(win,bd=15,relief=RIDGE)
    frame2.place(x=0,y=500,width=1535,height=240)

    ss_btn = Button(win,text='Save ',font='ariel 15 bold',bg='green',fg='white',bd=6,cursor='hand2',command=save)
    ss_btn.place(x=330,y=741,width=290)

    c_btn = Button(win,text='Clear',font='ariel 15 bold',bg='blue',fg='white',bd=6,cursor='hand2',command=clear)
    c_btn.place(x=650,y=741,width=270)

    e_btn = Button(win,text='Exit',font='ariel 15 bold',bg='red',fg='white',bd=6,cursor='hand2',command=exit)
    e_btn.place(x=963,y=741,width=270)

    scroll_x = ttk.Scrollbar(frame2,orient=HORIZONTAL)
    scroll_x.pack(side='bottom',fill='x')

    scroll_y = ttk.Scrollbar(frame2,orient=VERTICAL)
    scroll_y.pack(side='right',fill='y')

    table = ttk.Treeview(frame2, columns=('c_id','c_n','ph','rel','p_id'),xscrollcommand=scroll_y.set,yscrollcommand=scroll_x.set )
    scroll_x=ttk.Scrollbar(command=table.xview)
    scroll_y=ttk.Scrollbar(command=table.yview)

    table.heading('c_id',text='contact_id')
    table.heading('c_n',text='contact_name')
    table.heading('ph',text='phone')
    table.heading('rel',text='relation')
    table.heading('p_id',text='patient_id')


    table['show'] = 'headings'
    table.pack(fill = BOTH,expand=1)


    fetch_data()
    mainloop()

def display3():
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
                        text("INSERT INTO nurse(nurse_id, patient_id, emp_id, dept_id) VALUES (:n_id, :p_id, :e_id, :d_id)"),
                        {
                            'n_id': nurse_id.get(),
                            'p_id': patient_id.get(),
                            'e_id': emp_id.get(),
                            'd_id': dept_id.get(),
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
                result = conn.execute(text('SELECT * FROM nurse'))
                rows = result.fetchall()

                # Clear existing data in the table widget
                table.delete(*table.get_children())

                # Insert fetched data into the table widget
                for item in rows:
                    table.insert('', END, values=item)
        except Exception as err:
            messagebox.showerror('Error', f'Failed to fetch data: {err}')
            print(f'Failed to fetch data -- {err}')



    def get_data(event=''):
        cursor_row = table.focus()
        data = table.item(cursor_row)
        row = data['values']
        nurse_id.set(row[0])
        patient_id.set(row[1])
        emp_id.set(row[2]) 
        dept_id.set(row[3])
    
            



    def clear():
        nurse_id.set('')
        patient_id.set('')
        emp_id.set('')
        dept_id.set('')

        

        
    def exit():
        confirm = messagebox.askyesno('confirmation',' ARE YOU SURE YOU WANT TO EXIT')
        if confirm>0:
            win.destroy()
            return
                    
        

    Label(win,text='PSHL HOSPITAL',font='impack 31 bold',bg='black',fg='white').pack(fill=X)

    frame1 = Frame(win,bd=15,relief=RIDGE)
    frame1.place(x=0,y=55,width=1535,height=450)

    lf1 = LabelFrame(frame1,text='NURSE',font='ariel 28 bold',bd=10,bg='pink')
    lf1.place(x=8,y=0,width=1500,height=425)

    Label(lf1,text='nurse_id',font='ariel 15',bg='pink').place(x=5,y=50)
    Label(lf1,text='patient_id',font='ariel 15',bg='pink').place(x=5,y=100)
    Label(lf1,text='emp_id',font='ariel 15',bg='pink').place(x=5,y=150)
    Label(lf1,text='dept_id',font='ariel 15',bg='pink').place(x=5,y=200)


    nurse_id = IntVar()
    patient_id = IntVar()
    emp_id = IntVar()
    dept_id= IntVar()


    e1 = Entry(lf1, bd=4)
    e1.place(x=200, y=50, width=200)
    e1.config(textvariable=nurse_id)

    e2 = Entry(lf1, bd=4)
    e2.place(x=200, y=100, width=200)
    e2.config(textvariable=patient_id)

    e3 = Entry(lf1, bd=4)
    e3.place(x=200, y=150, width=200)
    e3.config(textvariable=emp_id)

    e4 = Entry(lf1, bd=4)
    e4.place(x=200, y=200, width=200)
    e4.config(textvariable=dept_id)



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

    table = ttk.Treeview(frame2, columns=('n_id','p_id','e_id','d_id'),xscrollcommand=scroll_y.set,yscrollcommand=scroll_x.set )
    scroll_x=ttk.Scrollbar(command=table.xview)
    scroll_y=ttk.Scrollbar(command=table.yview)

    table.heading('n_id',text='nurse_id')
    table.heading('p_id',text='patient_id')
    table.heading('e_id',text='emp_id')
    table.heading('d_id',text='dept_id')


    table['show'] = 'headings'
    table.pack(fill = BOTH,expand=1)

    fetch_data()

    mainloop()

def display4():
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


    def save():
        if e1.get() == "" or e5.get() == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            try:
                with engine.connect() as conn:
                    conn.execute(
                        text("INSERT INTO Doctor (doctor_ID, qualifications, emp_id, specialization, dept_id) VALUES (:doc_id, :qua, :e_id, :spl, :d_id)"),
                        {
                            'doc_id': doctor_id.get(),
                            'qua': qualification.get(),
                            'e_id': emp_id.get(),
                            'spl': specialization.get(),
                            'd_id': dept_id.get()
                        }
                    )
                    conn.commit()
                fetch_data()  # Update the displayed data after insertion
                messagebox.showinfo("SUCCESS", "Record has been inserted")
            except Exception as err:
                print(f'Failed to insert record -- {err}')



    def fetch_data():
        try:
            # Create the engine for database connection
            db_uri = f"postgresql+psycopg2://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
            engine = create_engine(db_uri)

            with engine.connect() as conn:
                result = conn.execute(text('SELECT * FROM Doctor'))
                rows = result.fetchall()

                # Clear existing data in the table widget
                table.delete(*table.get_children())

                # Insert fetched data into the table widget
                for item in rows:
                    item = list(item)  # Convert tuple to list for modification
                    item[3] = ' '.join(item[3:4])
                    table.insert('', END, values=item)
        except Exception as err:
            messagebox.showerror('Error', f'Failed to fetch data: {err}')
            print(f'Failed to fetch data -- {err}')

    
    def get_data(event=''):
        cursor_row = table.focus()
        data = table.item(cursor_row)
        row = data['values']
        doctor_id.set(row[0])
        qualification.set(row[1])
        emp_id.set(row[2]) 
        specialization.set(row[3])
        dept_id.set(row[4])
        
        
        
    def clear():
        doctor_id.set('')
        qualification.set('')
        emp_id.set('')
        specialization.set('')
        dept_id.set('')

        

        
    def exit():
        confirm = messagebox.askyesno('confirmation',' ARE YOU SURE YOU WANT TO EXIT')
        if confirm>0:
            win.destroy()
            return
                    
        

    Label(win,text='PSHL HOSPITAL',font='impack 31 bold',bg='black',fg='white').pack(fill=X)

    frame1 = Frame(win,bd=15,relief=RIDGE)
    frame1.place(x=0,y=55,width=1535,height=450)

    lf1 = LabelFrame(frame1,text='DOCTOR',font='ariel 28 bold',bd=10,bg='pink')
    lf1.place(x=8,y=0,width=1500,height=425)

    Label(lf1,text='doctor_id',font='ariel 15',bg='pink').place(x=5,y=50)
    Label(lf1,text='qualification',font='ariel 15',bg='pink').place(x=5,y=100)
    Label(lf1,text='emp_id',font='ariel 15',bg='pink').place(x=5,y=150)
    Label(lf1,text='specialization',font='ariel 15',bg='pink').place(x=5,y=200)
    Label(lf1,text='dept_id',font='ariel 15',bg='pink').place(x=5,y=250)


    doctor_id = IntVar()
    qualification = StringVar()
    emp_id = IntVar()
    specialization= StringVar()
    dept_id=IntVar()


    e1 = Entry(lf1, bd=4)
    e1.place(x=200, y=50, width=200)
    e1.config(textvariable=doctor_id)

    e2 = Entry(lf1, bd=4)
    e2.place(x=200, y=100, width=200)
    e2.config(textvariable=qualification)

    e3 = Entry(lf1, bd=4)
    e3.place(x=200, y=150, width=200)
    e3.config(textvariable=emp_id)

    e4 = Entry(lf1, bd=4)
    e4.place(x=200, y=200, width=200)
    e4.config(textvariable=specialization)

    e5 = Entry(lf1, bd=4)
    e5.place(x=200, y=250, width=200)
    e5.config(textvariable=dept_id)



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

    table = ttk.Treeview(frame2, columns=('doc_id','qua','e_id','spl','d_id'),xscrollcommand=scroll_y.set,yscrollcommand=scroll_x.set )
    scroll_x=ttk.Scrollbar(command=table.xview)
    scroll_y=ttk.Scrollbar(command=table.yview)

    table.heading('doc_id',text='doctor_id')
    table.heading('qua',text='qualification')
    table.heading('e_id',text='emp_id')
    table.heading('spl',text='specialization')
    table.heading('d_id',text='dept_id')


    table['show'] = 'headings'
    table.pack(fill = BOTH,expand=1)

    fetch_data()

    mainloop()   

def display5():
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
                        text("INSERT INTO DEPARTMENT (dept_id, dept_head, dept_name, emp_count) VALUES (:d_id, :d_h, :d_n, :e_c)"),
                        {
                            'd_id': dept_id.get(),
                            'd_h': dept_head.get(),
                            'd_n': dept_name.get(),
                            'e_c': emp_count.get(),
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
                result = conn.execute(text('SELECT * FROM department'))
                rows = result.fetchall()

                # Clear existing data in the table widget
                table.delete(*table.get_children())

                # Insert fetched data into the table widget
                for item in rows:
                    item = list(item)  # Convert tuple to list for modification
                    item[1] = ' '.join(item[1:2])
                    table.insert('', END, values=item)
        except Exception as err:
            messagebox.showerror('Error', f'Failed to fetch data: {err}')
            print(f'Failed to fetch data -- {err}')
    


    def get_data(event=''):
        cursor_row = table.focus()
        data = table.item(cursor_row)
        row = data['values']
        dept_id.set(row[0])
        dept_head.set(row[1])
        dept_name.set(row[2]) 
        emp_count.set(row[3])      




    def clear():
        dept_id.set('')
        dept_head.set('')
        dept_name.set('')
        emp_count.set('')

        

        
    def exit():
        confirm = messagebox.askyesno('confirmation',' ARE YOU SURE YOU WANT TO EXIT')
        if confirm>0:
            win.destroy()
            return
                    
        

    Label(win,text='PSHL HOSPITAL',font='impack 31 bold',bg='black',fg='white').pack(fill=X)

    frame1 = Frame(win,bd=15,relief=RIDGE)
    frame1.place(x=0,y=55,width=1535,height=450)

    lf1 = LabelFrame(frame1,text='DEPARTMENTS',font='ariel 28 bold',bd=10,bg='pink')
    lf1.place(x=8,y=0,width=1500,height=425)

    Label(lf1,text='dept_id',font='ariel 15',bg='pink').place(x=5,y=50)
    Label(lf1,text='dept_head',font='ariel 15',bg='pink').place(x=5,y=100)
    Label(lf1,text='dept_name',font='ariel 15',bg='pink').place(x=5,y=150)
    Label(lf1,text='emp_count',font='ariel 15',bg='pink').place(x=5,y=200)


    dept_id = IntVar()
    dept_head = StringVar()
    dept_name = StringVar()
    emp_count= IntVar()


    e1 = Entry(lf1, bd=4)
    e1.place(x=200, y=50, width=200)
    e1.config(textvariable=dept_id)

    e2 = Entry(lf1, bd=4)
    e2.place(x=200, y=100, width=200)
    e2.config(textvariable=dept_head)

    e3 = Entry(lf1, bd=4)
    e3.place(x=200, y=150, width=200)
    e3.config(textvariable=dept_name)

    e4 = Entry(lf1, bd=4)
    e4.place(x=200, y=200, width=200)
    e4.config(textvariable=emp_count)



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

    table = ttk.Treeview(frame2, columns=('d_id','d_h','d_n','e_c'),xscrollcommand=scroll_y.set,yscrollcommand=scroll_x.set )
    scroll_x=ttk.Scrollbar(command=table.xview)
    scroll_y=ttk.Scrollbar(command=table.yview)

    table.heading('d_id',text='dept_id')
    table.heading('d_h',text='dept_head')
    table.heading('d_n',text='dept_name')
    table.heading('e_c',text='emp_count')


    table['show'] = 'headings'
    table.pack(fill = BOTH,expand=1)


    fetch_data()
    mainloop()

def display6():
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


    def save():
        if e1.get() == "":
            messagebox.showerror("Error", "Doctor ID is required")
        else:
            try:
                # Fetch and display patient details for the entered doctor ID
                doc_id = int(doctor_id.get())  # Ensure doctor_id is converted to an integer
                fetch_data(doc_id)  # Pass the doctor ID to fetch_data function
                messagebox.showinfo("SUCCESS", "Patient details fetched successfully")
            except ValueError:
                messagebox.showerror("Error", "Invalid Doctor ID")
            except Exception as err:
                messagebox.showerror("Error", f"Failed to fetch patient details: {err}")


    def save():
        if e1.get() == "":
            messagebox.showerror("Error", "Doctor ID is required")
        else:
            try:
                # Fetch and display patient details for the entered doctor ID
                fetch_data(doctor_id.get())  # Pass the doctor ID to fetch_data function
                messagebox.showinfo("SUCCESS", "Patient details fetched successfully")
            except Exception as err:
                messagebox.showerror("Error", f"Failed to fetch patient details: {err}")

    def fetch_data(doc_id):
        try:
            # Create the engine for database connection
            db_uri = f"postgresql+psycopg2://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
            engine = create_engine(db_uri)

            with engine.connect() as conn:
                # Create a text construct with a bind parameter for doc_id
                stmt = text('SELECT * FROM view_doctor_patient_details(:doc_id)')
                
                # Bind the value of doc_id to the bind parameter
                stmt = stmt.bindparams(doc_id=doc_id)
                
                # Execute the statement
                result = conn.execute(stmt)
                rows = result.fetchall()

                # Clear existing data in the table widget
                table.delete(*table.get_children())

                # Insert fetched data into the table widget
                for item in rows:
                    table.insert('', END, values=item)
        except Exception as err:
            messagebox.showerror('Error', f'Failed to fetch data: {err}')





    def get_data(event=''):
        cursor_row = table.focus()
        data = table.item(cursor_row)
        row = data['values']
        doctor_id.set(row[0])
        
    
            



    def clear():
        doctor_id.set('')
        

        

        
    def exit():
        confirm = messagebox.askyesno('confirmation',' ARE YOU SURE YOU WANT TO EXIT')
        if confirm>0:
            win.destroy()
            return
                    
        

    Label(win,text='PSHL HOSPITAL',font='impack 31 bold',bg='black',fg='white').pack(fill=X)

    frame1 = Frame(win,bd=15,relief=RIDGE)
    frame1.place(x=0,y=55,width=1535,height=650)

    lf1 = LabelFrame(frame1,text='FUNCTION',font='ariel 28 bold',bd=10,bg='pink')
    lf1.place(x=8,y=0,width=1500,height=600)

    Label(lf1,text='doctor_id',font='ariel 15',bg='pink').place(x=5,y=50)


    doctor_id = IntVar()


    e1 = Entry(lf1, bd=4)
    e1.place(x=200, y=50, width=200)
    e1.config(textvariable=doctor_id)





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

    table = ttk.Treeview(frame2, columns=('doc_id','d_fn','d_ln','qua','p_id','p_fn','p_ln','ph','add','age','b_t','gen','adm_d','dis_d','pre_id','m_n','dose','pre_d','b_id','b_d','t_c'),xscrollcommand=scroll_y.set,yscrollcommand=scroll_x.set )
    scroll_x=ttk.Scrollbar(command=table.xview)
    scroll_y=ttk.Scrollbar(command=table.yview)

    table.heading('doc_id',text='doctor_id')
    table.heading('d_fn',text='dcotor_fname')
    table.heading('d_ln',text='dcotor_lname')
    table.heading('qua',text='qualifications')
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
    table.heading('pre_id',text='prescription_id')
    table.heading('m_n',text='medicine_name')
    table.heading('dose',text='dosage')
    table.heading('pre_d',text='prescription_date')
    table.heading('b_id',text='bill_id')
    table.heading('b_d',text='bill_date')
    table.heading('t_c',text='total_cost')

    table['show'] = 'headings'
    table.pack(fill = BOTH,expand=1)

    fetch_data()

    mainloop()


def display7():
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
        admission_date.set('')
        discharge_date.set('')

        

        
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
    patient_admission_date=DateEntry(lf1)

    patient_discharge_date=StringVar()




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
    e9.config(textvariable=patient_admission_date)

    e10 = Entry(lf1, bd=4)
    e10.place(x=700, y=150, width=200)
    e10.config(textvariable=patient_discharge_date)
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
                            'adm_d': patient_admission_date.get(),  # Assuming admission_date is associated with an entry widget for date input
                            'dis_d': patient_discharge_date.get(),  # Assuming discharge_date is associated with an entry widget for date input
                        }
                    )

                    conn.commit()  # Commit the transaction
                    fetch_data()  # Update the displayed data after insertion
                    messagebox.showinfo("SUCCESS", "Record has been inserted")
            except Exception as err:
                messagebox.showerror("Error", f"Failed to insert record: {err}")



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

    
def display8():
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

    def save():
        if e1.get() == "" or e5.get() == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            # Create the engine for database connection
            db_uri = f"postgresql+psycopg2://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
            engine = create_engine(db_uri)

            try:
                with engine.connect() as conn:
                    conn.execute(
                        text("INSERT INTO appointment (Appointment_ID, Scheduled_on, date, time, doctor_id, patient_id) VALUES (:a_id, :s_o, :date, :time, :doc_id, :p_id)"),
                        a_id=appt_id.get(),
                        s_o=scheduled_on.get(),
                        datest=date.get(),
                        date = datetime.strptime(datest,'%Y-%m-%d'),
                        time=time.get(),
                        doc_id=doctor_id.get(),
                        p_id=patient_id.get(),
                        
                    )
                    conn.commit()
                fetch_data()  # Update the displayed data after insertion
                messagebox.showinfo("SUCCESS", "Record has been inserted")
            except Exception as err:
                print(f'Failed to insert record -- {err}')




    def fetch_data():
        try:
            # Create the engine for database connection
            db_uri = f"postgresql+psycopg2://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
            engine = create_engine(db_uri)

            with engine.connect() as conn:
                result = conn.execute(text('SELECT * FROM appointment'))
                rows = result.fetchall()

                # Clear existing data in the table widget
                table.delete(*table.get_children())

                # Insert fetched data into the table widget
                for item in rows:
                    # Convert the scheduled_on column from datetime to string with format
                    item = list(item)  # Convert tuple to list for modification
                    item[1] = item[1].strftime('%Y-%m-%d %H:%M:%S')  # Format scheduled_on
                    table.insert('', END, values=item)
        except Exception as err:
            messagebox.showerror('Error', f'Failed to fetch data: {err}')
            print(f'Failed to fetch data -- {err}')



    def get_data(event=''):
        cursor_row = table.focus()
        data = table.item(cursor_row)
        row = data['values']
        appt_id.set(row[0])
        scheduled_on.set(row[1])
        date.set(row[2]) 
        time.set(row[3])
        doctor_id.set(row[4])
        patient_id.set(row[5])
            


    def delete():
        try:
            # Create the engine for database connection
            db_uri = f"postgresql+psycopg2://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
            engine = create_engine(db_uri)

            with engine.connect() as conn:
                # Assuming 'Reference' is the column name to match against for deletion
                conn.execute(text("DELETE FROM patient WHERE Reference = :ref_id"), ref_id=ref.get())
            
            fetch_data()  # Update the displayed data after deletion
            messagebox.showinfo('Deleted', 'Patient data has been deleted')
        except Exception as err:
            print(f'Failed to delete record -- {err}')

    def clear():
        appt_id.set('')
        scheduled_on.set('')
        date.set('')
        time.set('')
        doctor_id.set('')
        patient_id.set('')
        

        
    def exit():
        confirm = messagebox.askyesno('confirmation',' ARE YOU SURE YOU WANT TO EXIT')
        if confirm>0:
            win.destroy()
            return
                    
        

    Label(win,text='PSHL HOSPITAL',font='impack 31 bold',bg='black',fg='white').pack(fill=X)

    frame1 = Frame(win,bd=15,relief=RIDGE)
    frame1.place(x=0,y=55,width=1535,height=450)

    lf1 = LabelFrame(frame1,text='APPOINTMENTS',font='ariel 28 bold',bd=10,bg='pink')
    lf1.place(x=8,y=0,width=1500,height=425)

    Label(lf1,text='appt_id',font='ariel 15',bg='pink').place(x=5,y=50)
    Label(lf1,text='scheduled_on',font='ariel 15',bg='pink').place(x=5,y=100)
    Label(lf1,text='date',font='ariel 15',bg='pink').place(x=5,y=150)
    Label(lf1,text='time',font='ariel 15',bg='pink').place(x=5,y=200)
    Label(lf1,text='doctor_id',font='ariel 15',bg='pink').place(x=5,y=250)
    Label(lf1,text='patient_id',font='ariel 15',bg='pink').place(x=5,y=300)

    appt_id = IntVar()
    scheduled_on = IntVar()
    date = IntVar()
    time= IntVar()
    doctor_id = IntVar()
    patient_id = IntVar()
    #Address =StringVar()

    e1 = Entry(lf1, bd=4)
    e1.place(x=200, y=50, width=200)
    e1.config(textvariable=appt_id)

    e2 = Entry(lf1, bd=4)
    e2.place(x=200, y=100, width=200)
    e2.config(textvariable=scheduled_on)

    e3 = Entry(lf1, bd=4)
    e3.place(x=200, y=150, width=200)
    e3.config(textvariable=date)

    e4 = Entry(lf1, bd=4)
    e4.place(x=200, y=200, width=200)
    e4.config(textvariable=time)

    e5 = Entry(lf1, bd=4)
    e5.place(x=200, y=250, width=200)
    e5.config(textvariable=doctor_id)

    e6 = Entry(lf1, bd=4)
    e6.place(x=200, y=300, width=200)
    e6.config(textvariable=patient_id)



    frame2 = Frame(win,bd=15,relief=RIDGE)
    frame2.place(x=0,y=500,width=1535,height=240)

    del_btn = Button(win,text='Delete',font='ariel 15 bold',bg='brown',fg='white',bd=6,cursor='hand2',command=delete)
    del_btn.place(x=4,y=741,width=270)

    s_btn = Button(win,text='Save ',font='ariel 15 bold',bg='green',fg='white',bd=6,cursor='hand2',command=save)
    s_btn.place(x=630,y=741,width=290)

    c_btn = Button(win,text='Clear',font='ariel 15 bold',bg='blue',fg='white',bd=6,cursor='hand2',command=clear)
    c_btn.place(x=950,y=741,width=270)

    e_btn = Button(win,text='Exit',font='ariel 15 bold',bg='red',fg='white',bd=6,cursor='hand2',command=exit)
    e_btn.place(x=1263,y=741,width=270)

    scroll_x = ttk.Scrollbar(frame2,orient=HORIZONTAL)
    scroll_x.pack(side='bottom',fill='x')

    scroll_y = ttk.Scrollbar(frame2,orient=VERTICAL)
    scroll_y.pack(side='right',fill='y')

    table = ttk.Treeview(frame2, columns=('a_id','s_o','date','time','d_id','p_id'),xscrollcommand=scroll_y.set,yscrollcommand=scroll_x.set )
    scroll_x=ttk.Scrollbar(command=table.xview)
    scroll_y=ttk.Scrollbar(command=table.yview)

    table.heading('a_id',text='appt_id')
    table.heading('s_o',text='scheduled_on')
    table.heading('date',text='date')
    table.heading('time',text='time')
    table.heading('d_id',text='doctor_id')
    table.heading('p_id',text='patient_id')



    table['show'] = 'headings'
    table.pack(fill = BOTH,expand=1)


    fetch_data()
    mainloop()

def display9():
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
                        text("INSERT INTO medicine (medicine_id, m_name, m_quantity, m_cost) VALUES (:m_id, :m_n, :m_q, :m_c)"),
                        {
                            'm_id': medicine_id.get(),
                            'm_n': m_name.get(),
                            'm_q': m_quantity.get(),
                            'm_c': m_cost.get(),
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
                result = conn.execute(text('SELECT * FROM medicine'))
                rows = result.fetchall()

                # Clear existing data in the table widget
                table.delete(*table.get_children())

                # Insert fetched data into the table widget
                for item in rows:
                    table.insert('', END, values=item)
        except Exception as err:
            messagebox.showerror('Error', f'Failed to fetch data: {err}')
            print(f'Failed to fetch data -- {err}')

    def get_data(event=''):
        cursor_row = table.focus()
        data = table.item(cursor_row)
        row = data['values']
        medicine_id.set(row[0])
        m_name.set(row[1])
        m_quantity.set(row[2]) 
        m_cost.set(row[3])
        
        
        
        


    def clear():
        medicine_id.set('')
        m_name.set('')
        m_quantity.set('')
        m_cost.set('')

        

        
    def exit():
        confirm = messagebox.askyesno('confirmation',' ARE YOU SURE YOU WANT TO EXIT')
        if confirm>0:
            win.destroy()
            return
                    
        

    Label(win,text='PSHL HOSPITAL',font='impack 31 bold',bg='black',fg='white').pack(fill=X)

    frame1 = Frame(win,bd=15,relief=RIDGE)
    frame1.place(x=0,y=55,width=1535,height=450)

    lf1 = LabelFrame(frame1,text='MEDICINE',font='ariel 28 bold',bd=10,bg='pink')
    lf1.place(x=8,y=0,width=1500,height=425)

    Label(lf1,text='medicine_id',font='ariel 15',bg='pink').place(x=5,y=50)
    Label(lf1,text='m_name',font='ariel 15',bg='pink').place(x=5,y=100)
    Label(lf1,text='m_quantity',font='ariel 15',bg='pink').place(x=5,y=150)
    Label(lf1,text='m_cost',font='ariel 15',bg='pink').place(x=5,y=200)



    medicine_id = IntVar()
    m_name = StringVar()
    m_quantity = IntVar()
    m_cost= IntVar()


    e1 = Entry(lf1, bd=4)
    e1.place(x=200, y=50, width=200)
    e1.config(textvariable=medicine_id)

    e2 = Entry(lf1, bd=4)
    e2.place(x=200, y=100, width=200)
    e2.config(textvariable=m_name)

    e3 = Entry(lf1, bd=4)
    e3.place(x=200, y=150, width=200)
    e3.config(textvariable=m_quantity)

    e4 = Entry(lf1, bd=4)
    e4.place(x=200, y=200, width=200)
    e4.config(textvariable=m_cost)



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

    table = ttk.Treeview(frame2, columns=('m_id','m_n','m_q','m_c'),xscrollcommand=scroll_y.set,yscrollcommand=scroll_x.set )
    scroll_x=ttk.Scrollbar(command=table.xview)
    scroll_y=ttk.Scrollbar(command=table.yview)

    table.heading('m_id',text='medicine_id')
    table.heading('m_n',text='m_name')
    table.heading('m_q',text='m_quantity')
    table.heading('m_c',text='m_cost')


    table['show'] = 'headings'
    table.pack(fill = BOTH,expand=1)

    fetch_data()

    mainloop()

def display10():
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

    def save():
        if e1.get() == "" or e5.get() == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            # Create the engine for database connection
            db_uri = f"postgresql+psycopg2://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
            engine = create_engine(db_uri)

            try:
                with engine.connect() as conn:
                    conn.execute(
                        text("INSERT INTO bill (bill_id, date, room_cost, test_cost, m_cost,total,patient_id,policy_number) VALUES (:b_id, :d, :r_c, :t_c, :m_c, :tot, :p_id, :p_n)"),
                        b_id=bill_id.get(),
                        d=date.get(),
                        r_c=room_cost.get(),
                        t_c=test_cost.get(),
                        m_c=m_cost.get(),
                        tot=total.get(),
                        p_id=patient_id.get(),
                        p_n=policy_number.get(),
                        
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
                result = conn.execute(text('SELECT * FROM bill'))
                rows = result.fetchall()

                # Clear existing data in the table widget
                table.delete(*table.get_children())

                # Insert fetched data into the table widget
                for item in rows:
                    table.insert('', END, values=item)
        except Exception as err:
            messagebox.showerror('Error', f'Failed to fetch data: {err}')
            print(f'Failed to fetch data -- {err}')


    def get_data(event=''):
        cursor_row = table.focus()
        data = table.item(cursor_row)
        row = data['values']
        bill_id.set(row[0])
        date.set(row[1])
        room_cost.set(row[2]) 
        test_cost.set(row[3]) 
        m_cost.set(row[4]) 
        total.set(row[5])
        patient_id.set(row[6])
        policy_number.set(row[7])

        
        
        
            


    def clear():
        bill_id.set('')
        date.set('')
        room_cost.set('')
        test_cost.set('')
        m_cost.set()
        total.set()
        patient_id.set()
        policy_number.set()

        

        
    def exit():
        confirm = messagebox.askyesno('confirmation',' ARE YOU SURE YOU WANT TO EXIT')
        if confirm>0:
            win.destroy()
            return
                    
        

    Label(win,text='PSHL HOSPITAL',font='impack 31 bold',bg='black',fg='white').pack(fill=X)

    frame1 = Frame(win,bd=15,relief=RIDGE)
    frame1.place(x=0,y=55,width=1535,height=450)

    lf1 = LabelFrame(frame1,text='BILL',font='ariel 28 bold',bd=10,bg='pink')
    lf1.place(x=8,y=0,width=1500,height=425)

    Label(lf1,text='bill_id',font='ariel 15',bg='pink').place(x=5,y=50)
    Label(lf1,text='date',font='ariel 15',bg='pink').place(x=5,y=100)
    Label(lf1,text='room_cost',font='ariel 15',bg='pink').place(x=5,y=150)
    Label(lf1,text='test_cost',font='ariel 15',bg='pink').place(x=5,y=200)
    Label(lf1,text='m_cost',font='ariel 15',bg='pink').place(x=5,y=250)
    Label(lf1,text='total',font='ariel 15',bg='pink').place(x=5,y=300)
    Label(lf1,text='patient_id',font='ariel 15',bg='pink').place(x=5,y=350)
    Label(lf1,text='policy_number',font='ariel 15',bg='pink').place(x=5,y=400)



    bill_id = IntVar()
    date = IntVar()
    room_cost = IntVar()
    test_cost= IntVar()
    m_cost=IntVar()
    total=IntVar()
    patient_id=IntVar()
    policy_number=StringVar()


    e1 = Entry(lf1, bd=4)
    e1.place(x=200, y=50, width=200)
    e1.config(textvariable=bill_id)

    e2 = Entry(lf1, bd=4)
    e2.place(x=200, y=100, width=200)
    e2.config(textvariable=date)

    e3 = Entry(lf1, bd=4)
    e3.place(x=200, y=150, width=200)
    e3.config(textvariable=room_cost)

    e4 = Entry(lf1, bd=4)
    e4.place(x=200, y=200, width=200)
    e4.config(textvariable=test_cost)

    e5 = Entry(lf1, bd=4)
    e5.place(x=200, y=250, width=200)
    e5.config(textvariable=m_cost)

    e6 = Entry(lf1, bd=4)
    e6.place(x=200, y=300, width=200)
    e6.config(textvariable=total)

    e7 = Entry(lf1, bd=4)
    e7.place(x=200, y=350, width=200)
    e7.config(textvariable=patient_id)

    e8 = Entry(lf1, bd=4)
    e8.place(x=200, y=400, width=200)
    e8.config(textvariable=policy_number)


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

    table = ttk.Treeview(frame2, columns=('b_id','d','r_c','t_c','m_c','t','p_id','p_n'),xscrollcommand=scroll_y.set,yscrollcommand=scroll_x.set )
    scroll_x=ttk.Scrollbar(command=table.xview)
    scroll_y=ttk.Scrollbar(command=table.yview)

    table.heading('b_id',text='bill_id')
    table.heading('d',text='date')
    table.heading('r_c',text='room_cost')
    table.heading('t_c',text='test_cost')
    table.heading('m_c',text='m_cost')
    table.heading('t',text='total')
    table.heading('p_id',text='patient_id')
    table.heading('p_n',text='policy_number')



    table['show'] = 'headings'
    table.pack(fill = BOTH,expand=1)

    fetch_data()

    mainloop()

def display11():
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

    def save():
        if e1.get()=="" or e3.get()=="":
            messagebox.showerror("Error","all fields are required")
        else:
            # Create the engine for database connection
            db_uri = f"postgresql+psycopg2://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
            engine = create_engine(db_uri)

            try:
                with engine.connect() as conn:
                    conn.execute(
                        text("INSERT INTO prescription (prescripyion_id, patient_id, medicine_id, date, dosage, doctor_id) VALUES (:pre_id, :p_id, :m_id, :d, :dose, :d_id)"),
                        pre_id=prescription_id.get(),
                        p_id=patient_id.get(),
                        m_id=medicine_id.get(),
                        d=date.get(),
                        dose=dosage.get(),
                        d_id=doctor_id.get(),
                        
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
                result = conn.execute(text('SELECT * FROM prescription'))
                rows = result.fetchall()

                # Clear existing data in the table widget
                table.delete(*table.get_children())

                # Insert fetched data into the table widget
                for item in rows:
                    table.insert('', END, values=item)
        except Exception as err:
            messagebox.showerror('Error', f'Failed to fetch data: {err}')
            print(f'Failed to fetch data -- {err}')

    def get_data(event=''):
        cursor_row = table.focus()
        data = table.item(cursor_row)
        row = data['values']
        prescription_id.set(row[0])
        patient_id.set(row[1])
        medicine_id.set(row[2]) 
        date.set(row[3])
        dosage.set(row[4])
        doctor_id.set(row[5])     
        
    

    def clear():
        prescription_id.set('')
        patient_id.set('')
        medicine_id.set('')
        date.set('')
        dosage.set('')
        doctor_id.set('')

        

        
    def exit():
        confirm = messagebox.askyesno('confirmation',' ARE YOU SURE YOU WANT TO EXIT')
        if confirm>0:
            win.destroy()
            return
                    
        

    Label(win,text='PSHL HOSPITAL',font='impack 31 bold',bg='black',fg='white').pack(fill=X)

    frame1 = Frame(win,bd=15,relief=RIDGE)
    frame1.place(x=0,y=55,width=1535,height=450)

    lf1 = LabelFrame(frame1,text='PRESCRIPITION',font='ariel 28 bold',bd=10,bg='pink')
    lf1.place(x=8,y=0,width=1500,height=425)

    Label(lf1,text='prescripition_id',font='ariel 15',bg='pink').place(x=5,y=50)
    Label(lf1,text='patient_id',font='ariel 15',bg='pink').place(x=5,y=100)
    Label(lf1,text='medicine_id',font='ariel 15',bg='pink').place(x=5,y=150)
    Label(lf1,text='date',font='ariel 15',bg='pink').place(x=5,y=200)
    Label(lf1,text='dosage',font='ariel 15',bg='pink').place(x=5,y=250)
    Label(lf1,text='doctor_id',font='ariel 15',bg='pink').place(x=5,y=300)



    prescription_id = IntVar()
    patient_id = IntVar()
    medicine_id = IntVar()
    date= IntVar()
    dosage=IntVar()
    doctor_id=IntVar()


    e1 = Entry(lf1, bd=4)
    e1.place(x=200, y=50, width=200)
    e1.config(textvariable=prescription_id)

    e2 = Entry(lf1, bd=4)
    e2.place(x=200, y=100, width=200)
    e2.config(textvariable=patient_id)

    e3 = Entry(lf1, bd=4)
    e3.place(x=200, y=150, width=200)
    e3.config(textvariable=medicine_id)

    e4 = Entry(lf1, bd=4)
    e4.place(x=200, y=200, width=200)
    e4.config(textvariable=date)

    e5 = Entry(lf1, bd=4)
    e5.place(x=200, y=250, width=200)
    e5.config(textvariable=dosage)

    e6 = Entry(lf1, bd=4)
    e6.place(x=200, y=300, width=200)
    e6.config(textvariable=doctor_id)


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

    table = ttk.Treeview(frame2, columns=('pre_id','p_id','m_id','d','dose','d_id'),xscrollcommand=scroll_y.set,yscrollcommand=scroll_x.set )
    scroll_x=ttk.Scrollbar(command=table.xview)
    scroll_y=ttk.Scrollbar(command=table.yview)

    table.heading('pre_id',text='prescription_id')
    table.heading('p_id',text='patient_id')
    table.heading('m_id',text='medicine_id')
    table.heading('d',text='date')
    table.heading('dose',text='dosage')
    table.heading('d_id',text='doctor_id')


    table['show'] = 'headings'
    table.pack(fill = BOTH,expand=1)


    fetch_data()
    mainloop()


def display12():
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

    def save():
        if e1.get()=="" or e3.get()=="":
            messagebox.showerror("Error","all fields are required")
        else:
            # Create the engine for database connection
            db_uri = f"postgresql+psycopg2://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
            engine = create_engine(db_uri)

            try:
                with engine.connect() as conn:
                    conn.execute(
                        text("INSERT INTO insurance (policy_number, patient_id, ins_code, end_date, provider) VALUES (:p_n, :p_id, :i_c, :e_d, :pro)"),
                        p_n=policy_number.get(),
                        p_id=patient_id.get(),
                        i_c=ins_code.get(),
                        e_d=end_date.get(),
                        pro=provider.get(),
                        
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
                result = conn.execute(text('SELECT * FROM insurance'))
                rows = result.fetchall()

                # Clear existing data in the table widget
                table.delete(*table.get_children())

                # Insert fetched data into the table widget
                for item in rows:
                    table.insert('', END, values=item)
        except Exception as err:
            messagebox.showerror('Error', f'Failed to fetch data: {err}')
            print(f'Failed to fetch data -- {err}')

    def get_data(event=''):
        cursor_row = table.focus()
        data = table.item(cursor_row)
        row = data['values']
        policy_number.set(row[0])
        patient_id.set(row[1])
        ins_code.set(row[2]) 
        end_date.set(row[3])
        provider.set(row[4])
        
        
    
            




    def clear():
        policy_number.set('')
        patient_id.set('')
        ins_code.set('')
        end_date.set('')
        provider.set('')

        

        
    def exit():
        confirm = messagebox.askyesno('confirmation',' ARE YOU SURE YOU WANT TO EXIT')
        if confirm>0:
            win.destroy()
            return
                    
        

    Label(win,text='PSHL HOSPITAL',font='impack 31 bold',bg='black',fg='white').pack(fill=X)

    frame1 = Frame(win,bd=15,relief=RIDGE)
    frame1.place(x=0,y=55,width=1535,height=450)

    lf1 = LabelFrame(frame1,text='INSURANCE',font='ariel 28 bold',bd=10,bg='pink')
    lf1.place(x=8,y=0,width=1500,height=425)

    Label(lf1,text='policy_number',font='ariel 15',bg='pink').place(x=5,y=50)
    Label(lf1,text='patient_id',font='ariel 15',bg='pink').place(x=5,y=100)
    Label(lf1,text='ins_code',font='ariel 15',bg='pink').place(x=5,y=150)
    Label(lf1,text='end_date',font='ariel 15',bg='pink').place(x=5,y=200)
    Label(lf1,text='provider',font='ariel 15',bg='pink').place(x=5,y=250)


    policy_number = StringVar()
    patient_id = IntVar()
    ins_code = StringVar()
    end_date= IntVar()
    provider=StringVar()


    e1 = Entry(lf1, bd=4)
    e1.place(x=200, y=50, width=200)
    e1.config(textvariable=policy_number)

    e2 = Entry(lf1, bd=4)
    e2.place(x=200, y=100, width=200)
    e2.config(textvariable=patient_id)

    e3 = Entry(lf1, bd=4)
    e3.place(x=200, y=150, width=200)
    e3.config(textvariable=ins_code)

    e4 = Entry(lf1, bd=4)
    e4.place(x=200, y=200, width=200)
    e4.config(textvariable=end_date)

    e5 = Entry(lf1, bd=4)
    e5.place(x=200, y=250, width=200)
    e5.config(textvariable=provider)



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

    table = ttk.Treeview(frame2, columns=('p_n','p_id','i_c','e_d','pro'),xscrollcommand=scroll_y.set,yscrollcommand=scroll_x.set )
    scroll_x=ttk.Scrollbar(command=table.xview)
    scroll_y=ttk.Scrollbar(command=table.yview)

    table.heading('p_n',text='policy_number')
    table.heading('p_id',text='patient_id')
    table.heading('i_c',text='ins_code')
    table.heading('e_d',text='end_date')
    table.heading('pro',text='provider')


    table['show'] = 'headings'
    table.pack(fill = BOTH,expand=1)


    fetch_data()
    mainloop()
   
def display13():
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


    def save():
        if e1.get() == "":
            messagebox.showerror("Error", "Patient ID is required")
        else:
            try:
                
                p_id = patient_id.get()
                ph=phone.get()  
                fetch_data(p_id,ph)  
                messagebox.showinfo("SUCCESS", "Patient details fetched successfully")
            except Exception as err:
                messagebox.showerror("Error", f"Failed to fetch patient details: {err}")

    def fetch_data(p_id,ph):
        try:
            
            stmnt = 'SELECT * UpdatePatientInfoFunction(:p_id)'
            
            # Create the engine for database connection
            db_uri = f"postgresql+psycopg2://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
            engine = create_engine(db_uri)

            with engine.connect() as conn:
                result = conn.execute(text(stmnt), p_id=p_id, ph=ph)
                rows = result.fetchall()

                # Clear existing data in the table widget
                table.delete(*table.get_children())

                # Insert fetched data into the table widget
                for item in rows:
                    table.insert('', END, values=item)
        except Exception as err:
            messagebox.showerror('Error', f'Failed to fetch data: {err}')


    def get_data(event=''):
        cursor_row = table.focus()
        data = table.item(cursor_row)
        row = data['values']
        patient_id.set(row[0])
        phone.set(row[1])
        
    
            



    def clear():
        patient_id.set('')
        phone.set(''),
        

        

        
    def exit():
        confirm = messagebox.askyesno('confirmation',' ARE YOU SURE YOU WANT TO EXIT')
        if confirm>0:
            win.destroy()
            return
                    
        

    Label(win,text='PSHL HOSPITAL',font='impack 31 bold',bg='black',fg='white').pack(fill=X)

    frame1 = Frame(win,bd=15,relief=RIDGE)
    frame1.place(x=0,y=55,width=1535,height=650)

    lf1 = LabelFrame(frame1,text='UpdatePatientInfoFunction',font='ariel 28 bold',bd=10,bg='pink')
    lf1.place(x=8,y=0,width=1500,height=600)

    Label(lf1,text='patient_id',font='ariel 15',bg='pink').place(x=5,y=50)
    Label(lf1,text='phone',font='ariel 15',bg='pink').place(x=5,y=100)


    patient_id = IntVar()
    phone=IntVar()


    e1 = Entry(lf1, bd=4)
    e1.place(x=200, y=50, width=200)
    e1.config(textvariable=patient_id)

    e2 = Entry(lf1, bd=4)
    e2.place(x=200, y=100, width=200)
    e2.config(textvariable=phone)





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

    table = ttk.Treeview(frame2, columns=('p_id','p_fn','p_ln','ph','add'),xscrollcommand=scroll_y.set,yscrollcommand=scroll_x.set )
    scroll_x=ttk.Scrollbar(command=table.xview)
    scroll_y=ttk.Scrollbar(command=table.yview)


    table.heading('p_id',text='patient_id')
    table.heading('p_fn',text='patient_fname')
    table.heading('p_ln',text='patient_lname')
    table.heading('ph',text='phone')
    table.heading('add',text='address')


    table['show'] = 'headings'
    table.pack(fill = BOTH,expand=1)

    fetch_data(p_id,ph)

    mainloop()
    



def display15():
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


    def save():
        if e1.get() == "":
            messagebox.showerror("Error", " Patient ID  is required")
        else:
            try:
                
                p_id = patient_id.get()
                doc_id = doctor_id.get() 
                fetch_data(p_id,doc_id)  
                messagebox.showinfo("SUCCESS", "Patient details fetched successfully")
            except Exception as err:
                messagebox.showerror("Error", f"Failed to fetch patient details: {err}")

    def fetch_data(p_id,doc_id):
        try:
            
            stmnt = 'SELECT * FROM scheduleappointment(:p_id,doc_id)'
            
            # Create the engine for database connection
            db_uri = f"postgresql+psycopg2://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
            engine = create_engine(db_uri)

            with engine.connect() as conn:
                result = conn.execute(text(stmnt), p_id = p_id,doc_id=doc_id)
                rows = result.fetchall()

                # Clear existing data in the table widget
                table.delete(*table.get_children())

                # Insert fetched data into the table widget
                for item in rows:
                    table.insert('', END, values=item)
        except Exception as err:
            messagebox.showerror('Error', f'Failed to fetch data: {err}')


    def get_data(event=''):
        cursor_row = table.focus()
        data = table.item(cursor_row)
        row = data['values']
        patient_id.set(row[0])
        doctor_id.set(row[1])
        
    
            



    def clear():
        patient_id.set('')
        doctor_id.set('')
        

        

        
    def exit():
        confirm = messagebox.askyesno('confirmation',' ARE YOU SURE YOU WANT TO EXIT')
        if confirm>0:
            win.destroy()
            return
                    
        

    Label(win,text='PSHL HOSPITAL',font='impack 31 bold',bg='black',fg='white').pack(fill=X)

    frame1 = Frame(win,bd=15,relief=RIDGE)
    frame1.place(x=0,y=55,width=1535,height=650)

    lf1 = LabelFrame(frame1,text='ScheduleAppointment',font='ariel 28 bold',bd=10,bg='pink')
    lf1.place(x=8,y=0,width=1500,height=600)

    Label(lf1,text='patient_id',font='ariel 15',bg='pink').place(x=5,y=50)
    Label(lf1,text='doctor_id',font='ariel 15',bg='pink').place(x=5,y=100)


    patient_id = IntVar()
    doctor_id = IntVar()


    e1 = Entry(lf1, bd=4)
    e1.place(x=200, y=50, width=200)
    e1.config(textvariable=patient_id)

    e2 = Entry(lf1, bd=4)
    e2.place(x=200, y=100, width=200)
    e2.config(textvariable=doctor_id)





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

    table = ttk.Treeview(frame2, columns=('sch_app'),xscrollcommand=scroll_y.set,yscrollcommand=scroll_x.set )
    scroll_x=ttk.Scrollbar(command=table.xview)
    scroll_y=ttk.Scrollbar(command=table.yview)

    table.heading('sch_app',text='Scheduleappointment')


    table['show'] = 'headings'
    table.pack(fill = BOTH,expand=1)

    #fetch_data(p_id,doc_id)

    mainloop()

def display16():
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

    def fetch_data():
        try:
            # Adjust SQL query to filter patient details by the provided doctor ID
            stmnt = 'SELECT * FROM GetTotalPatientsByBloodType()'
            
            # Create the engine for database connection
            db_uri = f"postgresql+psycopg2://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
            engine = create_engine(db_uri)

            with engine.connect() as conn:
                result = conn.execute(text(stmnt))
                rows = result.fetchall()

                # Clear existing data in the table widget
                table.delete(*table.get_children())

                # Insert fetched data into the table widget
                for item in rows:
                    table.insert('', END, values=item)
        except Exception as err:
            messagebox.showerror('Error', f'Failed to fetch data: {err}')

    
    def exit():
        confirm = messagebox.askyesno('confirmation',' ARE YOU SURE YOU WANT TO EXIT')
        if confirm>0:
            win.destroy()
            return
                    
        

    Label(win,text='PSHL HOSPITAL',font='impack 31 bold',bg='black',fg='white').pack(fill=X)

    frame1 = Frame(win,bd=15,relief=RIDGE)
    frame1.place(x=0,y=55,width=1335,height=650)

    lf1 = LabelFrame(frame1,text='No. of Patients having same blood type',font='ariel 20 bold',bd=10,bg='pink')
    lf1.place(x=8,y=0,width=1300,height=600)

    #Label(lf1,text='doctor_id',font='ariel 15',bg='pink').place(x=5,y=50)

    frame2 = Frame(win,bd=15,relief=RIDGE)
    frame2.place(x=0,y=200,width=1335,height=540)

    #s_btn = Button(win,text='Save ',font='ariel 15 bold',bg='green',fg='white',bd=6,cursor='hand2',command=save)
    #s_btn.place(x=330,y=641,width=290)

    #c_btn = Button(win,text='Clear',font='ariel 15 bold',bg='blue',fg='white',bd=6,cursor='hand2',command=clear)
    #c_btn.place(x=650,y=641,width=270)

    e_btn = Button(win,text='Exit',font='ariel 15 bold',bg='red',fg='white',bd=6,cursor='hand2',command=exit)
    e_btn.place(x=510,y=741,width=270)

    scroll_x = ttk.Scrollbar(frame2,orient=HORIZONTAL)
    scroll_x.pack(side='bottom',fill='x')

    scroll_y = ttk.Scrollbar(frame2,orient=VERTICAL)
    scroll_y.pack(side='right',fill='y')

    table = ttk.Treeview(frame2, columns=('bloodtype','totalpatients'),xscrollcommand=scroll_y.set,yscrollcommand=scroll_x.set )
    scroll_x=ttk.Scrollbar(command=table.xview)
    scroll_y=ttk.Scrollbar(command=table.yview)

    table.heading('bloodtype',text='bloodtype')
    table.heading('totalpatients',text='totalpatients')

    table['show'] = 'headings'
    table.pack(fill = BOTH,expand=1)

    fetch_data()

    mainloop()

def display17():
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

    def fetch_data():
        try:
            # Adjust SQL query to filter patient details by the provided doctor ID
            stmnt = 'SELECT * FROM GetPatientAgeGroupCount()'
            
            # Create the engine for database connection
            db_uri = f"postgresql+psycopg2://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
            engine = create_engine(db_uri)

            with engine.connect() as conn:
                result = conn.execute(text(stmnt))
                rows = result.fetchall()

                # Clear existing data in the table widget
                table.delete(*table.get_children())

                # Insert fetched data into the table widget
                for item in rows:
                    table.insert('', END, values=item)
        except Exception as err:
            messagebox.showerror('Error', f'Failed to fetch data: {err}')

    
    def exit():
        confirm = messagebox.askyesno('confirmation',' ARE YOU SURE YOU WANT TO EXIT')
        if confirm>0:
            win.destroy()
            return
                    
        

    Label(win,text='PSHL HOSPITAL',font='impack 31 bold',bg='black',fg='white').pack(fill=X)

    frame1 = Frame(win,bd=15,relief=RIDGE)
    frame1.place(x=0,y=55,width=1235,height=650)

    lf1 = LabelFrame(frame1,text='No. of Patients corresponding to each age group',font='ariel 20 bold',bd=10,bg='pink')
    lf1.place(x=8,y=0,width=1200,height=600)

    #Label(lf1,text='doctor_id',font='ariel 15',bg='pink').place(x=5,y=50)

    frame2 = Frame(win,bd=15,relief=RIDGE)
    frame2.place(x=0,y=200,width=1235,height=540)

    #s_btn = Button(win,text='Save ',font='ariel 15 bold',bg='green',fg='white',bd=6,cursor='hand2',command=save)
    #s_btn.place(x=330,y=641,width=290)

    #c_btn = Button(win,text='Clear',font='ariel 15 bold',bg='blue',fg='white',bd=6,cursor='hand2',command=clear)
    #c_btn.place(x=650,y=641,width=270)

    e_btn = Button(win,text='Exit',font='ariel 15 bold',bg='red',fg='white',bd=6,cursor='hand2',command=exit)
    e_btn.place(x=450,y=741,width=270)

    scroll_x = ttk.Scrollbar(frame2,orient=HORIZONTAL)
    scroll_x.pack(side='bottom',fill='x')

    scroll_y = ttk.Scrollbar(frame2,orient=VERTICAL)
    scroll_y.pack(side='right',fill='y')

    table = ttk.Treeview(frame2, columns=('agegroup','count'),xscrollcommand=scroll_y.set,yscrollcommand=scroll_x.set )
    scroll_x=ttk.Scrollbar(command=table.xview)
    scroll_y=ttk.Scrollbar(command=table.yview)

    table.heading('agegroup',text='agegroup')
    table.heading('count',text='count')

    table['show'] = 'headings'
    table.pack(fill = BOTH,expand=1)

    fetch_data()

    mainloop()


def signin():
    username = user.get()
    password = passw.get()

    if username == 'admin' and password == '1234':
        # Destroy the login screen
        root.destroy()

        # Create new screen
        screen = Tk()
        screen.title("PSHL HOSPITAL")
        screen.geometry('925x500+300+200')
        screen.config(bg='white')

        # Create buttons
        Button(screen, text='PATIENT', width=15, height=3, bg='sky blue', command=display7).grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        Button(screen, text=' DEPARTMENT', width=15, height=3, bg='green', command=display5).grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        Button(screen, text='STAFF', width=15, height=3, bg='red', command=display2).grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        Button(screen, text='DOCTOR', width=15, height=3, bg='orange', command=display4).grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        Button(screen, text='NURSE', width=15, height=3, bg='purple', command=display3).grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        Button(screen, text='EMERGENCY CONTACT', width=15, height=3, bg='yellow', command=display1).grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        Button(screen, text='INSURANCE', width=15, height=3, bg='brown', command=display12).grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        Button(screen, text='MEDICINE', width=15, height=3, bg='pink', command=display9).grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

        Button(screen, text='PRESCRIPTION', width=15, height=3, bg='cyan', command=display11).grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        Button(screen, text='APPOINTMENT', width=15, height=3, bg='magenta', command=display8).grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        Button(screen, text='ROOM', width=15, height=3, bg='grey', command=display).grid(row=2, column=2, padx=10, pady=10, sticky="nsew")
        Button(screen, text='BILL', width=15, height=3, bg='lightgreen', command=display10).grid(row=2, column=3, padx=10, pady=10, sticky="nsew")

        Button(screen, text='FUNCTION', width=15, height=3, bg='blue', command=display6).grid(row=4, column=1,  padx=10, pady=10, sticky="nsew")  # New Button

        Button(screen, text='UPDATING PATIENT INFO', width=15, height=3, bg='lightblue',command=display13).grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
       # Button(screen, text='DOCTOR AVAILABILITY', width=15, height=3, bg='lightpink',command=display14).grid(row=4, column=1, padx=10, pady=10, sticky="nsew")
        Button(screen, text='SCHEDULE APPOINTMENT', width=15, height=3, bg='lightyellow',command=display15).grid(row=4, column=2, padx=10, pady=10, sticky="nsew")
        Button(screen, text='BLOOD COUNT', width=15, height=3, bg='lightgrey',command=display16).grid(row=4, column=3, padx=10, pady=10, sticky="nsew")
        Button(screen, text='AGE GROUP', width=15, height=3, bg='lightcoral',command=display17).grid(row=5, column=0, padx=10, pady=10, sticky="nsew")
        
        screen.grid_rowconfigure(0, weight=1)
        screen.grid_rowconfigure(1, weight=1)
        screen.grid_rowconfigure(2, weight=1)
        screen.grid_rowconfigure(3, weight=1)
        screen.grid_columnconfigure(0, weight=1)
        screen.grid_columnconfigure(1, weight=1)
        screen.grid_columnconfigure(2, weight=1)
        screen.grid_columnconfigure(3, weight=1)

        screen.mainloop()

    elif username != 'admin' and password != '1234':
        messagebox.showerror('INVALID', 'Invalid username and password')

    elif password != '1234':
        messagebox.showerror('INVALID', 'Invalid password')

    elif username != 'admin':
        messagebox.showerror('INVALID', 'Invalid username')

def toggle_password():
    if passw['show'] == "*":
        passw.config(show="")
        show_password_button.config(text="Hide Password")
    else:
        passw.config(show="*")
        show_password_button.config(text="Show Password")
       
def on_enter_password(e):
    if passw.get() == 'Password':
        passw.delete(0, 'end')
        passw.config(fg='black')
    elif passw['show'] == "":
        passw.delete(0, 'end')
        passw.insert(0, '*' * len(passw.get()))
        passw.config(fg='black')

def on_leave_password(e):
    if passw.get() == '':
        passw.insert(0, 'Password')
        passw.config(fg='grey')
    elif passw['show'] == "":
        passw.delete(0, 'end')
        passw.insert(0, '*' * len(passw.get()))
        passw.config(fg='black')

frame = Frame(root, width=400, height=350, bg="white")
frame.place(x=300, y=70)

heading = Label(frame, text='sign in', fg='#57a1f8', bg='white', font=('ariel black', 23, 'bold'))
heading.place(x=100, y=5)

def on_enter_username(e):
    user.delete(0, 'end')

def on_leave_username(e):
    if user.get() == '':
        user.insert(0, 'Username')

user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('ariel black', 11))
user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter_username)
user.bind('<FocusOut>', on_leave_username)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

passw = Entry(frame, width=18, fg='black', border=0, bg='white', font=('ariel black', 11), show="")
passw.place(x=30, y=150)
passw.insert(0, 'Password')
passw.bind('<FocusIn>', on_enter_password)
passw.bind('<FocusOut>', on_leave_password)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

show_password_button = Button(frame, text="Show Password", bg='white', fg='#57a1f8', command=toggle_password)
show_password_button.place(x=200, y=145)

Button(frame, width=30, pady=7, text='sign in', bg='#57a1f8', fg='white', border=0, command=signin).place(x=35, y=204)
# label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('ariel black', 9))
# label.place(x=65, y=270)

# sign_up = Button(frame, width=6, text='sign up', border=0, bg='white', cursor='hand2', fg='#57a1f8')
# sign_up.place(x=215, y=264)

root.mainloop()

