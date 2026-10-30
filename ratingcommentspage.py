import csiagooglesheet
import customtkinter as ctk 
import tkinter.messagebox as tkmb 
import tkinter as tk

csiagooglesheet.main()
sheet, SPREADSHEET_ID = csiagooglesheet.getsheetinfo()
username = []
menuname = []
rating = []
comment = []
feedback = []
firstoptionfixed = ''
average_rating = 0
values = ['None']
class RatingComments(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		self.create_widgets()

	def create_widgets(self):
		self.button_gohome = ctk.CTkButton(self, text='go to login screen', command = self.gotohome, width=200, height=40)
		self.button_gohome.pack(pady=10, padx=20, anchor='sw')

		self.button_gomanager = ctk.CTkButton(self, text='go to manager', command = self.gotomanager, width=200, height=40)
		self.button_gomanager.pack(pady=10, padx=20, anchor='sw')

		self.type_label = ctk.CTkLabel(self, text='Choose the type you want to view ratings')
		self.type_label.pack(pady=5, padx=20)
		self.type_options = ctk.CTkOptionMenu(self, values=["beverages", "desserts", "foods"])
		self.type_options.set(firstoptionfixed)
		self.type_options.pack(pady=10, padx=20)

		self.menu_label = ctk.CTkLabel(self, text='Choose menu you want to view rating & comments')
		self.menu_label.pack(pady=10, padx=10)
		self.menu_options = ctk.CTkOptionMenu(self, values = values)
		self.menu_options.pack(pady=10, padx=20)

		self.button_update = ctk.CTkButton(self, text='apply type', command = self.update_values, width=200, height=40)
		self.button_update.pack(pady=5, padx=10, anchor = 'se')

		self.button_search = ctk.CTkButton(self, text='search', command = self.search, width=200, height=40)
		self.button_search.pack(pady=5, padx=10, anchor = 'se')

		self.scroll_text = tk.Text(self, wrap=tk.NONE, width=40, height=10, font=('Calibri', 15))
		self.scroll_text.pack(pady=20, padx=10, side='left', fill='both', expand=True)
		
		self.scrollbar = tk.Scrollbar(self, command=self.scroll_text.yview)
		self.scrollbar.pack(side='right', fill='y')
		self.scroll_text.config(yscrollcommand=self.scrollbar.set)
		
		for i in range(len(username)):
			if i == 0:  # Insert average rating only once
				label_text = f"Avg Rating: {average_rating}\n\n"
				self.scroll_text.insert(tk.END, label_text)
			label_text = f"Username: {username[i]}\nMenuname: {menuname[i]}\nRating: {rating[i]}\nComment: {comment[i]}\nFeedback: {feedback[i]}\n\n"
			self.scroll_text.insert(tk.END, label_text)

		#username, rating, comment 보여주기
		
	def get_umrc(self):
		username_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Rating&comments!D2:D").execute().get('values', [])
		username = [item[0] for item in username_result]
		menu_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Rating&comments!E2:E").execute().get('values', [])
		menu = [item[0] for item in menu_result]
		rating_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Rating&comments!F2:F").execute().get('values', [])
		rating = [item[0] for item in rating_result]
		comment_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Rating&comments!G2:G").execute().get('values', [])
		comment = [item[0] for item in comment_result]
		feedback_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Rating&comments!H2:H").execute().get('values', [])
		feedback = [item[0] for item in feedback_result]

		self.group_umrc = list(zip(username, menu, rating, comment, feedback))

	def create_list(self):
		global username, menuname, rating, comment, feedback
		username = []
		menuname = []
		rating = []
		comment = []
		feedback = []
		for x in range(len(self.group_umrc)):
			if self.group_umrc[x][1] in self.display_group:
				username.append(str(self.group_umrc[x][0]))
				menuname.append(str(self.group_umrc[x][1]))
				rating.append(str(self.group_umrc[x][2]))
				comment.append(str(self.group_umrc[x][3]))
				feedback.append(str(self.group_umrc[x][4]))
		global average_rating
		average_rating = round(sum([int(x) for x in rating]) / len(rating), 1)

		return username, menuname, rating, comment, feedback
	
	def update_values(self):
		global firstoptionfixed
		global values
		if self.type_options.get() == 'beverages':
			values_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="menu page!A3:A8").execute().get('values', [])
			values = [item[0] for item in values_result]
			values.append('all')
			tkmb.showinfo(title = "Info", message = "Beverages are selected")
			firstoptionfixed = 'beverages'
			self.update_comments()
		elif self.type_options.get() == 'desserts':
			values_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="menu page!A12:A17").execute().get('values', [])
			values = [item[0] for item in values_result]
			values.append('all')
			tkmb.showinfo(title = "Info", message = "Desserts are selected")
			firstoptionfixed = 'desserts'
			self.update_comments()
		elif self.type_options.get() == 'foods':
			values_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="menu page!A21:A26").execute().get('values', [])
			values = [item[0] for item in values_result]
			values.append('all')
			tkmb.showinfo(title = "Info", message = "Foods are selected")
			firstoptionfixed = 'foods'
			self.update_comments()

	def search(self):
		menulist = values
		if self.type_options.get() != None and self.menu_options.get() == 'all':
				self.get_umrc()
				self.display_group = menulist
				username, menuname, rating, comment, feedback = self.create_list()
				self.update_comments()
		elif self.menu_options.get() != None and self.type_options.get() != 'all':
			self.get_umrc()
			self.display_group = [self.menu_options.get()]
			username, menuname, rating, comment, feedback = self.create_list()
			self.update_comments()
				
	def update_comments(self):
		self.destroy()
		newcomments = RatingComments(self.master)
		newcomments.pack(pady=20, padx=40, fill='both', expand=True)

	def gotohome(self):
		from loginscreen import LoginScreen
		self.destroy()
		main_page = LoginScreen(self.master)
		main_page.pack(pady=20, padx=40, fill='both', expand=True)

	def gotomanager(self):
		from managerpage import ManagerPage
		self.destroy()
		manager_page = ManagerPage(self.master)
		manager_page.pack(pady=20, padx=40, fill='both', expand=True)


if __name__ == "__main__":
	app = ctk.CTk()
	app.geometry("1280x850")
	app.title("please revisit us!")
	main_page = RatingComments(app)
	main_page.pack(pady=20, padx=40, fill='both', expand=True)
	app.mainloop()