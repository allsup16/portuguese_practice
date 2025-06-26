import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import sql_job
import Sele_General
import csv_out
from datetime import datetime


db = "./CPV"
table ="CPVs"
csv_ ="./CPV"
site = 'https://www.base.gov.pt/Base4/en/'
cpv = ['30192000-1']
setup_columns_link = 'https://www.base.gov.pt/Base4/en/detail/?type=contratos&id=11512833'





def main():
    driver = Sele_General.selenium(['Edge',"google",[1,2]])
    driver.open_edge()
    driver.navigate_address_bar(site) 
    columns = {"publication_date": "DATE","contract_types": "TEXT","framework_agreement_nr": "TEXT",
    "framework_agreement_description": "TEXT","special_measure_typology": "TEXT","procedure_type": "TEXT",
    "description": "TEXT","fundamentation": "TEXT","justification_direct_award": "TEXT",
    "regime": "TEXT","material_criteria": "TEXT","contracting_entities": "TEXT",
    "contracted_entities": "TEXT","contract_object": "TEXT","centralized_procedure": "TEXT",
    "cpvs": "TEXT","contract_date": "DATE","contract_value": "TEXT",
    "execution_deadline": "TEXT","execution_place": "TEXT","competing_entities": "TEXT",
    "announcement": "TEXT","procedure_parts": "TEXT","contractual_modifications": "TEXT",
    "documents": "TEXT","observations": "TEXT","environmental_criteria": "TEXT",
    "justification_not_written": "TEXT","warning": "TEXT","end_of_contract_cause": "TEXT","contract_closure_date": "DATE",
    "total_effective_price": "TEXT","deadline_change_causes": "TEXT","price_change_causes": "TEXT",
    "collected_date":"DATE"
    }

    unique = ["contract_date", "contract_object", "contracted_entities", "contract_value"]

    sql_job.create_table_statement(db,table,columns=columns,unique=unique)

    
    #entries = {}
    #for col in columns:
    #    entries[col] = ''


    for entry in cpv:
        button = driver.find_elements(By.XPATH,'//*[@id="advanced_contratos"]')#find advanced search button
        driver.click(button[0][0])
        CPVinput = driver.find_elements(By.XPATH,'//*[@id="cpv"]')#find cpv input section
        driver.location(CPVinput[0][0])
        driver.click(CPVinput[0][0])
        driver.typing(entry,enter=True)
        driver.wait_to_load(By.CSS_SELECTOR, '#no-more-tables-mx767 table tbody tr:nth-child(1)', sleep=200, only_visual=True)
        for child in range(1,5):#len(total_rows)+1):
                rows = driver.find_elements(By.CSS_SELECTOR, '#no-more-tables-mx767 > table > tbody > tr')
                if child > len(rows):
                    print(f"⚠️ Row #{child} no longer exists.")
                    break
                selector = f'#no-more-tables-mx767 > table > tbody > tr:nth-child({child}) > td:nth-child(7) > a'
                result_button = driver.find_element(By.CSS_SELECTOR,selector)
                driver.click(result_button)
                driver.switch_tab(mode="wait_latest")
                driver.custom_sleep(15)
                
                column_names = sql_job.all_column_names_stripped(sql_job.all_column_names(db,table))
                insert_list = dict.fromkeys(column_names,None)
                col_keys = list(insert_list.keys())
                for i, col_name in enumerate(col_keys):
                    child_index = i + 1  # td:nth-child is 1-indexed
                    value = None
                    try:
                        selector = f'#no-more-tables-mx767>table:nth-child(1)>tbody>tr:nth-child({child_index})>td'
                        td_data = driver.find_elements(By.CSS_SELECTOR, selector, get_text=True)
                        value = td_data[0][0].strip()
                    except Exception as e:
                        if col_name == 'collected_date':
                            value = datetime.today().strftime('%Y-%m-%d')
                        else:
                            value = '-'

                    insert_list[col_name] = value
                sql_job.insert(db,table,insert_list)
                
                driver.switch_tab(mode='original')
    csv_out.export_sqlite_to_csv(db,table,csv_)
    driver.close_page()
main()