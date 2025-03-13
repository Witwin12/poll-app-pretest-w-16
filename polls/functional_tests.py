import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from django.test import LiveServerTestCase


class PollsFunctionalTest(LiveServerTestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_vote_and_check_results(self):
        driver = self.driver
        
        # Step 1: Go to the polls index page
        driver.get("http://127.0.0.1:8000/polls/")
        self.assertIn("Warm Questions", driver.page_source)
        self.assertIn("Hot Questions", driver.page_source)

        # Step 2: Click on a question (assuming ID 1)
        question_link = driver.find_element(By.CSS_SELECTOR, "body > ul:nth-child(4) > li > a")
        question_link.click()

        
        # Step 3: Vote for choice 1
        choice_radio = self.driver.find_element(By.ID, "choice1")
        choice_radio.click()


        # Step 4: Submit the vote
        vote_button = driver.find_element(By.CSS_SELECTOR, "body > form > input[type=submit]:nth-child(3)")
        vote_button.click()

        # Step 5: Verify the results page
        time.sleep(0.1)
        self.assertIn("vote", driver.page_source)
# สมชายได้ยินมาว่า เว็บ polls มีการฟังชันใหม่เป็น ฟังชันเกี่ยวกับ pivate polls
# เขาจึงได้ลองเข้าไปที่ http://localhost:8000/polls/pivate/ เขาขะเห็นหน้าเว็บเป็น "Pivate Polls" และคำถามอีก 3 ข้อ 
# เขาลองกดเข้าไปที่คำถาม pivate_1 
# หลังจากนั้นเขาจะเห็นตัวเลือกเป็น pivate_1 และ pivate_2
# จากนั้นเขาลองโหวต pivate_1 แล้วกดโหวต
# หลังจากที่เขากดโหวตเขาจะเห็นคะแนนเพิ่มขึ้น

class PivatePollsTest(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_vote_and_check_results(self):
        driver = self.driver
        
        # Step 1: Go to the polls index page
        driver.get("http://localhost:8000/polls/pivate/")
        self.assertIn("Pivate Questions", driver.page_source)

        # Step 2: Click on a question (assuming ID 1)
        question_link = driver.find_element(By.CSS_SELECTOR, "body > ul > li:nth-child(3) > a")
        question_link.click()

        # Step 3: Vote for choice 1
        choice_radio = self.driver.find_element(By.ID, "choice2")
        choice_radio.click()

        # Step 4: Submit the vote
        vote_button = driver.find_element(By.CSS_SELECTOR, "body > form > input[type=submit]:nth-child(3)")
        vote_button.click()

        # Step 5: Verify the results page
        time.sleep(0.1)
        self.assertIn("vote", driver.page_source)


