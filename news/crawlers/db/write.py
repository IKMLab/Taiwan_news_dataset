import sqlite3
from typing import Sequence

from news.crawlers.db.schema import RawNews


def write_new_records(cur: sqlite3.Cursor, news_list: Sequence[RawNews]):
    r'''輸入目標資料庫的cursor與`news_list`，將`news_list`內的資料保存到目標
    資料庫中
    '''

    # 取出已存在目標資料庫的url，避免重複保存相同的資料
    existed_url = list(cur.execute('''
        SELECT url_pattern FROM news
    '''))
    existed_url = set(map(lambda url: url[0], existed_url))

    # 過濾掉`news_list`內重複的資料
    tmp = []
    for n in news_list:
        if n.url_pattern not in existed_url:
            tmp.append(n)
            existed_url.add(n.url_pattern)

    # 從`news_list`內的資料取出id以外的欄位
    news_list = [
        (
            news.company_id,
            news.raw_xml,
            news.url_pattern
        ) for news in tmp]

    cur.executemany(
        '''
        INSERT INTO news(company_id, raw_xml, url_pattern)
        VALUES (?, ?, ?)
        ''',
        news_list
    )