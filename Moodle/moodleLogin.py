from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import getpass

username = input("Enter your Moodle username\n")
password = getpass.getpass("Enter your Moodle password(You won't be able to see the password as you are typing)\n")

PATH = "chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://moodle.iitd.ac.in/login/index.php")

user_box = driver.find_element_by_id("username")
pass_box = driver.find_element_by_id("password")
loginButton = driver.find_element_by_id("loginbtn")
captchaBox = driver.find_element_by_id("valuepkg3")
login = driver.find_element_by_id("login")

user_box.clear()
pass_box.clear()
captchaBox.clear()

user_box.send_keys(username)
pass_box.send_keys(password)

text = login.text
textArray = re.split(' |\n',text)
index = textArray.index("Please") + 1


answer = 0

if textArray[index] == "add":
    num1 = int(textArray[index+1])
    num2 = int(textArray[index+3])
    answer = num1+num2
elif textArray[index] == "subtract":
    num1 = int(textArray[index+1])
    num2 = int(textArray[index+3])
    answer = num1-num2 
elif textArray[index] == "enter":
    if textArray[index+1] == "first":
        answer = int(textArray[index+3])
    else:
        answer = int(textArray[index+5])
else:
    print("Something went wrong")

captchaBox.send_keys(answer)
loginButton.click()