from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import smtplib
import time
from concurrent.futures import ThreadPoolExecutor
from selenium.common.exceptions import TimeoutException
import json
import os

def send_email(store, url):
    try:
        sender = "chrispierrebacon@gmail.com"
        receiver = ["chrispierrebacon@gmail.com"]
        message = f"{store} IS ACTIVE!\n Go here: {url}"

        server = smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.ehlo()
        server.login("chrispierrebacon@gmail.com","")
        server.sendmail(sender, receiver,message)
    except smtplib.SMTPException:
        print("Failed to send mail.")

def ping(store_obj):
    if store_obj["enabled"]:
        driver = webdriver.Firefox()
        driver.get(store_obj["url"])
        while True:
            try:
                time.sleep(10)
                element = WebDriverWait(driver,10,.5).until(EC.presence_of_element_located((By.XPATH, store_obj["xpath"])))
                innerHTML = element.get_attribute(store_obj["sold_out_attribute"]).strip()
                if innerHTML == store_obj["sold_out_string"]:
                    print(f"{store_obj['name']} still out of stock.")
                    driver.refresh()
                else:
                    send_email(store_obj['name'], store_obj['url'])
                    break
            except Exception as ex:
                print(f"{store_obj['name']} exception: {str(ex)}")
                break

def main():
    config_contents = open("./config.json").read()
    config_json = json.loads(config_contents)
    
    executor = ThreadPoolExecutor(max_workers=10)
    results = executor.map(ping, config_json["Stores"])

if __name__ == "__main__":
    # execute only if run as a script
    main()
