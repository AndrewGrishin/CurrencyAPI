import os
from datetime import datetime

import fire
import pandas as pd

from currencyapi.utils import collect_currency


def launch(
    currency: str,
    start: str,  # start date: yyyy-mm-dd
    end: str,  # end date: yyyy-mm-dd
) -> None:
    scheme = "https://cbr.ru/currency_base/"
    scheme += "daily/?UniDbQuery.Posted=True&UniDbQuery.To={}.{}.2023"

    date_scheme = "{}-{}-{}"

    dates = pd.date_range(
        start=datetime.strptime(start, "%Y-%m-%d"),
        end=datetime.strptime(end, "%Y-%m-%d"),
        freq="D",
    )

    data = collect_currency(
        dates=dates,
        date_scheme=date_scheme,
        scheme=scheme,
        currency=currency,
    )

    a, b = zip(*data)
    df = pd.DataFrame({"Date": a, "RUB/{}".format(currency): b})

    if "output" not in os.listdir():
        os.mkdir("output")

    df.to_csv(
        "output/RUB-{} {}-{}.csv".format(
            currency,
            start.replace("/", ""),
            end.replace("/", ""),
        ),
        index=False,
    )


if __name__ == "__main__":
    fire.Fire(launch)
