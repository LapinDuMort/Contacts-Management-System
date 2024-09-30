import sqlite3, random
from prettytable import PrettyTable

db = sqlite3.connect("contacts.sqlite")
#Creates table after connecting to db, we are using str for phone numbers to prevent the table dropping 0's at the cost of allowing users to add non-numeric numbers
db.execute("CREATE TABLE IF NOT EXISTS contacts(name TEXT phone TEXT email TEXT)")

select_cursor = db.cursor()


def add():
    #Add new contact functionality, taking in Name, Phone and Email.
    addname = input("Please enter a new name: ")
    addnumber = input("Please enter a new phone number: ")
    addemail = input("Please enter a new email address: ")

    #Formats name with a capital letter, makes emails lowercase and strips whitespace, stores numbers as strings but removes some common characters.
    addname = addname.title()
    addemail = addemail.lower().strip()
    addnumber = addnumber.strip(" abcdefghijklmnopqrstuvwxyz+()[]ABCDEFGHIJKLMNOPQRSTUVWXYZ") #partial accounting for non-numeric values
    
    #confirmation option accepting Y/N options to add a contact to the database
    confirm = input(f"You wish to add a contact called {addname}, with a phone number of {addnumber} and an email of {addemail}. Is this correct? Y/N: ")
    confirm = confirm.upper()
    
    while confirm != "Y" and confirm != "N":
        confirm = input(f"Please enter Y to confirm addition or N to decline addition: ")
        confirm = confirm.upper()
    
    if confirm == "Y":
        db.execute(f"INSERT INTO contacts(name, phone, email) Values('{addname}', '{addnumber}','{addemail}')")
        print("Successfully added contact!")
        db.commit()
        customerchoice()
    
    elif confirm == "N":
        print("Contact NOT added to database.")
        customerchoice()


