import inspect
import re
from datetime import datetime
from inspect import Parameter, Signature
from typing import Dict, Final, List, Optional, Union

import news.crawlers.db.schema
import news.crawlers.epochtimes
import news.crawlers.util.normalize


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.epochtimes, 'get_datetime_from_url')
    assert inspect.isfunction(news.crawlers.epochtimes.get_datetime_from_url)
    assert inspect.signature(
        news.crawlers.epochtimes.get_datetime_from_url,
    ) == Signature(
        parameters=[
            Parameter(
                name='url',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[str],
            ),
        ],
        return_annotation=Union[datetime, None],
    )
    assert hasattr(news.crawlers.epochtimes, 'get_max_page')
    assert inspect.isfunction(news.crawlers.epochtimes.get_max_page)
    assert inspect.signature(
        news.crawlers.epochtimes.get_max_page,
    ) == Signature(
        parameters=[
            Parameter(
                name='category_api',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[str],
            ),
            Parameter(
                name='kwargs',
                kind=Parameter.VAR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[Optional[Dict]],
            ),
        ],
        return_annotation=int,
    )
    assert hasattr(news.crawlers.epochtimes, 'get_start_page')
    assert inspect.isfunction(news.crawlers.epochtimes.get_start_page)
    assert inspect.signature(
        news.crawlers.epochtimes.get_start_page,
    ) == Signature(
        parameters=[
            Parameter(
                name='category_api',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[str],
            ),
            Parameter(
                name='current_datetime',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[datetime],
            ),
            Parameter(
                name='max_page',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[int],
            ),
            Parameter(
                name='past_datetime',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[datetime],
            ),
            Parameter(
                name='continue_fail_count',
                kind=Parameter.KEYWORD_ONLY,
                default=5,
                annotation=Final[Optional[int]],
            ),
            Parameter(
                name='debug',
                kind=Parameter.KEYWORD_ONLY,
                default=False,
                annotation=Final[Optional[bool]],
            ),
            Parameter(
                name='kwargs',
                kind=Parameter.VAR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[Optional[Dict]],
            ),
        ],
        return_annotation=int,
    )
    assert hasattr(news.crawlers.epochtimes, 'get_news_list')
    assert inspect.isfunction(news.crawlers.epochtimes.get_news_list)
    assert inspect.signature(
        news.crawlers.epochtimes.get_news_list,
    ) == Signature(
        parameters=[
            Parameter(
                name='category_api',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[str],
            ),
            Parameter(
                name='current_datetime',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[datetime],
            ),
            Parameter(
                name='first_page',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[int],
            ),
            Parameter(
                name='last_page',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[int],
            ),
            Parameter(
                name='past_datetime',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[datetime],
            ),
            Parameter(
                name='continue_fail_count',
                kind=Parameter.KEYWORD_ONLY,
                default=5,
                annotation=Final[Optional[int]],
            ),
            Parameter(
                name='debug',
                kind=Parameter.KEYWORD_ONLY,
                default=False,
                annotation=Final[Optional[bool]],
            ),
            Parameter(
                name='kwargs',
                kind=Parameter.VAR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[Optional[Dict]],
            ),
        ],
        return_annotation=List[news.crawlers.db.schema.RawNews],
    )
    assert hasattr(news.crawlers.epochtimes, 'main')
    assert inspect.isfunction(news.crawlers.epochtimes.main)
    assert inspect.signature(news.crawlers.epochtimes.main) == Signature(
        parameters=[
            Parameter(
                name='current_datetime',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[datetime],
            ),
            Parameter(
                name='db_name',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[str],
            ),
            Parameter(
                name='past_datetime',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[datetime],
            ),
            Parameter(
                name='kwargs',
                kind=Parameter.VAR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[Optional[Dict]],
            ),
        ],
        return_annotation=None,
    )


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.crawlers.epochtimes, 'CATEGORY_API_LOOKUP_TABLE')
    assert news.crawlers.epochtimes.CATEGORY_API_LOOKUP_TABLE == {
        '大陸': 'nsc413',
        '美國': 'nsc412',
        '香港': 'ncid1349362',
        '國際': 'nsc418',
        '台灣': 'ncid1349361',
        '科技': 'nsc419',
        '財經': 'nsc420',
        '文化': 'nsc2007'
    }
    assert hasattr(news.crawlers.epochtimes, 'COMMIT_PAGE_INTERVAL')
    assert news.crawlers.epochtimes.COMMIT_PAGE_INTERVAL == 10
    assert hasattr(news.crawlers.epochtimes, 'COMPANY_ID')
    assert (
        news.crawlers.epochtimes.COMPANY_ID ==
        news.crawlers.util.normalize.get_company_id(company='大紀元')
    )
    assert hasattr(news.crawlers.epochtimes, 'COMPANY_URL')
    assert (
        news.crawlers.epochtimes.COMPANY_URL == news.crawlers.util.normalize
        .get_company_url(company_id=news.crawlers.epochtimes.COMPANY_ID)
    )
    assert hasattr(news.crawlers.epochtimes, 'DATE_PATTERN')
    assert news.crawlers.epochtimes.DATE_PATTERN == re.compile(
        news.crawlers.epochtimes.COMPANY_URL + r'(\d+)/(\d+)/(\d+)/n\d+\.htm',
    )
    assert hasattr(news.crawlers.epochtimes, 'FIRST_PAGE')
    assert news.crawlers.epochtimes.FIRST_PAGE == 2
