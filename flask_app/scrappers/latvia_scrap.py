from bs4 import BeautifulSoup
import requests


""" VISAAC  """

# Minsk visaac


def get_minsk_visaac(soup):

    adress_minsk = soup.find("h5").find_next("p").find_next("p").text
    issue_worktime = soup.find_all("p")[13].text
    apply_worktime = soup.find_all("p")[15].text
    telephone1 = (
        soup.find("h4").find_next_sibling("p").find_next("span").find_next("a").text
    )
    visaac1 = {
        "ADRESS": adress_minsk,
        "ISSUE_WORKING_HOURS": issue_worktime,
        "APPLY_WORKING_HOURS": apply_worktime,
        "PHONE_NUMBER": telephone1,
        "EMAIL": None,
    }
    return visaac1


# Vitebsk visaac
def get_vitebsk_visaac(soup):
    address_vitebsk = soup.find("h5").find_next("p").find_next("p").find_next("p").text
    telephone2 = (
        soup.find("h4")
        .find_next_sibling("p")
        .find_next("span")
        .find_next("a")
        .find_next("a")
        .text
    )
    issue_worktime = soup.find_all("p")[13].text
    apply_worktime = soup.find_all("p")[15].text
    visaac2 = {
        "ADRESS": address_vitebsk,
        "ISSUE_WORKING_HOURS": issue_worktime,
        "APPLY_WORKING_HOURS": apply_worktime,
        "PHONE_NUMBER": telephone2,
        "EMAIL": None,
    }
    return visaac2


def collect_visaac():
    res = requests.get(
        "https://pony-visa.by/ru/contacts",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        },
    )
    soup = BeautifulSoup(res.text, "html.parser")

    list_visaac = []
    list_visaac.append(get_minsk_visaac(soup))
    list_visaac.append(get_vitebsk_visaac(soup))

    return list_visaac


""" Consulate """


def get_vitebsk_consulate(loader):
    url_vitebsk_consulate = "https://www2.mfa.gov.lv/ru/vitebsk"
    page = loader.load_page(url_vitebsk_consulate)
    soup = BeautifulSoup(page, "html.parser")

    info_table = (
        soup.find("div", class_="fulltext").find("table").find("tbody").find_all("tr")
    )

    values = []
    for item in info_table:
        value = (
            item.find_next("td")
            .find_next("td")
            .get_text()
            .strip()
            .replace("\n", "")
            .replace("  ", "")
        )
        values.append(value)

    address = values[0]
    phone = values[1].replace(u"\xa0", u" ")
    time = values[3].split("(")[0].capitalize()

    email = soup.find_all("a", href="mailto:consulate.vitebsk@mfa.gov.lv")
    email = email[-1].text

    consulate = {
        "ADRESS": address,
        "EMAIL": email,
        "PHONE_NUMBER_1": phone,
        "PHONE_NUMBER_2": None,
        "WORKING_HOURS": time,
    }
    return consulate


""" embassy """


def get_minsk_consulate(loader):
    url_time_of_work = "https://www2.mfa.gov.lv/ru/belarus/posolstvo/vremya-raboty"
    url_minsk_consul = "https://www2.mfa.gov.lv/ru/belarus"

    headers = {
        "Accept": "*/*",
        "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)\
    Chrome/98.0.4758.102 Safari/537.36",
    }

    req_time_of_work = requests.get(url_time_of_work, headers=headers)
    src_time_of_work = req_time_of_work.text

    req = requests.get(url_minsk_consul, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, "html.parser").find("div", class_="fulltext")

    address = soup.find_all("td")[1].get_text().strip().partition("(")[0]
    phone_number = (
        soup.find_all("td")[4]
        .find("span", class_="baec5a81-e4d6-4674-97f3-e9220f0136c1")
        .get_text()
        .strip()
    )

    time_of_work = (
        str(
            BeautifulSoup(src_time_of_work, "html.parser")
            .find_all("p")[1]
            .get_text()
            .strip()
        )
        + " "
        + str(
            BeautifulSoup(src_time_of_work, "html.parser")
            .find_all("p")[2]
            .get_text()
            .strip()
        )
    )

    page = loader.load_page(url_minsk_consul)
    soup = BeautifulSoup(page, "html.parser")
    email = soup.find_all("td")[8].find("p").get_text().strip()
    email = email.replace(";", "")

    embassy_information = {
        "ADRESS": address,
        "PHONE_NUMBER_1": phone_number,
        "PHONE_NUMBER_2": None,
        "EMAIL": email,
        "WORKING_HOURS": time_of_work,
    }

    return embassy_information


def collect_consulates(loader):
    consulates = []
    consulates.append(get_minsk_consulate(loader))
    consulates.append(get_vitebsk_consulate(loader))
    return consulates


""" news """


def get_news(loader):
    url = "https://www2.mfa.gov.lv/ru/belarus"
    news = []
    src = loader.load_page(url)

    soup = BeautifulSoup(src, "html.parser")
    data = soup.find_all("p", style="text-align: center;")

    del data[-1]

    for i in data:
        news.append(
            {
                "TITLE": i.text[:66] + "...",
                "BODY": i.text[:250],
                "LINK": url,
                "DATE": None,
            }
        )

    return news


def get_union_latvia_data(loader):
    data = {
        "VISAAC": collect_visaac(),
        "CONSULATE": collect_consulates(loader),
        "NEWS": get_news(loader),
    }
    return data
