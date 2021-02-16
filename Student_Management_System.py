from tkinter import *
from tkinter.scrolledtext import *
from tkinter.messagebox import *
from sqlite3 import *
import requests
import bs4
import matplotlib.pyplot as plt

root = Tk()
root.title("S.M.S")
root.geometry("400x500+550+150")
root.resizable(FALSE,FALSE)

con = None
try:

    con = connect("student_info.db")
    sql = "create table if not exists student(rno int primary key, name text , marks int)"
    cursor = con.cursor()
    cursor.execute(sql)
except Exception:
    showerror("Error", "Database connection error")
else:
    if con is not None:
        con.close()


def oAdd():
	root.withdraw() 
	add_stu.deiconify() 

def cAdd():
	add_stu.withdraw()
	root.deiconify()

def View():
	root.withdraw()
	view_stu.deiconify()
	viewstu_stdata.delete(1.0, END)
	con = None
	try:
		con = connect("student_info.db")
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		print(data)
		info = ""
		for d in data:
			info = info + "rno = " + str(d[0]) + " name = " + str(d[1]) + "\n" + "marks = " + str(d[2]) + "\n"
		viewstu_stdata.insert(INSERT, info)
	except Exception as e:
		showerror("Error", str(e))
		con.rollback()
	finally:
		if con is not None:	
			con.close()

def oView():
	view_stu.withdraw()
	root.deiconify()

def Add():
	add_rno = addstu_entrno.get()
	add_name = addstu_entname.get()
	add_marks = addstu_entmarks.get()
	if not add_rno.isdigit():
		showerror("Error", "Roll no is Invalid")
	elif not (add_name.isalpha() and len(add_name) >= 2):
		showerror("Error", "Name is Invalid")
	elif not (add_marks.isdigit() and 0 <= int(add_marks) <= 100):
		showerror("Error", "Marks are not valid")
	else:
		con = None
		try:
			con = connect("student_info.db")
			cursor = con.cursor()
			sql = "insert into student values('%d', '%s', '%d')"
			rno = int(addstu_entrno.get())
			name = addstu_entname.get()
			marks = int(addstu_entmarks.get())
			cursor.execute(sql % (rno, name, marks))
			con.commit()
			showinfo("Success", "Record added sucessfully")
		except Exception as e:
			showerror("Error", str(e))
			con.rollback()
		finally:
			if con is not None:	
				con.close()

def Update():
	upt_rno= updatestu_entrno.get()
	upt_name = updatestu_entname.get()
	upt_marks = updatestu_entmarks.get()
	if not upt_rno.isdigit():
    		showerror("Error", "Roll no is invalid")
	elif not (upt_name.isalpha() and len(upt_name)>=2):
		showerror("Error", "Name is Invalid")
	elif not (upt_marks.isdigit() and 0<=int(upt_marks)<=100):
		showerror("Error", "Marks are not valid")
	else:
		pass
	con = None
	try:
		con = connect("student_info.db")
		sql = "update student set name = '%s', marks = '%d' where rno = '%d' "
		cursor = con.cursor()
		rno = int(updatestu_entrno.get())
		name = updatestu_entname.get()
		marks = int(updatestu_entmarks.get())
		cursor.execute(sql % (name,marks,rno))
		if cursor.rowcount==1:
			con.commit()
			showinfo("Info", "Record updated successfully")
		else:
			showerror("Error", "Record does not exists")
	except Exception as e:
			showerror("Error", e)
	else:
			if con is not None:
				con.close()

def oUpdate():
	root.withdraw()
	update_stu.deiconify()

def cUpdate():
	update_stu.withdraw()
	root.deiconify()

def Del():
	try:
		con = connect("student_info.db")
		sql = "delete from student where rno = '%d'"
		cursor = con.cursor()
		rno = int(delstu_entrno.get())
		cursor.execute(sql%(rno))
		if cursor.rowcount > 0:
			con.commit()
			showinfo("Info", "Record deleted successfully")
		else:
			showerror("Error", "Record does not exists")
	except Exception as e:
		showerror("Error",e)
	else:
		if con is not None:
			con.close()

def oDel():
	root.withdraw()
	del_stu.deiconify()

def cDel():
	del_stu.withdraw()
	root.deiconify()

def Chart():
	name = []
	marks = []
	con = None
	try:
		con = connect("student_info.db")
		sql = "select * from student"
		cursor = con.cursor()
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			name.append(d[1])
			marks.append(d[2])
		plt.bar(name, marks)
		plt.xlabel("Names")
		plt.ylabel("Marks")
		plt.title("Batch Information")
		plt.show()
	except Exception as e:
		showerror("Error", "Database Error")
	else:
		if con is not None:
			con.close()



#root 
root_addbtn = Button(root, text = "Add", width = 10, font = ('arial', 18,'bold'), command = oAdd)
root_viewbtn = Button(root, text = "View",width = 10, font = ('arial', 18,'bold'), command = View)
root_updatebtn = Button(root, text = "Update",width = 10, font = ('arial', 18,'bold'), command = oUpdate)
root_delbtn = Button(root, text = "Delete", width = 10, font = ('arial', 18,'bold'), command = oDel)
root_chartbtn = Button(root, text = "Chart", width = 10, font = ('arial', 18, 'bold'),command = Chart)

root_addbtn.pack(pady = 10)
root_viewbtn.pack(pady = 10)
root_updatebtn.pack(pady = 10)
root_delbtn.pack(pady = 10)
root_chartbtn.pack(pady = 10)

