from tech_news.analyzer.reading_plan import (
    ReadingPlanService,
)  # noqa: F401, E261, E501
import pytest
from unittest.mock import Mock, patch


all_news = [
    {"title": "news1", "reading_time": 5},
    {"title": "news2", "reading_time": 6},
    {"title": "news3", "reading_time": 7},
    {"title": "news4", "reading_time": 8},
]

expected = {
    "readable": [
        {
            "unfilled_time": 3,
            "chosen_news": [("news1", 5), ("news2", 6)],
        },
        {
            "unfilled_time": 0,
            "chosen_news": [("news3", 7)],
        },
    ],
    "unreadable": [("news4", 8)],
}


def test_reading_plan_group_news():
    mock_news = Mock(return_value=all_news)

    with pytest.raises(ValueError):
        ReadingPlanService.group_news_for_available_time(0)

    with patch(
        "tech_news.analyzer.reading_plan.ReadingPlanService._db_news_proxy",
        mock_news,
    ):
        result_expect = ReadingPlanService.group_news_for_available_time(13)

    assert result_expect == expected
