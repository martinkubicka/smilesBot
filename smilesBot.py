from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def writeNeededInfo(drugName):
    tmpFile = open("tmpFile.txt", "r")
    outputFile = open("output.txt", "a")
    count = 0
    for i in tmpFile.readlines():
        if count != 0:
            outputFile.write(drugName + "," + i)
        count += 1
    tmpFile.close()
    outputFile.close()

def getCsvFile(driver):
    while True:
        try:
            driver.find_element_by_xpath("//h2[text()='Please Wait...']")
        except:
            break
    try:
        driver.find_element_by_xpath("//h1[text()='Server Error (500)']")
        return 0
    except:
        link = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='d-flex align-items-center justify-content-between']/div[2]/a"))).get_attribute("href")
        r = requests.get(link, verify=False, allow_redirects=True)
        open('tmpFile.txt', 'wb').write(r.content)
        return 1

def writeNotFound(smiles):
    file = open("notFound.txt", "a")
    file.write(smiles + "\n")
    file.close()

def getAdmetInfo(driver, smiles, drugName):
    action = ActionChains(driver)
    while True:
        if requests.get("https://admetmesh.scbdd.com/service/evaluation/index", verify=False).status_code == 200:
            driver.get("https://admetmesh.scbdd.com/service/evaluation/index")
            textBox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='smiles']")))
            action.send_keys_to_element(textBox, smiles).perform()
            time.sleep(0.3)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Submit']"))).click()
            if getCsvFile(driver) == 1:
                writeNeededInfo(drugName)
            else:
                writeNotFound(smiles)
            break

def getLine(driver):
    inputFile = open("input_smiles.txt", "r")
    for line in inputFile.readlines():
        if '"' in line:
            if line.split('"')[1] != "not_found":
                getAdmetInfo(driver, line.split('"')[1], line.split("#")[0])
        else:
            if line.split("#")[1] != "not_found":
                getAdmetInfo(driver, line.split("#")[1], line.split("#")[0])
    inputFile.close()

def ctor():
    open("output.txt", "w").close()
    open("notFound.txt", "w").close()
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.set_window_size(1200, 1100)
    driver.get("https://admetmesh.scbdd.com/service/evaluation/index")
    input("Please allow access and hit enter..")
    return driver

def dtor(driver):
    driver.quit()

def main():
    driver = ctor()
    getLine(driver)
    dtor(driver)
    print("Program completed!")
    input("Press enter to continue..")

if __name__ == '__main__':
    main()
    #TODO - COMMENTS