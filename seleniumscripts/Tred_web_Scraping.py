import time
from selenium import webdriver
from openpyxl import Workbook
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

#Here,ChromeDriverManager has been used to take care of the driver automatically and it will return as the driver
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()  #start the application

#Open the applications
driver.get(
    "https://www.tred.com/buy?body_style=&distance=50&exterior_color_id=&make=&miles_max=100000&miles_min=0&model=&page_size=24&price_max=100000&price_min=0&query=&requestingPage=buy&sort=desc&sort_field=updated&status=active&year_end=2022&year_start=1998&zip=")
#is to specify the amount of time the WebDriver instance
driver.implicitly_wait(5)

#used to uniquely identify a web element within the web page and send_keys() method is used to enter zipcode
driver.find_element(By.XPATH, "//input[@value]").send_keys("90222")

#suspends the execution of the current thread for the given number of seconds
time.sleep(2)

#returns a list of Vehicle matching under the given zipcode
gridbox = driver.find_elements(By.XPATH, "//div[@class='grid-box-container']/a")

name_list = []
summary_list = []
prices_list = []
option_list = []

for n in range(len(gridbox)):
    add = str(n + 1)
    #used to uniquely identify Vehicle under the given zipcode
    link = driver.find_element(By.XPATH, "(//div[@class='grid-box-container']/a)" + "[" + add + "]")

    #click()' method to help you perform various mouse-based operations. Here,I used to enter the identified vehicle page
    link.click()

    #used to uniquely identify Vehicle Name
    name = driver.find_element(By.XPATH, "//h1[@class='bigger no-top-margin hidden-xs']").text
    split_name = name.split()  # splite the name text
    str_name = ' '.join(map(str, split_name))  # convert list to str

    # Here,unwanted words have been removed that are associated with the name of the vehicle. like, 'for sell' and (....'s).
    if "'s" in name:
        split_name = split_name[1:-2]
        str_name = ' '.join(map(str, split_name))
        name_list.append(str_name)  # append the vehicle Name
    else:
        split_name = split_name[:-2]
        str_name = ' '.join(map(str, split_name))
        name_list.append(str_name)

    # used to uniquely identify Vehicle summary
    summary = driver.find_element(By.XPATH,
                                  "//div[@class='col-md-7' or @class='col-md-12']/table/tbody").text.splitlines()

    str_summary = ' '.join(map(str, summary[1:]))
    summary_list.append(str_summary) # append the vehicle summary

    # used to uniquely identify Vehicle option.
    # Options are not available for many the vehicle.for this condition I used try except.
    try:
        option = driver.find_element(By.XPATH, "//div[@class='col-md-5']/table/tbody/tr/td").text.splitlines()
        str_option = ' '.join(map(str, option))
        option_list.append(str_option)
    except:
        option_list.append("None")

    # used to uniquely identify Vehicle Price.
    # Price are not available for many the vehicle.for this condition I used try except.
    try:
        price = driver.find_element(By.XPATH, "//div[@class='price-box no-arrow']/h2").text.splitlines()
        str_price = ' '.join(map(str, price))
        prices_list.append(str_price)
    except:
        prices_list.append("None")

    # This method has been used to move a page back.
    driver.back()

#Has been used for returns a single iterator object.
final_list = zip(name_list, prices_list, summary_list, option_list)

#The Excel binary workbook files helped me in storing the information in the Binary format instead of the xlsx format.
wb = Workbook()
wb['Sheet'].title='Tred_data'
sheet1 = wb.active
sheet1.append(['Name','price','summery','options'])
for x in list(final_list):
    sheet1.append(x)
wb.save("tred_data1.xlsx")
driver.quit()
