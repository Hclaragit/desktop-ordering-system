import customtkinter as ctk 
import tkinter.messagebox as tkmb 
import csiagooglesheet
import re

csiagooglesheet.main()

tusername, tpassword, tsecurity, sheet, SPREADSHEET_ID, num = csiagooglesheet.getvariables()
managerusername_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="login screen!G2").execute().get('values', [])
managerusername = managerusername_result[0][0]
managerpassword_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="login screen!H2").execute().get('values', [])
managerpassword = managerpassword_result[0][0]
# Selecting GUI theme - dark, light , system (for system default) 
ctk.set_appearance_mode("light") 
# Selecting color theme - blue, green, dark-blue 
ctk.set_default_color_theme("dark-blue") 

class LoginScreen(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		self.create_widgets()

	def create_widgets(self):
		self.label = ctk.CTkLabel(self, text="Welcome to the shop")
		self.label.pack(pady=20)
		self.label.configure(font=('Calibri', 15))

		self.label_username = ctk.CTkLabel(self, text='Please enter your username and password')
		self.label_username.pack(pady=12, padx=10)
		self.label_username.configure(font=('Calibri', 15))

		self.user_entry = ctk.CTkEntry(self, placeholder_text="Username", width=200, height=30)
		self.user_entry.pack(pady=17, padx=20)
		self.user_entry.configure(font=('Calibri', 15))

		self.user_pass = ctk.CTkEntry(self, placeholder_text="Password",width=200, height=30, show="*")
		self.user_pass.pack(pady=17, padx=20)
		self.user_pass.configure(font=('Calibri', 15))

		self.button_login = ctk.CTkButton(self, text='Login', command=self.login, width=200, height=40)
		self.button_login.pack(pady=12, padx=10)
		self.button_login.configure(font=('Calibri', 15))

		self.button_signin = ctk.CTkButton(self, text='Sign In', command=self.sign_in, width=200, height=40)
		self.button_signin.pack(pady=12, padx=10)
		self.button_signin.configure(font=('Calibri', 15))
		
		self.button_change_pass = ctk.CTkButton(self, text='Change Password', command=self.change_password, width=200, height=40)
		self.button_change_pass.pack(pady=12, padx=10)
		self.button_change_pass.configure(font=('Calibri', 15))
	
	def login(self):
		tusername, tpassword, tsecurity, sheet, SPREADSHEET_ID, num = csiagooglesheet.getvariables()
		username = self.user_entry.get()
		userpassword = self.user_pass.get()
		if username in tusername:
			for x in range(len(tusername)):
				if username == tusername[x]:
					password = tpassword[x]
					body = {"values": [[tusername[x]]]}
					sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=("menu page!G2"), valueInputOption="RAW", body=body).execute()

			if userpassword == password:
				new_window = ctk.CTkToplevel(self.master)
				new_window.title("New Window")
				new_window.geometry("350x200")
				tkmb.showinfo(title="Login Successful", message="You have logged in Successfully")
				new_window.destroy()
				self.load_mainpage()
			elif userpassword != password:
				tkmb.showwarning(title='Wrong password', message='Please check your password')
		else:
			if username == managerusername:
				if userpassword == managerpassword:
					self.destroy()
					from managerpage import ManagerPage
					manager_page = ManagerPage(self.master)
					manager_page.pack(pady=20, padx=40, fill='both', expand=True)
					tkmb.showinfo(title="Login Successful", message="Welcome, manager!")
				else:
					tkmb.showwarning(title='Login failed', message='Invalid username')
	
	def sign_in(self):
		signinfunc = SignInWindow(self.master)
		signinfunc.mainloop()

	def change_password(self):
		signinfunc = Changepass(self.master)
		signinfunc.mainloop()

	def load_mainpage(self):
		self.destroy()
		from mainpage import MainPage
		main_page = MainPage(self.master)
		main_page.pack(pady=20, padx=40, fill='both', expand=True)

