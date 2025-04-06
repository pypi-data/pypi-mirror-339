import time
from sevenapps.utils.file_manager import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class SeleniumConnector:

    def __init__(self):
        self.driver = self.init_webdriver()

    def init_webdriver(self):
        print('Configuring web driver...')
        chromedriver_path = "selenium/chromedriver/chromedriver"
        chrome_app_path = "selenium/chrome/google_chrome.app/Contents/MacOS/Google Chrome for Testing"

        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--start-maximized')

        options.binary_location = chrome_app_path

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        download_path = os.path.join(project_root, "results")

        prefs = {
            'download.default_directory': download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "download.safebrowsing.enabled": True
        }
        options.add_experimental_option('prefs', prefs)

        return webdriver.Chrome(service=Service(chromedriver_path), options=options)

    def open_url(self, url):
        self.driver.get(url)

    def focus_browser(self):
        # Crea una instancia de ActionChains
        actions = ActionChains(self.driver)

        # Mantiene la ventana activa simulando movimientos del ratón
        for _ in range(10):
            actions.move_by_offset(10, 0).perform()
            print('en el for')
            time.sleep(2)

    def waiting_for_download_results(self, css_selector, file_to_check):
        file_downloaded = False
        tries_to_check_if_file_exist = 3

        while not file_downloaded:
            try:
                download_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
                )
                download_button.click()
                time.sleep(3)

                for index in range(tries_to_check_if_file_exist):
                    print(f'[Check Nº {str(index + 1)}]: Checking if the file has been downloaded...')

                    if check_if_exist_file_in_folder(file_to_check):
                        print('[File Found]: The file has been found, ending the search.')
                        file_downloaded = True
                        break
                    else:
                        print('[File not Found]: File not found in folder, waiting 2 seconds to try again')
                        time.sleep(2)


            except:
                print('[INFO]: Waiting for the log download button...')

        return file_downloaded

    def close_connection(self):
        self.driver.quit()



