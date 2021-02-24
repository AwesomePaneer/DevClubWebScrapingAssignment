from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import shutil

min_diff = input("Enter minimum difficulty level\n")
max_diff = input("Enter maximum difficulty level\n")
driver = webdriver.Firefox(executable_path="geckodriver.exe")
scrape_link = "https://codeforces.com/problemset?tags="+min_diff+"-"+max_diff
driver.get(scrape_link)
driver.implicitly_wait(10)
problem_links_table = driver.find_elements_by_xpath("//*[@class='problems']/tbody/tr/td[1]")
problem_links = []
for problem_link in problem_links_table:
    problem_links.append(problem_link.find_element_by_tag_name("a").get_attribute("href"))
current_directory = os.getcwd()
for problem_link in problem_links:
    driver.get(problem_link)
    problem_index = problem_link.split("/")[-2] + problem_link.split("/")[-1]
    try:
        problem_frame = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME,"problem-statement"))
        )
    except:
        driver.close()
    
    problem_path = os.path.join(os.getcwd(),problem_index)
    if(os.path.exists(problem_index)):
        shutil.rmtree(problem_index)
    os.mkdir(problem_path)
    problem_frame.screenshot(os.path.join(problem_path,"problem.png"))

    inputs = problem_frame.find_elements_by_class_name("input")
    i=1
    for input_element in inputs:
        inputText = input_element.find_element_by_tag_name("pre").text
        inputFile = open(os.path.join(problem_path,"input"+str(i)+".txt"),"w+")
        inputFile.write(inputText)
        inputFile.close()
        i=i+1

    outputs = problem_frame.find_elements_by_class_name("output")
    i=1
    for output_element in outputs:
        outputText = output_element.find_element_by_tag_name("pre").text
        outputFile = open(os.path.join(problem_path,"output"+str(i)+".txt"),"w+")
        outputFile.write(outputText)
        outputFile.close()
        i=i+1


driver.close()