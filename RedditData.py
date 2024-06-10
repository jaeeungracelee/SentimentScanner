import praw
from dotenv import load_dotenv
import os

# load environment variables from the .env file
# gotta keep my info hidden
load_dotenv()

# retrieve reddit API credentials from .env 
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
user_agent = os.getenv('USER_AGENT')

print(f"Client ID: {client_id}")
print(f"Client Secret: {client_secret}")
print(f"User Agent: {user_agent}")

# initialize reddit API client with the retrieved credentials
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# specify the subreddit you want to scrape
subreddit = reddit.subreddit('mentalhealth')

# retrieve the top 10 posts from the subreddit
top_posts = subreddit.top(limit=10)

# loop through the top posts and print some details
for post in top_posts:
    print(f"Title: {post.title}")
    print(f"Score: {post.score}")
    print(f"ID: {post.id}")
    print(f"URL: {post.url}")
    print(f"Number of comments: {post.num_comments}")
    print(f"Created: {post.created}")
    print(f"Body: {post.selftext}\n")
