

#File Protection for University
#Final Year Project Developed by Chai Jian Ming TP054898

#---------------------------------------------------------------------------------------------------------------------
#Importing Libraries.
#---------------------------------------------------------------------------------------------------------------------
#tkinter for building GUI.
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

#Pycryptodome for Encrypting algorithms.
from Crypto.Cipher import AES
from Crypto.Cipher import DES3
from Crypto.Cipher import DES

#Pycryptodome utilities for enhanced key security and padding.
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

#for interacting with Operating System.
import os

#for interacting with Web Browser.
import webbrowser

#---------------------------------------------------------------------------------------------------------------------
#Variable Initialization.
#---------------------------------------------------------------------------------------------------------------------
#Global variable to hold the selected file path.
temp_filename = ''

#Global variable for salt in bytes, used to strengthen password.
salt = b'\x12\x9d\xc7\x1b\xf8Z\x80&\xc1\xe2\xa77\x13.\x90\x0eS\xeb3\xe6\x13J\xe4\xce\xeeO-\x154\x98'
#Salt is hardcoded, use lines below to generate salt.
#from Crypto.Random import get_random_bytes
#print(get_random_bytes(32))

#For choice of algorithm.
clicked = StringVar()
#Preset the recommended algorithm.

clicked.set("AES EAX mode (Recommended)")

window1 = Tk()
window1.withdraw()
window = Toplevel()
window_menu = Menu(window)
window.config(menu = window_menu)

#settings for window name, size and colour.
window.title('File Protection for University (FPU) v4.0')
window.geometry("616x427")
window.configure(bg = "#ffffff")

#---------------------------------------------------------------------------------------------------------------------
#For the Top Menu.
#---------------------------------------------------------------------------------------------------------------------
#To display intructions for the program when function is called.
def help_clicked():
    messagebox.showinfo("Instructions",
    " 1. Select a file with Browse. \n 2. Enter a Key. \n 3. Select Algorithm. \n 4. Select to Encrypt or Decrypt.")

#To display more info about the program when function is called.
def about_clicked():
    messagebox.showinfo("About", 
    "File Protection for University (FPU) is a file encryption program based on the AES, 3DES and DES algorithms, developed by Chai Jian Ming TP054898.")

#To direct user to a contact page in the web browser when function is called.
def contact_clicked():
    webbrowser.open("https://www.apu.edu.my/explore-apu/contact-us")

#Help Menu. Contains Intructions and Quit.
help_menu = Menu(window_menu)
window_menu.add_cascade(label = "Help", menu = help_menu)
help_menu.add_command(label = "Instructions", command = help_clicked,)
help_menu.add_separator()
#Quits program.
help_menu.add_command(label = "Quit", command = window.quit)

#About Menu. Contains About and Direct link.
about_menu = Menu(window_menu)
window_menu.add_cascade(label = "About", menu = about_menu)
about_menu.add_command(label = "FPU", command = about_clicked,)
about_menu.add_separator()
about_menu.add_command(label = "Contact Us", command = contact_clicked)

#---------------------------------------------------------------------------------------------------------------------
#Function for browsing and selecting file path.
#---------------------------------------------------------------------------------------------------------------------
def browse_file():

    #To get file path.
    window.filename = filedialog.askopenfilename(initialdir="/", title="", filetypes=[("all files", "*.*")])
    
    #Storing file path to global.
    global temp_filename
    temp_filename = window.filename
    
    #Create a text box to display file path.
    label = Label(
                window,
                text = window.filename,
                bd = 0,
                bg = "#d9d9d9",
                highlightthickness = 0,)
    
    label.place(
            x = 145, y = 211,
            width = 319,
            height = 19)