def read():
    #Read functionality using PrettyTable for a nicer output
    table = PrettyTable()
    table.field_names = ["Name", "Phone", "Email"]

    #Accepts either searches by Name, Phone or Email, or displays all with *
    inputtype = input("Would you like to search for a contact by [name], [phone] or [email]? Alternatively you can type [*] to view all saved contacts: ")
    inputtype = inputtype.lower().strip("[]")
    
    #Only accepts Name, Phone, Email, Quit or *
    while inputtype != "name" and inputtype != "phone" and inputtype != "email" and inputtype!= "quit" and inputtype!= "*":
        inputtype = input("Please either type [name] to search by name, [phone] to search by phone, [email] to search by email, [*] to view all contacts or [quit] to return to menu: ")
        inputtype = inputtype.lower().strip("[]")

    #Quit returns to original choice
    if inputtype == "quit":
        customerchoice()

    #* here or under the other options returns the entire database
    if inputtype == "*":
            select_cursor = db.cursor()
            for row in select_cursor.execute("SELECT * FROM contacts"):
                rowname, rowphone, rowemail = row
                table.add_row([rowname, rowphone, rowemail])
 
            print(table)

    #reads the name input to return any contacts with that exact name from the database
    if inputtype == "name":
        custnameread = input("To read contact's info please enter the contact's name or type [*] to view all: ")
        custnameread = custnameread.title().strip()

    #Returns all results in database with *    
        if custnameread == "*":
            select_cursor = db.cursor()
            for row in select_cursor.execute("SELECT * FROM contacts"):
                rowname, rowphone, rowemail = row
                table.add_row([rowname, rowphone, rowemail])
 
            print(table)

    #Returns all results with that name from database, or an error message returning to the first menu if they do not exist.
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

    #if input is "phone" returns all contacts exactly matching that phone number or all contacts if * is selected or returns to menu if contact is not in the database
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
        
    #allows selection by email, returning all details that fully match the given email, all contacts on input of * or returns to menu if contact is not in the database
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

    #Allows the user to delete all contacts listed under a name, phone number, email or just delete all contacts. Comment out db.commit while testing
    inputtype = input("Would you like to update a contact by [name], [phone] or [email]? Alternatively you can type [quit] to return to the main menu: ")
    inputtype = inputtype.lower().strip("[]")

    #Only accepts name, phone, email or quit, otherwise will loop until one is entered
    while inputtype != "name" and inputtype != "phone" and inputtype != "email" and inputtype!= "quit":
        inputtype = input("Please either type [name] to update by name, [phone] to update by phone number, [email] to update by email, or [quit] to return to menu: ")
        inputtype = inputtype.lower().strip("[]")
    
    if inputtype == "quit": #Returns to main menu 
        customerchoice()
    
    elif inputtype == "name":
        custnameupdate = input("To update a contact's info please enter the contact's name: ")
        custnameupdate = custnameupdate.title()
        select_cursor = db.cursor()
        db_info = select_cursor.execute("SELECT rowid, * FROM contacts WHERE name = ?", [custnameupdate]).fetchone()
    
        if db_info is not None:

            rowid, currentname, currentphone, currentemail = db_info
            confirm = input(f"You wish to edit the contact called {currentname}, with a phone number of {currentphone} and an email of {currentemail}. Is this correct? Y/N: ")           
            confirm = confirm.upper()

            while confirm != "Y" and confirm != "N":
                confirm = input(f"Please enter [Y] to confirm update or [N] to decline update: ")
                confirm = confirm.upper()

            if confirm == "Y":
                newname = input(f"Please enter a new name for {currentname} or leave blank to keep the current name: ")
                newphone = input(f"Please enter a new phone number for {currentname} or leave blank to keep the current number: ")
                newemail = input(f"Please enter a new email for {currentname} or leave blank to keep the current email: ")

                if newname == "": #Allows the user to keep details the same by entering a blank input
                    newname = currentname
                if newemail == "":
                    newemail = currentemail
                if newphone == "":
                    newphone = currentphone

                newname = newname.title()
                newphone = newphone.strip(" abcdefghijklmnopqrstuvwxyz+()[]ABCDEFGHIJKLMNOPQRSTUVWXYZ") #partial accounting for non-numeric values
                newemail = newemail.lower()
                db.execute(f"UPDATE contacts SET name = '{newname}', phone = '{newphone}', email= '{newemail}' WHERE rowid = ?", [rowid])
                print(f"Successfully updated contact! New contact info: Name: {newname}, Phone: {newphone}, Email: {newemail}.")
                db.commit()
                customerchoice()

            elif confirm == "N":
                print("Contact NOT updated.")
                customerchoice()
            
        else:
            print("That user does not appear to be in the database. If you would like to add them, please type [add].")
            customerchoice()

    elif inputtype == "phone":
        custphoneupdate = input("To update a contact's info please enter the contact's phone number: ")
        custphoneupdate = custphoneupdate.title()
        select_cursor = db.cursor()
        db_info = select_cursor.execute("SELECT rowid, * FROM contacts WHERE phone = ?", [custphoneupdate]).fetchone()
    
        if db_info is not None:

            rowid, currentname, currentphone, currentemail = db_info
            confirm = input(f"You wish to edit the contact called {currentname}, with a phone number of {currentphone} and an email of {currentemail}. Is this correct? Y/N: ")           
            confirm = confirm.upper()

            while confirm != "Y" and confirm != "N":
                confirm = input(f"Please enter [Y] to confirm update or [N] to decline update: ")
                confirm = confirm.upper()

            if confirm == "Y":
                newname = input(f"Please enter a new name for {currentname} or leave blank to keep the current name: ")
                newphone = input(f"Please enter a new phone number for {currentname} or leave blank to keep the current number: ")
                newemail = input(f"Please enter a new email for {currentname} or leave blank to keep the current email: ")

                if newname == "": #Allows the user to keep details the same by entering a blank input
                    newname = currentname
                if newemail == "":
                    newemail = currentemail
                if newphone == "":
                    newphone = currentphone
                    
                newname = newname.title()
                newphone = newphone.strip(" abcdefghijklmnopqrstuvwxyz+()[]ABCDEFGHIJKLMNOPQRSTUVWXYZ") #partial accounting for non-numeric values
                newemail = newemail.lower()

                db.execute(f"UPDATE contacts SET name = '{newname}', phone = '{newphone}', email= '{newemail}' WHERE rowid = ?", [rowid])
                print(f"Successfully updated contact! New contact info: Name: {newname}, Phone: {newphone}, Email: {newemail}.")
                db.commit()
                customerchoice()

            elif confirm == "N":
                print("Contact NOT updated.")
                customerchoice()
        else:
            print("That number does not appear to be in the database. If you would like to add them, please type [add].")
            customerchoice()

    elif inputtype == "email":
        custemailupdate = input("To update a contact's info please enter the contact's email address: ")
        custemailupdate = custemailupdate.title()
        select_cursor = db.cursor()
        db_info = select_cursor.execute("SELECT rowid, * FROM contacts WHERE email = ?", [custemailupdate]).fetchone()
    
        if db_info is not None:

            rowid, currentname, currentphone, currentemail = db_info
            confirm = input(f"You wish to edit the contact called {currentname}, with a phone number of {currentphone} and an email of {currentemail}. Is this correct? Y/N: ")           
            confirm = confirm.upper()

            while confirm != "Y" and confirm != "N":
                confirm = input(f"Please enter [Y] to confirm update or [N] to decline update: ")
                confirm = confirm.upper()

            if confirm == "Y":
                newname = input(f"Please enter a new name for {currentname} or leave blank to keep the current name: ")
                newphone = input(f"Please enter a new phone number for {currentname} or leave blank to keep the current number: ")
                newemail = input(f"Please enter a new email for {currentname} or leave blank to keep the current email: ")

                if newname == "": #Allows the user to keep details the same by entering a blank input
                    newname = currentname
                if newemail == "":
                    newemail = currentemail
                if newphone == "":
                    newphone = currentphone
                    
                newname = newname.title()
                newphone = newphone.strip(" abcdefghijklmnopqrstuvwxyz+()[]ABCDEFGHIJKLMNOPQRSTUVWXYZ") #partial accounting for non-numeric values
                newemail = newemail.lower()
                
                db.execute(f"UPDATE contacts SET name = '{newname}', phone = '{newphone}', email= '{newemail}' WHERE rowid = ?", [rowid])
                print(f"Successfully updated contact! New contact info: Name: {newname}, Phone: {newphone}, Email: {newemail}.")
                db.commit()
                customerchoice()

            elif confirm == "N":
                print("Contact NOT updated.")
                customerchoice()
        else:
            print("That email address does not appear to be in the database. If you would like to add it, please type [add].")
            customerchoice()

