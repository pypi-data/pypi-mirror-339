#!/usr/bin/env python
# coding: utf-8

# In[1]:


import glob
import os
import re
import rsa
import getpass
import time
from datetime import datetime
import pandas as pd
import shutil
import win32com.client
import logging
from pathlib import Path
import xml.etree.cElementTree as ET
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# In[2]:


class Download():
    def __init__(self, logger_name):
        self.base_path = 'C:\\Users\\' + getpass.getuser() + '\\OneDrive - Landmark Group\\Work\Automations\\GUI\\'
        self.chrome_service = Service(self.base_path + 'chromedriver.exe')
        self.xml_path = os.path.join(self.base_path, 'ipynb_metadata_v2.xml')
        self.init_logger(logger_name, os.path.join(self.base_path,  'API.log'))
        with open(os.path.join(self.base_path , 'Keys', 'priv_key.PEM'), mode='rb') as f:
            private_key = f.read()
            private_key = rsa.PrivateKey.load_pkcs1(private_key)

        with open(os.path.join(self.base_path, 'Keys', 'qv_login.txt'), mode='rb') as f:
            qv = f.read()
            self.qv_usrname, self.qv_pswd = rsa.decrypt(qv, private_key).decode().split('###')

        with open(os.path.join(self.base_path, 'Keys', 'er_login.txt'), mode='rb') as f:
            er = f.read()
            self.er_usrname, self.er_pswd = rsa.decrypt(er, private_key).decode().split('###')
    
    def qv(self, url, save_path, download_time, column_order=[], cols_to_convert=[], typ='float', lx=False, stop_date='', extension='csv', lx_mon=[], include_today=False, check_date_filter=True):
        global driver
        self.driver = self.start_browser(url)
        self.status = self.check_update()
        # Checks if QV is refreshed or not
        if self.status:
            max_retries = 3         # Try to select required dates three times after which abort download
            if lx:                  # Check if the download is needed for last X days or entire duration
                time.sleep(2)
                while max_retries > 0:
                    if self.download_lx_days(stop_date, url, include_today, check_date_filter):     # Select the dates until stop date is reached
                        self.logger.debug('Last X days filter success')
                        # print('Got the LX filter')
                        break
                    else:
                        max_retries -= 1
                        self.logger.error("Can't find first date of last X days filtered date")
                        # print('Cant find first date')
                        continue
            if max_retries == 0 and lx == True:        # Abort download if date selection fails 3 times
                self.driver.close()
                return 'LX Failed'
            if len(lx_mon) > 0:
                pass
            d_status = self.download(download_time)
            # Checks if download completed successfully or not
            if d_status:
                self.csv_format(column_order, save_path, cols_to_convert, typ, extension)
            else:
                self.driver.close()
                return 'Download Failed'
        else:
            self.driver.close()
            return 'QV Old'
        self.driver.close()
        return True


    def er_v2(self, bookmark_name, save_path, export_format='csv', direct_export=True, filter_name='', start_date='', stop_date='', concept='Home Center', user='Omkar', filters=10, single_value_filter=''):
        self.driver = self.start_browser('https://lmer.landmarkgroup.com/my.policy')
        while True:
            if len(self.driver.find_elements(By.CLASS_NAME , 'CatalogActionLink')) > 0:
                elements = self.driver.find_elements(By.CLASS_NAME , 'CatalogActionLink')
                break
            time.sleep(1)
        element_text = [elem.text for elem in elements]
        bookmark_present_status = True if bookmark_name in element_text else False
        if bookmark_present_status:
            print('Bookmark found at homepage')
            while True:
                try:
                    elements[element_text.index(bookmark_name)+3].click()       # Clicks the More button
                    break
                except:
                    print('Unable to find {} in list. It should be in the list'.format(bookmark_name))
                    elements = self.driver.find_elements(By.CLASS_NAME , 'CatalogActionLink')
                    element_text = [elem.text for elem in elements]
                    time.sleep(1)
        else:
            print(element_text)
            print('Bookmark not found in homepage, navigating the catalog')
            ######################### CATALOG NAVIGATION
            for element in self.driver.find_elements(By.CLASS_NAME, 'HeaderMenuBarText.HeaderMenuNavBarText'):
                if element.text == 'Catalog':
                    element.click()           # Clicks catalog in the navigation bar
                    break
            status = 0
            while status == 0:
                for element in self.driver.find_elements(By.CLASS_NAME, 'ListItem.masterAccordionBottomContentAreaPanel.CatalogListVerboseCell'):
                    if element.find_element(By.CLASS_NAME, 'masterHeader.CatalogObjectListItemTitle').text == 'Concepts':
                        if element.find_element(By.CLASS_NAME, 'CatalogActionLink').text == 'Expand':
                            element.find_element(By.CLASS_NAME, 'CatalogActionLink').click()
                            status = 1
                            break

            status = 0
            while status == 0:
                for element in self.driver.find_elements(By.CLASS_NAME, 'ListItem.masterAccordionBottomContentAreaPanel.CatalogListVerboseCell'):
                    if element.find_element(By.CLASS_NAME, 'masterHeader.CatalogObjectListItemTitle').text == concept:
                        if element.find_element(By.CLASS_NAME, 'CatalogActionLink').text == 'Expand':
                            element.find_element(By.CLASS_NAME, 'CatalogActionLink').click()
                            status = 1
                            break
            status = 0
            while status == 0:
                for element in self.driver.find_elements(By.CLASS_NAME, 'ListItem.masterAccordionBottomContentAreaPanel.CatalogListVerboseCell'):
                    if element.find_element(By.CLASS_NAME, 'masterHeader.CatalogObjectListItemTitle').text == user:
                        if element.find_element(By.CLASS_NAME, 'CatalogActionLink').text == 'Expand':
                            element.find_element(By.CLASS_NAME, 'CatalogActionLink').click()
                            status = 1
                            break
            if direct_export:
                status = 0
                while status == 0:
                    for element in self.driver.find_elements(By.CLASS_NAME, 'ListItem.masterAccordionBottomContentAreaPanel.CatalogListVerboseCell'):
                        if element.find_element(By.CLASS_NAME, 'masterHeader.CatalogObjectListItemTitle').text == bookmark_name:
                            if element.find_elements(By.CLASS_NAME, 'CatalogActionLink')[2].text == 'More':
                                element.find_elements(By.CLASS_NAME, 'CatalogActionLink')[2].click()
                                status = 1
                                break
                        time.sleep(1)
        ########################## DIRECT EXPORT MODE ##########################
        if direct_export:
            print('Entering Direct Export Mode')
            for element in self.driver.find_elements(By.CLASS_NAME, 'contextMenuOptionText'):       # Clicks the Export button
                if element.text == 'Export':
                    element.click()
                    print('Export clicked')
                    break
            for element in self.driver.find_elements(By.CLASS_NAME, 'contextMenuOptionText'):       # Click Data
                if element.text == 'Data':
                    element.click()
                    print('Data clicked')
                    break
            if export_format == 'csv':
                self.driver.find_element(By.ID, 'menuOptionItem_CSV').click()                           # Export CSV
                print('Exporting to CSV')
            elif export_format == 'xlsx':
                self.driver.find_element(By.ID, 'menuOptionItem_Excel').click()                         # Export as Excel
                print('Exporting to Excel')
            
            while True:     # Wait for the download confirmation popup to show up
                time.sleep(1)
                if self.driver.find_element(By.CLASS_NAME, 'dialogTitle').text == 'Confirmation':
                    self.logger.debug('{} downloaded successfuly'.format(bookmark_name))
                    break

            self.get_latest_download(export_format)
            shutil.move(self.most_recent_file, save_path)
            self.driver.close()
            return True
        ########################## EDIT MODE ##########################
        else:
            print('Entering Edit Mode')
            if bookmark_present_status:
                while True:
                    try:
                        elements[element_text.index(bookmark_name)+2].click()
                    except:
                        # self.logger.warning('Cannot find the specified bookmark')
                        time.sleep(1)
                        elements = self.driver.find_elements(By.CLASS_NAME , 'CatalogActionLink')
                        element_text = [elem.text for elem in elements]
                    else:
                        break
            else:
                status = 0
                while status == 0:
                    for element in self.driver.find_elements(By.CLASS_NAME, 'ListItem.masterAccordionBottomContentAreaPanel.CatalogListVerboseCell'):
                        if element.find_element(By.CLASS_NAME, 'masterHeader.CatalogObjectListItemTitle').text == bookmark_name:
                            if element.find_elements(By.CLASS_NAME, 'CatalogActionLink')[1].text == 'Edit':
                                element.find_elements(By.CLASS_NAME, 'CatalogActionLink')[1].click()
                                status = 1
                                break
                        time.sleep(1)

            try:        # Click Criteria tab
                element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'criteriaTab_tab')))
            finally:
                element.click()

            self.edit_filter(filter_name, start_date, stop_date, filters, single_value_filter)

            try:        # Click Results tab
                element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'resultsTab_tab')))
            finally:
                element.click()
            try:        # Click export button
                element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'idAnswersCompoundViewToolbar_export_image')))
            finally:
                element.click()
            try:        # Click data in the dropdown
                element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.NAME, 'exportData')))
            finally:
                element.click()
            try:        # Click CSV in the extended menu after dropdown from data
                element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.NAME, 'csv')))
            finally:
                element.click()


            while True:
                try:
                    self.driver.find_element(By.NAME, 'OK').click()
                except:
                    time.sleep(1)
                    continue
                else:
                    break
            # return self.driver
            self.get_latest_download(export_format)
            shutil.move(self.most_recent_file, save_path)
            self.driver.close()
            return True

    def edit_filter(self, filter_name, start_date, stop_date, filters, single_value_filter=''):
        index = 99999
        try:        # Click Results tab
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'cell1_hightlightrow0_hightlighttable0'))
            )
        finally:
            for i in range(filters):
                if filter_name in self.driver.find_element(By.ID, 'cell1_hightlightrow' + str(i) + '_hightlighttable0').text:
                    index = str(i)
                    break
        if index == str(99999):      # If index not changed equals edit filter was not found for the filter specified
            return False
        # Click the edit filter button for that specific filter
        selected_filter = self.driver.find_element(By.ID, 'floatcell_hightlightrow' + index + '_hightlighttable0')
        selected_filter.find_element(By.XPATH, ".//img[@title='Edit Filter']").click()

        if filter_name == 'Date':
            final_expected_text = 'Date  is between  ' + start_date + ' and ' + stop_date
            self.driver.find_elements(By.ID, 'datePicker_D')[0].clear()
            self.driver.find_elements(By.ID, 'datePicker_D')[0].send_keys(start_date)
            self.driver.find_elements(By.ID, 'datePicker_D')[1].clear()
            self.driver.find_elements(By.ID, 'datePicker_D')[1].send_keys(stop_date)
            self.driver.find_element(By.NAME, 'OK').click()

            # Check if the date filter has been applied correctly or not
            if self.driver.find_element(By.ID, 'cell1_hightlightrow' + index + '_hightlighttable0').text == final_expected_text:
                # log filter applied successfully
                return True
        if filter_name == 'Territory':
            self.driver.find_elements(By.ID, 'dropdownid')[0].clear()
            self.driver.find_elements(By.ID, 'dropdownid')[0].send_keys(single_value_filter)
            self.driver.find_element(By.NAME, 'OK').click()
        if filter_name == 'Location Code':
            self.driver.find_elements(By.ID, 'dropdownid')[0].clear()
            self.driver.find_elements(By.ID, 'dropdownid')[0].send_keys(single_value_filter)
            self.driver.find_element(By.NAME, 'OK').click()

    def init_logger(self, logger_name, log_path):
        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = False
        if not len(self.logger.handlers):
            self.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')
            file_handler = logging.FileHandler(log_path)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def start_browser(self, url):
        self.driver = webdriver.Chrome(service=self.chrome_service)
        self.driver.get(url)
        usrname = self.qv_usrname
        pswd = self.qv_pswd
        if 'lmer' in url:
            usrname = self.er_usrname
            pswd = self.er_pswd
            try:
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'click here.'))
                )
            except:
                self.logger.error('Stuck at login screen! Click here button not available')
            else:
                self.driver.find_element(By.PARTIAL_LINK_TEXT, 'click here.').click()
        self.driver.find_element(By.NAME, 'username').send_keys(usrname)
        self.driver.find_element(By.NAME, 'password').send_keys(pswd)
        self.driver.find_element(By.CLASS_NAME, 'credentials_input_submit').click()
        return self.driver

    def download(self, export_wait_time):
        self.logger.debug('Attempting Download')
        status = 0
        while status == 0:
            table = self.driver.find_element(By.XPATH, "//div[starts-with(@class, 'QvFrame Document_CH')]")
            if table.get_attribute('objsubtype') == 'CH' and table.get_attribute('objtype') == 'Grid':
                action = ActionChains(self.driver)
                action.context_click(table).perform()
                status = 1
        time.sleep(0.5)
        for element in self.driver.find_elements(By.CLASS_NAME, 'ctx-menu-text'):
            if element.text =='Export...':
                element.click()
                break
        t_end = time.time() + export_wait_time
        status = 0
        while True and time.time() <= t_end:
            if len(self.driver.window_handles) > 1:
                status = 1
                break
        if status == 0:
            print('beeg sheet')
            self.logger.warning('File not downloaded! Rerun the code')
            return False
        self.logger.debug('File downloaded successfully')
        return True

    def download_v2(self, export_format, export_wait_time):
        self.logger.debug('Attempting Download')
        status = 0
        while status == 0:
            table = self.driver.find_element(By.XPATH, "//div[starts-with(@class, 'QvFrame Document_CH')]")
            if table.get_attribute('objsubtype') == 'CH' and table.get_attribute('objtype') == 'Grid':
                action = ActionChains(self.driver)
                action.context_click(table).perform()
                status = 1
        time.sleep(0.5)
        for element in self.driver.find_elements(By.CLASS_NAME, 'ctx-menu-text'):
            if element.text ==export_format:
                element.click()
                break
        t_end = time.time() + export_wait_time
        status = 0
        while True and time.time() <= t_end:
            if len(self.driver.window_handles) > 1:
                status = 1
                break
        if status == 0:
            print('beeg sheet')
            self.logger.warning('File not downloaded! Rerun the code')
            return False
        self.logger.debug('File downloaded successfully')
        return True


    def strip_chars(self, vals):
        final = []
        for x in vals:
            x = str(x)
            pattern = re.compile(r'[^\d.]+')
            if x[0] == '-':
                final.append(float('-'+pattern.sub('', str(x))))
            else:
                final.append(float(pattern.sub('', str(x))))
        return final

    def strip_chars_v2(self, vals):
        final = []
        for x in vals:
            x = str(x)
            pattern = re.compile(r'[^\d.]+')
            if x[0] == '-':
                try:
                    final.append(float('-'+pattern.sub('', str(x))))
                except:
                    final.append(0)
            elif x[0] == '.' or x == '':
                return 0
            else:
                final.append(float(pattern.sub('', str(x))))
        return final

    def strip_chars_v3(self, df, column_names):
        df_old = df.copy()
        # Compile the regex pattern to remove non-numeric characters except '-' and '.'
        pattern = re.compile(r'[^\d.-]+')
        
        # Loop through each column and apply the cleaning and conversion
        try:
            for column in column_names:
                df[column] = (
                    df[column]
                    .astype(str)  # Ensure the column is string type for regex application
                    .str.replace(pattern, '', regex=True)  # Remove unwanted characters
                    .astype(float)  # Convert the cleaned strings to float
                )
        except:
            print('{} column failing, check manually. Returning old df'.format(column))
            return df_old
        else:
        # df[column_names] = df[column_names].apply(pd.to_numeric, errors='coerce')
        # df[column_names] = df[column_names].fillna(0)
            return df

    def gen_read_uda_lite(self):
        uda_path = os.path.join(r'C:\Users', getpass.getuser(), r'OneDrive - Landmark Group\Work\Automations\GUI\gen_uda_lite.xlsm')
        self.call_macro(uda_path, ['CompressLatestUDAFile'])
        print('Finished generating UDA lite')
        uda_lite_path = os.path.join(r'C:\Users', getpass.getuser(), r'Desktop\uda_lite.xlsx')
        df = pd.read_excel(uda_lite_path)
        print('Finished reading UDA lite')
        return df
    
    def get_latest_download(self, extension='csv'):
        time.sleep(1)
        downloads_path = str(Path.home() / "Downloads")
        files = glob.glob(downloads_path + r'\*{}'.format(extension))
        if len(files) == 0:
            self.get_latest_download(extension)
        else:
            self.most_recent_file = max(files, key=os.path.getctime)
            diff = datetime.today() - datetime.fromtimestamp(os.path.getmtime(self.most_recent_file))
            if diff.seconds < 30:
                self.logger.debug('Latest downloaded CSV found:%s', self.most_recent_file)
                return self.most_recent_file
            else:
                self.get_latest_download(extension)

    def csv_format(self, column_order, save_path, cols_to_convert_to_float, typ, extension='csv'):
        self.get_latest_download(extension)
        filename = os.path.basename(save_path)
        try:
            df = pd.read_csv(self.most_recent_file, parse_dates=['Date'], dayfirst=True)[1:]
        except:
            df = pd.read_csv(self.most_recent_file)[1:]
        if len(column_order) != 0:
            df = df[column_order]
        else:
            self.logger.warning('No column order list provided.... saving file with the order of columns as provided by QV!')
        if len(cols_to_convert_to_float) != 0:
            df[cols_to_convert_to_float] = df[cols_to_convert_to_float].apply(self.strip_chars_v2)
            if typ == 'float':
                df[cols_to_convert_to_float] = df[cols_to_convert_to_float].astype('float32')
            elif typ == 'int':
                df[cols_to_convert_to_float] = df[cols_to_convert_to_float].astype('int32')
        else:
            self.logger.warning("""Column types for numeric columns were not changed and are still string. This is result in an error in excel 
            saying number stored as text. To correct this please specify the columns which need to get converted to numeric using
            the list 'cols_to_convert_to_float'!""")

        if 'Date' in df.columns:
            # print('we be where? we be here')
            df['Date'] = df['Date'].dt.strftime('%d/%m/%Y')
            # print(df['Date'][:10])

        if 'csv' in save_path:
            df.to_csv(save_path, index=False)
        elif 'xlsx' in save_path:
            df.to_excel(save_path, index=False)
        elif 'parquet' in save_path:
            df.to_parquet(save_path, index=False)
        self.logger.debug('{} saved successfully'.format(filename))
        os.remove(self.most_recent_file)

    def check_update(self):
        status = 0
        while status == 0:
            elems = self.driver.find_elements(By.CLASS_NAME, 'QvContent')
            elems = [elem.text.split('\n') for elem in elems]
            for i in range(len(elems)):
                if 'Last Refresh:  ' in elems[i]:
                    lr_index = i
                    status = 1
                    break
        lr = elems[lr_index][1].split(',')[0]
        lr = datetime.strptime(lr, '%d-%b-%Y').strftime('%d-%m-%Y')
        today = datetime.now().date().strftime('%d-%m-%Y')
        if lr == today:
            return True
        else:
            self.logger.warning('QV is not refreshed... Aborting download!')
            return False
        
    def set_xml_property(self, child_node):
        tree = ET.parse(self.xml_path)
        Files = tree.getroot()
        for child in Files:
            if child.tag == child_node:
                child.set('Last_Successful_Run', datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
                break
        tree.write(self.xml_path, encoding="utf-8")
        self.logger.debug('XML updated')

    def call_macro(self, excel_file_path, macro_name):
        xlapp = win32com.client.DispatchEx("Excel.Application")
        filename = os.path.basename(excel_file_path)
        try:
            wb = xlapp.Workbooks.Open(excel_file_path)
        except:
            self.logger.error('FileNotFoundError: {}'.format(filename))
            xlapp.Application.Quit()
            return 0
        xlapp.DisplayAlerts = False
        self.logger.debug('{} loaded, please do not open the file'.format(filename))
        for macro in macro_name:
            xlapp.Run(macro)
            self.logger.debug('Macro {} completed'.format(macro))
        wb.Save()
        wb.Close()
        self.logger.debug('{} closed'.format(filename))
        xlapp.Application.Quit()

    def refresh_excel(self, excel_file_path):
        xlapp = win32com.client.DispatchEx("Excel.Application")
        filename = os.path.basename(excel_file_path)
        try:
            wb = xlapp.Workbooks.Open(excel_file_path)
        except:
            self.logger.error('FileNotFoundError: {}'.format(filename))
            xlapp.Application.Quit()
            return 0
        xlapp.DisplayAlerts = False
        self.logger.debug('{} loaded, please do not open the file'.format(filename))
        wb.RefreshAll()
        xlapp.CalculateUntilAsyncQueriesDone()
        self.logger.debug('{} refreshed'.format(filename))
        wb.Save()
        wb.Close()
        xlapp.Quit()
        self.logger.debug('{} closed'.format(filename))
        xlapp = None
        del xlapp

    def send_mail(self, to_list, cc_list, subject, attachments=[], html_body='', body='', send_flag=False):
        outlook = win32com.client.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = to_list
        mail.CC = cc_list
        mail.Subject = subject
        if body == '' and html_body != '':
            mail.HTMLBody = html_body
        elif(body != '' and html_body == ''):
            mail.Body = body
        if len(attachments) > 0:
            for attachment in attachments:
                mail.Attachments.Add(attachment)
        if send_flag:
            mail.Send()
        else:
            mail.Display()

    def download_lx_days(self, stop_date, url, include_today, check_date_filter):
        print('')
        elems = self.driver.find_elements(By.CLASS_NAME,'QvGrid')
        for elem in elems:
            if elem.text == 'Date':
                try:
                    elem.click()
                    break
                except:
                    print('Date already clicked.... skipping to date selection')
        time.sleep(2)
        elems = self.driver.find_elements(By.CLASS_NAME,'QvOptional')
        dates = [elem.text for elem in elems]
        stop_date = datetime.strptime(stop_date, '%d/%m/%Y')
        pattern = '^\d{2}/\d{2}/\d{4}'
        ActionChains(self.driver).key_down(Keys.CONTROL).perform()
        count = 0
        for elem, date in zip(elems, dates):
            if not include_today and date == datetime.today().strftime('%d/%m/%Y'):
                continue
            else:
                if re.search(pattern, date):
                    elem.click()
                    time.sleep(0.5)
                    if datetime.strptime(date, '%d/%m/%Y') <= stop_date:
                        ActionChains(self.driver).key_up(Keys.CONTROL).perform()
                        break
        if check_date_filter:
            first_date = datetime(2020,1,1)
            while first_date != stop_date:
                if 'com%20analysis%20%2D%20pdp%20homecentre.qvw' in url:
                    try:
                        for idx, element in enumerate(self.driver.find_elements(By.CSS_SELECTOR, 'div.page')):
                            texts = element.text.split('\n')
                            for tidx, telement in enumerate(texts):
                                if re.search(pattern, telement):
                                    index = idx
                                    tindex = tidx
                                    # break
                                    first_date = datetime.strptime(self.driver.find_elements(By.CSS_SELECTOR, 'div.page')[index].text.split('\n')[tindex], '%d/%m/%Y')
                                    if first_date == stop_date:
                                        break
                    except:
                        time.sleep(1)
                        print('sheeeet 1')
                        continue
                else:
                    try:
                        for idx, element in enumerate(self.driver.find_elements(By.CSS_SELECTOR, 'div.page')):
                            if re.search(pattern, element.text):
                                index = idx
                                # break
                                first_date = datetime.strptime(self.driver.find_elements(By.CSS_SELECTOR, 'div.page')[index].text.split('\n')[0], '%d/%m/%Y')
                                if first_date == stop_date:
                                    break
                    except:
                        time.sleep(1)
                        continue
                time.sleep(1)
            if first_date == stop_date:
                return True
            else:
                return False
        else:
            time.sleep(10)
            return True

