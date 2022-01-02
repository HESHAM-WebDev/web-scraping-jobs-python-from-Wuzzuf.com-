# step 1 import libraries
import requests
import csv
from bs4 import BeautifulSoup
from itertools import zip_longest

company_location = []
comp_name = []
job_title = []
job_description = []
links = []
salary = []
responsibilites = []
date = []
page_num = 0

while True:
    try:
        result = requests.get(f"https://wuzzuf.net/search/jobs/?q=python&a=navbl={page_num}")
        # step 3 save page content
        src = result.content
        # step 4 using BeautifulSoup
        soup = BeautifulSoup(src, "lxml")
        page_limit = int(soup.find("strong").text)

        if (page_num > page_limit // 15):
            print("ended")

        # step 5 scrap main page
        job_titles = soup.find_all("h2", {"class": "css-m604qf"})
        company_name = soup.find_all("a", {"class": "css-17s97q8"})
        company_address = soup.find_all("span", {"class": "css-5wys0k"})
        job_desc = soup.find_all("div", {"class": "css-y4udm8"})
        posted_new = soup.find_all("div", {"class": "css-4c4ojb"})
        posted_old = soup.find_all("div", {"class": "css-do6t5g"})
        posted = [*posted_new, *posted_old]

        for i in range(len(job_titles)):
            job_title.append(job_titles[i].text)
            links.append("https://wuzzuf.net" + job_titles[i].find("a").attrs['href'])
            company_location.append(company_address[i].text)
            comp_name.append(company_name[i].text)
            job_description.append(job_desc[i].text)
            date.append(posted[i].text)
        page_num += 1
        print("page switched")
    except:
        print("error ")
        break
    for link in links:
        result = requests.get(link)
        src = result.content
        soup = BeautifulSoup(src, "lxml")
        requirements = soup.find("div", {"class": "css-1t5f0fr"}).ul
        respon_text = ""
        print(requirements.text)

        for li in requirements.find_all("li"):
            respon_text += li.text+"| "
            respon_text =respon_text[:-2]
        responsibilites.append(respon_text)

    # step 6 save data in csv file
    file_list = [job_title, comp_name, date, company_location, job_description, links, responsibilites]
    exported = zip_longest(*file_list)
    with open("/home/hesham/Projects/scrppaing/data.csv", "w") as myfile:
        wr = csv.writer(myfile)
        wr.writerow(["job title", "company name", "date", "location", "skills", "links", "responsibilites"])
        wr.writerows(exported)
    # inner pages to get salaries and job requirements
