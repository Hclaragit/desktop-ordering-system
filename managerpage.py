import csiagooglesheet
import customtkinter as ctk 
import tkinter.messagebox as tkmb 
import tkinter as tk

csiagooglesheet.main()
sheet, SPREADSHEET_ID, service = csiagooglesheet.getsheetinfofinal()

fisrtoptionfixed = ''

username = []
finish = []
purchase_details = []
date_ordered = []

username, finish, purchase_details, date_ordered = csiagooglesheet.getmanagerpage()

class ManagerPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		self.create_widgets()
		
	def create_widgets(self):
		self.button_gohome = ctk.CTkButton(self, text='go to login screen', command = self.gotohome)
		self.button_gohome.pack(pady=10, padx=20, anchor='ne')
		self.button_gohome.configure(font=('Calibri', 15))

		self.label_previously_ordered = ctk.CTkLabel(self, text='Previously ordered items')
		self.label_previously_ordered.configure(font=('Calibri', 15))
		self.label_previously_ordered.pack(pady=5, padx=20, anchor = 'sw')
		
		self.frame_left = tk.Frame(self)
		self.frame_left.pack(side='left', padx=20, pady=5, fill='y')

        # Create a Text widget for scrolling with larger font
		self.scroll_text = tk.Text(self.frame_left, wrap=tk.NONE, width=70, height=10, font=('Calibri', 15))
		self.scroll_text.pack(side='left', fill='both', expand=False)

        # Create a Scrollbar and associate it with the Text widget
		self.scrollbar = tk.Scrollbar(self.frame_left, command=self.scroll_text.yview)
		self.scrollbar.pack(side='right', fill='y')
		self.scroll_text.config(yscrollcommand=self.scrollbar.set)

        # Insert labels into Text widget
		for i in range(len(username)):
			label_text = f"Username: {username[i]}\nFinish: {finish[i]}\nPurchase details: {purchase_details[i]}\n\n"
			self.scroll_text.insert(tk.END, label_text)

        # OptionMenu widget on the right
		self.frame_right = tk.Frame(self)
		self.frame_right.pack(side='left', padx=60, pady=20)

		self.label_finish = ctk.CTkLabel(self.frame_right, text='Order finised for customer: ')
		self.label_finish.configure(font=('Calibri', 15))
		self.label_finish.pack(padx=20, pady=10)
		
		self.type_options = ctk.CTkOptionMenu(self.frame_right, values=date_ordered)
		self.type_options.set(fisrtoptionfixed)
		self.type_options.pack(padx=10, pady=10)

		self.button_confirm = ctk.CTkButton(self.frame_right, text='Confirm', command = self.finish_order, width=60, height=30)
		self.button_confirm.pack(padx=10, pady=10,)
		self.button_confirm.configure(font=('Calibri', 15))

		self.button_orderhistory = ctk.CTkButton(self.frame_right, text='Order History', command = self.to_order_history, width=200, height=40)
		self.button_orderhistory.pack(padx=10, pady=10)
		self.button_orderhistory.configure(font=('Calibri', 15))

		self.button_ratingcomments = ctk.CTkButton(self.frame_right, text='Rating & Comments', command = self.to_rating_comments, width=200, height=40)
		self.button_ratingcomments.pack(padx=10, pady=10)
		self.button_ratingcomments.configure(font=('Calibri', 15))


	def finish_order(self):
		finish = "TRUE"
		selected_date = self.type_options.get()
		for x in range(len(date_ordered)):
			if selected_date == date_ordered[x]:
				self.index = x
				break
		colA = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="order history page!A2:A").execute().get('values', [])
		colABCD = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="order history page!A2:D").execute().get('values', [])

		# Delete the row from the manager page Google Sheet
		
		if len(colA) > 0:
			body = {"values": colABCD}
			sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=("order history page!A3:D"), valueInputOption="RAW", body=body).execute()
		body = {"values": [[username[self.index], finish, purchase_details[self.index], date_ordered[self.index]]]}
		sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=("order history page!A2:D"), valueInputOption="RAW", body=body).execute()
		self.delete_row(service, SPREADSHEET_ID, "manager page", (self.index+2))
		self.update_order()
		tkmb.showinfo(title="Order Finished", message="Order has been moved to order history page")
		
		self.datacollecting()
		self.destroy()
		from managerpage import ManagerPage
		managing = ManagerPage(self.master)
		managing.pack(pady=20, padx=40, fill='both', expand=True)

	def datacollecting(self):
		global username, finish, purchase_details, date_ordered
		csiagooglesheet.main()
		username, finish, purchase_details, date_ordered = csiagooglesheet.getmanagerpage()


		
	def update_order(self):
		global username, finish, purchase_details, date_ordered
		username, finish, purchase_details, date_ordered = csiagooglesheet.getmanagerpage()
		self.scroll_text.delete("1.0", tk.END)
		for i in range(len(username)):
			label_text = f"Username: {username[i]}\nFinish: {finish[i]}\nPurchase details: {purchase_details[i]}\n\n"
			self.scroll_text.insert(tk.END, label_text)
		

	def delete_row(self, service, spreadsheet_id, sheet_name, row_index):
		sheet_id = self.get_sheet_id(service, spreadsheet_id, sheet_name)
		request = {"requests": [{"deleteDimension": {"range": {"sheetId": sheet_id,"dimension": "ROWS",
                        "startIndex": row_index-1 ,  # Adjust for 0-based index
                        "endIndex": row_index  # If deleting single row, endIndex should be start index + 1
						}}}]}
		response = service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID,body=request).execute()

	def get_sheet_id(self, service, spreadsheet_id, sheet_name):
		sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
		sheets = sheet_metadata.get('sheets', [])
		for sheet in sheets:
			if sheet['properties']['title'] == sheet_name:
				return sheet['properties']['sheetId']
	
	def to_order_history(self):
		self.destroy()
		from orderhistorypage import OrderhistoryPage
		order_history_page = OrderhistoryPage(self.master)
		order_history_page.pack(pady=20, padx=40, fill='both', expand=True)

	def gotohome(self):
		self.destroy()
		from loginscreen import LoginScreen
		main_page = LoginScreen(self.master)
		main_page.pack(pady=20, padx=40, fill='both', expand=True)
	
	def to_rating_comments(self):
		self.destroy()
		from ratingcommentspage import RatingComments
		rating_comments_page = RatingComments(self.master)
		rating_comments_page.pack(pady=20, padx=40, fill='both', expand=True)

if __name__ == "__main__":
	app = ctk.CTk()
	app.geometry("1280x850")
	app.title("please revisit us!")
	main_page = ManagerPage(app)
	main_page.pack(pady=20, padx=40, fill='both', expand=True)
	app.mainloop()