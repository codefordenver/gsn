from selenium import webdriver

browser = webdriver.Chrome()
browser.get("http://192.168.99.100:8000/gsndb/referral/")

drop_down_menus = browser.find_elements_by_class_name("form-control")

for menu in drop_down_menus:
    if menu.get_attribute("name") == 'student':
        print(menu)

browser.quit()
