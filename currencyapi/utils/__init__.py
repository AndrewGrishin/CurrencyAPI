import re
from time import sleep
from typing import Optional

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tqdm.auto import tqdm


def get_resp(
    url: str,
    params: Optional[dict] = None,
) -> requests.Response:

    if params is None:
        params = dict()

    ua = UserAgent()
    headers = {"UserAgent": ua.random}
    resp = requests.get(
        url=url,
        params=params,
        headers=headers,
    )

    return resp


def get_soup(resp: requests.Response) -> BeautifulSoup:
    return BeautifulSoup(resp.text, "lxml")


def get_val(soup: BeautifulSoup, currency: str) -> float:
    rows = soup.select("table.data tr")[1:]
    rows = list(
        map(
            lambda x: x.text.replace("\n", " ").strip(),
            rows,
        )
    )
    rows = "\n".join(rows)
    usd = re.findall("{}.+".format(currency), rows)[0]
    val = float(usd.split()[-1].replace(",", "."))
    return val


def collect_currency(
    dates: list,
    date_scheme: str,
    scheme: str,
    currency: str,
) -> list:
    data = list()

    pbar = tqdm(dates, ncols=80)
    for date in pbar:
        year, month, day = str(date).split()[0].split("-")
        tmp_date = date_scheme.format(year, month, day)
        pbar.set_description(tmp_date)

        url = scheme.format(day, month)
        resp = get_resp(url=url)
        soup = get_soup(resp=resp)
        val = get_val(
            soup=soup,
            currency=currency,
        )
        data.append((tmp_date, val))
        sleep(0.2)
    return data
