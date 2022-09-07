from scrappers.page_loader import PageLoader
from scrappers.spain_scrap import get_union_spain_data
from scrappers.latvia_scrap import get_union_latvia_data
from scrappers.lithuania_scrap import get_union_lithuania_data
from scrappers.thailand_scrap import get_union_thailand_data
from scrappers.polish_scrap import PolishScraper
from es.EsDumper import EsDumper
from time import sleep
import json


def main():

    sleep(10)
    loader = PageLoader()
    while True:
        spain_data = {}
        # spain_data = get_union_spain_data(loader)
        with open("scrappers/spain_data.json", "r", encoding="utf-8") as file:
            spain_data = json.load(file)
        latvia_data = get_union_latvia_data(loader)
        lithuania_data = get_union_lithuania_data()
        polish_data = PolishScraper().get_union_poland_data()
        thailand_data = get_union_thailand_data(loader)

        es_dumper.init_indices(spain_data, "spain")
        es_dumper.init_indices(latvia_data, "latvia")
        es_dumper.init_indices(lithuania_data, "lithuania")
        es_dumper.init_indices(polish_data, "poland")
        es_dumper.init_indices(thailand_data, "thailand")

        print("DONE insert into ES")
        sleep(120)


if __name__ == "__main__":
    es_dumper = EsDumper()
    main()