def deleteall():
# Function allowing all contacts to be deleted at once, clearing the contacts log, which can be called on by the user in the delete menu
            confirmchoice = input("Are you SURE you wish to delete all contacts? Y/N: ")
            confirmchoice = confirmchoice.upper().strip(" []")
        
            while confirmchoice != "Y" and confirmchoice != "N":
                    confirmchoice = input(f"Please enter [Y] to confirm deletion or [N] to decline deletion: ")
                    confirmchoice = confirmchoice.upper().strip("[] ")
        
            if confirmchoice == "Y":
                confirmchoice = input("Are you Absolutely CERTAIN you wish to delete all contacts? Y/N: ")
                confirmchoice = confirmchoice.upper().strip(" []")
            
                while confirmchoice != "Y" and confirmchoice != "N":
                    confirmchoice = input(f"Please enter [Y] to confirm deletion or [N] to decline deletion: ")
                    confirmchoice = confirmchoice.upper().strip("[] ")
            
                if confirmchoice == "Y": # Silly addition forces user to solve a random sum to confirm deletion
                    vara = random.randrange(100)
                    varb = random.randrange(100)
                    answer = vara + varb
                    sumcheck = int(input(f"To delete all contacts answer the following question: {vara} + {varb} = "))
                
                    if answer == sumcheck:
                        select_cursor = db.cursor()
                     #As SQLITE3 does not have drop table functionality, this iterates through the database and deletes each instance row by row
                        for name in select_cursor.execute("SELECT name FROM contacts"): 
                            deletename = str(name)
                            deletename = deletename.strip("()',")
                            db.execute("DELETE FROM contacts WHERE name = ?", [deletename])
                            db.commit()

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

