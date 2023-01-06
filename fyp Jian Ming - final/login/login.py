
#from email.mime import image
import time
import pyotp
#import qrcode

import os

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

import os

key = "6XJRENXUZHIJK66WJ4CM2R4UV6RV6XH5"
#key = pyotp.random_base32()
#print(key)
#use above code to generate key

uri = pyotp.totp.TOTP(key).provisioning_uri(
    name='User',
    issuer_name='File Protection for University (FPU)')
#to genarate OTP

#qrcode.make(uri).save("qr.png")
#use above code to generate QR

totp = pyotp.TOTP(key)

def btn_clicked():
    OTP = entry0.get()
    status = (totp.verify(OTP)) 
    #print(status)
    if status == True:
        root.withdraw()
        import fyp_self
        #if OTP is correct, goes to main GUI
    
    else:
        messagebox.showerror("Error","Invalid OTP.")
        entry0.delete(0,END)
        return

    #ammeded key to OTP
root = Tk()

root.title('FPU Login')
root.geometry("313x276")
root.configure(bg = "#ffffff")
canvas = Canvas(
    root,
    bg = "#ffffff",
    height = 276,
    width = 313,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"login/background_login.png")
background = canvas.create_image(
    156.5, 138.0,
    image=background_img)

entry0_img = PhotoImage(file = f"login/img_textBox_login.png")
entry0_bg = canvas.create_image(
    119.5, 236.0,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

entry0.place(
    x = 71, y = 228,
    width = 97,
    height = 14)

img0 = PhotoImage(file = f"login/img_login.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 185, y = 227,
    width = 58,
    height = 17)

root.resizable(False, False)
root.mainloop()

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