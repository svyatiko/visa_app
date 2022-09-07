# import json
import requests

LINK = "https://d2ab400qlgxn2g.cloudfront.net/dev/spaces/xxg4p8gt3sg6/environments/master/entries"

headers = {
    "Host": "d2ab400qlgxn2g.cloudfront.net",
    "Sec-Ch-Ua": '"(Not(A:Brand";v="8", "Chromium";v="99"',
    "Accept": "application/json, text/plain, */*",
    "Authorization": "Bearer 5YpTBRikGN59YHwM18CyGr5F43bFuaak9U8FSMEDmb8",
    "Sec-Ch-Ua-Mobile": "?0",
    "X-Contentful-User-Agent": "sdk contentful.js/0.0.0-determined-by-semantic-release; platform browser; os Windows;",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Origin": "https://visa.vfsglobal.com",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://visa.vfsglobal.com/",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
}

address_params = {
    "content_type": "resourceGroup",
    "fields.locale": "vfs&ru&ltu&ltu > ru&ltu > blr&ltu > blr > ru",
    "limit": "500",
}


time_params = {
    "content_type": "countryLocation",
    "fields.title[match]": "ltu > blr > ru",
    "order": "fields.vacName",
    "limit": "200",
}

news_params_1 = {
    "content_type": "countryNews",
    "fields.locale": "ltu > blr > ru&ltu > ru",
    "sys.updatedAt[gte]": "2022-05-11T21:00:00.000Z",
}

news_params_2 = {
    "content_type": "countryNews",
    "fields.locale": "ltu > blr > ru&ltu > ru",
    "fields.permanent": "true",
}

# visaac
def parse_info_visa_centre() -> dict:
    response = requests.get(
        LINK,
        headers=headers,
        params=address_params,
        verify=False,
    )
    data = response.json()
    phone = data["items"][4]["fields"]["resources"]["contactus.phonenumber1"]
    email = data["items"][4]["fields"]["resources"]["contactus.emailaddress2"]
    info = dict()
    info["Страна"] = "Литва"
    info["Телефон"] = phone
    info["Email"] = email
    return info


def parse_visa_centre() -> list:
    response_address = requests.get(
        LINK,
        headers=headers,
        params=address_params,
        verify=False,
    )
    address_data = response_address.json()

    response_time = requests.get(
        LINK,
        headers=headers,
        params=time_params,
        verify=False,
    )
    time_data = response_time.json()

    minsk_address = {
        "ADRESS": address_data["items"][4]["fields"]["resources"]["vacaddress.minsk"],
    }
    gomel_address = {
        "ADRESS": address_data["items"][4]["fields"]["resources"]["vacaddress.gomel"],
    }
    mogilev_address = {
        "ADRESS": address_data["items"][4]["fields"]["resources"]["vacaddress.mogilev"],
    }
    vitebsk_address = {
        "ADRESS": address_data["items"][4]["fields"]["resources"]["vacaddress.vitebsk"],
    }
    brest_address = {
        "ADRESS": address_data["items"][4]["fields"]["resources"]["vacaddress.brest"],
    }
    baranovichi_address = {
        "ADRESS": address_data["items"][4]["fields"]["resources"][
            "vacaddress.baranovichi"
        ],
    }
    pinsk_address = {
        "ADRESS": address_data["items"][4]["fields"]["resources"]["vacaddress.pinsk"],
    }
    grodno_address = {
        "ADRESS": address_data["items"][4]["fields"]["resources"]["vacaddress.grodno"],
    }
    lida_address = {
        "ADRESS": address_data["items"][4]["fields"]["resources"]["vacaddress.lida"],
    }

    for town in time_data["items"]:
        if town["fields"]["vacName"] == "Минск":
            minsk_address["APPLY_WORKING_HOURS"] = " ".join(
                list(town["fields"]["openingHoursObject"][0].values())
            )
            minsk_address["ISSUE_WORKING_HOURS"] = " ".join(
                list(town["fields"]["openingHoursObject"][1].values())
            )
        if town["fields"]["vacName"] == "Гомель":
            gomel_address["APPLY_WORKING_HOURS"] = " ".join(
                list(town["fields"]["openingHoursObject"][0].values())
            )
            gomel_address["ISSUE_WORKING_HOURS"] = " ".join(
                list(town["fields"]["openingHoursObject"][1].values())
            )
        if town["fields"]["vacName"] == "Могилев":
            mogilev_address["APPLY_WORKING_HOURS"] = " ".join(
                list(town["fields"]["openingHoursObject"][0].values())
            )
            mogilev_address["ISSUE_WORKING_HOURS"] = " ".join(
                list(town["fields"]["openingHoursObject"][1].values())
            )
        if town["fields"]["vacName"] == "Витебск":
            vitebsk_address["APPLY_WORKING_HOURS"] = " ".join(
                list(town["fields"]["openingHoursObject"][0].values())
            )
            vitebsk_address["ISSUE_WORKING_HOURS"] = " ".join(
                list(town["fields"]["openingHoursObject"][1].values())
            )
        if town["fields"]["vacName"] == "Брест":
            brest_address["APPLY_WORKING_HOURS"] = " ".join(
                list(town["fields"]["openingHoursObject"][0].values())
            )
            brest_address["ISSUE_WORKING_HOURS"] = " ".join(
                list(town["fields"]["openingHoursObject"][1].values())
            )
        if town["fields"]["vacName"] == "Барановичи":
            baranovichi_address["APPLY_WORKING_HOURS"] = " ".join(
                list(town["fields"]["openingHoursObject"][0].values())
            )
            baranovichi_address["ISSUE_WORKING_HOURS"] = " ".join(
                list(town["fields"]["openingHoursObject"][1].values())
            )
        if town["fields"]["vacName"] == "Пинск":
            pinsk_address["APPLY_WORKING_HOURS"] = " ".join(
                list(town["fields"]["openingHoursObject"][0].values())
            )
            pinsk_address["ISSUE_WORKING_HOURS"] = " ".join(
                list(town["fields"]["openingHoursObject"][1].values())
            )
        if town["fields"]["vacName"] == "Гродно":
            grodno_address["APPLY_WORKING_HOURS"] = " ".join(
                list(town["fields"]["openingHoursObject"][0].values())
            )
            grodno_address["ISSUE_WORKING_HOURS"] = " ".join(
                list(town["fields"]["openingHoursObject"][1].values())
            )
        if town["fields"]["vacName"] == "Лида":
            lida_address["APPLY_WORKING_HOURS"] = " ".join(
                list(town["fields"]["openingHoursObject"][0].values())
            )
            lida_address["ISSUE_WORKING_HOURS"] = " ".join(
                list(town["fields"]["openingHoursObject"][1].values())
            )

    visa_centre = [
        minsk_address,
        gomel_address,
        mogilev_address,
        vitebsk_address,
        brest_address,
        baranovichi_address,
        pinsk_address,
        grodno_address,
        lida_address,
    ]

    info = parse_info_visa_centre()

    for town in visa_centre:
        town["PHONE_NUMBER"] = info["Телефон"]
        town["EMAIL"] = info["Email"]

    return visa_centre


