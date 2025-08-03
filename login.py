import sys
import os
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QDialogButtonBox,
    QLineEdit, QLabel, QWidget
)
from PyQt6.QtGui import QMovie
from PyQt6 import uic
otp = ''.join(random.choice('0123456789qwertyuiopasdfghjkxcvbnm!@#$%^&*()') for _ in range(6))
usernamelist = []  
passlist = []      
namelist = []      

daylist = []
monthlist = []
yearlist = []

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("hoahocvui.ui", self)  
        global username
        global password



        self.signin.clicked.connect(self.signinfunc)
        self.signup.clicked.connect(self.open_signup)
    def signinfunc(self):
        self.username = self.usrn.text()
        password = self.passw.text()
        
        if not self.username or not password:
            self.show_message("Login Error", "Vui lòng nhập đầy đủ thông tin", QMessageBox.Icon.Warning)
        elif self.username in usernamelist and password in passlist and usernamelist.index(self.username) == passlist.index(password):
            self.show_message("Nhập mã OTP", "Vui lòng nhập mã OTP", QMessageBox.Icon.Information)
            self.send_OTP()
            self.show_otp_input()
        else:
            self.show_message("Login Error", "Sai mật khẩu!", QMessageBox.Icon.Warning)
    
    def send_OTP(self):
        email = "noreplytenkiyohou@gmail.com"
        passw = "nedr jnfa vnyt qpym" 
        recipient_email = self.username

        try:
            session = smtplib.SMTP("smtp.gmail.com", 587)
            session.starttls()
            session.login(email, passw)
            mail_content = f"Mã OTP của bạn: {otp}"
            message = MIMEMultipart()
            message["Subject"] = "Mã OTP để đăng nhập"
            message["From"] = email
            message["To"] = recipient_email
            message.attach(MIMEText(mail_content, "plain"))
            session.sendmail(email, recipient_email, message.as_string())
            print("Mail sent successfully")
        except Exception as e:
            print(f"Failed to send email. Error: {e}")
            print(otp)
        finally:
            session.quit()
    
    def show_otp_input(self):
        self.setWindowTitle("Nhập mã OTP")
        self.setGeometry(100, 100, 400, 200)
        
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        
        label = QLabel("Nhập mã OTP", main_widget)
        label.setGeometry(20, 20, 200, 30)
        
        self.otp_input = QLineEdit(main_widget)
        self.otp_input.setGeometry(20, 60, 200, 30)
        
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, main_widget)
        button_box.setGeometry(20, 100, 200, 30)
        button_box.accepted.connect(self.verify_otp)
        button_box.rejected.connect(self.close)
    
    def verify_otp(self):
        user_otp = self.otp_input.text()
        if user_otp == otp:
            self.show_message("Thành công", "Đăng nhập thành công", QMessageBox.Icon.Information)
            r_main.show()
        else:
            self.show_message("Thất bại", "Sai mã OTP!", QMessageBox.Icon.Warning)

    def open_signup(self):
        self.signup_window = register()

        self.signup_window.show()

    def show_message(self, title, message, icon):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setIcon(icon)
        msgBox.exec()
class register(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(rf"C:\Users\{os.getlogin()}\Downloads\天気予報\サインアップ.ui", self)
        self.spin_day.setRange(1, 31)
        self.spin_month.setRange(1, 12)
        self.spin_year.setRange(1900, 2024)
        self.PB_create.clicked.connect(self.check_signup)
        self.PB_Return.clicked.connect(self.show_gd_login)
    
    def show_gd_login(self):
        r_login.show()
        self.close()
    
    def check_signup(self):
        emailsignup = self.line_emailsignup.text()
        passsignup = self.line_passsignup.text()
        name = self.line_name.text()
        day = self.spin_day.value()
        month = self.spin_month.value()
        year = self.spin_year.value()

        if not emailsignup or not passsignup or not name:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("SignUp Error")
            msgBox.setText("Please enter all required information!")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.exec()
        else:
            if ((day > 30 and month in [4, 6, 9, 11]) or (day > 28 and month == 2) or (day > 29 and month == 2 and year % 4 == 0)):
                msgBox = QMessageBox()
                msgBox.setWindowTitle("SignUp Error")
                msgBox.setText("Invalid date input!")
                msgBox.setIcon(QMessageBox.Icon.Warning)
                msgBox.exec()
            else:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Successfully Signed Up")
                msgBox.setText("Account created successfully!")
                usernamelist.append(emailsignup)
                passlist.append(passsignup)
                daylist.append(day)
                monthlist.append(month)
                yearlist.append(year)
                namelist.append(name)
                msgBox.setIcon(QMessageBox.Icon.Information)
                msgBox.exec()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

app = QApplication(sys.argv)
r_login = LoginWindow()
r_main = MainWindow()

r_login.show()
sys.exit(app.exec())

