import praw
import tweepy
from bitlyshortener import Shortener
import time

# BITLY RELATED TOKENS

BITLY_ACCESS_TOKEN = ['X']


# TWITTER RELATED AUTHORISATION LINKS


# STARTS AN INSTANCE OF REDDIT
def reddit_instance():
    print('working')
    reddit = praw.Reddit(
        user_agent='reddit Twitter tool monitoring ',
        client_id='dEEbK2AqmzqQGg',
        client_secret='q3t_RQSIavCya_e78hKtEgRXw-k')
    subreddit = reddit.subreddit('Automate')  # Write the sub that you want of course
    return subreddit


def tweet_creator(subreddit):
    post_dict = {}
    post_ids = []

    print("[bot] Getting posts from Reddit")
    # subreddit. hot, new, top
    # This fetches the post , checks if it has been posted , if it hasnt it then adds to current lib to post
    for submission in subreddit.hot(limit=5):
        # strip_title function is defined later
        post_id = submission.id
        posted = post_checker(post_id)
        if posted > 0:
            post_dict[shorten_title(submission.title)] = submission.url
            post_ids.append(submission.id)


    print("[bot] Generating short link using Bitly")
    # This generates the links for the posts and stores them
    mini_post_dict = {}

    for post in post_dict:
        post_title = post
        post_link = [post_dict[post]]
        # the shortener function is defined later
        short_link = shorten_url(post_link)
        mini_post_dict[post_title] = short_link

    return mini_post_dict, post_ids


# Used Bitly to shorten reddit.com links
def shorten_url(url):
    shortener = Shortener(tokens=BITLY_ACCESS_TOKEN, max_cache_size=8192)

    if any('reddit' in s for s in url):
        link = shortener.shorten_urls(url)
    else:
        link = url
    return link

# Limits the title length of tweet
def shorten_title(title):
    # Shortens a tweet so that it does not get rejected by twitter on char limit
    if len(title) < 94:
        return title
    else:
        return title[:93] + "..."


def add_id_to_file(post_id):
    # Open the txt file and adds the according id to ensure that
    # Not posted twice - I think tweepy actually errors out if you try to anyhow
    with open('posted_posts.txt', 'a') as file:
        file.write(str(post_id) + "\n")


def duplicate_checker(post_id):
    found = 0
    with open('posted_posts.txt', 'r') as file:
        for line in file:
            if post_id in line:
                found = 1

    return found


def post_checker(post_id):
    # Checks for duplicate posts
    found = duplicate_checker(post_id)
    posted = 0
    if found < 1:
        add_id_to_file(post_id)
        posted = 1
    return posted


def tweeter(post_dict, post_ids):

    # Access token taken from twitter Dev account

    ACCESS_TOKEN = 'X'
    ACCESS_TOKEN_SECRET = 'X'
    CONSUMER_KEY = 'X'
    CONSUMER_SECRET = 'X'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # This loop posts to twitter
    for post, post_id in zip(post_dict, post_ids):

        i = str(*post_dict[post])
        new_tweet = (post + ' ' + i + '#automation' + ' ' + '#automate' + ' ' + '#robotics' + ' ' + '#AI')
        print(new_tweet)
        # Delay to prevent twitter from banning account
        time.sleep(1200)
        api.update_status(status=new_tweet)


def main():
    subreddit = reddit_instance()
    post_dict, post_ids = tweet_creator(subreddit)
    tweeter(post_dict, post_ids)



if __name__ == '__main__':
    main()
    print('finished')
