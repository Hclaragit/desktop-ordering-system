import os
import csiagooglesheet
import customtkinter as ctk 
csiagooglesheet.main()
import tkinter.messagebox as tkmb 
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


sheet, SPREADSHEET_ID, beveragename, beverageprice, dessertname, dessertprice, foodname, foodprice = csiagooglesheet.getmenuvariables()
username_values = csiagooglesheet.getusername()

sheet, SPREADSHEET_ID, service = csiagooglesheet.getsheetinfofinal()


class Menupage(ctk.CTkFrame):
    def __init__(self, master, option, cart_items):
        super().__init__(master)
        self.master = master
        self.option = option
        self.cart_items = cart_items
        self.create_menus(self.option)

    def load_menus(self, option):
        if option == "beverages":
            names = beveragename
            prices = beverageprice
        elif option == "desserts":
            names = dessertname
            prices = dessertprice
        else:
            names = foodname
            prices = foodprice

        self.menu_groups = []
        
        for x in range(len(names)):
            menu_label = names[x] + ' | ' + prices[x] + ' $'
            menu = ctk.CTkLabel(self, text=menu_label)
            menu.configure(font=("Calibri", 20))
            menu.pack(padx=10, pady=10, anchor='center')

            num_entry = ctk.CTkEntry(self, placeholder_text='Enter number to buy', width = 200)
            num_entry.pack(padx=10, pady=10, anchor='center')
            num_entry.configure(font=('Calibri', 15))

        # Store menu item details in menu_groups
            menu_group = (names[x], prices[x], num_entry)
            self.menu_groups.append(menu_group)
        
        self.add_to_cart_button = ctk.CTkButton(self, text="Add to cart", command=self.add_to_cart, width=200, height=40)
        self.add_to_cart_button.pack(pady=20, padx=10, side = 'right')
        self.add_to_cart_button.configure(font=('Calibri', 15))

        self.delete_from_cart_button = ctk.CTkButton(self, text="Delete from cart", command=self.delete_from_cart, width=200, height=40)
        self.delete_from_cart_button.pack(pady=20, padx=10, side = 'right')
        self.delete_from_cart_button.configure(font=('Calibri', 15))

        self.purchase_button = ctk.CTkButton(self, text="Purchase", command=self.purchase, width=200, height=40)
        self.purchase_button.pack(pady=20, padx=10,side = 'right')
        self.purchase_button.configure(font=('Calibri', 15))

    def purchase(self):
        cartnew = self.cart_items
        self.clear_item()
        purchasepg = PurchaseWindow(self.master, cartnew)
        purchasepg.mainloop()
        
    
    def delete_from_cart(self):
        self.cart_items2 = []

        for name, price, num_entry in self.menu_groups:
            quantity = num_entry.get()

            if quantity == '':
                continue
            elif int(quantity) <= 0 or not int(quantity)>0:
                tkmb.showwarning(message = "Please enter a valid quantity.\n")
                break
            elif int(quantity) > 0:
            # Check if item is already in cart_items, update quantity if so
                self.cart_items2.append((name, price, int(quantity)))
      
        if len(self.cart_items2) != 0:
            count = 0
            for i in range(len(self.cart_items2)):
                print('cart2 =', self.cart_items2[i])
                for y in range(len(self.cart_items)):
                    cart_item_list = list(self.cart_items[y])
                    cart_item_list2 = list(self.cart_items2[i])
                    if cart_item_list[0] == cart_item_list2[0] and int(cart_item_list[2]) >= int(cart_item_list2[2]):
                        a = int(cart_item_list[2])
                        b = int(cart_item_list2[2])
                        cart_item_list[2] = (a-b)
                        self.cart_items[y] = (cart_item_list[0], cart_item_list[1], cart_item_list[2])

                        if cart_item_list[2] == 0:
                            self.cart_items.pop(y)
                        
                    elif cart_item_list[0] == cart_item_list2[0] and int(cart_item_list[2]) < int(cart_item_list2[2]):
                        tkmb.showwarning(message ="You cannot delete more than you have in your cart.\n")
                        break

                    elif cart_item_list2[0] != cart_item_list[0]:
                        count +=1
                        if count == len(self.cart_items):
                            tkmb.showwarning(message = cart_item_list2[0]+" not in your cart.\n")
                            break

            
        for name, price, quantity in self.cart_items:
            existing_item_index = None
            
            column_D = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="menu page!D6:D").execute().get('values', [])
            
            for x, value in enumerate(column_D):
                if value and value[0] == name:
                    existing_item_index = x + 6
                    break

            if existing_item_index is not None:
            # Update existing item
                body = {"values": [[name, price, quantity]]}
                sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=("menu page!D" + str(existing_item_index) + ":F"), valueInputOption="RAW", body=body).execute()
        self.show_previous_purchase_details_popup()

        for _, _, num_entry in self.menu_groups:
            num_entry.delete(0, 'end')

    def add_to_cart(self):
    
        for name, price, num_entry in self.menu_groups:
            quantity = num_entry.get()
            if quantity == '':
                continue
            elif int(quantity) <= 0:
                tkmb.showwarning(message = "Please enter a valid quantity.\n")
                break
            elif int(quantity) > 0:
            # Check if item is already in cart_items, update quantity if so
                updated = False
                for i in range(len(self.cart_items)):
                    if self.cart_items[i][0] == name:
                        self.cart_items[i] = (name, price, int(quantity))
                        updated = True
                        break
                        
                if not updated:
                    self.cart_items.append((name, price, int(quantity)))
            
        for name, price, quantity in self.cart_items:
            existing_item_index = None
            
            column_D = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="menu page!D6:D").execute().get('values', [])
            
            for i, value in enumerate(column_D):
                if value and value[0] == name:
                    existing_item_index = i + 6
                    break

            if existing_item_index is not None:
            # Update existing item
                body = {"values": [[name, price, quantity]]}
                sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=("menu page!D" + str(existing_item_index) + ":F"), valueInputOption="RAW", body=body).execute()
            else:
            # Add new item
                row_number = len(column_D) + 6
                body = {"values": [[name, price, quantity]]}
                sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=("menu page!D" + str(row_number) + ":F"), valueInputOption="RAW", body=body).execute()
        self.show_previous_purchase_details_popup()

        for _, _, num_entry in self.menu_groups:
            num_entry.delete(0, 'end')

    def show_previous_purchase_details_popup(self):
        self.popup_message = "Here are your previous purchase details:\n"
        previous_purchases = self.cart_items
        if previous_purchases:
            for purchase in previous_purchases:
                self.popup_message += f"{purchase[0]} - Quantity: {purchase[2]}\n"
        else:
            self.popup_message += "No previous purchases found."
    
        tkmb.showinfo("Previous Purchases", self.popup_message)

    def create_menus(self,option):
        if option == "beverages":
            self.label = ctk.CTkLabel(self, text="Beverages")
            self.label.configure(font=("Calibri", 30))
            self.label.pack(pady=20)

            self.button_gotomypage = ctk.CTkButton(self, text='Go to mypage', command = self.to_mypage, width=200, height=40)
            self.button_gotomypage.pack(pady=12, padx=10, anchor='sw')
            self.button_gotomypage.configure(font=('Calibri', 15))

            self.button_gofoods = ctk.CTkButton(self, text='Go to \nfoods', command = self.to_food, width=100, height=100)
            self.button_gofoods.pack(side='left',pady=12, padx=10)
            self.button_gofoods.configure(font=('Calibri', 15))
            

            self.button_godesserts = ctk.CTkButton(self, text='Go to \nDesserts', command = self.to_dessert, width=100, height=100)
            self.button_godesserts.pack(side='right',pady=12, padx=10)
            self.button_godesserts.configure(font=('Calibri', 15))

            self.load_menus(option)

        elif option == "desserts":
            self.label = ctk.CTkLabel(self, text="Desserts")
            self.label.configure(font=("Calibri", 30))
            self.label.pack(pady=20)

            self.button_gotomypage = ctk.CTkButton(self, text='Go to mypage', command = self.to_mypage, width=200, height=40)
            self.button_gotomypage.pack(pady=12, padx=10, anchor='sw')
            self.button_gotomypage.configure(font=('Calibri', 15))

            self.button_gobeverages = ctk.CTkButton(self, text='Go to \nbeverages', command = self.to_beverage, width=100, height=100)
            self.button_gobeverages.pack(side='left',pady=12, padx=10)
            self.button_gobeverages.configure(font=('Calibri', 15))

            self.button_gofoods = ctk.CTkButton(self, text='Go to \nfoods', command = self.to_food, width=100, height=100)
            self.button_gofoods.pack(side='right',pady=12, padx=10)
            self.button_gofoods.configure(font=('Calibri', 15))

            self.load_menus(option)

        elif option == "foods":
            self.label = ctk.CTkLabel(self, text="Foods")
            self.label.configure(font=("Calibri", 30))
            self.label.pack(pady=20)

            self.button_gotomypage = ctk.CTkButton(self, text='Go to mypage', command = self.to_mypage, width=200, height=40)
            self.button_gotomypage.pack(pady=12, padx=10, anchor='sw')
            self.button_gotomypage.configure(font=('Calibri', 15))  

            self.button_godesserts = ctk.CTkButton(self, text='Go to \nDesserts', command = self.to_dessert, width=100, height=100)
            self.button_godesserts.pack(side='left',pady=12, padx=10)
            self.button_godesserts.configure(font=('Calibri', 15))

            self.button_gobeverages = ctk.CTkButton(self, text='Go to \nbeverages', command = self.to_beverage, width=100, height=100)
            self.button_gobeverages.pack(side='right',pady=12, padx=10)
            self.button_gobeverages.configure(font=('Calibri', 15))

            self.load_menus(option)
        
    def to_beverage(self):
        self.destroy()
        option = "beverages"
        menu_page = Menupage(self.master,option, cart_items= self.cart_items)
        menu_page.pack(pady=20, padx=40, fill='both', expand=True)
    def to_dessert(self):
        self.destroy()
        option = "desserts"
        menu_page = Menupage(self.master,option, cart_items= self.cart_items)
        menu_page.pack(pady=20, padx=40, fill='both', expand=True)
    def to_food(self):
        self.destroy()
        option = "foods"
        menu_page = Menupage(self.master,option, cart_items= self.cart_items)
        menu_page.pack(pady=20, padx=40, fill='both', expand=True)
    
    def to_mypage(self):
        self.destroy()
        from mypage import MyPage
        mypage = MyPage(self.master)
        mypage.pack(pady=20, padx=40, fill='both', expand=True)

    def clear_item(self):
        self.cart_items = []


