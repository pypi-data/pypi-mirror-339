
# Inhouse Automation Library for HC

After pip install is complete run the following in the command line. This will create a directory in your One Drive - C:\Users\USER_ID\OneDrive - Landmark. Group\Work\Automations\GUI. This setup file will promt you for your QV username & pswd and ER username & pswd. The password is hidden by default and you will not see the characters as you type.
```python
python -m hcautomation.post_install_setup
```
*Your login credentials are then securely encrypted and stored in a format that is not readable.

To use this library, import the following class & create an object of this class using:

```python
  from hcautomation import Download
  obj = Download('name_of_project')
```


## Library Usage
#### QV Download
This function downloads data from a QV bookmark.
```python
obj.qv(url, save_path, download_time, column_order=[], cols_to_convert=[], typ='float', lx=False, stop_date='', extension='csv', lx_mon=[], include_today=False, check_date_filter=True)
```

Parameters starting with **!** are REQUIRED, rest are OPTIONAL
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| **!** `url` | `string` | Link to the QV bookmark |
| **!** `save_path`  | `string` |  Path with filename for the save location of file downloaded from QV |
| **!** `download_time` | `int` |  Maximum time to wait for download to finish |
| `column_order` | `list` | Order of columns to reorder columns in downloaded file |
| `cols_to_convert` | `list` | If file is downloaded as CSV, convert given list of columns to float |
| `lx` | `Boolean` | Set to True if you want to select the dates for which data has to be downloaded. |
| `stop_date` | `string` | Download data from this date onwards till today. Format: dd/mm/yyyy |
| `extension` | `string` | File format to download final data in. 'csv' or 'xlsx' |
| `lx_mon` | `string` | WIP |
| `include_today` | `Boolean` | Default False. Download today's data as well if set to True |
| `check_date_filter` | `Boolean` | Default True. Check if date filter has been applied |


#### ER Download
This function downloads data from a ER bookmark.
```python
obj.er_v2(bookmark_name, save_path, export_format='csv', direct_export=True, filter_name='', start_date='', stop_date='', concept='Home Center', user='Omkar', filters=10, single_value_filter=''):
```
Parameters starting with **!** are REQUIRED, rest are OPTIONAL
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| **!** `bookmark_name` | `string` | Name of the bookmark in ER |
| **!** `save_path`  | `string` |  Path with filename for the save location of file downloaded from ER |
| `export_format` | `string` | Defaults to csv, change to 'xlsx' for excel format |
| `direct_export` | `string` | Defaults to True. If set to True, the data will be directly exported from the homepage of ER. If False, it will go into edit more. **!Set to False if you want to modify filters** |
| `filter_name` | `string` | Defaults to blank, change to the name of the filter you want to edit |
| `start_date` | `string` | Defaults to blank. If you are using Date filter then add the start date here in the format 'dd/mm/yyyy' |
| `end_date` | `string` | Defaults to blank. If you are using Date filter then add the end date here in the format 'dd/mm/yyyy' |
| `concept` | `string` | Defaults to 'Home Center', change to your specific concept. This is used if the bookmark is not found in the homepage it will navigate into the folder structure to get the bookmark |
| `user` | `string` | Defaults to 'Omkar', change to your name so it navigates into your folder where the bookmark is stored |
| `filters` | `int` | Defaults to 10. Iterates the over the available filters. Increase it to the number of your filters if you have more than 10  |
| `single_value_filter` | `string` | Defaults to blank. If you have to edit a filter which takes single textbox as input, enter the name of the value to enter in the filter here |

#### Change data type of numeric columns to float64
```python
obj.strip_chars_v3(df, ['col1', 'col2'])
```
Parameters starting with **!** are REQUIRED, rest are OPTIONAL
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| **!** `df` | `dataframe` | Dataframe in which columns need to be converted to float64 |
| **!** `column_names` | `list` | List of columns to convert |

#### Call excel macros
```python
obj.call_macro(excel_file_path, macro_name)
```
Parameters starting with **!** are REQUIRED, rest are OPTIONAL
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| **!** `excel_file_path` | `path` | Absolute path of the excel file |
| **!** `macro_name` | `list` | List of macros to run |

#### Refresh All Data in excel
```python
obj.refresh_excel(excel_file_path)
```
Parameters starting with **!** are REQUIRED, rest are OPTIONAL
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| **!** `excel_file_path` | `path` | Absolute path of the excel file |

#### Send email
```python
obj.send_mail(to_list, cc_list, subject, attachments=[], html_body='', body='', send_flag=False)
```
Parameters starting with **!** are REQUIRED, rest are OPTIONAL
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| **!** `to_list` | `string` | string of all emails in to To: section separated by ; |
| **!** `cc_list` | `string` | string of all emails in to CC: section separated by ; |
| **!** `subject` | `string` | Subject of the mail body |
|`attachments` | `list` | List of attachments with file paths to add in the mail |
|`html_body` | `string` | HTML body part - if excel tables/structured email needs to be sent, insert HTML string here  |
|`body` | `string` | Subject of the mail body |