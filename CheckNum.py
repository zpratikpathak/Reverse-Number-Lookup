# a program which uses selenium to open chrome and save all data of chrome in a folder name "ChromeData"
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pathlib
import shutil




# create a folder name "ChromeData" in current directory
os.makedirs("ChromeData", exist_ok=True)
scriptDirectory = pathlib.Path().absolute()

def login():
    # create a chrome options object
    chrome_options = Options()

    # add argument to chrome options object to save data in "ChromeData" folder
    # chrome_options.add_argument('--user-data-dir=ChromeData')


    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--window-size=1200,800")
    chrome_options.add_argument(f"user-data-dir={scriptDirectory}\\ChromeData")

    # create a chrome driver object

    driver = webdriver.Chrome(options=chrome_options)
    # driver.maximize_window()
    driver.get("https://web.whatsapp.com/")
    time.sleep(20)

    # create a file name "login.txt" in current directory
    # and write "loged In" in it
    # this file will be used to check if user is logged in or not
    with open("login.txt", "w") as file:
        file.write("loged In")

def findName(num="", number=""):
    # create a chrome options object
    if num != "":
        chrome_options = Options()

        # add argument to chrome options object to save data in "ChromeData" folder
        # chrome_options.add_argument('--user-data-dir=ChromeData')


        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--window-size=1200,800")
        chrome_options.add_argument(f"user-data-dir={scriptDirectory}\\ChromeData")

        # make chrome headless
        # chrome_options.add_argument("--headless")

        # create a chrome driver object
        driver = webdriver.Chrome(options=chrome_options)
        # driver.maximize_window()
        # driver.get("https://web.whatsapp.com/")
        # time.sleep(20)

        # open a new tab
        # driver.find_element("tag",'body').send_keys(Keys.CONTROL + 't') 
        driver.get("https://wa.me/+91"+num)
        

        try:
            # find element by xpath
            driver.find_element("xpath",'//*[@id="action-button"]/span').click()
            time.sleep(2)
            name = driver.find_element("xpath",'//*[@id="fallback_block"]/div/div/h4[2]/a/span').click()

            sendMsgBox = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'
            # wait until sendMsgBox is visible
            wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, sendMsgBox)))

            driver.find_element("xpath",'//*[@id="main"]/header/div[2]/div[1]/div').click()
            time.sleep(2)

            
            # time.sleep(400)
            # print name
            print(name.text)
            # close chrome
            driver.close()
            return name.text
        except Exception as e:
            print(e)
            # print("Number not found")

        # close chrome
        driver.close()

    elif number != "":
        # open file "numbers.txt" in read mode
        with open(number, "r") as file:
            # read all lines from file "numbers.txt" and store it in a list
            numbers = file.readlines()

        # create a chrome options object
        chrome_options = Options()

        # add argument to chrome options object to save data in "ChromeData" folder
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--window-size=1200,800")
        chrome_options.add_argument(f"user-data-dir={scriptDirectory}\\ChromeData")

        # make chrome headless
        # chrome_options.add_argument("--headless")

        # create a chrome driver object
        driver = webdriver.Chrome(options=chrome_options)

        for num in numbers:
            driver.get("https://wa.me/+91"+num)

            try:
                # find element by xpath
                # wait until sendMsgBox is visible
                sendMsgBox = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'
                wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, sendMsgBox)))

                driver.find_element("xpath",'//*[@id="action-button"]/span')
                time.sleep(2)
                name = driver.find_element("xpath",'//*[@id="fallback_block"]/div/div/h4[2]/a/span')
                # print(name.text)

                # write number and name in names.txt file
                with open("names.txt", "a") as file:
                    file.write(num.strip("\n") + "," + name.text + "\n")
            except Exception as e:
                # if number is not found then write number and "Not Found" in names.txt file
                with open("error.txt", "a") as file:
                    file.write(num.strip("\n") + "," + "Not Found" + "," + "Error: "+ str(e) +"\n")
                # print("Number not found")

        # close chrome
        driver.close()

def clearBrowserData():
    # remove the folder "ChromeData" and all its content from current directory for both windows and linux
    shutil.rmtree("ChromeData", ignore_errors=True)

    # remove the file "login.txt" from current directory
    os.remove("login.txt")

    # restart the program
    os.system("python CheckNum.py")


# print(findName("8286978547"))

if __name__ == "__main__":
    # check if file "login.txt" is present in current directory or not
    if os.path.isfile("login.txt") != True:
        # if file "login.txt" is not present in current directory
        # then call login function
        print("You are not logged in")
        print("Please scan QR code to login")
        login()

    # create a terminal menu in a loop unless user select exit option
    while True:
        print("1. Check Number")
        print("2. Check Number in Bulk")
        print("3. Reset Tool")
        print("4. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            num = input("Enter number: ")
            print(findName(num))
        if choice == 2:
            # check if file "numbers.txt" is present in current directory or not
            if os.path.isfile("numbers.txt") != True:
                # if file "numbers.txt" is not present in current directory
                # then create a file "numbers.txt" in current directory
                # and write "Enter numbers line by line" in it
                print("File numbers.txt not found")
                print("Please create a file numbers.txt in current directory and enter numbers line by line")
                with open("numbers.txt", "w") as file:
                    file.write("Enter numbers line by line")
                continue
            # open file "numbers.txt" in read mode
            findName(number="numbers.txt")
        elif choice == 3:
            clearBrowserData()
        elif choice == 4:
            break
        else:
            print("Invalid choice")
        print()



