from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from pykeyboard import PyKeyboard
import time
import os
import json
from utils import clipboard


key = PyKeyboard()

def run(*args):
    usr, pwd, driver, article_id, title, content = args

    #处理弹框
    try:
        key.tap_key(key.enter_key)
    except:
        pass
        
    driver.get("https://baijiahao.baidu.com/builder/rc/edit?type=news&app_id=1600282401631826")

    #COOKIE登录
    driver.delete_all_cookies()
    if os.path.exists(os.getcwd()+'\\utils\\baijiacookie.json'):
        with open(os.getcwd()+'\\utils\\baijiacookie.json', 'r', encoding='utf-8') as f:
    #单独调试的时候的路径
    # if os.path.exists(os.path.dirname(os.getcwd())+'\\utils\\baijiacookie.json'):
    #     with open(os.path.dirname(os.getcwd())+'\\utils\\baijiacookie.json', 'r', encoding='utf-8') as f:
            for cookie in json.loads(f.read()):
                driver.add_cookie({
                    'domain': '.baidu.com',
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'path': '/',
                    'expires': None
                })
            driver.get("https://baijiahao.baidu.com/builder/rc/edit?type=news&app_id=1600282401631826")
    
    if driver.current_url == "https://baijiahao.baidu.com/builder/author/register/index":
        driver.get("https://passport.baidu.com")
        time.sleep(5)
        elements_select_login = driver.find_element_by_id("TANGRAM__PSP_3__footerULoginBtn")
        elements_select_login.click()
        elements_usrname = driver.find_element_by_id("TANGRAM__PSP_3__userName")
        elements_usrname.send_keys(usr)
        elements_pwd = driver.find_element_by_id("TANGRAM__PSP_3__password")
        elements_pwd.send_keys(pwd)
        elements_login_submit = driver.find_element_by_id("TANGRAM__PSP_3__submit")
        elements_login_submit.click()
        time.sleep(3)
        driver.get("https://baijiahao.baidu.com/builder/rc/home")
        with open(os.getcwd()+'\\utils\\baijiacookie.json', 'w') as f:
        # with open(os.path.dirname(os.getcwd())+'\\utils\\baijiacookie.json', 'w') as f:
            f.write(json.dumps(driver.get_cookies()))
    driver.get("https://baijiahao.baidu.com/builder/rc/edit?type=news&app_id=1600282401631826")
    elements_title = driver.find_element_by_xpath("//div[@class='input-box']//input")
    elements_title.send_keys(title)
    time.sleep(3)
    elements_insert_pic = driver.find_element_by_id("edui20_body")
    elements_insert_pic.click()
    driver.switch_to.frame("edui14_iframe")
    time.sleep(3)
    elements_select_pic = driver.find_element_by_id("filePickerReady")
    elements_select_pic.click()
    # ActionChains(driver).move_to_element(elements_select_pic).click(elements_select_pic).perform()
    # time.sleep(2)
    driver.switch_to.default_content()
    pic_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'\\cover\\'+str(article_id)+'.png'
    clipboard.settext(pic_path)
    key.press_keys([key.control_key, 'V'])
    key.tap_key(key.enter_key)
    key.tap_key(key.enter_key)
    time.sleep(3)
    # elements_confirm_addPic = driver.find_element_by_id("edui19_body") 
    elements_confirm_addPic = driver.find_element_by_id("edui19")
    ActionChains(driver).move_to_element(elements_confirm_addPic).click(elements_confirm_addPic).perform()
    #elements_confirm_addPic.click()
    # driver.switch_to.active_element.send_keys(content)
    clipboard.settext(content)
    key.press_keys([key.control_key, 'V'])
    driver.switch_to.default_content()
    #跳过封面方式选择
    # elements_cover_radio = driver.find_element_by_xpath("//div[@class='cover-radio-group']//lable[3]/span/input")
    # elements_cover_radio.click()
    #TODO:领域的选择暂时跳过,页面有BUG
    #下拉菜单处理，需要引入Select
    #elements_field_select = Select(driver.find_element_by_class_name("ant-select-selection__rendered"))
    elements_publish = driver.find_element_by_xpath("//span[@class='op-list']//button[3]")
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(20)
    elements_publish.click()
    time.sleep(10)
    #处理弹框
    try:
        key.tap_key(key.enter_key)
    except:
        pass

if __name__ == "__main__":
    run()
    