from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random 


class selenium:
    def __init__(self,settings):
        self.browser = settings[0]
        self.site    = settings[1]
        self.tab     = ''
        self.low     = settings[2][0]
        self.high    = settings[2][1]

        
    #random timer; small way to try and fool security systems with random fluxuations in typing speeds    
    def type_speed(self):
        return random.randint(self.low,self.high)/1000

    def typing(self,sentence,enter=False):
        typer=self.driver.switch_to.active_element
        for letter in range(len(sentence)):
            typer.send_keys(sentence[letter])
            time.sleep(self.type_speed())
        if enter:
            typer.send_keys(Keys.ENTER)

    def open_edge(self):
        self.driver = webdriver.Edge()
        try:
            self.driver.get("https://www."+self.site+".com")
            self.tab = self.driver.current_window_handle
            time.sleep(self.type_speed)
        except Exception as e:
            print(e)

    def navigate_address_bar(self,destination,delay=0.1):
        self.driver.get(destination)
        self.site = destination
        time.sleep(delay)
    

    def find_elements(self,func,search_term,get_att=None,get_text=False,collection_amount=None):
        selection = []
        items = self.driver.find_elements(func,search_term)
        if collection_amount is None:
            collection_amount = len(items)
        for i in range(collection_amount):
            item = items[i]
            if get_att is not None:
                selection.append([item.get_attribute(get_att)])
            elif get_text:
                selection.append([item.text])
            else:
                selection.append([item])
        return selection
    
    def wait_until_enabled(self, by, selector, timeout=30):
        WebDriverWait(self.driver, timeout).until(
        lambda d: d.find_element(by, selector).get_attribute("disabled") is None)


    def click(self, element=None, delay=0.25):
        element.click()
        time.sleep(delay)


        
    def location(self,element,scroll={'y_offset':100,'step':50,'delay':0.05}):
        if scroll:
            self.smooth_scroll_to(y_position=element.location['y'],y_offset=scroll['y_offset'],step=scroll['step'],delay=scroll['delay'])
        return element.location
        
    def smooth_scroll_to(self, y_position, y_offset=100, step=50, delay=0.05):
        current_position = self.driver.execute_script("return window.pageYOffset;")
        while current_position < y_position-y_offset:
            current_position += step
            self.driver.execute_script(f"window.scrollTo(0, {current_position});")
            time.sleep(delay)

    def new_page_wait(self,timeout=30):
        old_url = self.site
        WebDriverWait(self.driver, timeout).until(lambda d: d.current_url != old_url)
        self.site = self.driver.current_url
    
    def wait_to_load(self, func, search_term, sleep=10, only_visual=True,new_page_timer=-1):
        if new_page_timer > 0:
            self.new_page_wait(new_page_timer)
        wait = WebDriverWait(self.driver, sleep)
        if only_visual:
            wait.until(EC.visibility_of_element_located((func, search_term)))
        else:
            wait.until(EC.element_to_be_clickable((func, search_term)))

    def wait_for_tab(self):
        WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)
        new_tab = [h for h in self.driver.window_handles if h != self.tab][0]
        self.driver.switch_to.window(new_tab)
        self.tab = new_tab

    def custom_sleep(self,sleep=5):
        time.sleep(sleep)

    def close_page(self):
        self.driver.quit()

