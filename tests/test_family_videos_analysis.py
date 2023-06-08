import sys
import os

import pandas as pd

from unittest.mock import patch

code_path = os.path.join(os.path.dirname(__file__), '../code')
sys.path.append(code_path)

from family_videos_analysis import analyze_family_videos

@patch('family_videos_analysis.AMAZON_PRIME_VIDEO_FILE_PATH', 'tests/test_amazon_prime_videos.csv')
@patch('family_videos_analysis.DISNEY_PLUS_VIDEO_FILE_PATH', 'tests/test_disney_plus_videos.csv')
@patch('family_videos_analysis.ANALYSIS_RESULT_FILE_NAME', 'tests/test_results.csv')
def test_end_to_end_both_tv_series_and_movies():
    analyze_family_videos(analyze_movies_only = False)

    test_result = pd.read_csv('tests/test_results.csv')

    assert test_result.loc[0]['actor'] == 'Actor 2'
    assert test_result.loc[0]['air_time_in_minutes'] == 473
    assert test_result.loc[1]['actor'] == 'Actor 3'
    assert test_result.loc[1]['air_time_in_minutes'] == 360
    assert test_result.loc[2]['actor'] == 'Actor 1'
    assert test_result.loc[2]['air_time_in_minutes'] == 113