def get_visa_centre() -> dict:
    visaac = parse_visa_centre()
    return visaac


# news
def get_visa_centres_news() -> list:
    main_link = "https://visa.vfsglobal.com/blr/ru/ltu/"
    response_news_1 = requests.get(
        LINK,
        headers=headers,
        params=news_params_1,
        verify=False,
    )
    news_data_1 = response_news_1.json()
    response_news_2 = requests.get(
        LINK,
        headers=headers,
        params=news_params_2,
        verify=False,
    )
    news_data_2 = response_news_2.json()
    news = []
    for item in news_data_1["items"]:
        body = item["fields"]["intro"]["content"][0]["content"][0]["value"]
        news.append(
            {
                "LINK": main_link + item["fields"]["slug"],
                "TITLE": body[:66] + "...",
                "BODY": body[:255] + "...",
                "DATE": item["fields"]["date"],
            }
        )

    for item in news_data_2["items"]:
        body = item["fields"]["intro"]["content"][0]["content"][0]["value"]
        news.append(
            {
                "LINK": main_link + item["fields"]["slug"],
                "TITLE": body[:66] + "...",
                "BODY": body[:255] + "...",
                "DATE": item["fields"]["date"],
            }
        )
    return news


def get_consulate():
    cons = [
        {
            "ADRESS": "ул. Захарова 68 220088 Минск, Беларусь",
            "EMAIL": " При посылке (досылке) информации, необходимой для приема решения о выдаче визы, по эл. почте в тексте письма (не в приложениях) необходимо указать, когда были переданы документы, в какое окно, имя и фамилию заявителя, для которого досылаются документы, а также необходимо указать контакты отправителя письма. Письма с приложениями без указанной информации Посольством не рассматриваются. Документы, поступившие в Посольство по электронной почте, не будут приложены к Вашему ходатайству, если они не были запрошены Посольством.",
            "WORKING_HOURS": "ВИЗЫ  Понедельник - Пятница  9.00-13.00 (прием документов для получения визы)  Понедельник - Четверг  16.00-17.00,  Пятница  15.00-16.00 (выдача паспортов) КОНСУЛЬСКАЯ ПОМОЩЬ  Вторник - Четверг  14.00-16.30 (приём и консультации по вопросам гражданства, разрешений на временное проживание на территории Литовской Республики, получения, замены паспортов граждан Литовской Республики, консульских справок, свидетельств (метрик), нотариальные действия)  Вторник - Четверг  16.30-17.00 (выдача паспортов, консульских справок, свидетельств)",
            "PHONE_NUMBER_1": "+375 17 285 2449",
            "PHONE_NUMBER_2": "+375 17 285 2448",
        }
    ]
    return cons


def get_union_lithuania_data():
    visa_centre = get_visa_centre()
    news = get_visa_centres_news()
    consulates = get_consulate()
    data = {"VISAAC": visa_centre, "CONSULATE": consulates, "NEWS": news}
    # with open("data1.json", "w", encoding="utf-8") as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)
    return data


# get_union_lithuania_data()
