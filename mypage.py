import customtkinter as ctk 
import tkinter.messagebox as tkmb 
import csiagooglesheet

values = ['None']
row_num = 0
firstoptionfixed = ''
csiagooglesheet.main()
sheet, SPREADSHEET_ID = csiagooglesheet.getsheetinfo()

class MyPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		self.create_widgets()

	def create_widgets(self):
		self.type_label = ctk.CTkLabel(self, text='Type')
		self.type_label.configure(font=('Arial', 15))
		self.type_label.pack(pady=7, padx=10)

		self.type_options = ctk.CTkOptionMenu(self, values=["beverages", "desserts", "foods"])
		self.type_options.set(firstoptionfixed)
		self.type_options.pack(pady=7,padx=20)

		self.menu_label = ctk.CTkLabel(self, text='Menu')
		self.menu_label.configure(font=('Arial', 15))
		self.menu_label.pack(pady=7, padx=10)

		self.menu_options = ctk.CTkOptionMenu(self, values=values)
		self.menu_options.pack(pady=7, padx=20)
		
		#rating 창, lbael, entry
		self.rating_label = ctk.CTkLabel(self, text='rating')
		self.rating_label.configure(font=('Arial', 15))
		self.rating_label.pack(pady=7, padx=10)

		self.rating_options = ctk.CTkOptionMenu(self, values=["1", "2", "3", "4", "5"])
		self.rating_options.pack(pady=7, padx=20)
		
		#comment 창, label, entry
		self.comment_label = ctk.CTkLabel(self, text='comment')
		self.comment_label.configure(font=('Arial', 15))
		self.comment_label.pack(pady=10, padx=10)

		self.comment_entry = ctk.CTkEntry(self, placeholder_text="Enter your comment please", width=700, height=350)
		self.comment_entry.pack(pady=10, padx=5)
		
		#save button
		self.button_applytype = ctk.CTkButton(self, text='apply type', command = self.update_values, width=200, height=40)
		self.button_applytype.pack(pady=5, padx=10, anchor='ne')
		self.button_save = ctk.CTkButton(self, text='save', command = self.save_toDB, width=200, height=40)
		self.button_save.pack(pady=5, padx=10, anchor='ne')

		#메인페로 가는 버튼
		self.button_tomain = ctk.CTkButton(self, text='Main', command = self.to_mainpg, width=100, height=40)
		self.button_tomain.pack(pady=5, padx=20, anchor='nw')
	def getusername (self):
		self.username = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="menu page!G2").execute().get('values', [])[0][0]

	def update_values(self):
		global values
		global firstoptionfixed
		if self.type_options.get() == 'beverages':
			values_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="menu page!A3:A8").execute().get('values', [])
			values = [item[0] for item in values_result]
			tkmb.showinfo(title = "Info", message = "Beverages are selected")
			firstoptionfixed = 'beverages'
			self.update_comments()
		elif self.type_options.get() == 'desserts':
			values_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="menu page!A12:A17").execute().get('values', [])
			values = [item[0] for item in values_result]
			tkmb.showinfo(title = "Info", message = "Desserts are selected")
			firstoptionfixed = 'desserts'
			self.update_comments()
		elif self.type_options.get() == 'foods':
			values_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="menu page!A21:A26").execute().get('values', [])
			values = [item[0] for item in values_result]
			tkmb.showinfo(title = "Info", message = "Foods are selected")
			firstoptionfixed = 'foods'
			self.update_comments()

	def update_comments(self):
		self.destroy()
		newcomments = MyPage(self.master)
		newcomments.pack(pady=20, padx=40, fill='both', expand=True)

	def save_toDB(self):
		menuchosen = self.menu_options.get()
		rating = self.rating_options.get()
		comment = self.comment_entry.get()
		feedback = 'None'

		self.getusername()
		body = {"values": [[self.username, menuchosen, rating, comment, feedback]]}

		global row_num
		row_num = 2
		while True:
			range_value = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=("Rating&comments!D"+str(row_num))).execute()
			values = range_value.get('values', [])
			if not values:
				break
			row_num += 1
		sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=("Rating&comments!D"+str(row_num)+":H"), valueInputOption="RAW", body=body).execute()
		tkmb.showinfo(title="Save Successful", message="Your comment has been saved successfully!")
		self.comment_entry.delete(0, 'end')
		self.ask_feedback()
	
	def upadate_DB(self):
		colD = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Rating&comments!D2:D").execute().get('values', [])
		colDEFGH = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Rating&comments!D2:G").execute().get('values', [])
		if len(colD) > 0:
			body = {"values": colDEFGH}
			sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=("Rating&comments!D3:H"), valueInputOption="RAW", body=body).execute()

	def to_mainpg(self):
		self.destroy()
		from mainpage import MainPage
		main_page = MainPage(self.master)
		main_page.pack(pady=20, padx=40, fill='both', expand=True)

	def ask_feedback(self):
		if int(self.rating_options.get()) <=3:
			self.feedback = Feedback(self.master)
			self.feedback.mainloop()

class Feedback(ctk.CTkToplevel):
	def __init__(self, app):
		super().__init__(app)
		tkmb.showinfo(title="Feedback", message="Thanks for sharing your opinion! \nCan we get some feedbacks about our foods?")
		self.title("Please give us feedback!")
		self.geometry("800x600")

		self.label_feedback = ctk.CTkLabel(self, text="Please leave your feedback.")
		self.label_feedback.pack(pady=10)
		self.entry_feedback = ctk.CTkEntry(self, placeholder_text="Enter your feedback here please.", width=700, height=350)
		self.entry_feedback.pack(pady=10)

		self.button_save = ctk.CTkButton(self, text='Save', command = self.save_feedback, width=200, height=40)
		self.button_save.pack(pady=5, padx=10)
	
	def save_feedback(self):
		body = {"values": [[self.entry_feedback.get()]]}
		sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=("Rating&comments!H"+str(row_num)), valueInputOption="RAW", body=body).execute()
		tkmb.showinfo(title="Feedback", message="Your feedback has successfully sent! \nThank you for your feedback!")
		self.destroy()

			


if __name__ == "__main__":
	app = ctk.CTk()
	app.geometry("1280x850")
	app.title("please revisit us!")
	main_page = MyPage(app)
	main_page.pack(pady=20, padx=40, fill='both', expand=True)
	app.mainloop()