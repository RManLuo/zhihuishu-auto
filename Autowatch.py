from pyquery import PyQuery as pq
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from config import *
from datetime import datetime
import time
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 50)
def AutoPlay():
	try:
		mouse = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#vjs_mediaplayer > div.videoArea.container")))
		ActionChains(browser).move_to_element(mouse).perform()
		browser.find_element_by_css_selector("#playButton > div").click()
	except:
		print("no need to start video")
		
def IntoNextCourse():
	global Nowcouse
	Nowcouse=Nowcouse+1
	SwitchTime=int((Nowcouse-1)/2)
	
	for i in range(SwitchTime):
		browser.find_element_by_css_selector("#course_recruit_studying_next").click()
	into_study_page(Nowcouse)
def audiooff():
	mouse = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#vjs_mediaplayer > div.videoArea.container")))
	ActionChains(browser).move_to_element(mouse).perform()
	audio=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#vjs_mediaplayer > div.controlsBar > div.volumeBox > div.volumeIcon")))
	audio.click()
	time.sleep(5)
def speed():
	mouse = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#vjs_mediaplayer > div.videoArea.container")))
	ActionChains(browser).move_to_element(mouse).perform()
	mouse2=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#vjs_mediaplayer > div.controlsBar > div.speedBox")))
	ActionChains(browser).move_to_element(mouse2).perform()
	speelevel=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#vjs_mediaplayer > div.controlsBar > div.speedBox > div > div.speedTab15")))
	speelevel.click()
def tryPress():
    print('tryPress')
    try:
        popBtnCancel = browser.find_elements_by_class_name("popbtn_cancel")
        for i in popBtnCancel:
            try:
                i.click()
            except:
                pass
		#popBtnCancel.click():
    except:
        print ("no need to cancel")
	
def into_index():
	try:
		print('正在进入主页......')
		browser.get('http://www.zhihuishu.com/')
		first_place = wait.until(
		        EC.element_to_be_clickable((By.XPATH, "//*[@id='login-register']/li[1]/a"))
		    )
		first_place.click()
		time.sleep(1)
		login()
	except TimeoutException:
		print("超时，重新进入主页......")
		into_index()

def login():
	try:
		print('进入主页成功，准备进入登录页面......')
		print('尝试登录，正在输入账号和密码......')
		u = wait.until(
		        EC.presence_of_element_located((By.CSS_SELECTOR, "#lUsername"))
		    )
		p = wait.until(
		        EC.presence_of_element_located((By.CSS_SELECTOR, "#lPassword"))
		    )
		Login = wait.until(
				EC.element_to_be_clickable((By.CSS_SELECTOR, "#f_sign_up > div > span"))
			)
		u.send_keys(username)
		p.send_keys(password)
		Login.click()
		global Nowcouse
		Nowcouse=Nowcouse-1
		time.sleep(10)
		IntoNextCourse()	
	except TimeoutException:
		print('登录失败,重新进入主页......')
		into_index()

def into_study_page(num):
	try:
		print('登录成功，进入学习页面......')
		print("当前学习课程%d" %(num))
		second_place = wait.until(
				EC.element_to_be_clickable((By.CSS_SELECTOR, "#course_recruit_studying_ul > li:nth-child(%d) > div.new_stuCurseInfoBox.fr > div.promoteSchedule.mt15.clearfix > a" %(num)))
			)
		second_place.click()
		time.sleep(5)
		# 重定向窗口
		browser.switch_to_window(browser.window_handles[1])
		print ('sw sucess')
		#find_element_by_css_selector("#tm_dialog_win_1521046402473 > div.box_popboxes > div.popboxes_btn > a.popbtn_yes > span").click()
		#check()
		time.sleep(5)
		tryPress()
		time.sleep(3)
		try:
			p_1 = WebDriverWait(browser, 5).until(
					EC.element_to_be_clickable((By.XPATH, "//*[starts-with(@id, 'tm_dialog_win_')]/div[1]/div[2]/a[1]"))
				)
			p_1.click()
			print("close warning")
		except TimeoutException:
			print('......')
		time.sleep(3)
		try:
			p_2 = WebDriverWait(browser, 10).until(
					EC.element_to_be_clickable((By.CSS_SELECTOR, "#j-assess-criteria_popup > span.popup_delete.j-popup-close"))
				)
			#time.sleep(5)
			p_2.click()
			print("close info")
			time.sleep(3)
		except TimeoutException:
			print('......')
		#mouse = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#vjs_mediaplayer > div.videoArea.container")))
		#ActionChains(browser).move_to_element(mouse).perform()
		#playbutton=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#playButton")))#playButton
		#playbutton.click()
		audiooff()
		time.sleep(5)
		speed()
		time.sleep(5)
		all_time = get_all_time()
		while True:
			if all_time == 0:
				try:
					print('进入下一节学习成功')
					#video_look(all_time)
					#check()
					time.sleep(5)
					try:
						next_page = browser.find_element_by_css_selector("body > div.study_page > div.main_left > div > div.next_lesson > div > a")
						next_page.click()
					except:
						raise Exception('no next vidoe')
					time.sleep(10)
					audiooff()
					
					time.sleep(10)
					speed()
					
					
					print('进入下一节的学习......')
					time.sleep(10)
					all_time = get_all_time()
				except:
					print('本节课学习完毕')
					browser.close()
					browser.switch_to_window(browser.window_handles[0])
					time.sleep(10)
					global total
					total=total-1
					
					if total!=0:
						IntoNextCourse()
					else:
						print ("学习结束")
						
			else:
				print('翻页失败，尝试重新进入下一节')
				tryPress()
				time.sleep(3)
				next_page.click()
				time.sleep(10)
				all_time = get_all_time()

	except TimeoutException:
		print('超时了...')



def get_all_time():
	start = datetime.now()
	mouse = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#vjs_mediaplayer > div.videoArea.container")))
	ActionChains(browser).move_to_element(mouse).perform()
	tt1 = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"vjs_mediaplayer\"]/div[10]/div[4]/span[2]")))
	T1 = tt1.text
	T_all= int((int(T1[3:5])*60+int(T1[6:])))+15
	
	while True:
		tryPress()
		time.sleep(3)
		T1=1
		T2=2
		try:
			mouse = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#vjs_mediaplayer > div.videoArea.container")))
			ActionChains(browser).move_to_element(mouse).perform()
			tt2 = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"vjs_mediaplayer\"]/div[10]/div[4]/span[1]")))
			tt1 = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"vjs_mediaplayer\"]/div[10]/div[4]/span[2]")))
			T1 = tt1.text
			T2 = tt2.text
			if T1 == T2:
				return 0
			
		except:
			pass
		end = datetime.now()
		if (end - start).seconds > T_all:
			return 0
		time.sleep(3)
		AutoPlay()
		time.sleep(10)
		print('本次视频时长：', T1)
		print('已观看时间',T2)
		
		time.sleep(20)
		
	#return all_time

def main():
	into_index()
	login()
	browser.close()


if __name__ == '__main__':
	main()

