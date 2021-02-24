from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import os
import shutil

driver = webdriver.Firefox(executable_path="geckodriver.exe")

def scrapeContestNumber(contest_number):
    contest_link = "https://codeforces.com/contest/"+contest_number
    driver.get(contest_link)
    problemsetLink = driver.find_element_by_link_text("Complete problemset")
    problemsetLink.click()

    try:
        problem_frame = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME,"problem-frames"))
        )
    except:
        driver.close()

    current_directory = os.getcwd()
    contest_path = os.path.join(current_directory, contest_number)
    if(os.path.exists(contest_path)):
        shutil.rmtree(contest_path)
    os.mkdir(contest_path)

    problemList = problem_frame.find_elements_by_class_name("problemindexholder")
    for problem in problemList:
        title = problem.find_element_by_class_name("title")
        problemIndex = title.text.split(".")[0]
        driver.fullscreen_window()
        path = os.path.join(contest_path, problemIndex)
        os.mkdir(path)
        problem.screenshot(os.path.join(path,"problem.png"))
        inputs = problem.find_elements_by_class_name("input")
        i=1
        for input_element in inputs:
            inputText = input_element.find_element_by_tag_name("pre").text
            inputFile = open(os.path.join(path,"input"+str(i)+".txt"),"w+")
            inputFile.write(inputText)
            inputFile.close()
            i=i+1

        outputs = problem.find_elements_by_class_name("output")
        i=1
        for output_element in outputs:
            outputText = output_element.find_element_by_tag_name("pre").text
            outputFile = open(os.path.join(path,"output"+str(i)+".txt"),"w+")
            outputFile.write(outputText)
            outputFile.close()
            i=i+1

contest_number = sys.argv[1]
scrapeContestNumber(contest_number)
driver.close()