import bot_class
import string


def comment_parse(s):
    # remove all punctuation
    exclude = set(string.punctuation)
    s = ''.join(ch for ch in s if ch not in exclude)
    # remove all digits
    t = ''.join(char for char in s if not char.isdigit())
    return t.split()


def is_palindrome(s):
    if len(s) > 2:
        return s == s[::-1]
    else:
        return False


def palindrome_finder(sub, r, posts_replied_to):

    """reply to a reddit comment given a subreddit, search term, and reply"""
    subreddit = r.subreddit(sub)

    for submission in subreddit.hot(limit=10):
        # see if bot has already replied to the post
        if submission.id not in posts_replied_to:
            submission.comments.replace_more(limit=0)
            palindrome_set = set()
            for comment in submission.comments.list():
                for word in comment_parse(comment.body):
                    if is_palindrome(word):
                        palindrome_set.add(word)
                        # found palindrome, add to comments palindrome list
                        print(word)
                print(palindrome_set)
                if palindrome_set:
                    bot.handle_ratelimit(comment.reply, bot.reply_format(palindrome_set))
                    print('bot replying to : ', submission.title)
                    # add post id to list
                    posts_replied_to.append(submission.id)

'''
for word in comment_parse(comment):
    print(str(is_palindrome(word)))
'''

if __name__ == '__main__':
    bot = bot_class.RedditBot('thepalindromebot')
    print(bot.posts_replied_to)
    palindrome_finder('pythonforengineers', bot.r, bot.posts_replied_to)
    # this 'kills' the bot
    bot.reply_tracking_pack()
