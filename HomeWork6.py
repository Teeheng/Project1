from tkinter import *
from tkinter import ttk, messagebox
import csv
from datetime import datetime

GUI = Tk()
GUI.title('Program calculation expense vr.2.0.1')
GUI.geometry('1000x800')



menubar = Menu(GUI)
GUI.config(menu=menubar)

filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Export CSV')

def About():
	messagebox.showinfo('About','test test')

helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About', command=About)

Tab = ttk.Notebook(GUI)
T1 = Frame(Tab, width=400)
T2 = Frame(Tab, width=400)
Tab.pack(fill = BOTH, expand=True)

icon_t1 = PhotoImage(file='EP3\expense.png').subsample(2)
icon_t2 = PhotoImage(file='EP3\list.png').subsample(2)
Tab.add(T1, text = f'{"add expense":^{20}}', image=icon_t1, compound='top') #กำหนดขนาดTabและalign
Tab.add(T2, text = f'{"All":^{20}}', image=icon_t2, compound='top')

Form1 = Frame(T1)
Form1.pack()

days = {'Mon' : 'จันทร์',
	'Tue' : 'อังคาร',
	'Wed' : 'พุธ',
	'Thu' : 'พฤหัส',
	'Fri' : 'ศุกร์',
	'Sat' : 'เสาร์',
	'Sun' : 'อาทิตย์',
	}

Font1 = ('BrowalliaUPC',20)

main_icon = PhotoImage(file='EP3\MainPhoto.png')
Mainicon = Label(Form1, image=main_icon)
Mainicon.pack()

L1 = ttk.Label(Form1, text='ชื่อสินค้า', font=Font1)
L1.pack()

v_name = StringVar()
E1 = ttk.Entry(Form1, textvariable=v_name, font=Font1)
E1.pack()

L2 = ttk.Label(Form1, text='จำนวน', font=Font1)
L2.pack()

v_quantity = StringVar()
E2 = ttk.Entry(Form1, textvariable=v_quantity, font=Font1)
E2.pack()

L3 = ttk.Label(Form1, text='ราคา(บาท)', font=Font1)
L3.pack()

v_price = StringVar()
E3 = ttk.Entry(Form1, textvariable=v_price, font=Font1)
E3.pack()




def Save(event=None):
	name = v_name.get()
	quantity = v_quantity.get()
	price = v_price.get()

	if name == '' or price == '' or quantity == '':
		print('No Data')
		messagebox.showwarning('Error','Input not complete')
		return
	elif price =='':
		messagebox.showwarning('Error','Input not complete')
		return
	elif quantity == '':
		messagebox.showwarning('Error','Input not complete')
		return

	today = datetime.now().strftime('%a')
	print(today)
	stamp = datetime.now()
	dt = stamp.strftime('%Y-%m-%d %H:%M:%S')
	transactionid = stamp.strftime('%Y%m%d%H%M%f')
	dt = days[today] + '-' + dt
	print(type(v_price))
	
	try:
		total = float(price)*int(quantity)
		print('สินค้าชื่อ {} จำนวน {} ชิ้น ราคาต่อชิ้น {} บาท รวมเป็นเงิน {} บาท เมื่อเวลา {}'.format(name, quantity, price, total, dt))
		text = 'รายการ:{} ราคา:{}\n'.format(name,price)
		text = text + 'จำนวน: {} รวมทั้งหมด: {} บาท'.format(quantity,total)
		v_result.set(text)
		v_name.set('')
		v_price.set('')
		v_quantity.set('')

		with open('homework.csv', 'a', encoding='utf-8', newline='') as f:
			fw = csv.writer(f)
			data = [transactionid, name, price, quantity, total, dt]
			fw.writerow(data)
		E1.focus()
		update_table()
	except Exception as e:
		print('Error', e)
		
		#messagebox.showwarning('Error','Input again')
		messagebox.showerror('Error','Input again')
		#messagebox.showinfo('Error','Input again')
		v_name.set('')
		v_price.set('')
		v_quantity.set('')		
	
GUI.bind('<Return>', Save)

icon_b1 = PhotoImage(file='EP3\save.png')
B = ttk.Button(Form1, text='save', image=icon_b1, compound='left', command=Save)
B.pack(ipadx=50,ipady=20,pady=20)

v_result = StringVar()
v_result.set('------ผลลัพธ์-------')
result = ttk.Label(Form1, textvariable=v_result, font=Font1, foreground='green')
result.pack(pady=20)

def read_csv():
	with open('homework.csv', newline='', encoding='utf-8') as f:
		fr = csv.reader(f)
		data = list(fr)
	return data
		# for a,b,c,d,e in data:
		# 	print(b)

#rs = read_csv()
#print(rs)

L = ttk.Label(T2, text='table of result', font=Font1).pack(pady=20)
header = ['รหัส','รายการ', 'ค่าใช้จ่าย', 'จำนวน', 'รวม','วัน-เวลา']
resulttable = ttk.Treeview(T2, columns=header, show='headings',height=20)
resulttable.pack()

for h in header:
	resulttable.heading(h, text=h)

headwidth = [170,170,80,80,80,150]
for h,w in zip(header, headwidth):
	resulttable.column(h, width=w)

alltransaction = {}

def UpdateCSV():
	with open('homework.csv','w', newline='', encoding='utf-8') as f:
		fw = csv.writer(f)
		data = list(alltransaction.values())
		fw.writerows(data)
		print('Table was updated')
		

def DeleteRecord(event=None):
	check = messagebox.askyesno('confirm?','ต้องการลบ?')
	print('YES/NO:', check)

	if check == True:
		print('delete')
		select = resulttable.selection()
		print(select)
		data = resulttable.item(select)
		data = data['values']
		transactionid = data[0]
		print(transactionid)
		del alltransaction[str(transactionid)]
		print(alltransaction)
		UpdateCSV()
		update_table()
	else:
		print('cancel')

Bdelete = ttk.Button(T2, text='ลบ', command = DeleteRecord)
Bdelete.pack()

resulttable.bind('<Delete>',DeleteRecord)

def update_table():
	resulttable.delete(*resulttable.get_children())
	try:
		data = read_csv()
		#print(data)
		for i in data:
			alltransaction[i[0]] = i
			resulttable.insert('',0,value=i)
		print(alltransaction)
	except:
		print('No File')

###right click menu###
rightclick = Menu(GUI, tearoff=0) #tearoff = 0 ดึงออกมาเป็นหน้าต่างใหม่ไม่ได้
rightclick.add_command(label='Edit')
rightclick.add_command(label='Delete', command=DeleteRecord)

def menupopup(event):
	#print(event.x_root, event.y_root)
	rightclick.post(event.x_root, event.y_root)


resulttable.bind('<Button-3>', menupopup)


update_table()
print('GET CHILD', resulttable.get_children())
GUI.bind('<Tab>', lambda x: E2.focus())
GUI.mainloop()
