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
    
    def find_element(self, func, search_term, get_att=None, get_text=False):
        item = self.driver.find_element(func, search_term)
    
        if get_att is not None:
            return item.get_attribute(get_att)
        elif get_text:
            return item.text
        else:
            return item
    
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

    
    def wait_to_load(self, func, search_term, sleep=10, only_visual=True):
        wait = WebDriverWait(self.driver, sleep)
        if only_visual:
            wait.until(EC.visibility_of_element_located((func, search_term)))
        else:
            wait.until(EC.element_to_be_clickable((func, search_term)))
        self.site = self.driver.current_url
        self.custom_sleep()

    def switch_tab(self, mode="original", index=None, timeout=10):
        """
        Switches the driver's tab.

        Parameters:
            - mode: "original", "latest", "wait_latest", or "index"
            - index: required for mode="index"
        """
        handles = self.driver.window_handles

        if mode == "original":
            self.driver.switch_to.window(handles[0])
            self.tab = handles[0]

        elif mode == "latest":
            self.driver.switch_to.window(handles[-1])
            self.tab = handles[-1]

        elif mode == "wait_latest":
            WebDriverWait(self.driver, timeout).until(lambda d: len(d.window_handles) > 1)
            new_tabs = [h for h in self.driver.window_handles if h != self.tab]
            if new_tabs:
                self.driver.switch_to.window(new_tabs[-1])
                self.tab = new_tabs[-1]
            else:
                raise Exception("No new tab detected after waiting.")

        elif mode == "index":
            if index is None or index >= len(handles):
                raise ValueError(f"Tab index {index} is out of range.")
            self.driver.switch_to.window(handles[index])
            self.tab = handles[index]

        else:
            raise ValueError(f"Unknown switch_tab mode: {mode}")
        self.custom_sleep()


    def custom_sleep(self,sleep=5):
        time.sleep(sleep)


    def close_page(self):
        self.driver.quit()

