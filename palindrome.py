import string

# comment = 'this ia a comment that has the palindrome, racecar.'


def comment_parse(s):
    # all punctuation
    exclude = set(string.punctuation)
    # add all digits as well
    exclude = list(exclude).append(list(set(string.digits)))
    s = ''.join(ch for ch in s if ch not in exclude)
    s = [word for word in s.split(' ')]
    return s


def is_palindrome(s):
    if len(s) > 1:
        return s == s[::-1]
    else:
        return False

'''
for word in comment_parse(comment):
    print(str(is_palindrome(word)))
'''
