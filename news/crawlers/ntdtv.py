import re
from collections import Counter
from datetime import datetime
from typing import List, Tuple

import dateutil
import dateutil.parser
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

import news.crawlers
import news.preprocess
from news.db.schema import News

FIRST_PAGE = 1
PAGE_INTERVAL = 50
URL_PATTERN = re.compile(
    r'https://www.ntdtv.com/b5/(\d+)/(\d+)/(\d+)/a\d+.html'
)


def find_page_range(
    category: str,
    current_datetime: datetime,
    api: str,
    past_datetime: datetime,
    *,
    debug: bool = False,
) -> Tuple[int, int]:
    # Get max page of this category.
    try:
        url = f'https://www.ntdtv.com/b5/prog{api}/1'
        response = requests.get(
            url,
            timeout=news.crawlers.util.REQUEST_TIMEOUT,
        )
        response.close()

        # Raise exception if status code is not 200.
        news.crawlers.util.check_status_code(
            company='ntdtv',
            response=response
        )

        soup = BeautifulSoup(response.text, 'html.parser')
        max_page = soup.select('div.pagination > a.page-numbers')[-2].text
        max_page = int(max_page.replace(',', ''))
    except Exception as err:
        # Only 1 page is available.
        return 1

    # Only show progress bar in debug mode.
    iter_range = range(FIRST_PAGE, max_page)
    if debug:
        iter_range = tqdm(iter_range, desc='Find start page loop')

    # Find start page loop.
    start_page = 1
    for page in iter_range:
        page_url = f'https://www.ntdtv.com/b5/prog{api}/{page}'

        try:
            response = requests.get(
                page_url,
                timeout=news.crawlers.util.REQUEST_TIMEOUT,
            )
            response.close()

            # Raise exception if status code is not 200.
            news.crawlers.util.check_status_code(
                company='ntdtv',
                response=response
            )

            # Parse date in this page.
            soup = BeautifulSoup(response.text, 'html.parser')
            a_tags = soup.select(
                'div.post_list > div.list_wrapper > div.one_post div.title > a'
            )
            matches = filter(
                bool,
                map(lambda a_tag: URL_PATTERN.match(a_tag['href']), a_tags)
            )
            news_datetimes = map(
                lambda match: {
                    'year': int(match.group(1)),
                    'month': int(match.group(2)),
                    'day': int(match.group(3)),
                },
                matches,
            )
            news_datetimes = list(map(
                lambda n: dateutil.parser.isoparse(
                    f"{n['year']:04d}-{n['month']:02d}-{n['day']:02d}T00:00:00Z"
                ),
                news_datetimes,
            ))

            # Break loop if `news_datetime < past_datetime`.
            if news_datetimes[0] < past_datetime:
                break
            # If this page contains valid news, we start crawling from this page.
            news_datetimes = filter(bool, map(
                lambda n: past_datetime <= n <= current_datetime,
                news_datetimes,
            ))

            news_datetimes = list(news_datetimes)

            if news_datetimes:
                start_page = page
                break
        except Exception as err:
            # Some pages may not be available.
            continue

    return start_page, max_page


def get_news_list(
    category: str,
    current_datetime: datetime,
    api: str,
    past_datetime: datetime,
    page_range: List[int],
    *,
    debug: bool = False,
) -> List[News]:
    news_list: List[News] = []
    logger = Counter()

    iter_range = range(page_range[0], page_range[1])
    # Only show progress bar in debug mode.
    if debug:
        iter_range = tqdm(iter_range, desc='Crawling loop.')

    # Crawling loop.
    is_datetime_valid = True
    for page in iter_range:
        if not is_datetime_valid:
            break

        page_url = f'https://www.ntdtv.com/b5/prog{api}/{page}'

        try:
            response = requests.get(
                page_url,
                timeout=news.crawlers.util.REQUEST_TIMEOUT,
            )
            response.close()

            # Raise exception if status code is not 200.
            news.crawlers.util.check_status_code(
                company='ntdtv',
                response=response
            )

            # If `status_code == 200`, parse links in this page.
            soup = BeautifulSoup(response.text, 'html.parser')
            a_tags = soup.select(
                'div.post_list > div.list_wrapper > div.one_post div.title > a'
            )
        except Exception as err:
            if err.args:
                logger.update([err.args[0]])
            continue

        for a_tag in a_tags:
            try:
                news_url = a_tag['href']

                response = requests.get(
                    news_url,
                    timeout=news.crawlers.util.REQUEST_TIMEOUT,
                )
                response.close()

                # Raise exception if status code is not 200.
                news.crawlers.util.check_status_code(
                    company='ntdtv',
                    response=response
                )

                # Parse news in this page.
                parsed_news = news.preprocess.ntdtv.parse(ori_news=News(
                    raw_xml=response.text,
                    url=news_url,
                ))
                news_datetime = dateutil.parser.isoparse(parsed_news.datetime)

                # If `news_datetime > current_datetime` just continue.
                if news_datetime > current_datetime:
                    continue
                # If `past_datetime > news_datetime` stop crawling loop.
                if past_datetime > news_datetime:
                    is_datetime_valid = False
                    break

                news_list.append(parsed_news)
            except Exception as err:
                if err.args:
                    logger.update([err.args[0]])

    # Only show error stats in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    return news_list


CATEGORIES = {
    '國際': 202,
    '港澳': 205,
    '財經': 208,
    '健康': 1255,
    '體育': 211,
    '美國': 203,
    '大陸': 204,
    '文史': 647,
}


def main(
    current_datetime: datetime,
    db_name: str,
    past_datetime: datetime,
    *,
    debug: bool = False,
):

    if past_datetime > current_datetime:
        raise ValueError('Must have `past_datetime <= current_datetime`.')

    # Get database connection.
    conn = news.db.util.get_conn(db_name=f'raw/{db_name}')
    cur = conn.cursor()
    news.db.create.create_table(cur=cur)

    for category, api in CATEGORIES.items():
        # Find page range that consistent with specified time range.
        start_page, max_page = find_page_range(
            category=category,
            current_datetime=current_datetime,
            api=api,
            past_datetime=past_datetime,
            debug=debug,
        )

        # Make range inclusive.
        max_page += 1

        # Commit database when crawling 10 pages.
        for page in range(start_page, max_page, PAGE_INTERVAL):
            page_range = [
                page,
                min(page + PAGE_INTERVAL, max_page),
            ]
            news_list = get_news_list(
                category=category,
                current_datetime=current_datetime,
                debug=debug,
                api=api,
                past_datetime=past_datetime,
                page_range=page_range,
            )
            # When news violate `past_datetime` break for loop.
            if not news_list:
                break
            news.db.write.write_new_records(
                cur=cur,
                news_list=news_list,
            )

            conn.commit()

    # Close database connection.
    conn.close()
