import json
import time
from functools import wraps
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    InvalidArgumentException,
    TimeoutException,
    NoSuchElementException, WebDriverException, ElementNotInteractableException, StaleElementReferenceException
)

from .heal import Heal


def click(element: WebElement, driver):
    try:
        print("Attempting WebDriverWait click...")
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable(element)).click()
    except Exception as e:
        print("Exception occurred selenium click on element: ", str(e))
        try:
            print("Attempting ActionChains click...")
            actions = ActionChains(driver)
            actions.move_to_element(element).click().perform()
            print("Action chain click successful.")
            return
        except WebDriverException as e:
            print(f"ActionChains click failed: {str(e)}. Trying JavaScript click...")
            try:
                driver.execute_script("arguments[0].click();", element)
                print("JavaScript click successful.")
                return
            except Exception as e:
                print(f"JavaScript click also failed: {str(e)}.")


def conditions_met(driver):
    # Check if the document is fully loaded
    document_ready = driver.execute_script("return document.readyState") == "complete"

    # Inject code to track active API requests
    driver.execute_script("""
    if (typeof window.activeRequests === 'undefined') {
        window.activeRequests = 0;
        (function(open) {
            XMLHttpRequest.prototype.open = function() {
                window.activeRequests++;
                this.addEventListener('readystatechange', function() {
                    if (this.readyState === 4) {
                        window.activeRequests--;
                    }
                }, false);
                open.apply(this, arguments);
            };
        })(XMLHttpRequest.prototype.open);
    }
    """)

    # Check if any API requests are in progress
    active_requests = driver.execute_script("return window.activeRequests;")

    # Return True only if both conditions are met
    return document_ready and active_requests == 0


def is_element_interactable(driver: webdriver.Remote, element: WebElement) -> bool:
    try:
        if not element.is_displayed() or not element.is_enabled():
            if not element.is_displayed():
                opacity = element.value_of_css_property("opacity")
                if opacity == "0":
                    print("Element has opacity 0")
                    return True
            print("Element is not visible or enabled")
            return False

        return True

    except (ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException) as e:
        print(f"Exception: {str(e)} - Element is not interactable")
        return False

def retry(driver: webdriver.Chrome, operation_idx: str):
    print("Retrying()...")

    WebDriverWait(driver, 180, poll_frequency=1).until(conditions_met)

    response = Heal(operation_idx, driver).list_xpaths()

    if response.status_code == 200:
        response_dict = json.loads(response.text)
        xpaths = response_dict.get('xpaths')
        lambda_hooks(driver, "Locator Autohealed ")
        print("XPaths Autohealed: ", xpaths)
        return xpaths
    else:
        print("Error in Getting Xpaths")
        return []

def go_to_url(driver: webdriver.Chrome, url: str):
    try:
        WebDriverWait(driver, 3).until(EC.url_changes(driver.current_url))
        driver.get(url)

    except TimeoutException:
        driver.get(url)


def find_element(driver: webdriver.Chrome, locators: list, operation_idx: str, max_retries: int = 2,
                 current_retry: int = 0, shadow=""):
    print("Finding element...")
    
    if current_retry >= max_retries:
        print("MAX RETRIES EXCEEDED")
        driver.implicitly_wait(15)  # Reset implicit wait
        return None

    # Check if this is an upload operation
    from .config import get_metadata
    metadata = get_metadata()
    op_data = metadata.get(operation_idx, {})
    upload_file = op_data.get('operation_type') == "UPLOAD"
    
    if upload_file:
        print("Upload operation detected")
        time.sleep(2)

    driver.implicitly_wait(6)  # Set initial implicit wait to 6 seconds

    for locator in locators:
        try:
            if shadow != "":
                element = shadow.find_element(By.XPATH, locator)
            else:
                element = driver.find_element(By.XPATH, locator)
            
            # For upload operations, return element immediately
            if upload_file:
                print("Found upload element")
                driver.implicitly_wait(15)  # Reset implicit wait
                return element
            
            if is_element_interactable(driver, element):
                print(f"Element found using locator: {locator} is interactable")
                driver.implicitly_wait(15)  # Reset implicit wait
                return element  # Return the element if interactable
            else:
                print("Element is Not Interactable, Retrying...")
                continue  # Continue to the next locator if the element is not interactable

        except Exception as e:
            print(f"Unable to find element using locator: {locator}\nError: {str(e)}\nSwitching to next locator...")
            continue  # Continue to the next locator if the element is not found

    driver.implicitly_wait(15)  # Reset implicit wait
    
    locators = retry(driver=driver, operation_idx=operation_idx)
    
    if locators:
        return find_element(driver, locators, operation_idx, max_retries, current_retry + 1,
                            shadow=shadow)  # Retry with incremented attempt count

    return None  # Return None if no element was found or retry exhausted

def lambda_hooks(driver: webdriver.Chrome, argument: str):
    try:
        script = f'lambdatest_executor: {{"action": "stepcontext", "arguments": {{"data": "{argument}", "level": "info"}}}}'
        driver.execute_script(script)
        print(f"\n{argument}")
    except:
        print(f"\n{argument}")


def switch_to_frame(driver:webdriver.Chrome,operation_index:str,shadow="",max_retries=3,frame_info=""):
    for index in range(1,max_retries + 2):
        if index!=1:
            driver.switch_to.default_content()
            frame_info = retry(driver=driver,operation_idx=operation_index).get('frameInformation')
            frame_info = json.dumps(frame_info)
        try:
            if frame_info and frame_info != "":
                frames = json.loads(frame_info)
                for frame in frames:
                    key, value = list(frame.items())[0]
                    if key == "iframe":
                        if shadow == "":
                            if isinstance(value,list):
                                for index in range(0,len(value)):
                                    try:
                                        iframe = driver.find_element(By.XPATH, value[index])
                                        break
                                    except:
                                        continue
                            else:
                                iframe = driver.find_element(By.XPATH, value)
                            driver.switch_to.frame(iframe)
                        else:
                            iframe = shadow.find_element(By.XPATH, value)
                            driver.switch_to.frame(iframe)
                            shadow = ""
                    elif key == "shadow":
                        if shadow != "":
                            shadow_childrens = shadow.find_element(By.XPATH, value)
                            shadow = driver.execute_script("return arguments[0].shadowRoot.children[0]", shadow_childrens)
                        else:
                            shadow = driver.execute_script("return arguments[0].shadowRoot.children[0]", driver.find_element(By.XPATH, value))
            return shadow
        except Exception as e:
            pass
    return "unresolved"