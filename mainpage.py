import customtkinter as ctk 
import tkinter as tk


ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("blue")
option = ""
cart_items = []

class MainPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		self.create_buttons()

	def create_buttons(self):
		
		self.button_mypage = ctk.CTkButton(self, text='mypage', command = self.to_mypage, width=200, height=50)
		self.button_mypage.pack(pady=12, padx=10)
		self.button_mypage.configure(font=('Calibri', 15))

		self.button_gotohome = ctk.CTkButton(self, text='Home', command = self.to_loginscreen, width=200, height=50)
		self.button_gotohome.pack(pady=12, padx=10)
		self.button_gotohome.configure(font=('Calibri', 15))

		self.middle_frame = tk.Frame(self, width=1200) 
		self.middle_frame.pack(pady=150)
		label = tk.Label(self.middle_frame, text="What's in our shop?", font=('Calibri', 15))
		label.pack(pady=30)

		self.button_beverages = ctk.CTkButton(self.middle_frame, text='Beverages', command = self.to_beverages, width=200, height=200)
		self.button_beverages.pack(side='left', pady=12, padx=100)
		self.button_beverages.configure(font=('Calibri', 15))
		
		self.button_desserts = ctk.CTkButton(self.middle_frame, text='Desserts', command = self.to_desserts, width=200, height=200)
		self.button_desserts.pack(side='left',pady=12, padx=100)
		self.button_desserts.configure(font=('Calibri', 15))
		
		self.button_foods = ctk.CTkButton(self.middle_frame, text='Foods', command = self.to_foods, width=200, height=200)
		self.button_foods.pack(side='right',pady=12, padx=100)
		self.button_foods.configure(font=('Calibri', 15))

	def to_mypage(self):
		self.destroy()
		from mypage import MyPage
		my_page = MyPage(self.master)
		my_page.pack(pady=20, padx=40, fill='both', expand=True)

	def to_loginscreen(self):
		self.destroy()
		from loginscreen import LoginScreen
		login_screen = LoginScreen(self.master)
		login_screen.pack(pady=20, padx=40, fill='both', expand=True)

	def to_beverages(self):
		self.destroy()
		global option
		option = "beverages"
		from menupage import Menupage
		menu_page = Menupage(self.master,option, cart_items= [])
		menu_page.pack(pady=20, padx=40, fill='both', expand=True)

	def to_desserts(self):
		self.destroy()
		global option
		option = "desserts"
		from menupage import Menupage
		menu_page = Menupage(self.master,option, cart_items= [])
		menu_page.pack(pady=20, padx=40, fill='both', expand=True)

	def to_foods(self):
		self.destroy()
		global option
		option = "foods"
		from menupage import Menupage
		menu_page = Menupage(self.master,option, cart_items= [])
		menu_page.pack(pady=20, padx=40, fill='both', expand=True)

if __name__ == "__main__":
	app = ctk.CTk()
	app.geometry("1280x850")
	app.title("please revisit us!")
	main_page = MainPage(app)
	main_page.pack(pady=20, padx=40, fill='both', expand=True)
	app.mainloop()