class SignInWindow(ctk.CTkToplevel):
	def __init__(self, app):
		super().__init__(app)
		self.title("Sign In")
		self.geometry("800x600")
			
		self.label_username = ctk.CTkLabel(self, text="Username")
		self.label_username.pack(pady=10)
		self.label_username.configure(font=('Calibri', 15))

		self.entry_username = ctk.CTkEntry(self, placeholder_text="Enter username", width=200, height=30)
		self.entry_username.pack(pady=5)
		self.entry_username.configure(font=('Calibri', 15))
		
		self.label_password = ctk.CTkLabel(self, text="Password")
		self.label_password.pack(pady=10)
		self.label_password.configure(font=('Calibri', 15))
		self.entry_password = ctk.CTkEntry(self, placeholder_text="Enter password", show="*", width=200, height=30)
		self.entry_password.pack(pady=5)
		self.entry_password.configure(font=('Calibri', 15))
			
		self.label_security_question = ctk.CTkLabel(self, text="Security Question")
		self.label_security_question.pack(pady=10)
		self.label_security_question.configure(font=('Calibri', 15))
		self.entry_security_question = ctk.CTkEntry(self, placeholder_text="What's your favourite thing?", width=200, height=30)
		self.entry_security_question.pack(pady=5)
		self.entry_security_question.configure(font=('Calibri', 15))
			
		self.button_submit = ctk.CTkButton(self, text="sign in", command=self.sign_in, width=200, height=40)
		self.button_submit.pack(pady=10)
		self.button_submit.configure(font=('Calibri', 15))
		
	def get_variables(self):
		newun = self.entry_username.get() 
		newps = self.entry_password.get()
		newsq = self.entry_security_question.get()
		return newun, newps, newsq
		
	def sign_in(self):
		
		newun, newps, newsq = self.get_variables()
		point = 5

		if not re.match(r"[\w.+-]+@[\w-]+\.[\w.-]+", newun):
			tkmb.showwarning(title='Invalid Username', message='Username should be in email format')
		elif newun in tusername:
			tkmb.showerror(title="Sign In Failed", message="Username already exists")
		else:
			if not newun or not newps or not newsq:
				tkmb.showwarning(title='Incomplete Information', message='Please fully complete each box')
			elif len(newps) <5:
				tkmb.showwarning(title='Weak Password', message='Password should be at least 5 characters')
			else:

				body1 = {"values": [[newun]]}
				sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=("login screen!A" + str(num+2)),valueInputOption="RAW", body=body1).execute()

				body2 = {"values": [[newps]]}
				sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=("login screen!B" + str(num+2)),valueInputOption="RAW", body=body2).execute()
				
				body3 = {"values": [[newsq]]}
				sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=("login screen!C" + str(num+2)), valueInputOption="RAW", body=body3).execute()

				body4 = {"values": [[point]]}
				sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=("login screen!D" + str(num+2)), valueInputOption="RAW", body=body4).execute()
				
				tkmb.showinfo(title='Sign in succeeded', message='Thanks for signing in!\n You just earned 5 points!')
				csiagooglesheet.main()
				self.destroy()

class Changepass(ctk.CTkToplevel):
	def __init__(self, app):
		super().__init__(app)
		self.title("change password")
		self.geometry("800x600")
			
		self.label_username = ctk.CTkLabel(self, text="Username")
		self.label_username.pack(pady=10)
		self.label_username.configure(font=('Calibri', 15))

		self.entry_username = ctk.CTkEntry(self, placeholder_text="Enter username", width=200, height=30)
		self.entry_username.pack(pady=5)
		self.entry_username.configure(font=('Calibri', 15))
		
		self.label_password = ctk.CTkLabel(self, text="Current Password")
		self.label_password.pack(pady=10)
		self.label_password.configure(font=('Calibri', 15))
		self.entry_password = ctk.CTkEntry(self, placeholder_text="Enter password", show="*", width=200, height=30)
		self.entry_password.pack(pady=5)
		self.entry_password.configure(font=('Calibri', 15))
			
		self.label_security_question = ctk.CTkLabel(self, text="Security Question")
		self.label_security_question.pack(pady=10)
		self.label_security_question.configure(font=('Calibri', 15))
		self.entry_security_question = ctk.CTkEntry(self, placeholder_text="What's your favourite thing?", width=200, height=30)
		self.entry_security_question.pack(pady=5)
		self.entry_security_question.configure(font=('Calibri', 15))

		self.label_newpass = ctk.CTkLabel(self, text="New Password")
		self.label_newpass.pack(pady=10)
		self.label_newpass.configure(font=('Calibri', 15))

		self.entry_newpass = ctk.CTkEntry(self, placeholder_text="Enter new password", show="*", width=200, height=30)
		self.entry_newpass.pack(pady=5)
		self.entry_newpass.configure(font=('Calibri', 15))
			
		self.button_submit = ctk.CTkButton(self, text="change password", command=self.change_pass, width=200, height=40)
		self.button_submit.pack(pady=10)
		self.button_submit.configure(font=('Calibri', 15))

		self.tusername, self.tpassword, self.tsecurity, self.sheet, self.SPREADSHEET_ID, self.num = csiagooglesheet.getvariables()
		
	def get_variables(self):
		un = self.entry_username.get() 
		pswd = self.entry_password.get()
		newps = self.entry_newpass.get()
		sq = self.entry_security_question.get()
		return un, pswd, newps, sq
	
	def change_pass(self):
		un, pswd, newps, sq = self.get_variables()
		if un not in self.tusername:
			tkmb.showerror(title="Username not found", message="Username does not exist")
		elif un in self.tusername and pswd != self.tpassword[self.tusername.index(un)]:
			tkmb.showerror(title="Incorrect password", message="Incorrect password")
		elif un in self.tusername and pswd == self.tpassword[self.tusername.index(un)] and sq != self.tsecurity[self.tusername.index(un)]:
			tkmb.showerror(title="Incorrect security question", message="Incorrect security question")
		else:
			if len(newps) <5:
				tkmb.showwarning(title='Weak Password', message='Password should be at least 5 characters')
			else:
				body = {"values": [[newps]]}
				self.sheet.values().update(spreadsheetId=self.SPREADSHEET_ID, range=("login screen!B" + str(self.tusername.index(un)+2) + ":C"), valueInputOption="RAW", body=body).execute()
				tkmb.showinfo(title='Password changed', message='Password changed successfully')
				csiagooglesheet.main()

				self.destroy()

if __name__ == "__main__":
	app = ctk.CTk()
	app.geometry("1280x850")
	app.title("please revisit us!")
	login_screen = LoginScreen(app)
	login_screen.pack(pady=20, padx=40, fill='both', expand=True)
	app.mainloop()