#---------------------------------------------------------------------------------------------------------------------
#Function for Encryption.
#---------------------------------------------------------------------------------------------------------------------
def encrypt_clicked():

    #Get file path from global.
    global temp_filename

    #Get the hardcoded Salt from global.
    global salt
    salt = salt

    #Get the algorithm selected.
    choice = clicked.get()

    #AES EAX mode.
    if choice == "AES EAX mode (Recommended)":

        #Error for empty file path.
        if temp_filename == '':

            messagebox.showerror("Error","No file selected.")
            return

        else:

            #Get password from user.
            password = entry0.get()

            #Strengthen user password with Salt and turning it into 16 Bytes, which is 128 bits.
            key = PBKDF2(password, salt, dkLen=16) 
            
            #Create a cipher with the key, using EAX mode, and generating a nonce (number used once).
            cipher = AES.new(key, AES.MODE_EAX)

            #Read the original file and get data.
            with open(temp_filename,'rb') as f:

                read_data = f.read()

            #Encrypting the data and generate tag.
            output_data, tag = cipher.encrypt_and_digest(read_data)

            #Extracting the file format.
            file_name, file_extension = os.path.splitext(temp_filename)

            #Writing the nonce, tag and the encrypted data into a new file.
            with open(file_name + "_AES_EAX" + file_extension, "wb") as f:

                f.write(cipher.nonce)
                f.write(tag)
                f.write(output_data)
                messagebox.showinfo("Encryption Completed",temp_filename + " has been Encrypted.")

            #Clear input and cipher.
            entry0.delete(0,END)
            del cipher
    
    #AES CBC mode.
    elif choice == "AES CBC mode": #ammended elif, on decrypt also

        if temp_filename == '':

            messagebox.showerror("Error","No file selected.")
            return

        else:

            password = entry0.get()

            key = PBKDF2(password, salt, dkLen=16) 

            with open(temp_filename,'rb') as f:

                read_data = f.read()
            
            #Padding the data.
            read_data = pad(read_data, AES.block_size)

            #Create cipher with CBC mode, also generates IV (Initializing Vector).
            cipher = AES.new(key, AES.MODE_CBC)

            output_data = cipher.encrypt(read_data)

            file_name, file_extension = os.path.splitext(temp_filename)

            with open(file_name + "_AES_CBC" + file_extension, "wb") as f:

                f.write(cipher.iv)
                f.write(output_data)
                messagebox.showinfo("Encryption Completed",temp_filename + " has been Encrypted.")

            entry0.delete(0,END)
            del cipher

    #3DES mode.
    elif choice == "3DES":

        if temp_filename == '':

            messagebox.showerror("Error","No file selected.")
            return

        else:

            password = entry0.get()

            key = PBKDF2(password, salt, dkLen=16)

            #Generate a key for 3DES, also 16 Bytes.
            key_3DES = DES3.adjust_key_parity(key)

            cipher = DES3.new(key_3DES, DES3.MODE_EAX)

            with open(temp_filename,'rb') as f:

                read_data = f.read()

            output_data, tag = cipher.encrypt_and_digest(read_data)

            file_name, file_extension = os.path.splitext(temp_filename)

            with open(file_name + "_3DES" + file_extension, "wb") as f:

                f.write(cipher.nonce)
                f.write(tag)
                f.write(output_data)
                messagebox.showinfo("Encryption Completed",temp_filename + " has been Encrypted.")

            entry0.delete(0,END)
            del cipher

    #DES mode.
    elif choice == "DES":

        if temp_filename == '':

            messagebox.showerror("Error","No file selected.")
            return

        else:

            password = entry0.get()

            #DES key is in 8 bytes, which is 64 bits.
            key = PBKDF2(password, salt, dkLen=8) 

            cipher = DES.new(key, DES.MODE_EAX)

            with open(temp_filename,'rb') as f:
                read_data = f.read()

            output_data, tag = cipher.encrypt_and_digest(read_data)

            file_name, file_extension = os.path.splitext(temp_filename)

            with open(file_name + "_DES" + file_extension, "wb") as f:

                f.write(cipher.nonce)
                f.write(tag)
                f.write(output_data)
                messagebox.showinfo("Encryption Completed",temp_filename + " has been Encrypted.")

            entry0.delete(0,END)
            del cipher


