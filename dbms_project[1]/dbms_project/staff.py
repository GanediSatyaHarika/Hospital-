#staff

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

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

def save():
    if e1.get() == "" or e3.get() == "":
        messagebox.showerror("Error", "All fields are required")
    else:
        # Create the engine for database connection
        db_uri = f"postgresql+psycopg2://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
        engine = create_engine(db_uri)

        try:
            with engine.connect() as conn:
                # Truncate the employee type if it exceeds the expected length
                emp_type_value = emp_type.get()[:50]  # Assuming the max length is 50 characters
                conn.execute(
                    text("INSERT INTO staff (emp_id, emp_fname, emp_lname, emp_type, address, dept_id) VALUES (:e_id, :e_fn, :e_ln, :e_t, :add, :d_id)"),
                    {
                        'e_id': emp_id.get(),
                        'e_fn': emp_fname.get(),
                        'e_ln': emp_lname.get(),
                        'e_t': emp_type_value,  # Use the truncated value
                        'add': address.get(),
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
            result = conn.execute(text('SELECT * FROM staff'))
            rows = result.fetchall()

            # Clear existing data in the table widget
            table.delete(*table.get_children())

            # Insert fetched data into the table widget
            for item in rows:
                # Ensure that the emp_type is fetched correctly (adjust the index if needed)
                item_data = list(item)
                emp_type_value = item_data[3]  # Assuming emp_type is at index 3
                item_data[3] = emp_type_value[:50]  # Truncate if needed
                table.insert('', END, values=item_data)
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