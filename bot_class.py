import os
import sys
import time
import praw
import secrets


class RedditBot:
    # TODO: Need to define method to determine rate limit
    def __init__(self, name):
        self.name = name
        self.r = self.login()
        self.posts_replied_to = self.reply_tracking_unpack()

    def login(self):
        secrets.determine_creds(self.name)

        # connect to reddit and create instance
        user_agent = 'testing by /u/'+self.name+' v0.9.0'
        r = praw.Reddit(user_agent=user_agent,
                        client_id=secrets.creds.client_id,
                        client_secret=secrets.creds.client_secret,
                        username=secrets.creds.username,
                        password=secrets.creds.password)
        return r

    def reply_tracking_unpack(self):
        """returns list of posts the bot has already replied to"""
        filename = self.name+'_posts_replied_to.txt'
        if os.path.isfile(filename):
            # file exists, read contents into list
            with open(filename, 'r') as f:
                post_ids = f.read()
                post_ids = post_ids.split("\n")
                post_ids = list(filter(None, post_ids))
        else:
            # create empty list
            post_ids = []
        return post_ids

    def reply_tracking_pack(self):
        """take updated list and write to txt"""
        filename = self.name + '_posts_replied_to.txt'
        with open(filename, 'w') as f:
            print(filename)
            for post_id in self.posts_replied_to:
                f.write(post_id + '\n')
    '''
    def reply_to_comment(self, sub, search_term, reply):
        """reply to a reddit comment given a subreddit, search term, and reply"""
        subreddit = self.r.subreddit(sub)
        for submission in subreddit.hot(limit=5):
            # see if bot has already replied to the post
            if submission.id not in self.posts_replied_to:
                submission.comments.replace_more(limit=0)
                for comment in submission.comments.list():
                    if search_term.lower() in comment.body:
                        comment.reply(reply)
                        print('bot replying to : ', submission.title)
                        # add post id to list
                        self.posts_replied_to.append(submission.id)
    '''

    def reply_format(self, s):
        return '''\
{0}

[Code](https://github.com/henkhaus/reddit_bot_testing) |\
u/{1} |\
[Feedback](https://np.reddit.com/message/compose/?to={1}&subject=Feedback)
        '''.format(s, self.name)

    def handle_ratelimit(self, func, *args, **kwargs):
        while True:
            try:
                func(*args, **kwargs)
                break
            except praw.exceptions.APIException as error:
                print('Sleeping for 600 seconds')# % error.sleep_time)
                time.sleep(600)


