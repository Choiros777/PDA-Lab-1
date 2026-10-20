import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import json


def parse_vacancies():
    driver = webdriver.Chrome()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    page_url = "https://spb.hh.ru/search/vacancy?area=113"
    vacancies_data = []
    session = requests.Session()
    session.headers.update(headers)

    total_pages = 20
    current_page = 1

    while current_page <= total_pages:
        print(f"\nПарсим страницу {current_page} из {total_pages}...")

        try:
            driver.get(page_url )
            time.sleep(random.uniform(3, 5))

            soup = BeautifulSoup(driver.page_source, "html.parser")

            zero = soup.find("ol", class_=re.compile("vacancies-list"))
            if zero is None:
                print(f"На странице {current_page} вакансии не найдены")
                break

            vacancylist = zero.find_all("li")
            page_count = 0

            for vacancy in vacancylist:
                try:
                    infourl_tag = vacancy.find("a", attrs={"data-qa": "serp-item__title"}, href=True)
                    if not infourl_tag: continue
                    infourl = infourl_tag.get('href')

                    time.sleep(random.uniform(0.5, 1.0))
                    response = session.get(infourl, timeout=10)
                    response.raise_for_status()

                    vacancylink = BeautifulSoup(response.text, "html.parser")
                    name_tag = vacancy.find("span", attrs={"data-qa": "serp-item__title-text"})
                    employer_tag = vacancy.find("span", attrs={"data-qa": "vacancy-serp__vacancy-employer-text"})
                    address_tag = vacancy.find("span", attrs={"data-qa": "vacancy-serp__vacancy-address"})
                    experience = (
                            vacancylink.find("span", attrs={"data-qa": "vacancy-experience"}) or
                            vacancylink.find("p", attrs={"data-qa": "work-experience-text"})
                    )
                    workformat = vacancylink.find(attrs={"data-qa": "work-formats-text"})
                    workinghours = vacancylink.find(attrs={"data-qa": "working-hours-text"})
                    workingdays = vacancylink.find(attrs={"data-qa": "work-schedule-by-days-text"})
                    employmenttype = vacancylink.find(attrs={"data-qa": "common-employment-text"})
                    payfrequency = vacancylink.find(attrs={"data-qa": "compensation-frequency-text"})

                    try:
                        salary_tag = vacancy.find("span", class_=re.compile("magritte-text_typography-label-1-regular"))
                        salary = salary_tag.text if salary_tag else 'None'
                    except:
                        salary = 'None'

                    vacancies_data.append({
                        "name": name_tag.text if name_tag else "None",
                        "employer": employer_tag.text if employer_tag else "None",
                        "address": address_tag.text if address_tag else "None",
                        "salary": salary,
                        "experience": experience.text if experience else "None",
                        "workinghours": workinghours.text if workinghours else "None",
                        "workingdays": workingdays.text if workingdays else "None",
                        "employmenttype": employmenttype.text if employmenttype else "None",
                        "workformat": workformat.text if workformat else "None",
                        "payfrequency": payfrequency.text if payfrequency else "None",
                    })
                    page_count += 1
                except Exception as e:
                    # Если одна вакансия не загрузилась, просто пропускаем
                    continue

            print(f"Со страницы {current_page} спарсено: {page_count} вакансий")
            print(f"Всего в базе: {len(vacancies_data)}")


            if current_page % 5 == 0:
                with open("vacancies_temp.json", "w", encoding="utf-8") as f:
                    json.dump(vacancies_data, f, ensure_ascii=False, indent=2)

            # Пагинация
            pager = soup.find("nav", attrs={"data-qa": "pager-block"})
            if pager:
                next_link = pager.find("a", attrs={"data-qa": "pager-next"})
                if next_link:
                    page_url  = urljoin(page_url , next_link["href"])
                    current_page += 1
                    time.sleep(random.uniform(2, 4))
                else:
                    print("Достигнут конец пагинации")
                    break
            else:
                break

        except Exception as e:
            print(f"Ошибка на странице {current_page}: {e}")
            break

    driver.quit()
    print(f"\nВсего собрано {len(vacancies_data)} вакансий.")
    return vacancies_data