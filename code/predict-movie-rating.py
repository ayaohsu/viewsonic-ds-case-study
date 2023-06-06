
import pandas as pd
import numpy as np


def get_interested_videos(raw_video_data):
    min_release_year = 2000
    newer_videos = amazon_prime_raw_data.query(f'release_year > {min_release_year}')

    interested_catogory = 'Kids'
    kids_suitable_rating = ('ALL','ALL_AGES','G','PG','TV-G','7+', 'TV-Y', 'TV-Y7')
    kids_suitable_videos = newer_videos.loc[newer_videos['rating'].isin(kids_suitable_rating) | newer_videos['listed_in'].str.contains(interested_catogory)]
    return kids_suitable_videos


if __name__ == '__main__':

    amazon_prime_raw_data = pd.read_csv('data/amazon_prime_titles.csv')
    print(f'Loading amazon prime videos [count={len(amazon_prime_raw_data.index)}]')

    amazon_interested_videos = get_interested_videos(amazon_prime_raw_data)
    print(f'Select only the interested videos [count={len(amazon_interested_videos.index)}]')
