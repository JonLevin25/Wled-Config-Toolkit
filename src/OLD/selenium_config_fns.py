# from selenium import webdriver
# from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
#
# from utils.web_utils import *
# import requests
# from typing import Dict, Any
#
# def manual_cfg_upload_selenium(conf_file: str, cfgs_to_build = None):
#     mdns_to_cfg_map = build_cfg_jsons_from_conf(conf_file)
#     mdns_to_files_map = write_cfg_jsons(mdns_to_cfg_map)
#     for mdns_name in mdns_to_files_map:
#         selenium_open_edit_page(mdns_name)  # use new driver so we dont change page
#
# def selenium_open_edit_page(mdns_or_ip: str):
#     url = f'http://{get_host(mdns_or_ip)}/edit'
#     cfg_btn_id = '/cfg.json'
#
#     try:
#         chrome_options = Options()
#         chrome_options.add_experimental_option("detach", True)
#         driver = webdriver.Chrome(options=chrome_options)
#         driver.maximize_window()
#
#         driver.get(url)
#         WebDriverWait(driver, timeout=6).until(lambda d: d.find_element(By.ID, cfg_btn_id))
#         button = driver.find_element(By.ID, cfg_btn_id)
#         button.click()
#         # driver.close()
#     except WebDriverException as e:
#         print(f'WebDriverError on page {url}\nMsg:{e.msg}')
#
