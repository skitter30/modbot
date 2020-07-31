from donbot import Donbot
from lxml import html, cssselect
import re

class GetVotes(Donbot):
    def __init__(self, username, password, postdelay=1.5):
        super(GetVotes, self).__init__(username, password)

    def parse_post(self, post):

        post_string = str(html.tostring(post).decode("utf-8"))
        post_string = re.sub("<blockquote>.*</blockquote>", "", post_string)
        post_string = re.sub("<.*?>", "", post_string)
        post_string = re.sub("\\\\n", "", post_string)
        post_string = re.sub("\\\\t", "", post_string)
        post_string = re.sub("\\\\", "", post_string)
        post_string = post_string

        return post_string


    def getISOs(self, thread, usernames):
        uids = [super(GetVotes, self).getUserID(user) for user in usernames]

        for i, uid in enumerate(uids):
            link = thread + "&user_select[]=" + uid + "&sort=Go&st=0&sk=t&sd=d"
            posts = []
            page = self.session.get(link)
            content = html.fromstring(page.content)
            #vote = content.cssselect(".postbody .bbvote")[0].text_content()
            #print(usernames[i] + '\t' + vote)

            #Get the number of ISO pages
            some_special_div = content.cssselect(".pagination")
            number_of_pages = int(int(html.tostring(some_special_div[0]).decode("utf-8").count("span")) / 2)
            number_of_pages=max(1, number_of_pages)

            for i in range(0, number_of_pages):
                link_temp = thread + "&user_select[]=" + uid + "&sort=Go&st=0&sk=t&sd=d&start=" + str(i*200)
                print(link_temp)
                page_temp = self.session.get(link_temp)
                content_temp = html.fromstring(page_temp.content)
                posts_temp = content.cssselect(".postbody .content")
                posts.extend(posts_temp)

            return [self.parse_post(post) for post in posts]
