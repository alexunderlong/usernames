import scrapy
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver


def start_selenium(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    sleep(5)
    return browser


def scroll_full_down(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        ActionChains(driver).send_keys(Keys.END).perform()
        sleep(1)
        ActionChains(driver).scroll_by_amount(0, -130).perform()
        sleep(1)
        ActionChains(driver).send_keys(Keys.END).perform()
        sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def get_usernames(driver: WebDriver):
    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')
    sel = scrapy.selector.Selector(text=source)
    for t in sel.xpath("//body//text()").extract():
        if t.startswith('@'):
            print(t)
    driver.quit()


ggurl = 'https://getgems.io'
namesfilter = '?filter=%7B"collections"%3A%5B"EQCA14o1-VWhS2efqoh_9M1b_A9DtKTuoqfmkn83AbJzwnPi"%5D%7D'
with open('ggusers.txt', 'r', encoding='UTF-8') as f:
    f = f.readlines()
    for i, user in enumerate(f):
        user = user.split('\n')[0]
        print(f'{i}/14249')
        userurl = ggurl+user+namesfilter
        driver = start_selenium(userurl)
        scroll_full_down(driver)
        get_usernames(driver)