#---------------------------------------------------------------------------------------------------------------------
#Function for Decryption.
#---------------------------------------------------------------------------------------------------------------------
def decrypt_clicked():

    global temp_filename

    #Get file format form file path.
    file_name, file_extension = os.path.splitext(temp_filename)

    global salt
    salt = salt

    choice = clicked.get()

    #AES EAX mode.
    if choice == "AES EAX mode (Recommended)":

        #Read the selected file.
        with open(temp_filename,'rb') as f:

            #Read first 16 bytes for nonce.
            nonce = f.read(16)

            #Read next 16 bytes for tag.
            tag = f.read(16)

            #Read the rest for encrypted data.
            read_data = f.read()

        if temp_filename == '':

            messagebox.showerror("Error","No file selected.")
            return

        else:

            password = entry0.get()

            key = PBKDF2(password, salt, dkLen=16)

            try:

                cipher = AES.new(key, AES.MODE_EAX, nonce)

                #Decrypt the data and compare the tag for verification.
                output_data = cipher.decrypt_and_verify(read_data,tag)

            #Error message for uncessful decryption and verification.
            except ValueError:

                messagebox.showerror("Error","Invalid File Format or Incorrect Key!")
                return

            #Write the decrypted data into a new file.
            with open(file_name + file_extension, 'wb') as f:

                f.write(output_data)
                messagebox.showinfo("Decryption Completed",temp_filename + " has been Decrypted.")

            entry0.delete(0,END)   
            del cipher

    #AES CBC mode.
    elif choice == "AES CBC mode":

        with open(temp_filename,'rb') as f:

            #Read first 16 bytes for IV.
            iv = f.read(16)
            read_data = f.read()

        if temp_filename == '':

            messagebox.showerror("Error","No file selected.")
            return

        else:

            password = entry0.get()

            key = PBKDF2(password, salt, dkLen=16)

            try:

                cipher = AES.new(key, AES.MODE_CBC, iv)
                output_data = cipher.decrypt(read_data)

                #Unpadding the decrypted data.
                output_data = unpad(output_data, AES.block_size)

            except ValueError:

                messagebox.showerror("Error","Invalid File Format or Incorrect Key!")
                return

            with open(file_name + file_extension, 'wb') as f:

                f.write(output_data)
                messagebox.showinfo("Decryption Completed",temp_filename + " has been Decrypted.")

            entry0.delete(0,END)   
            del cipher

    #3DES mode.
    elif choice == "3DES":

        with open(temp_filename,'rb') as f:

            nonce = f.read(16)
            tag = f.read(8)
            read_data = f.read()

        if temp_filename == '':

            messagebox.showerror("Error","No file selected.")
            return

        else:

            password = entry0.get()

            key = PBKDF2(password, salt, dkLen=16)

            key_3DES = DES3.adjust_key_parity(key)

            try:

                cipher = DES3.new(key_3DES, DES3.MODE_EAX, nonce)

                output_data = cipher.decrypt_and_verify(read_data, tag)

            except ValueError:

                messagebox.showerror("Error","Invalid File Format or Incorrect Key!")
                return

            with open(file_name + file_extension, 'wb') as f:

                f.write(output_data)
                messagebox.showinfo("Decryption Completed",temp_filename + " has been Decrypted.")

            entry0.delete(0,END)   
            del cipher

    #DES mode.
    elif choice == "DES":

        with open(temp_filename,'rb') as f:

            nonce = f.read(16)
            tag = f.read(8)
            read_data = f.read()

        if temp_filename == '':

            messagebox.showerror("Error","No file selected.")
            return

        else:

            password = entry0.get()

            key = PBKDF2(password, salt, dkLen=8)

            try:

                cipher = DES.new(key, DES.MODE_EAX, nonce)
                output_data = cipher.decrypt_and_verify(read_data,tag)

            except ValueError:

                messagebox.showerror("Error","Invalid File Format or Incorrect Key!")
                return

            with open(file_name + file_extension, 'wb') as f:
                f.write(output_data)
                messagebox.showinfo("Decryption Completed",temp_filename + " has been Decrypted.")

            entry0.delete(0,END)   
            del cipher


#Clear Button.
def clear_clicked():
    entry0.delete(0,END)
    return


#---------------------------------------------------------------------------------------------------------------------
#GUI Design.
#---------------------------------------------------------------------------------------------------------------------

canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 427,
    width = 616,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

#Importing background from file.
background_img = PhotoImage(file = f"main/background.png")
background = canvas.create_image(
    275.0, 211.5,
    image=background_img)

img0 = PhotoImage(file = f"main/img0.png")

#Button for Browse Function.
b0 = Button(
    window,
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = browse_file,
    relief = "flat")

b0.place(
    x = 483, y = 211,
    width = 69,
    height = 21)

#Button for Encrypt Function.
img1 = PhotoImage(file = f"main/img1.png")
b1 = Button(
    window,
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = encrypt_clicked,
    relief = "flat")

b1.place(
    x = 145, y = 352,
    width = 69,
    height = 21)

#Button for Decrypt Function.
img2 = PhotoImage(file = f"main/img2.png")
b2 = Button(
    window,
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = decrypt_clicked,
    relief = "flat")

b2.place(
    x = 395, y = 352,
    width = 69,
    height = 21)

#Button for Clear Function.
img3 = PhotoImage(file = f"main/img3.png")
b3 = Button(
    window,
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = clear_clicked,
    relief = "flat")

b3.place(
    x = 270, y = 352,
    width = 69,
    height = 21)

#Input field for Password.
entry0_img = PhotoImage(file = f"main/img_textBox0.png")
entry0_bg = canvas.create_image(
    304.5, 270.5,
    image = entry0_img)

entry0 = Entry(
    window,
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0,
    #show = "*", #Uncomment to mask password.
    )

entry0.place(
    x = 145, y = 260,
    width = 319,
    height = 19)

#Dropdown meny for selecting algorithm.
entry1 = OptionMenu(
    window,
    clicked, #variable
    "AES EAX mode (Recommended)",
    "AES CBC mode",
    "3DES",
    "DES",
    )

entry1.place(
    x = 145, y = 310,
    width = 319,
    height = 19)

#For Displaying the selected File path.
entry2_img = PhotoImage(file = f"main/img_textBox2.png")
entry2_bg = canvas.create_image(
    304.5, 221.5,
    image = entry2_img)

#Fixed sized window.
window.resizable(False, False)

window.mainloop()
#---------------------------------------------------------------------------------------------------------------------
#Intructions.
#---------------------------------------------------------------------------------------------------------------------
#1. Select a file with Browse. 
#2. Enter a Key. 
#3. Select Algorithm. 
#4. Select to Encrypt or Decrypt.
#---------------------------------------------------------------------------------------------------------------------
