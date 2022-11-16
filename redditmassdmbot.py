import os
import praw
import time
from dotenv import load_dotenv
from pathlib import Path


class MassMessenger:
    """
    Sends a mass message to a list of Reddit users.
    """

    def __init__(self, c_id, c_secret, user, pwd, user_agent, message_loc, urls_loc):
        self.r = praw.Reddit(client_id=c_id,
                     client_secret=c_secret, password=pwd,
                     user_agent=user_agent, username=user)
        self.message = self.get_contents(message_loc)
        self.urls = self.get_urls(urls_loc)
        self.list = self.get_users(self.urls)

    def get_users(self, urls:list) -> list:
        """
        Gets user list for comments under the post urls
        
        :param urls: list
        :return: list
        """
 
        users = []
        for url in self.urls:
            submission = self.r.submission(url=url)
            for top_level_comment in submission.comments:
                    print(top_level_comment.body)
                    
        return users


    def get_urls(self, location):
        """
        Gets content line by line of text file at location.
        
        :param location: str
        :return: list
        """
        file = open(location, 'r')
        urls = file.readlines()
        return urls

    def get_message(self, location):
        """
        Gets content of text file at location.

        :param location: str
        :return: str
        """
        file = open(location, 'r')
        message = file.read()
        if message[-1:] == "\n":
            return message[:len(message)-1]
        return message


    def run(self):
        """
        Runs main message sending code.
        """
        self.show_stats()
        count = 0
        pause_count = 0
        print("Sending messages:")
        for user in self.list:
            if pause_count >= 100:
                print('Paused for 2 hours at: ' + str(time.ctime()))
                time.sleep(7200)
                pause_count = 0
            try:
                self.r.redditor(user[0]).message(self.subject, self.message)
            except:
                pass
            else:
                print('Mailed ' + user[0])
                self.list[count][1] = 'Sent'
                count += 1
                pause_count += 1

    def show_stats(self):
        """
        Shows basic stats on current mass message.
        
        :return: str
        """
        print('sending to ' + str(len(self.list)) + ' users.')

if __name__ == '__main__':
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    # Setting client connection credentials
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")
    username = os.getenv("reddit_username")
    password = os.getenv("reddit_password")
    user_agent = os.getenv("reddit_user_agent")

    # Setting data sources
    urls = "sample-urls.txt"
    message = "sample-message.txt"
 
    m = MassMessenger(
        client_id,
        client_secret,
        username,
        password,
        user_agent,
        message,
        urls
    )

    # Running messenger
    m.run()