try:
    res = requests.get("https://ipinfo.io/")
    data = res.json()
    city_name = data['city']
    lblLoc = Label(root, text = "Location : ",font = ("arial", 15, 'bold'))
    lblLoc.place(x= 10, y = 370)
    loc = Label(root, text = city_name, font = ("arial", 15, 'bold'))
    loc.place(x = 110, y = 370)
except Exception:
    showerror("Error", "Location cannot be fetched")

try:
    temp_add = "http://api.openweathermap.org/data/2.5/weather?units=metric" + "&q=" + "Mumbai" + "&appid=c6e315d09197cec231495138183954bd"
    temp_res = requests.get(temp_add)
    data = temp_res.json()
    temp = data['main']['temp']
    temp = str(temp) + " \u00b0C"
    lblTemp = Label(root, text="Temp : ", font=("arial", 15, 'bold'))
    lblTemp.place(x=220, y=370)
    city_temp = Label(root, text=temp, font=("arial", 15, 'bold'))
    city_temp.place(x=300, y=370)
except Exception:
    showerror("Error", "Temperature cannot be fetched")

try:
    qotd_add = requests.get("https://www.brainyquote.com/quote_of_the_day")
    data = bs4.BeautifulSoup(qotd_add.text, 'html.parser')
    info = data.find('img', {"class":"p-qotd"})
    quote = info['alt']
    lbl_qotd = Label(root, text="QOTD:", font=("arial", 15, 'bold'))
    lbl_qotd.place(x = 5, y = 420)
    qotd = Label(root, text=quote, font=("arial", 14, 'bold'), wraplength = 340)
    qotd.place(x=75, y=420)
except Exception:
    showerror("Error", "QOTD cannot be fetched")


#add window

add_stu = Toplevel(root)
add_stu.title("Add Student")
add_stu.geometry("400x500+550+150")

addstu_lablrno = Label(add_stu, text = "Enter roll number", font = ('arial', 18,'bold'))
addstu_entrno = Entry(add_stu, bd = 5, font = ('arial', 18,'bold'))
addstu_lablname = Label(add_stu, text = "Enter name", font = ('arial', 18,'bold'))
addstu_entname = Entry(add_stu, bd = 5, font = ('arial', 18,'bold'))
addstu_lablmarks = Label(add_stu, text = "Enter marks", font = ('arial', 18,'bold'))
addstu_entmarks = Entry(add_stu, bd = 5, font = ('arial', 18,'bold'))
addstu_addbtn = Button(add_stu, text = "Save", width = 10, font = ('arial', 18,'bold'), command = Add)
addstu_viewbtn = Button(add_stu, text = "Back",width = 10, font = ('arial', 18,'bold'), command = cAdd)

addstu_lablrno.pack(pady = 5)
addstu_entrno.pack(pady = 5)
addstu_lablname.pack(pady = 5) 
addstu_entname.pack(pady = 5)
addstu_lablmarks.pack(pady = 5) 
addstu_entmarks.pack(pady = 5)  
addstu_addbtn.pack(pady = 5) 
addstu_viewbtn.pack(pady = 5) 

add_stu.withdraw()

view_stu = Toplevel(root)
view_stu.title("View Student")
view_stu.geometry("400x500+550+150") 

viewstu_stdata = ScrolledText(view_stu, width = 20, height = 10, font = ('arial', 18,'bold'))
viewstu_btnback = Button(view_stu, text = "Back",width = 10, font = ('arial', 18,'bold'), command = oView)

viewstu_stdata.pack(pady = 5)
viewstu_btnback.pack(pady = 5)

view_stu.withdraw()

#update 
update_stu = Toplevel(root)
update_stu.title("Update Student")
update_stu.geometry("400x500+550+150")

updatestu_lablrno = Label(update_stu, text = "Enter roll number", font = ('arial', 18,'bold'))
updatestu_entrno = Entry(update_stu, bd = 5, font = ('arial', 18,'bold'))
updatestu_lablname = Label(update_stu, text = "Enter name", font = ('arial', 18,'bold'))
updatestu_entname = Entry(update_stu, bd = 5, font = ('arial', 18,'bold'))
updatestu_lablmarks = Label(update_stu, text = "Enter marks", font = ('arial', 18,'bold'))
updatestu_entmarks = Entry(update_stu, bd = 5, font = ('arial', 18,'bold'))
updatestu_addbtn = Button(update_stu, text = "Save", width = 10, font = ('arial', 18,'bold'), command = Update)
updatestu_viewbtn = Button(update_stu, text = "Back",width = 10, font = ('arial', 18,'bold'), command = cUpdate)

updatestu_lablrno.pack(pady = 5)
updatestu_entrno.pack(pady = 5)
updatestu_lablname.pack(pady = 5) 
updatestu_entname.pack(pady = 5)
updatestu_lablmarks.pack(pady = 5) 
updatestu_entmarks.pack(pady = 5)  
updatestu_addbtn.pack(pady = 5) 
updatestu_viewbtn.pack(pady = 5) 

update_stu.withdraw()

del_stu = Toplevel(root)
del_stu.title("Update Student")
del_stu.geometry("400x300+550+150")

delstu_lablrno = Label(del_stu, text = "Enter rno:", font = ('arial', 18,'bold'))
delstu_entrno = Entry(del_stu, bd = 5, font = ('arial', 18,'bold'))
delstu_savebtn = Button(del_stu, text = "Save", width = 10, font = ('arial', 18,'bold'), command = Del)
delstu_backbtn = Button(del_stu, text = "Back",width = 10, font = ('arial', 18,'bold'), command = cDel)

delstu_lablrno.pack(pady = 5)
delstu_entrno.pack(pady = 5)
delstu_savebtn.pack(pady = 5) 
delstu_backbtn.pack(pady = 5) 

del_stu.withdraw()


root.mainloop()