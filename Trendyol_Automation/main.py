from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

service = Service("./chromedriver.exe")

driver = webdriver.Chrome(service=service)
driver.implicitly_wait(5)
driver.get("https://www.trendyol.com/")
driver.maximize_window()

def Close_popup():
    try:
        quit_button = driver.find_element(By.CLASS_NAME, "modal-close")
        quit_button.click()
    except:
        print("Herhangi bir pop up bulunamadı.")

def Login_click():
    login_page_button = driver.find_element(By.CLASS_NAME, "link-text")
    login_page_button.click()

def Login_process(mail,pw) :
    username = driver.find_element(By.ID, "login-email")
    username.send_keys(mail)

    password = driver.find_element(By.ID, "login-password-input")
    password.send_keys(pw)

    login_button = driver.find_element(By.XPATH, '//button[@type="submit" and contains(@class, "q-primary")]')
    login_button.click()


    error_message = driver.find_elements(By.XPATH, '//div[@id="error-box-wrapper"]')
    if len(error_message) > 0:
        print("Hatalı giriş algıladı")
    else:
        print("Giriş Başarılı")

def Search_product(searchkey):

    search = driver.find_element(By.XPATH, '//*[@data-testid = "suggestion"]')
    search.send_keys(searchkey)
    search.send_keys(Keys.ENTER)

def Sort_products():

    sort = driver.find_element(By.CLASS_NAME , "search-sort-container")
    sort.click()

    WebDriverWait(driver,5).until(expected_conditions.visibility_of_element_located((By.XPATH, '//span[text()="En çok satan"]')))

    #sort_type    = driver.find_element(By.XPATH, '//span[text()="En yüksek fiyat"]')
    #sort_type    = driver.find_element(By.XPATH, '//span[text()="En düşük fiyat"]')
    #sort_type    = driver.find_element(By.XPATH, '//span[text()="En favoriler"]')
    #sort_type    = driver.find_element(By.XPATH, '//span[text()="En yeniler"]')
    #sort_type    = driver.find_element(By.XPATH, '//span[text()="En çok değerlendirilen"]')
    #sort_type    = driver.find_element(By.XPATH, '//span[text()="Önerilen"]')

    sort_type = driver.find_element(By.XPATH, '//span[text()="En çok satan"]')
    sort_type.click()

    #sort_type    = driver.find_element(By.XPATH, '//span[text()="En yüksek fiyat"]')
    #sort_type    = driver.find_element(By.XPATH, '//span[text()="En düşük fiyat"]')
    #sort_type    = driver.find_element(By.XPATH, '//span[text()="En favoriler"]')
    #sort_type    = driver.find_element(By.XPATH, '//span[text()="En yeniler"]')
    #sort_type    = driver.find_element(By.XPATH, '//span[text()="En çok değerlendirilen"]')
    #sort_type    = driver.find_element(By.XPATH, '//span[text()="Önerilen"]')

def Select_first_product():
    all_products = driver.find_elements(By.CSS_SELECTOR, '.p-card-wrppr')
    if all_products:
        all_products[0].click()
    else:
        print("Ürün bulunamadı!")

def Click_event() :

    hover = ActionChains(driver)
    hover.move_by_offset(600,800).click().perform()

def Find_price():

    campaign = driver.find_elements(By.XPATH, "//div[@class='campaign-price']")
    if len(campaign) > 0:
       price = driver.find_element(By.XPATH, '//p[@class="campaign-price"]').text
       print(price)
    else:
       price = driver.find_element(By.XPATH, '//span[@class="prc-dsc"]').text
       print("Ürün Fiyatı : " + price)


Close_popup()
Login_click()
email = input("Email: ")
password = input("Şifre: ")
Login_process(email,password)

WebDriverWait(driver,10).until(expected_conditions.url_to_be("https://www.trendyol.com/"))

Search_product("masa")
Sort_products()

WebDriverWait(driver, 10).until(expected_conditions.url_contains("sst=BEST_SELLER"))

Select_first_product()

product_page = driver.window_handles[-1]
driver.switch_to.window(product_page)

Click_event()
Find_price()


product_page_url = driver.current_url   #satın alınan ürününün urlsi
add_to_basket = driver.find_element(By.CLASS_NAME, "add-to-basket")
add_to_basket.click()

driver.get(product_page_url)              #Sepete gitmeme durumları için önlem

go_to_basket = driver.find_element(By.CLASS_NAME , "account-basket")
go_to_basket.click()

if driver.current_url =="https://www.trendyol.com/sepet" :

    total_shipping_price = driver.find_element(By.XPATH , '//ul[@class="pb-summary-box-prices"]//li[span[text()="Kargo Toplam"]]//strong').get_attribute('title')

    shipping_discounts = driver.find_elements(By.XPATH , '//strong[@class="discount"]')   #kargo indirimi var mı

    if len(shipping_discounts) > 0 :

        shipping_discounts_price = driver.find_element(By.XPATH , '//strong[@class="discount"]').get_attribute('title')
        print("Kargo İndirim Bedeli : "+shipping_discounts_price)

    else:

        print("Kargo Ücreti Var")

    product_id = product_page_url.split("-p-")[1].split("?")[0]
    xpath_code = f'//div[@data-content-id="{product_id}"]//input[@class="counter-content"]'
    counter_value = driver.find_element(By.XPATH, xpath_code).get_attribute("value")
    price_value = driver.find_element(By.CLASS_NAME , "pb-summary-total-price").get_attribute("title")
    selected_products= driver.find_elements(By.XPATH, '//*[@name= "pb-basket-item-check"][@value = "true"]')

    print("Kargo Bedeli : " + total_shipping_price)
    print("Alınan Ürünün Idsi : " +product_id)
    print("Toplam Fiyat : " + price_value)
    print("Seçili Ürün Çeşidi : " +str(len(selected_products)))
    print("Ürünün Sepetteki Adedi: "+counter_value)

    product_types = driver.find_elements(By.CLASS_NAME, "pb-merchant-group")
    type_count = len(product_types)

    print("Sepetteki Ürün Çeşidi : "+str(type_count))
    count = 0
    if type_count > 0 :
        for item in product_types:
            count += int(item.find_element(By.CLASS_NAME , "counter-content").get_attribute("value"))

        print("Sepetteki Toplam Ürün Sayısı : " +str(count))

else:
    print("Sepetim sayfasına gidilemedi.")







