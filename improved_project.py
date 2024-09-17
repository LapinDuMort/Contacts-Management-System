import sqlite3, random
from prettytable import PrettyTable

db = sqlite3.connect("contacts.sqlite")

db.execute("CREATE TABLE IF NOT EXISTS contacts(name TEXT phone TEXT email TEXT)")
cursor = db.cursor()
select_cursor = db.cursor()
def add():
    addname = input("Please enter a new name: ")
    addnumber = input("Please enter a new phone number: ")
    addemail = input("Please enter a new email address: ")
    addname = addname.title()
    addemail = addemail.lower().strip()
    addnumber = addnumber.strip(" abcdefghijklmnopqrstuvwxyz+()[]ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    confirm = input(f"You wish to add a ontact called {addname}, with a phone number of {addnumber} and an email of {addemail}. Is this correct? Y/N: ")
    confirm = confirm.upper()
    while confirm != "Y" and confirm != "N":
        confirm = input(f"Please enter Y to confirm addition or N to decline addition: ")
    if confirm == "Y":
        db.execute(f"INSERT INTO contacts(name, phone, email) Values('{addname}', '{addnumber}','{addemail}')")
        print("Successfully added contact!")
        db.commit()
        customerchoice()
    elif confirm == "N":
        print("Contact NOT added to database.")
        customerchoice()


def read():
    table = PrettyTable()
    table.field_names = ["Name", "Phone", "Email"]
    inputtype = input("Would you like to search for a contact by [name], [phone] or [email]? Alternatively you can type [*] to view all saved contacts: ")
    inputtype = inputtype.lower().strip("[]")
    while inputtype != "name" and inputtype != "phone" and inputtype != "email" and inputtype!= "quit" and inputtype!= "*":
        inputtype = input("Please either type [name] to search by name, [phone] to search by phone or [email] to search by email: ")
        inputtype = inputtype.lower().strip("[]")

    if inputtype == "quit":
        customerchoice()

    if inputtype == "*":
            select_cursor = db.cursor()
            for row in select_cursor.execute("SELECT * FROM contacts"):
                rowname, rowphone, rowemail = row
                table.add_row([rowname, rowphone, rowemail])
 
            print(table)
    if inputtype == "name":
        custnameread = input("To read contact's info please enter the contact's name or type [*] to view all: ")
        custnameread = custnameread.title().strip()
        if custnameread == "*":
            select_cursor = db.cursor()
            for row in select_cursor.execute("SELECT * FROM contacts"):
                rowname, rowphone, rowemail = row
                table.add_row([rowname, rowphone, rowemail])
 
            print(table)
        else:
            select_cursor = db.cursor()
            db_info = select_cursor.execute("SELECT * FROM contacts WHERE name = ?", [custnameread]).fetchall()
            if db_info is None:
                print("That name does not appear to be in the contacts list. If you would like to add them, please type [add].")
                customerchoice()
            else:
                for name, phone, email in db_info:
                        table.add_row([name, phone, email])
            print(table)

    if inputtype == "phone":
        custnumread = input("To read a contact's info please enter the contact's phone number or type [*] to view all: ")
        custnumread = custnumread.strip()
        if custnumread == "*":
            select_cursor = db.cursor()
            for row in select_cursor.execute("SELECT * FROM contacts"):
                rowname, rowphone, rowemail = row
                table.add_row([rowname, rowphone, rowemail])
 
            print(table)

        else:
            select_cursor = db.cursor()
            
            db_info = select_cursor.execute("SELECT * FROM contacts WHERE phone = ?", [custnumread]).fetchall()
            if db_info is None:
                
                print("That phone number does not appear to be in the contacts list. If you would like to add them, please type [add].")
                customerchoice()
            else:
                for name, phone, email in db_info:
                        table.add_row([name, phone, email])
            print(table)
        
    if inputtype == "email":
            custemailread = input("To read a contact's info please enter the contact's email or type [*] to view all: ")
            custemailread = custemailread.lower().strip()
            if custemailread == "*":
                select_cursor = db.cursor()
                for row in select_cursor.execute("SELECT * FROM contacts"):
                    rowname, rowphone, rowemail = row
                    table.add_row([rowname, rowphone, rowemail])
 
                print(table)

            else:
                select_cursor = db.cursor()
                db_info = select_cursor.execute("SELECT * FROM contacts WHERE email = ?", [custemailread]).fetchall()
                
                if db_info is None:
                    print("That email does not appear to be in the contacts list. If you would like to add them, please type [add].")
                    customerchoice() 

                else:
                    for name, phone, email in db_info:
                        table.add_row([name, phone, email])
            print(table)     
    
   
    customerchoice()
        

def update():
    custnameupdate = input("To update a contact's info please enter the contact's name:")
    custnameupdate = custnameupdate.title()
    select_cursor = db.cursor()
    db_info = select_cursor.execute("SELECT * FROM contacts WHERE name = ?", [custnameupdate]).fetchone()
    if db_info is not None:
        currentname, currentphone, currentemail = db_info
        confirm = input(f"You wish to edit the contact called {currentname}, with a phone number of {currentphone} and an email of {currentemail}. Is this correct? Y/N: ")           
        confirm = confirm.upper()
        while confirm != "Y" and confirm != "N":
                confirm = input(f"Please enter [Y] to confirm update or [N] to decline update: ")
        if confirm == "Y":
            newname = input(f"Please enter a new name for {currentname} or leave blank to keep the current name: ")
            newphone = input(f"Please enter a new phone number for {currentname} or leave blank to keep the current number: ")
            newemail = input(f"Please enter a new email for {currentname} or leave blank to keep the current email: ")
            if newname == "":
                newname = currentname
            if newemail == "":
                newemail = currentemail
            if newphone == "":
                newphone = currentphone
            newname = newname.title()
            db.execute(f"UPDATE contacts SET name = '{newname}', phone = '{newphone}', email= '{newemail}' WHERE name = ?", [custnameupdate])
            print(f"Successfully updated contact! New contact info: Name: {newname}, Phone: {newphone}, Email: {newemail}.")
            db.commit()
            customerchoice()
        elif confirm == "N":
            print("Contact NOT updated.")
            customerchoice()
    else:
            print("That user does not appear to be in the database. If you would like to add them, please type [add].")
            customerchoice()

def delete():
    custnamedelete = input("To delete a contact's info please enter the contact's name or type [all] to delete all contacts: ")
    custnamedelete = custnamedelete.title().strip("[]")
    if custnamedelete == "All":
        confirmchoice = input("Are you SURE you wish to delete all contacts? Y/N: ")
        confirmchoice = confirmchoice.upper().strip(" []")
        while confirmchoice != "Y" and confirm != "N":
                confirmchoice = input(f"Please enter [Y] to confirm deletion or [N] to decline deletion: ")
                confirmchoice = confirmchoice.upper().strip("[] ")
        if confirmchoice == "Y":
            confirmchoice = input("Are you Absolutely CERTAIN you wish to delete all contacts? Y/N: ")
            confirmchoice = confirmchoice.upper().strip(" []")
            while confirmchoice != "Y" and confirm != "N":
                confirmchoice = input(f"Please enter [Y] to confirm deletion or [N] to decline deletion: ")
                confirmchoice = confirmchoice.upper().strip("[] ")
            if confirmchoice == "Y":
                vara = random.randrange(100)
                varb = random.randrange(100)
                answer = vara + varb
                sumcheck = int(input(f"To delete all contacts answer the following question: {vara} + {varb} = "))
                if answer == sumcheck:
                    select_cursor = db.cursor()
                    
                    for name in select_cursor.execute("SELECT name FROM contacts"): 
                        deletename = str(name)
                        deletename = deletename.strip("()',")
                        db.execute("DELETE FROM contacts WHERE name = ?", [deletename])
                        # Remove comment to make this stick! db.commit()

                    print("All contacts successfully deleted!")     
                    customerchoice()
                if answer != sumcheck:
                    print("Incorrect! Contacts are not deleted.")
                    customerchoice()
            if confirmchoice == "N":
                print("Contacts NOT Deleted.")
                customerchoice()
        if confirmchoice == "N":
            print("Contacts NOT Deleted.")
            customerchoice()
            db.execute(f"DELETE FROM contacts WHERE name = ?", [custnamedelete])
            print(f"Successfully deleted contact: {custnamedelete}.")
            db.commit()
            customerchoice()
        if confirmchoice == "N":
            print(f"Contact NOT deleted.")
            customerchoice()


    select_cursor = db.cursor()
    db_info = select_cursor.execute("SELECT * FROM contacts WHERE name = ?", [custnamedelete]).fetchone()
    if db_info is not None:
        currentname, currentphone, currentemail = db_info
        confirm = input(f"You wish to delete the contact called {currentname}, with a phone number of {currentphone} and an email of {currentemail}. Is this correct? Y/N: ")           
        confirm = confirm.upper().strip("[] ")
        while confirm != "Y" and confirm != "N":
                confirm = input(f"Please enter [Y] to confirm deletion or [N] to decline deletion: ")
                confirm = confirm.upper().strip("[] ")
        if confirm == "Y":
            db.execute(f"DELETE FROM contacts WHERE name = ?", [custnamedelete])
            print(f"Successfully deleted contact: {custnamedelete}.")
            db.commit()
            customerchoice()
        if confirm == "N":
            print(f"Contact NOT deleted.")
            customerchoice()


def customerchoice():
    userchoice = 0

    while userchoice != "update" and userchoice != "add" and userchoice != "read" and userchoice != "delete" and userchoice != "quit":
        userchoice = input("Type [update] to update a contact's info, [read] to read contact's info, [add] to add a new contact, [delete] to delete a contact from the database or [quit] to quit: ")
        userchoice = userchoice.lower().strip("[]")
    if userchoice == "update":
        update()
    elif userchoice == "add":
        add()
    elif userchoice == "read":
        read()
    elif userchoice == "delete":
        delete()
    elif userchoice == "quit":
        print("Thanks for accessing the database! Bye!")
        select_cursor.close()
        db.close()
        quit()
    else:
        "Invalid choice! Please type [update] to update contact info, [read] to read contact info, [add] to add a new contact, [delete] to delete a contact from the database or [quit] to quit: "

print("Welcome to the contacts database!")

while True:
    customerchoice()

