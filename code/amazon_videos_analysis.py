
import pandas as pd

TV_SERIES_SEASON_TO_MINS = 9 * 40

def get_filtered_amazon_videos_for_target_market(videos_df):
    min_release_year = 2000
    videos_df = videos_df.query(f'release_year > {min_release_year}')

    included_catogory = 'Kids'
    excluded_categories = ('Animation', 'Anime', 'Documentary')
    kids_suitable_rating = ('ALL','ALL_AGES','G','PG','TV-G','7+', 'TV-Y', 'TV-Y7', '13+', 'PG-13')
    return videos_df.loc[
                            (
                                videos_df['rating'].isin(kids_suitable_rating) 
                                | videos_df['listed_in'].str.contains(included_catogory)
                            )
                            & ~videos_df['listed_in'].str.contains(excluded_categories[0]) 
                            & ~videos_df['listed_in'].str.contains(excluded_categories[1])
                        ]

def get_filtered_disney_videos_for_target_market(videos_df):
    min_release_year = 2000
    videos_df = videos_df.query(f'release_year > {min_release_year}')

    excluded_categories = ('Animation', 'Anime', 'Docuseries', 'Documentary')
    return videos_df.loc[~videos_df['listed_in'].isin(excluded_categories)]

def get_actors_with_air_time_from_videos(videos_df):
    videos_with_non_empty_cast = videos_df[~videos_df['cast'].isnull()]
    
    videos_with_non_empty_cast.loc[:,'cast'] = videos_with_non_empty_cast['cast'].str.split(',')
    actors_with_durations = videos_with_non_empty_cast.explode('cast')[['cast', 'duration']].rename(columns={'cast':'actor'})
    actors_with_durations.loc[:,'actor'] = actors_with_durations['actor'].str.strip()
    
    actors_with_durations[['air_time_value','air_time_unit']] = actors_with_durations['duration'].str.split(' ', n=2, expand=True)
    unit_to_min = {
        'Season' : TV_SERIES_SEASON_TO_MINS,
        'Seasons' : TV_SERIES_SEASON_TO_MINS,
        'min': 1
    }
    actors_with_durations['air_time_in_minutes']\
          = actors_with_durations['air_time_unit'].map(unit_to_min) * pd.to_numeric(actors_with_durations['air_time_value'])
    
    actors_with_total_air_time = actors_with_durations[['actor', 'air_time_in_minutes']].groupby('actor').sum()
    return actors_with_total_air_time

if __name__ == '__main__':

    amazon_videos_df = pd.read_csv('data/amazon_prime_titles.csv', index_col=[0])
    print(f'Loading amazon prime videos [count={len(amazon_videos_df.index)}]')

    amazon_videos_df = get_filtered_amazon_videos_for_target_market(amazon_videos_df)

    amazon_videos_df = amazon_videos_df.loc[amazon_videos_df['cast'] != "1"]

    amazon_actors_with_air_time_df = get_actors_with_air_time_from_videos(amazon_videos_df)

    disney_videos_df = pd.read_csv('data/disney_plus_titles.csv', index_col=[0])
    print(f'Loading disney+ videos [count={len(disney_videos_df.index)}]')

    disney_videos_df = get_filtered_disney_videos_for_target_market(disney_videos_df)

    disney_actors_with_air_time_df = get_actors_with_air_time_from_videos(disney_videos_df)

    all_actors_df = pd.concat([amazon_actors_with_air_time_df, disney_actors_with_air_time_df])
    all_actors_df = all_actors_df.groupby('actor').sum()
    
    print('Actors with the most air time')
    print(all_actors_df.sort_values('air_time_in_minutes', ascending=False).head(20))