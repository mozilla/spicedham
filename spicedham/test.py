import requests
import spicedham as sham
spicy = sham.SpicedHam()
url = "https://input.mozilla.org/api/v1/feedback/"
r = requests.get(url)
for vote in r.json()['results']:
#vote = r.json()
#vote = vote['results'][randint(0, len(vote))]
    if spicy.is_spam(vote) > 0:
        print "spam!"
    else:
        print "ham"
