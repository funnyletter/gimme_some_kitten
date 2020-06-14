import tweepy as tw
import datetime

# asyncio bug workaround
import asyncio
import selectors

selector = selectors.SelectSelector()
loop = asyncio.SelectorEventLoop(selector)
asyncio.set_event_loop(loop)
# To-do: See if there's real fix for asyncio bug

api_keys = []

with open('config.ini') as file:
    for line in file:
        api_keys.append(line.strip())


auth = tw.OAuthHandler(api_keys[0], api_keys[1])
auth.set_access_token(api_keys[2], api_keys[3])
api = tw.API(auth, wait_on_rate_limit=True)


def search_tweets(search_term, result_type='recent', days_delta=7, tweet_count=200):
    """
    Searches twitter for the query given in search_term (string) starting
    from days_delta (int) in the past, and returns tweet_count (int) 
    tweets sorted by result_type ('popular' or 'recent').
    """
    start_date = datetime.datetime.today() - datetime.timedelta(days=days_delta)
    start_date = start_date.strftime('%Y-%m-%d')

    tweets = tw.Cursor(api.search,
              q=search_term + ' -filter:retweets',
              lang="en",
              result_type=result_type,
              since=start_date).items(tweet_count)
    
    tweetlist = []
    for status in tweets:
        status_dict = {}
        if 'media' in status.entities:
            status_dict['screen_name'] = status.user.screen_name
            status_dict['date'] = status.created_at
            status_dict['text'] = status.text
            status_dict['image_url'] = status.entities['media'][0]['media_url']
            tweetlist.append(status_dict)
            
    return tweetlist

