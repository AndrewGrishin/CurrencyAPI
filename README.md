# Currency Exchange Rate

## Structure

```bash
.
├── currencyapi
│   ├── __init__.py
│   └── utils
│       └── __init__.py
├── poetry.lock
├── pyproject.toml
├── Dockerfile
├── main.py
└── README.md
```

The main goal of all of the project is to collect the exchange rate from web-site of Russian [Central Bank](https://cbr.ru/insurance/reporting_stat/).

## Purpose

In many economic cases it is vital to have quick access to data that should be collected and organized in a specific order. The key idea behind this work is to provide the tool that allows to gather *exchange rates* by days in the following format: RUS/Foreign currency.

## Algorithm

The simpler code the better programme is. Hence, it is ok to use simple tools for monotonic work. `request` and `bs4` packages are the main ones here.

First of all, just after the launch, the scrapper goes to Central-Bank site and gathers information of exchange rates, presented there.

Key hyperparameters of the algorithm are:

1. `start` - start date we are interested in.
2. `end` - end date of the time range.
3. `currency` - currency name (like: USD or RUB).

As an output the `.csv` file is stored in the `output/` directory (**created automatically**) in the following format: `RUB-<currency> <start>-<end>.csv`. The inner structure of the file is as follows:

| Date     | RUB - \<Currency\> |
| :----:   | :----:           |
| `date_1` | `val_1`          |
| `date_2` | `val_2`          |
| `date_i` | `val_i`          |
| `date_n` | `val_n`          |

## Deploy scheme

0. `docker pull andreyygrishin/currency_api` - download the image.
1. `mkdir ./output/` - if not created (important).
2. `docker run --rm -it -v ./output/:/home/output/ currency` - launch container.
3. `python -m main --start="<start-date>" --end="<end-date>" --currency="<currency>"` - launch the script. **Date format**: `YYYY-MM-DD`.
4. The result will be stored to your local directory `./output/`.
5. Type: `exit` - the docker container will be killed.