class PurchaseWindow(ctk.CTkToplevel):
    def __init__(self, app, carty):
        super().__init__(app)
        self.title("Purchase")
        self.geometry("800x600")
        self.cart_items = carty

			
        self.label_choice = ctk.CTkLabel(self, text="Choose payment option: card or account")
        self.label_choice.configure(font=("Calibri", 15))
        self.label_choice.pack(pady=10)

        self.checkbox_card = ctk.CTkCheckBox(self, text="Card")
        self.checkbox_card.configure(font=("Calibri", 15))
        self.checkbox_card.pack(pady=5)

        self.checkbox_account = ctk.CTkCheckBox(self, text="Account")
        self.checkbox_account.configure(font=("Calibri", 15))
        self.checkbox_account.pack(pady=5)

		
        self.label_pointsq = ctk.CTkLabel(self, text="Use ponts for the discount? \n * 1 point is earned per 10$ \n *1 point corresponds to 1$")
        self.label_pointsq.configure(font=("Calibri", 15))
        self.label_pointsq.pack(pady=10)
        self.load_point()
        self.points = [row[0] for row in self.point_result.get("values", [])[0:]]
        self.point = int(self.points[0])
        self.label_points = ctk.CTkLabel(self, text="your total point: "+str(self.point))
        self.label_points.configure(font=("Calibri", 15))
        self.label_points.pack(pady=10)
        self.entry_points = ctk.CTkEntry(self, placeholder_text="Enter num of points to use",  width=200, height=30)
        self.entry_points.pack(pady=5)
        self.entry_points.configure(font=('Calibri', 15))
			
        self.purchase_button = ctk.CTkButton(self, text="purchase", command=self.purchase, width=200, height=40)
        self.purchase_button.configure(font=('Calibri', 15))
        self.purchase_button.pack(pady=10)

    def load_point(self):
        self.load_username()
        user_col = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="login screen!A2:A").execute()
        for x in range(len(user_col)):
            if user_col.get('values', [])[x][0] == self.username:
                self.point_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="login screen!D"+str(x+2)).execute()
                self.rownum = str(x+2)
    
    def update_point(self, new_point):
        body = {"values": [[new_point]]}
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=("login screen!D"+self.rownum), valueInputOption="RAW", body=body).execute()

    def purchase(self):
        #adding basic info: payment choice, date ordered, use points to the sheet

        choice = [self.checkbox_card.get(), self.checkbox_account.get()]
        if choice == [0,0]:
            tkmb.showinfo(title = "Error", message="Please choose a payment option")
            return
        elif choice == [1,1]:
            tkmb.showinfo(title = "Error", message="2 payment options are selected. Please choose only one")
            return
        else:
            if choice[0] == 1:
                paymentchoice = "card"
            elif choice[1] == 1:
                paymentchoice = "account"

        if self.entry_points.get().isdigit() and int(self.entry_points.get()) >0 and int(self.entry_points.get()) <= self.point:
            use_points = int(self.entry_points.get())
        elif not self.entry_points.get().isdigit() or not self.entry_points.get() or int(self.entry_points.get()) == 0:
            use_points = 0
        elif int(self.entry_points.get()) < 0:
            tkmb.showwarning(title = "Error", message = "Please enter a valid number of points")
            return
        elif int(self.entry_points.get()) > self.point:
            tkmb.showwarning(title = "Error", message= "You don't have enough points")
            return
            
        self.dateordered = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        column_A = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="manager page!A2:A").execute().get('values', [])
        column_ABCD = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="manager page!A2:D").execute().get('values', [])

        if len(column_A) > 0:
            body = {"values": column_ABCD}
            sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=("manager page!A3:D"), valueInputOption="RAW", body=body).execute()
        
        body = {"values": [[self.dateordered, paymentchoice]]}
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=("menu page!E2:F2"), valueInputOption="RAW", body=body).execute()
        self.pointcalculation(use_points)
        self.create_pop_up(self.total_price, use_points, self.new_total, self.new_point, paymentchoice, self.dateordered)
        self.clear_cart()
    
    def pointcalculation(self, use_points):
        #first, calculate the total price of the items in the cart
        self.total_price = 0
        for name, price, quantity in self.cart_items:
            self.total_price += float(price) * int(quantity)

        if use_points !=0:
            self.new_total = self.total_price - use_points
            self.new_point = self.total_price//10 + (self.point - use_points)
            return self.total_price, self.new_total, self.new_point
        elif use_points == 0:
            self.new_total = self.total_price
            self.new_point = self.total_price//10 + self.point
            return self.total_price, self.new_total, self.new_point
        
    def load_username(self):
        username_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="menu page!G2").execute()
        usernames = [row[0] for row in username_result.get("values", [])[0:]]
        self.username = usernames[0]
    
    def create_pop_up(self, total_price, use_points, new_total, new_point, paymentchoice, dateordered):
        self.load_username()
        popuplist = [total_price, use_points, new_total, new_point, paymentchoice, dateordered]
        earned = popuplist[0]//10
        self.pop_up = ""

        if use_points>0:
            # creates pop up
            self.pop_up += f"Total price: {str(popuplist[0])} $ \n"
            self.pop_up += f"New total price: {str(popuplist[2])} $ \n"
            self.pop_up += f"point used: {str(popuplist[1])}\n"
            self.pop_up += f"point earned: {str(earned)} \n"
            self.pop_up += f"New point: {str(popuplist[3])} \n"
            self.pop_up += f"Payment choice: {popuplist[4]} \n"
            self.pop_up += f"Date ordered: {popuplist[5]} \n"
            tkmb.showinfo("Your purchase details", self.pop_up)
            self.update_point(popuplist[3])
            self.send_email()
            self.add_to_manager_page()
            self.destroy()


        else:
            self.pop_up += f"Total price: {str(popuplist[0])} $ \n"
            self.pop_up += f"point earned: {str(earned)} \n"
            self.pop_up += f"New point: {str(popuplist[3])} \n"
            self.pop_up += f"Payment choice: {popuplist[4]} \n"
            self.pop_up += f"Date ordered: {popuplist[5]} \n"
            tkmb.showinfo("Your purchase details", self.pop_up)
            self.update_point(popuplist[3])
            self.send_email()
            self.add_to_manager_page()
            self.destroy()

    # 이메일 보내기, 매니저 페이지에 추가
    def send_email(self):
        shop_email = os.environ.get("SHOP_EMAIL")
        shop_password = os.environ.get("SHOP_EMAIL_APP_PASSWORD")
        if not shop_email or not shop_password:
            print("Email not sent: SHOP_EMAIL and SHOP_EMAIL_APP_PASSWORD are not set.")
            return
        subject = "Your Purchase Details"
        message = """\n Dear Customer,\n Thank you for your purchase.\n Here are your payment details:\n\n""" +self.pop_up+ """\n\n If you have any questions or concerns, \n please feel free to contact us.\n\n Best regards,\n\n Your Store"""

        # Create email message
        msg = MIMEMultipart()
        msg["From"] = shop_email
        msg["To"] = self.username
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

            # Send email
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(shop_email, shop_password)
                server.sendmail(shop_email, self.username, msg.as_string())
        except Exception as e:
                print("Failed to send email:", str(e))
    
    def clear_cart(self):
        request = service.spreadsheets().values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range="menu page!D6:F")
        response = request.execute()



    def load_purchase(self):
        self.purchased_details = ""
        name =[]
        price = []
        quantity = []

        purchase_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="menu page!D6:F").execute()
        purchase_values = [row[0] for row in purchase_result.get("values", [])[0:]]

        for x in range(0, len(purchase_values)-3, 3):
            name.append(purchase_values[x])
            price.append(purchase_values[x+1])
            quantity.append(purchase_values[x+2])
            self.purchased_details += f"{name} - Quantity: {quantity} | Price: {price} \n"

    def add_to_manager_page(self):
        self.load_purchase()
        finish = False
        body = {"values": [[self.username, finish, self.pop_up, self.dateordered]]}
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=("manager page!A2:D"), valueInputOption="RAW", body=body).execute()

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1280x850")
    app.title("please revisit us!")
    from mainpage import option  
    menu_page = Menupage(app,option)
    menu_page.pack(pady=20, padx=40, fill='both', expand=True)
    app.mainloop()
