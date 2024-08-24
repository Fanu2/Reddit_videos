import praw

# Your Reddit API credentials
client_id = 'I5KWMzt16qAvByWv0FEkSg'
client_secret = 'O12GGqh6WDnv0I_sPXO3L0mKOcG1TQ'
user_agent = 'RedditImageFetcher:1.0 (by /u/singh1021)'

# Initialize Reddit instance
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# Define the subreddit
subreddit_name = 'AskReddit'
subreddit = reddit.subreddit(subreddit_name)

# Fetch hot posts
hot_posts = subreddit.hot(limit=10)

# Print the titles of the hot posts
for post in hot_posts:
    print(post.title)
