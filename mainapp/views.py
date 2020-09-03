from django.shortcuts import render
import os, random, sys, time
from selenium import webdriver
from bs4 import BeautifulSoup
from mainapp.models import sentInvitation
from mainapp.forms import LinkedInForm

# Create your views here.
browser = webdriver.Chrome('driver/chromedriver.exe')

driver = browser

from mainapp.utilities import *

def general(request):
    
    return render(request,'general.html')

def login(request):
    
    browser.get('https://www.linkedin.com/uas/login')
    file = open('config.txt')
    lines = file.readlines()
    username = lines[0]
    password = lines[1]
    usernameID = browser.find_element_by_id('username')
    usernameID.send_keys(username)
    passwordID = browser.find_element_by_id('password')
    passwordID.send_keys(password)
    try:
        usernameID.submit()
    except:
        print("error")
    return render(request,'linkedin.html')

def send(request):
    form = LinkedInForm()
    keyword=request.POST.get('keyword')
    note=request.POST.get('note')
    print(keyword)
    links = []
    get_search(browser,keyword)
    sleep(0.5)
    scroll(browser)
    sleep(0.5)
    links += get_10(browser)
    page = 2
    num_people = int(request.POST.get('number'))
    print(num_people)
    
    for i in range(int(num_people/10)):
        if len(set(links)) <= num_people:
            get_search(browser,keyword, page)
            sleep(0.5)
            scroll(browser)
            sleep(0.5)
            
            links += get_10(browser)
            page += 1
        else:
            break
    
    links = links[:num_people]
    
    
    scarpe_details = []
    scarpe_details += save(browser,links,add_note=False, text=None)
    
    # browser.get('https://www.linkedin.com/m/logout/?lipi=urn%3Ali%3Apage%3Ad_flagship3_search_srp_people%3BezDT999kTce8ugkRrUzQLg%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_search_srp_people-nav.settings_signout')
    
    # browser.quit()


    a=scarpe_details
    l=len(scarpe_details)
    print(l)
    for i in range(l):
        name=a[i]['name']
        headline=a[i]['headline']
        location=a[i]['location']
        headings=a[i]['headings']
        highlights=a[i]['highlights']
        summary=a[i]['summary']
        activity=a[i]['activity']
        education=a[i]['education']
        skills=a[i]['skills']
        interests=a[i]['interests']
        url=a[i]['url']
        print(name)
        print(headline)
        print(url)
        Database=sentInvitation(name=name,headline=headline,location=location,headings=headings,highlights=highlights,summary=summary,activity=activity,education=education,skills=skills,interests=interests,url=url)
        Database.save()
        
                

    # search_group= browser.find_element_by_xpath('//*[@id="ember41"]/input')
    # search_group.send_keys(browser,keyword)
    # search_btn=browser.find_element_by_xpath('//*[@id="ember39"]/div[2]/button')
    # search_btn.click()
    return render(request,'linkedin.html')

def withdraw(request):
    list_withdraw(browser)
    #browser.get('https://www.linkedin.com/mynetwork/invitation-manager/sent/')
    
    return render(request,'linkedin.html')

def send_message(request):
    list_contact = ['Gaurav Chopra', 'akash paliwal']
    message="hey man, how r u."
    send_message1(browser, list_contact, message)
    
    return render(request,'linkedin.html')

def send_greetings(request):
    message = 'Glad to be connected'
    greetings(browser, message)
    return render(request,'linkedin.html')