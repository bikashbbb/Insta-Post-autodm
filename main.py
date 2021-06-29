import json
from selenium import webdriver
from time import sleep
from setofmesseges import AllMesseges
import time


class InstaPostBot:

    def __init__(self, username='amrit', password='nepalshop0',
                 savedurl='https://www.instagram.com/p/CMsVoq2LqEU/'):
        # get the variables
        self.driver = webdriver.Firefox(executable_path='./geckodriver')
        self.username = username
        self.password = password
        self.saved_url_link = savedurl
        self.totaldms = 0
        self.into_post()

    def into_post(self):
        self.driver.get('https://www.instagram.com/')
        self.driver.implicitly_wait(14)
        self.into_login_page()

    def into_login_page(self):
        self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(self.username)
        self.driver.implicitly_wait(2)
        password_field = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        password_field.send_keys(self.password)
        self.driver.implicitly_wait(4)
        password_field.submit()
        self.driver.implicitly_wait(10)
        self.not_now_clicked()

    def not_now_clicked(self):
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        sleep(4)
        self.notify_not_now()

    def notify_not_now(self):
        sleep(5)
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        self.driver.get(self.saved_url_link)
        self.into_total_like()

    def into_total_like(self):
        sleep(5)
        self.alluserlist = []
        self.t_end = time.time() + 210 * 1
        sleep(1)
        # total likes
        totalpostlike = self.driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div[2]/a')
        totalpostlike.click()
        sleep(3)
        self.getusers()

    def getusers(self):
        sleep(2)
        allpostlikers = self.driver.find_elements_by_css_selector('.MBL3Z')
        for individualuser in allpostlikers:
            if individualuser.get_attribute('href') not in self.alluserlist:
                self.alluserlist.append(individualuser.get_attribute('href'))
            else:
                pass
        if time.time() > self.t_end:
            print('# ALL {}DATA SAVED INTO FILE'.format(len(self.alluserlist)))
            self.savethelist()
        else:
            self.updown_scroller(allpostlikers)

    def updown_scroller(self, userlist):
        self.driver.execute_script("return arguments[0].scrollIntoView();", userlist[-1])
        print('Scrolling to the finish line')
        sleep(4)
        self.getusers()

    def savethelist(self):
        with open('listofurl.txt', 'w') as p:
            p.write(json.dumps(self.alluserlist))
            print('\n data saved ')
        self.get_account_fromlist()

    def get_account_fromlist(self):
        with open('listofurl.txt', 'r') as e:
            list_of_links = json.loads(e.read())
        for account in list_of_links:
            print('getting in the account of ', list_of_links.index(account))
            self.intoaccounts(account)

    def intoaccounts(self, account):
        self.driver.get(account)
        self.getusername()

    def getusername(self):
        sleep(5)
        self.username = self.driver.find_element_by_css_selector('.fDxYl').text
        self.add_the_account()

    def add_the_account(self):
        try:
            sleep(10)
            self.driver.find_element_by_css_selector('._6VtSN').click()
            self.click_messege()
        except Exception as e:
            print('Next user')

    def click_messege(self):
        try:
            sleep(8)
            self.driver.find_element_by_css_selector('._8A5w5').click()
            self.click_messege_field()
        except Exception as e:
            print('ERROR ')

    def click_messege_field(self):
        try:
            sleep(1)
            firstdm = self.driver.find_element_by_css_selector('.focus-visible')
            firstdm.send_keys(AllMesseges.listof_first_dms[AllMesseges.list_index], self.username + '\n'
                              ,AllMesseges.list_of_dms[AllMesseges.list_index])
            sleep(1)
            submit_button = self.driver.find_element_by_xpath('/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button')
            submit_button.click()
            sleep(2)
            sleep(1)
            AllMesseges.list_index += 1
            self.totaldms += 1
            if AllMesseges.list_index == 5:
                AllMesseges.list_index = 0
            print('Messege sent  sucess')
            self.maximundms()


        except Exception as p:
            print(p)

    def maximundms(self):

        if self.totaldms != AllMesseges.total_dms_in_an_hour:
            pass
        else:
            print('maxumun dms completed please wait')
            self.totaldms = 0
            sleep(2100)


runscript = InstaPostBot()
