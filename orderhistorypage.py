import csiagooglesheet
import customtkinter as ctk 
import tkinter.messagebox as tkmb 
import tkinter as tk

csiagooglesheet.main()
sheet, SPREADSHEET_ID = csiagooglesheet.getsheetinfo()

username_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="order history page!A2:A").execute().get('values', [])
username = [item[0] for item in username_result]
finish_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="order history page!B2:B").execute().get('values', [])
finish = [item[0] for item in finish_result]
purchase_details_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="order history page!C2:C").execute().get('values', [])
purchase_details = [item[0] for item in purchase_details_result]

class OrderhistoryPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		self.create_widgets()
		
	def create_widgets(self):
		self.label_previously_ordered = ctk.CTkLabel(self, text='Order history items')
		self.label_previously_ordered.configure(font=('Calibri', 15))
		self.label_previously_ordered.pack(pady=5, padx=20, anchor = 'sw')

        # Create a Text widget for scrolling with larger font
		self.scroll_text = tk.Text(self, wrap=tk.NONE, width=40, height=10, font=('Calibri', 15))
		self.scroll_text.pack(pady=10, padx=20, side='left', fill='both', expand=True)

        # Create a Scrollbar and associate it with the Text widget
		self.scrollbar = tk.Scrollbar(self, command=self.scroll_text.yview)
		self.scrollbar.pack(side='left', fill='y')
		self.scroll_text.config(yscrollcommand=self.scrollbar.set)

        # Insert labels into Text widget
		for i in range(len(username)):
			label_text = f"Username: {username[i]}\nFinish: {finish[i]}\nPurchase details: {purchase_details[i]}\n\n"
			self.scroll_text.insert(tk.END, label_text)

		self.button_gohome = ctk.CTkButton(self, text='go to login screen', command = self.gotohome, width=200, height=40)
		self.button_gohome.pack(pady=5, padx=20, anchor='se')
		self.button_gohome.configure(font=('Calibri', 15))
		self.button_gomanager = ctk.CTkButton(self, text='go to manager', command = self.gotomanager, width=200, height=40)
		self.button_gomanager.pack(pady=5, padx=20, anchor='se')
		self.button_gomanager.configure(font=('Calibri', 15))
	
	def gotohome(self):
		self.destroy()
		from loginscreen import LoginScreen
		main_page = LoginScreen(self.master)
		main_page.pack(pady=20, padx=40, fill='both', expand=True)

	def gotomanager(self):
		self.destroy()
		from managerpage import ManagerPage
		manager_page = ManagerPage(self.master)
		manager_page.pack(pady=20, padx=40, fill='both', expand=True)

if __name__ == "__main__":
	app = ctk.CTk()
	app.geometry("1280x850")
	app.title("please revisit us!")
	main_page = OrderhistoryPage(app)
	main_page.pack(pady=20, padx=40, fill='both', expand=True)
	app.mainloop()