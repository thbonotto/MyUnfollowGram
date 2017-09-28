#!/usr/bin/python3.4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from configparser import ConfigParser
import pickle 
from pathlib import Path
import re
sleepTime = 1
driver = webdriver.Firefox()

def unfollow(username):
    driver.get("https://www.instagram.com/"+username)
    element_present = EC.presence_of_element_located((By.CSS_SELECTOR, '._r9b8f'))
    WebDriverWait(driver, 30).until(element_present)
    if(driver.find_element_by_css_selector('._r9b8f').get_attribute("innerHTML")=='Following'):
        print("unfollowing"+username+"\n")
        driver.find_element_by_css_selector('._r9b8f').click(); 
        sleep(22)
    
def unlikePicture(username):
    driver.get("https://www.instagram.com/"+username)
    numPics = driver.find_element_by_css_selector('span._t98z6 > span:nth-child(1)').get_attribute("innerHTML");
    numPics = re.sub(',', '', numPics)
    numPics = int(numPics)
    if(numPics > 300):
        with open("over300.txt", 'a') as file_handler:
            file_handler.write("{}\n".format(username))
        return
    lineNumber = int(numPics)//3;
    line=1;
    if(lineNumber>0):
        remaing =  int(numPics)%3;
        for line in range(1, lineNumber+1):
            for collum in range(1, 3+1):
                currentPic = driver.find_element_by_css_selector('div._70iju:nth-child('+str(line)+') > div:nth-child('+str(collum)+')');
                currentPic.click();
                try:
                    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'coreSpriteComment'))
                    WebDriverWait(driver, 30).until(element_present)
                    driver.find_element_by_class_name('coreSpriteHeartFull').click(); 
                except:
                    pass
                driver.find_element_by_class_name('_dcj9f').click();
        line+=1   
    else:
        remaing=numPics;
 
    for collum in range(1, remaing+1):
            currentPic = driver.find_element_by_css_selector('div._70iju:nth-child(' + str(line) + ') > div:nth-child(' + str(collum) + ')');
            currentPic.click();
            try:
                element_present = driver.find_element_by_class_name('coreSpriteHeartFull')
                WebDriverWait(driver, 30).until(element_present)
                element_present.click(); 
            except:
                pass
            element_present = EC.presence_of_element_located((By.CLASS_NAME, '_dcj9f'))
            WebDriverWait(driver, 30).until(element_present)
            driver.find_element_by_class_name('_dcj9f').click();   

def login(username, password):
    cookie_file = Path("cookies.pkl")
    if cookie_file.is_file():
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        return
    sleep(sleepTime)
    logInButton = driver.find_element_by_css_selector("._b93kq")
    logInButton.click()
    sleep(sleepTime)
    usernameField = driver.find_element_by_name("username")
    usernameField.send_keys(username)
    passwordField = driver.find_element_by_name("password")
    passwordField.send_keys(password)
    sleep(sleepTime)
    logInButton = driver.find_element_by_css_selector("._qv64e")
    logInButton.click()
    sleep(sleepTime)
    pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
    return

def getFollow(username,follwing=True):
    if(follwing):
        followNumCss = "li._bnq48:nth-child(2) > a:nth-child(1) > span:nth-child(1)"
        followButton = "li._bnq48:nth-child(2) > a:nth-child(1)"
    else:
        followNumCss = "li._bnq48:nth-child(3) > a:nth-child(1) > span:nth-child(1)"
        followButton = "li._bnq48:nth-child(3) > a:nth-child(1)"
    driver.get("https://www.instagram.com/"+username)
    followingNum = driver.find_element_by_css_selector(followNumCss).get_attribute("innerHTML")
    followingButton = driver.find_element_by_css_selector(followButton)
    followingButton.click()
    sleep(sleepTime)
    followingList = []
    downKey = Keys()
    for i in range(1, int(followingNum)+1):
        #li._6e4x5:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)
        followingUsername = driver.find_element_by_css_selector('li._6e4x5:nth-child('+str(i)+') > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)')
        followingList.append(followingUsername.get_attribute("innerHTML"))
        followingUsername.send_keys(downKey.DOWN)
        sleep(0.250)
    return sorted(followingList)

def main():
    config = ConfigParser()
    config.read ("config.ini")
    username = config.get(("LoginInfo"), "username")
    password = config.get(("LoginInfo"), "password")
    driver.get("https://www.instagram.com/")
    login(username, password)
     
    following = getFollow(username)
    followers = getFollow(username,False)
    print(len(following))  
    print(len(followers))  
    nonFollowersBack = [item for item in following if item not in followers]
    nonFollowingBack = [item for item in followers if item not in following]
    print(nonFollowersBack)
    print(nonFollowersBack)
    with open("PeopleIDontFollowBack.txt", 'w') as file_handler:
        for item in nonFollowersBack:
            file_handler.write("https://www.instagram.com/{}\n".format(item))
    with open("PeopleWhodoesntFollowMeBack.txt", 'w') as file_handler:
        for item in nonFollowingBack:
            file_handler.write("{}\n".format(item))
  
##    text_file = open("nonFollowingBack.txt", "r")
##    lines = text_file.readlines()
    lines = nonFollowingBack;
    for line in lines:
        unlikePicture(re.sub('https://www.instagram.com/', '', line))
    
#   text_file = open("Non300Following.txt", "r")
#   lines = text_file.readlines()
    for line in lines:
        unfollow(line)

main()
driver.close()
