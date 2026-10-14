import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
BASE_URL="https://spb.hh.ru/search/vacancy?area=113"
driver.get(BASE_URL)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


while True:
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
    
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    zero = soup.find("ol", class_="vacancies-list--fKGBxTUjQkIkJ_iZ")
    vacancylist = zero.find_all("li")

    for vacancy in vacancylist:
        infourl =vacancy.find("a",attrs={"data-qa":"serp-item__title"},href=True).get('href')
    
        response = requests.get(infourl, headers=headers)
        vacancylink = BeautifulSoup(response.text, "html.parser") #переход на страницу вакансии

        name = vacancy.find("span", attrs={"data-qa":"serp-item__title-text"}).text #profession
        employer = vacancy.find("span", attrs={"data-qa":"vacancy-serp__vacancy-employer-text"}).text #company, names
        address = vacancy.find("span", attrs={"data-qa":"vacancy-serp__vacancy-address"}).text #city
        experience = vacancylink.find("p", attrs={"data-qa":"work-experience-text"})

        workinghours = vacancylink.find("div", attrs={"data-qa":"working-hours-text"}) #рабочие часы вечерние\кол-во в день
        workingdays = vacancylink.find("p", attrs={"data-qa":"work-schedule-by-days-text"}) #график 5\2 и тд
        employmenttype = vacancylink.find("div", attrs={"data-qa":"common-employment-text"}) #полная\частичная занятость
        workformat = vacancylink.find("p", attrs={"data-qa":"work-formats-text"}) # формат работы - на месте\удаленно\вахта
        payfrequency= vacancylink.find("p", attrs={"data-qa":"compensation-frequency-text"})

        try: #how much per month
            salary = vacancy.find("span", class_="magritte-text___pbpft_5-3-13_xhh magritte-text_style-primary___AQ7MW_5-3-13_xhh magritte-text_typography-label-1-regular___pi3R-_5-3-13_xhh").text
        except AttributeError:
            salary = 'None'


        # try:
        #     expparam = re.compile(r"^vacancy-serp__vacancy-work-experience-")
        #     experience = vacancy.find("div", attrs={"data-qa":expparam}).text 
        # except AttributeError:
        #     experience ="None"

        mydict = {"0":workinghours, "1":workingdays,
                "2":workformat,"3":payfrequency, "4":experience, "5":employmenttype}
        

        for i in range(len(mydict)):
            if (mydict[f"{i}"] is not None):
                mydict[f"{i}"] = mydict[f"{i}"].text
                mydict[f"{i}"] = re.sub(r'^.*?:', ' ',mydict[f"{i}"])
                
            else:
                mydict[f"{i}"] ="None"

        workinghours=mydict["0"]
        workingdays=mydict["1"]
        workformat=mydict["2"]
        payfrequency=mydict["3"]
        experience=mydict["4"]

        print("-----------------------------------------------------------------------")
        print(name, "|", employer, "|", address)
        # print(experience)
        # print(workinghours,"|", workingdays,"|", workformat)
        # print(payfrequency,"|",salary)
    try:
        #собираем следующие страницы
        #ищем pager внизу страницы
        pager = soup.find("nav", attrs={"data-qa": "pager-block"})

        """
        page_links = pager.find_all("a", attrs={"data-qa": "pager-page"})
        for a in page_links:
            num = a.get_text(strip=True)
            href = urljoin(BASE_URL, a["href"])
            current = a.get("aria-current") == "true"
            print(f"Стр. {num}{' (текущая)' if current else ''}: {href}")
        """
        # Ссылка "вперёд" (стрелочка →)
        #next_link = pager.find("a", attrs={"data-qa": "pager-next"})
        #if next_link:
            #print("Следующая:", urljoin(BASE_URL, next_link["href"]))
        """
        # 4. Последняя страница (после "...")
        ellipsis = pager.find("li", attrs={"data-qa": "number-pages-ellipsis"})
        if ellipsis:
            last = ellipsis.find_next("a", attrs={"data-qa": "pager-page"})
            if last:
                print("Последняя страница:", last.get_text(strip=True),
                      "->", urljoin(BASE_URL, last["href"]))
                      """
        #pager-page
        #next_button = driver.find_element(By.CSS_SELECTOR, "button.next-page")
        #next_button.click()
        next_link = driver.find_element(
            By.CSS_SELECTOR, 'a[data-qa="pager-next"]'
        )
        print("****************************************************************************")
        time.sleep(2)  # Wait for the next page to load
    except Exception:
        break

#driver.quit()


        

