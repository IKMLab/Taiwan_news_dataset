import test.news.crawlers.conftest
from datetime import datetime, timedelta, timezone
from typing import Final

import pytest

import news.crawlers.chinatimes
import news.crawlers.db.read
import news.crawlers.db.schema
import news.crawlers.util.request_url


def test_utc_timezone(db_name: Final[str]) -> None:
    r"""`current_datetime` and `past_datetime` must in utc timezone."""
    taiwan_current_datetime = datetime.now(
        tz=timezone(offset=timedelta(hours=8)),
    )
    with pytest.raises(ValueError) as excinfo:
        news.crawlers.chinatimes.main(
            current_datetime=taiwan_current_datetime,
            db_name=db_name,
            past_datetime=datetime.now(tz=timezone.utc),
        )

    assert '`current_datetime` must in utc timezone.' in str(excinfo.value)
    taiwan_current_datetime = datetime.now(
        tz=timezone(offset=timedelta(hours=8)),
    )

    with pytest.raises(ValueError) as excinfo:
        news.crawlers.chinatimes.main(
            current_datetime=datetime.now(tz=timezone.utc),
            db_name=db_name,
            past_datetime=taiwan_current_datetime,
        )

    assert '`past_datetime` must in utc timezone.' in str(excinfo.value)


def test_datetime_order(db_name: Final[str]) -> None:
    r"""Must have `past_datetime <= current_datetime`."""
    with pytest.raises(ValueError) as excinfo:
        news.crawlers.chinatimes.main(
            current_datetime=datetime.now(tz=timezone.utc),
            db_name=db_name,
            past_datetime=datetime.now(tz=timezone.utc) + timedelta(days=2),
        )

    assert (
        'Must have `past_datetime <= current_datetime`.' in str(excinfo.value)
    )


def test_save_news_to_db(
    db_name: Final[str],
    response_200: Final[test.news.crawlers.conftest.MockResponse],
    cleanup_db_file: Final,
    monkeypatch: Final,
) -> None:
    r"""Save crawling news to database with correct format."""

    def mock_get(**kwargs) -> test.news.crawlers.conftest.MockResponse:
        return response_200

    monkeypatch.setattr(
        news.crawlers.util.request_url,
        'get',
        mock_get,
    )

    news.crawlers.chinatimes.main(
        continue_fail_count=1,
        current_datetime=datetime.now(tz=timezone.utc),
        db_name=db_name,
        debug=False,
        past_datetime=datetime.now(tz=timezone.utc) - timedelta(days=2),
    )

    all_records = news.crawlers.db.read.read_all_records(db_name=db_name)
    assert len(all_records)

    for record in all_records:
        assert isinstance(record, news.crawlers.db.schema.RawNews)
        assert isinstance(record.idx, int)
        assert record.company_id == news.crawlers.chinatimes.COMPANY_ID
        assert isinstance(record.raw_xml, str)
        assert isinstance(record.url_pattern, str)