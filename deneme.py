from typing import Counter
from playwright.sync_api import sync_playwright
import hashlib
from bs4 import BeautifulSoup
import sys
import time
import datetime
import requests
import re
import math
import os
import json
import pickle
import schedule
import time

user_dir = '/tmp/playwright'

def job():
    print("Working....")
    with open("./read_file.txt","r", encoding="utf-8") as f:
        text = f.read()
        read_file(text)

def read_file(text):
    
    if text:
        text_split = text.split(",")
        for link in text_split:
            if "http" in link or "www" in link:
                if link:
                    open_browser(link)
            else:
                text = link
                link = "https://www.google.com.tr/?hl=tr"
                open_browser(link,text)

def open_browser(link,text=None):
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch_persistent_context(user_dir, headless=False)
        page = browser.new_page()
        
        #page.wait_for_timeout(30000000)
        try:    
            if link == "https://www.google.com.tr/?hl=tr":
                page.goto(link)
                page.wait_for_load_state()
                # bekletme koymak için
                page.wait_for_timeout(3000)
                page_content = page.content()
                soup = BeautifulSoup(page_content, 'html.parser')
                print("scroll not working")
                input_text(page,text)
                page_enter_click(page, text)
                href_selector_all(page)
                
            else:
                page.goto(link)
                page.wait_for_load_state()
                # bekletme koymak için
                page.wait_for_timeout(3000)
                page_content = page.content()
                soup = BeautifulSoup(page_content, 'html.parser')
                scroll_down_page(page)
                page.wait_for_timeout(visit_page_time)
                
            browser.close()
        except Exception as a:
            print(a)

def input_text(page, text=None):
    selector = "input.gLFyf.gsfi"
    page.fill(selector, text)
    page.wait_for_timeout(3000)
      
def page_enter_click(page, text=None):
    page.keyboard.press("Enter")   
    page.wait_for_timeout(3000)
    
def page_escape_click(page, text=None):
    page.keyboard.press("Escape")   
    page.wait_for_timeout(3000)
    
def href_selector_all(page):
    selector = href_selector_click
    search_link_ = page.query_selector_all(selector)
    count_link = len(search_link_)
    href_count = search_page_visi_count
    search_link_google = page_back_next(page)
    if href_count <= count_link:
        for link_count in range(0, href_count):
            item = page.query_selector_all(selector)[link_count]
            if item:
                #print("item True")
                item.click()
                page.wait_for_timeout(3000)
                page_escape_click(page)
                page.reload()
                page.set_default_navigation_timeout(50000)
                scroll_down_page(page)
                click_button_action(page,search_link_google)
                page.wait_for_timeout(visit_page_time)
                time.sleep(5)
                #page.go_back()
            
def page_back_next(page):
    base_url = "https://www.google.com"
    new_button_selector = "div.MUFPAc div.hdtb-mitem:nth-child(2) a"
    all_button_selector = "div.MUFPAc div.hdtb-mitem:nth-child(1) a,div.T47uwc a.NZmxZe:nth-child(1)"
    page.click(new_button_selector)
    page.wait_for_timeout(3000)
    go_back_page = page.query_selector(all_button_selector) 
    go_back_link= go_back_page.get_attribute("href")
    google_search_link = base_url + go_back_link
    page.click(all_button_selector)
    page.wait_for_timeout(3000)
    return google_search_link

def scroll_down_page(page):
    scroll_top = page.evaluate("window.scrollY")
    scroll_height = page.evaluate(f"document.querySelector('body').scrollHeight")
    scroll_pixel = 500
    selector = "body"
    wait_timeout = True
    while (scroll_height - scroll_top) > (scroll_pixel * 3):
        page.evaluate(f"window.scrollBy(0,{scroll_pixel})")
        scroll_top = page.evaluate("window.scrollY")
        scroll_height = page.evaluate(f"document.querySelector('{selector}').scrollHeight")
        if scroll_top == 0 or scroll_top < 100:
            print("scroll break")
            break
        else:
            page.wait_for_timeout(scrolling_time)
            page.wait_for_timeout(3000)
        
    return 

def click_button_action(page,search_link_google): 
    selector = "a"
    button_selector = page.query_selector_all(selector)
    button_count = len(button_selector)
    
    if button_count > 5:
        for button in range(0,5):
            #print(button,"----")
            try:
                if page.evaluate(f"document.querySelectorAll('a')[{button}].click();"):
                    page.wait_for_timeout(6000)  
                    page.go_back()
            except:
                print("next button not found")
                page.wait_for_timeout(6000)  
                page.reload()  
            print("check")

        page.goto(search_link_google)
        page.wait_for_timeout(3000)  

    else:
        for button in range(0,button_count):
            #print(button,"----")
            try:
                if page.evaluate(f"document.querySelectorAll('a')[{button}].click();"):
                    page.wait_for_timeout(6000)  
                    page.go_back()
            except:
                print("next button not found")
                page.wait_for_timeout(6000)  
                page.reload()  
            print("check")

        page.goto(search_link_google)
        page.wait_for_timeout(3000)  


def options_json():
    with open("./options.json","r") as f:
        options_data = json.loads(f.read()) 
    return options_data

if __name__ == "__main__":
    options_data = options_json()
    working_time = options_data.get("options").get("working_time")
    visit_page_time = options_data.get("options").get("page_visit_time")
    scrolling_time = options_data.get("options").get("scrolling_time")
    search_page_visi_count = options_data.get("options").get("search_page_visi_count")
    href_selector_click = options_data.get("options").get("href_selector_click")
    #job()
    schedule.every(working_time).minutes.do(job)
    print("hello")
    while True:
        if schedule.run_pending():
            time.sleep(1)

        
        