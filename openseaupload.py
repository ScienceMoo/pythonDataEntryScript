from tkinter import *
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.support.ui import Select

root = Tk()
is_polygon = BooleanVar()
is_polygon.set(False)

# _____MAIN_CODE_____
def main_program_loop():
    ###START###
    file_path = "/Users/moo/NFTs-Upload-to-OpenSea/pics"
    collection_link = "https://opensea.io/collection/coleuspics"
    start_num = 1
    end_num = 2
    # loop_price = float(price.input_field.get())
    

    ##chromeoptions
    opt = Options()
    opt.add_experimental_option("debuggerAddress", "localhost:8989")
    driver = webdriver.Chrome(
        executable_path="/chromedriver.exe",
        chrome_options=opt,
    )
    wait = WebDriverWait(driver, 60)

    ###wait for methods
    def wait_css_selector(code):
        wait.until(
            ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, code))
        )

    def wait_xpath(code):
        wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))

    current_num = start_num

    while end_num >= current_num:
        loop_title = "Coleus #" + current_num
        loop_file_format = "jpeg"
        loop_description = "Coleus #" + current_num + " in the Coleus collection"

        print("Start creating NFT " +  loop_title + str(current_num))
        driver.get(collection_link)
        # time.sleep(3)

        wait_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/span/a')
        additem = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/span/a')
        additem.click()
        time.sleep(1)

        wait_xpath('//*[@id="media"]')
        imageUpload = driver.find_element_by_xpath('//*[@id="media"]')
        imagePath = os.path.abspath(file_path + "/" + "coleus" + str(current_num) + "." + loop_file_format)  # change folder here
        imageUpload.send_keys(imagePath)

        name = driver.find_element_by_xpath('//*[@id="name"]')
        name.send_keys(loop_title)  # +1000 for other folders #change name before "#"
        time.sleep(0.5)

        desc = driver.find_element_by_xpath('//*[@id="description"]')
        desc.send_keys(loop_description)
        time.sleep(0.5)

        # Select Polygon blockchain if applicable
        if is_polygon.get():
            blockchain_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/main/div/div/section/div/form/div[7]/div/div[2]')
            blockchain_button.click()
            polygon_button_location = '//span[normalize-space() = "Mumbai"]'
            wait.until(ExpectedConditions.presence_of_element_located(
                (By.XPATH, polygon_button_location)))
            polygon_button = driver.find_element(
                By.XPATH, polygon_button_location)
            polygon_button.click()

        create = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/section/div[2]/form/div/div[1]/span/button')
        driver.execute_script("arguments[0].click();", create)
        time.sleep(1)

        wait_css_selector("i[aria-label='Close']")
        cross = driver.find_element_by_css_selector("i[aria-label='Close']")
        cross.click()
        time.sleep(1)

        main_page = driver.current_window_handle
        
        # change control to main page
        driver.switch_to.window(main_page)
        time.sleep(1)

        current_num = current_num + 1
        print('NFT creation completed!')


root.mainloop()