def delete():
#Allows the user to delete all contacts listed under a name, phone number, email or just delete all contacts. Comment out db.commit while testing
    inputtype = input("Would you like to delete a contact by [name], [phone] or [email]? Alternatively you can type [all] to delete all saved contacts: ")
    inputtype = inputtype.lower().strip("[]")
        
    #Only accepts Name, Phone, Email, Quit or All, otherwise will loop until one is entered
    while inputtype != "name" and inputtype != "phone" and inputtype != "email" and inputtype!= "quit" and inputtype!= "all":
        inputtype = input("Please either type [name] to search by name, [phone] to search by phone, [email] to search by email, [all] to delete all or [quit] to return to menu: ")
        inputtype = inputtype.lower().strip("[]")
    
    if inputtype == "quit": #Returns to main menu 
        customerchoice()
    
    elif inputtype == "all": #Runs delete all function from above
         deleteall()

    elif inputtype == "name": #Offers the choice to select by name or select all for deletion
    
        custnamedelete = input("To delete a contact's info please enter the contact's name or type [all] to delete all contacts: ")
        custnamedelete = custnamedelete.title().strip("[]")

        if custnamedelete == "All":
             deleteall()

        else:
            select_cursor = db.cursor()
            db_info = select_cursor.execute("SELECT rowid, * FROM contacts WHERE name = ?", [custnamedelete]).fetchone()
    
            if db_info is not None:
                rowid, currentname, currentphone, currentemail = db_info
                confirm = input(f"You wish to delete the contact called {currentname}, with an email of {currentemail} and a phone number of {currentphone}. Is this correct? Y/N: ")           
                confirm = confirm.upper().strip("[] ")
        
                while confirm != "Y" and confirm != "N":
                    confirm = input(f"Please enter [Y] to confirm deletion or [N] to decline deletion: ")
                    confirm = confirm.upper().strip("[] ")
            
                if confirm == "Y":
                    db.execute(f"DELETE FROM contacts WHERE rowid = ?", [rowid])
                    print(f"Successfully deleted contact: {custnamedelete}.")
                    db.commit()
                    customerchoice()
            
                if confirm == "N":
                    print(f"Contact NOT deleted.")
                    customerchoice()
            else:
                print("That user does not appear to be in the database. If you would like to add them, please type [add].")
                customerchoice()

    elif inputtype == "phone":
        
        custphonedelete = input("To delete a contact's info please enter the contact's phone number or type [all] to delete all contacts: ")
        custphonedelete = custphonedelete.strip("[]")

        if custphonedelete == "all" or custphonedelete == "All":
             deleteall()

        else:
            select_cursor = db.cursor()
            db_info = select_cursor.execute("SELECT rowid, * FROM contacts WHERE phone = ?", [custphonedelete]).fetchone()
    
            if db_info is not None:
                rowid, currentname, currentphone, currentemail = db_info
                confirm = input(f"You wish to delete the contact called {currentname}, with an email of {currentemail} and a phone number of {currentphone}. Is this correct? Y/N: ")           
                confirm = confirm.upper().strip("[] ")
        
                while confirm != "Y" and confirm != "N":
                    confirm = input(f"Please enter [Y] to confirm deletion or [N] to decline deletion: ")
                    confirm = confirm.upper().strip("[] ")
            
                if confirm == "Y":
                    db.execute(f"DELETE FROM contacts WHERE rowid = ?", [rowid])
                    print(f"Successfully deleted contacts with the number: {custphonedelete}.")
                    db.commit()
                    customerchoice()
            
                if confirm == "N":
                    print(f"Contact NOT deleted.")
                    customerchoice()
            else:
                print("That number does not appear to be in the database. If you would like to add them, please type [add].")
                customerchoice()

    elif inputtype == "email":
        
        custemaildelete = input("To delete a contact's info please enter the contact's email or type [all] to delete all contacts: ")
        custemaildelete = custemaildelete.lower().strip("[]")

        if custemaildelete == "all":
             deleteall()

        else:
            select_cursor = db.cursor()
            db_info = select_cursor.execute("SELECT rowid, * FROM contacts WHERE email = ?", [custemaildelete]).fetchone()
    
            if db_info is not None:
                rowid, currentname, currentphone, currentemail = db_info
                confirm = input(f"You wish to delete the contact called {currentname}, with an email of {currentemail} and a phone number of {currentphone}. Is this correct? Y/N: ")           
                confirm = confirm.upper().strip("[] ")
        
                while confirm != "Y" and confirm != "N":
                    confirm = input(f"Please enter [Y] to confirm deletion or [N] to decline deletion: ")
                    confirm = confirm.upper().strip("[] ")
            
                if confirm == "Y":
                    db.execute(f"DELETE FROM contacts WHERE rowid = ?", [rowid])
                    print(f"Successfully deleted contacts with the email: {custemaildelete}.")
                    db.commit()
                    customerchoice()
            
                if confirm == "N":
                    print(f"Contact NOT deleted.")
                    customerchoice()
            
            else:
                print("That email does not appear to be in the database. If you would like to add them, please type [add].")
                customerchoice()

def customerchoice(): #prevents previous user choice from causing the program to stick in one menu
    userchoice = 0

# Starter menu, customer is asked if they wish to update a contact, read contacts, add a new contact, delete contacts or quit the program. 

    while userchoice != "update" and userchoice != "add" and userchoice != "read" and userchoice != "delete" and userchoice != "quit":
        userchoice = input("Type [update] to update a contact's info, [read] to read contact's info, [add] to add a new contact, [delete] to delete a contact from the database or [quit] to quit: ")
        userchoice = userchoice.lower().strip("[]")
    
    if userchoice == "update": #runs update function
        update()
    
    elif userchoice == "add": #runs add user function
        add()
    
    elif userchoice == "read": #runs read database function
        read()
    
    elif userchoice == "delete": #runs delete contact function
        delete()
    
    elif userchoice == "quit": #quits the database and closes the instances of cursor and db
        print("Thanks for accessing the database! Bye!")
        select_cursor.close()
        db.close()
        quit()
    
    else:
        "Invalid choice! Please type [update] to update contact info, [read] to read contact info, [add] to add a new contact, [delete] to delete a contact from the database or [quit] to quit: "

print("Welcome to the contacts database!")
#Running the program gives this text and then starts the program by opening the function customerchoice() which is designed to run until user inputs quit
while True:
    customerchoice()

