from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import re

file = open('out.csv', 'w')

writer = csv.writer(file, delimiter=',')
header= ['year', 'volume', 'title', 'description', 'pdf_url', 'issn']
writer.writerow(header)


driver = webdriver.Chrome()

def parseArticle(href):
    driver.get(href)
    title = driver.find_element(by=By.XPATH, value="//div[@id='articleTitle']/h3").text
    volume = driver.find_element(by=By.XPATH, value="//div[@id='breadcrumb']/a[contains(text(), 'Vol')]").text
    volume, year = re.match("Vol *(\d*), No .* \((\d*)\)", volume).groups()
    description = driver.find_element(by=By.XPATH, value="//div[@id='articleAbstract']/div").text
    pdf_url = driver.find_element(by=By.XPATH, value="//div[@id='articleFullText']/a").get_attribute('href')
    issn = driver.find_element(by=By.XPATH, value="//center/descendant::span[contains(text(), 'E-ISSN')]").text
    writer.writerow([year, volume, title, description, pdf_url, issn])
    

def parseArchive(href):
    driver.get(href)
    link_elems = driver.find_elements(by=By.XPATH, value="//div[@class='tocTitle']/a")
    hrefs = [it.get_attribute('href') for it in link_elems]
    for href in hrefs:
        parseArticle(href)

driver.get("https://www.uel.br/revistas/uel/index.php/semagrarias/issue/archive")
link_elems = driver.find_elements(by=By.XPATH, value="//div[@id='issues']/div/div[starts-with(@id, 'issue-')]/h4/a[contains(text(), '(2021)')]")
hrefs = [it.get_attribute('href') for it in link_elems]
for href in hrefs:
    parseArchive(href)
file.close()
driver.close()

