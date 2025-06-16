import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import sql_job
import Sele_General
import csv_out
from datetime import datetime


db = "./Deliverables/Portugese-Site/CPV"
table ="CPVs"
csv_ ="./Deliverables/Portugese-Site/CPV"
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

    unique = ["publication_date","contract_types", "framework_agreement_nr", "framework_agreement_description", "special_measure_typology",
    "procedure_type", "description", "fundamentation", "justification_direct_award",
    "regime", "material_criteria", "contracting_entities", "contracted_entities", "contract_object",
    "centralized_procedure", "cpvs", "contract_date", "contract_value", "execution_deadline", "execution_place",
    "competing_entities", "announcement", "procedure_parts", "contractual_modifications", "documents", "observations",
    "environmental_criteria", "justification_not_written", "warning", "end_of_contract_cause",
    "contract_closure_date", "total_effective_price", "deadline_change_causes", "price_change_causes"]
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
        driver.wait_to_load(By.CSS_SELECTOR, '#no-more-tables-mx767 table tbody tr:nth-child(1)', sleep=30, only_visual=True, new_page_timer=200)
        child = 1
        result_button = driver.find_elements(By.CSS_SELECTOR,f'#no-more-tables-mx767 > table > tbody > tr:nth-child({child}) > td:nth-child(7) > a')
        driver.click(result_button[0][0])
        
        
        driver.wait_for_tab()
        driver.wait_to_load(By.CSS_SELECTOR, '#no-more-tables-mx767>table:nth-child(1)>tbody>tr:nth-child(1)>td', sleep=30, only_visual=True)
        
        columns = sql_job.all_column_names_stripped(sql_job.all_column_names(db,table))
        insert_list = dict.fromkeys(columns,None)
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
        print(sql_job.all_rows(db,table))
    csv_out.export_sqlite_to_csv(db,table,csv_)

    driver.close_page()
main()