import piston, os, datetime, time
from piston.blog import Blog

class Poster(object):
    """
    Makes automated posts about lottobot's stats. Created by
    Lottobot object.
    """

    def __init__(self, master, template):#'master' is a lottobot instance, template is a file passed from lottobot

        self.master = master
        self.template = template

    def postify_lottos(self, data):

        chunk = "<br/>"

        #order the numbers first
        for lot in sorted(data):
            
            chunk += "<li># " + str(data)
            chunk += " (from " + str(data["start"]) + " to " + str(data["end"]) + "):"
            chunk += " Winner - " + str(data["winner"]) + ";"
            chunk += " Total entrants - " + str(data["entrants"]) + "</li>"

        chunk += "<br/>"

        #print(chunk)

        return chunk

    def parse_post(self, postfile):
        """
        Parse the contents of a post file
        according to Lottobot's simplistic
        syntax
        """

        title = ""
        tags = []
        body = ""

        #formatted
        lottos = self.postify_lottos(self.master.daily_data["lottos"])

        #read from file
        with open(postfile, 'r') as post:

            title = post.readline()

            #I should be ashamed...
            tags.append(post.readline())
            tags.append(post.readline())
            tags.append(post.readline())
            tags.append(post.readline())
            tags.append(post.readline())

            body = post.readline()

        #calc avg entrants (avoid division by 0)
        try:
            avg = int(self.master.daily_data["total_entrants"]) / int(self.master.daily_data["total_winners"])
        except Exception:
            avg = 0

        #format body & title
        title = title.format(
            date = str(datetime.datetime.now().date()),
            acct = str(self.master.account_name),
            llnum = str(self.master.longlotto_number),
            prize = str(self.master.longlotto_prize),
            champ = str(self.master.longlotto_current_champ),
            lotto_list = str(lottos),
            num_lottos = str(self.master.daily_data["num_lottos"]),
            total_entrants = str(self.master.daily_data["total_entrants"]),
            total_winners = str(self.master.daily_data["total_winners"]),
            valid_winners = str(self.master.daily_data["valid_winners"]),
            random_winners = str(self.master.daily_data["random_winners"]),
            avg_entrants = str(avg),
            cur_lotto = str(self.master.lotto),
            cur_entrants = str(len(self.master.urls)),
            cur_endtime = str(time.ctime(self.master.target_end_time))
            )
        body = body.format(
            date = str(datetime.datetime.now().date()),
            acct = str(self.master.account_name),
            llnum = str(self.master.longlotto_number),
            prize = str(self.master.longlotto_prize),
            champ = str(self.master.longlotto_current_champ),
            lotto_list = str(lottos),
            num_lottos = str(self.master.daily_data["num_lottos"]),
            total_entrants = str(self.master.daily_data["total_entrants"]),
            total_winners = str(self.master.daily_data["total_winners"]),
            valid_winners = str(self.master.daily_data["valid_winners"]),
            random_winners = str(self.master.daily_data["random_winners"]),
            avg_entrants = str(avg),
            cur_lotto = str(self.master.lotto),
            cur_entrants = str(len(self.master.urls)),
            cur_endtime = str(time.ctime(self.master.target_end_time))
            )

        #return post
        return [title, body, tags]

##    def check(self):
##        """
##        Check if it is time to create a post. If it is,
##        do it.
##        """
##
##        if

    def post(self):
        """
        Make a post automatically.
        """

        post = self.parse_post(self.template)

        ptitle = post[0]
        pbody = post[1]
        pauthor = self.master.account_name
        ptags = post[2]

        try:

            self.master.steem.post(ptitle, pbody, author = pauthor, tags = ptags)

        except Exception:

            self.master.errstr += "FAILED TO POST UPDATE!\n\n"
            #print("!!!!!!!!!!!!!!!!!!")
