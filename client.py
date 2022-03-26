import requests
import json
import re
import datetime


class Client():
    # Init function to set required class variables
    def __init__(self):
        self.s = requests.Session()
        self.url = "None"
        self.status = "None"
        self.base_url = "http://127.0.0.1:8000/"
        self.json_headers = {'content-type': 'application/json'}
        self.form_headers = {'content-type': 'application/x-www-form-urlencoded'}
        self.category_list = ['tech', 'pol', 'art', 'trivia']
        self.region_list = ['uk', 'w', 'eu']

    # Login the user to a news agency if username, url, and password are valid
    def login(self):
        username = input("Please enter your username: ").strip()
        password = input("Please enter your password: ").strip()
        print("\nLogging In....")
        data = {'username': username, 'password': password}
        try:
            r = self.s.post(self.base_url + "api/login/", data=data, headers=self.form_headers, timeout=4)
            print(r.text)
            print("Status Code is %s" % r.status_code)
            if (r.status_code == 200):
                self.status = "(" + username + ") "
            else:
                self.url = "None"
        except requests.exceptions.RequestException:
            print("Error! Failed to establish connection to:", self.url)
            self.url = "None"

    # Logs the user out from current session if its active
    def logout(self):
        print("\nLoggin out....")
        try:
            r = self.s.post(self.base_url + "api/logout/", timeout=10)
            print(r.text)
            print("Status Code is %s" % r.status_code)
            if r.status_code == 200:
                self.status = "None"
        except requests.exceptions.RequestException:
            print("Error! Failed to logout from ", self.base_url)

    # Sends a post request to add a news story to a news agency
    def post(self):
        headline = input("Headline: ")
        category = ""
        while category not in self.category_list:
            category = input("Category (pol, art, trivia, tech): ")

        region = ""
        while region not in self.region_list:
            region = input("Region (eu, w, uk): ")
        details = input("Details: ")
        print("\nPosting Story....")
        payload = {'headline': headline, 'category': category, 'region': region, 'details': details}

        try:
            r = self.s.post(self.base_url + "api/poststory/", data=json.dumps(payload), headers=self.json_headers,
                            timeout=10)
            print(r.text)
            print("Status Code is %s" % r.status_code)
        except requests.exceptions.RequestException:
            print("Error! Failed to post to ", self.url)

    def delete(self, key):
        print("\nDeleting Story With Key:", key, "....")
        payload = {'story_key': key}

        try:
            r = self.s.post(self.base_url + "api/deletestory/", data=json.dumps(payload), headers=self.json_headers,
                            timeout=10)
            print(r.text)
            print("Status Code is %s" % r.status_code)
        except requests.exceptions.RequestException:
            print("Error! Failed to delete story with key ", key)

    def register(self):
        print("\nRegistering Service....")
        payload = {"agency_name": "Enter your agency name here",
                   "url": "http://???.pythonanywhere.com/",
                   "agency_code": "???"}

        r = self.s.post('http://directory.pythonanywhere.com/api/register/',
                        data=json.dumps(payload), headers=self.json_headers, timeout=10)
        print(r.text)
        print("Status Code is %s" % r.status_code)

    # Lists all agencies registered in the directory
    def list(self):
        data = {
        }
        try:
            r = self.s.get(self.base_url + "api/getstory/", data=json.dumps(data), headers=self.form_headers,
                           timeout=10)

            if r.status_code == 200:
                stories = r.json()
                i = 1
                for story in stories["stories"]:
                    print("\nStory ", i)
                    print("Key: ".ljust(20), story["key"])
                    print("Headline: ".ljust(20), story["headline"])
                    print("Category: ".ljust(20), story["story_cat"])
                    print("Region: ".ljust(20), story["story_region"])
                    print("Author Name: ".ljust(20), story["author"])
                    print("Date Published: ".ljust(20), story["story_date"])
                    print("Details: ".ljust(20), story["story_details"])
                    i += 1
            else:
                print("\nError! Failed to retrieve stories from ", self.base_url)
                if (len(r.text) <= 500):
                    print(r.text)
                print("Status Code is %s" % r.status_code)
        except Exception:
            print("\nError! Failed to retrieve stories from ", self.base_url)

    # Given the 3 letter agency code, will find and return the agency object
    def getAgency(self, code):
        r = self.s.get('http://directory.pythonanywhere.com/api/list/', timeout=10)

        if (r.status_code == 200):
            agencies = json.loads(r.text)
            for agency in agencies["agency_list"]:
                if (agency["agency_code"] == code):
                    return agency
        return "Not Found"

    def show(self):
        """
        print command menu
        """
        print("\n\t\t\t\t\t\t\tWelcome To News Sysyem")
        print("-" * 85)
        print("--> register")
        print("--> login")
        print("--> logout")
        print("--> post")
        print("--> list")
        print("--> get [key]")
        print("--> delete [key]")
        print("--> query [catgory default=*] [region default=*] [date default=*]")
        print("--> exit")
        print("--> show")
        print("-" * 85)

    def exit(self):
        exit(0)

    def run_server(self):
        """
        start service
        """
        self.show()
        while True:
            prompt = ">>>"
            command = input(prompt).strip().split()

            if not command:
                continue

            command_name = command[0]

            try:
                handler = self.__getattribute__(command_name)
            except AttributeError:
                print("the command is invalid, please try again!")
                continue
            if command_name == "news":
                self.processNewsInput(command)
            if command_name in ["delete", "detail"]:
                handler(command[1])
            else:
                handler()

    def detail(self, index):
        data = {
            "key": index
        }
        try:
            r = self.s.get(self.base_url + "api/getstory/", data=json.dumps(data), headers=self.form_headers, timeout=10)

            if r.status_code == 200:
                stories = r.json()
                i = 1
                for story in stories["stories"]:
                    print("\nStory ", i)
                    print("Key: ".ljust(20), story["key"])
                    print("Headline: ".ljust(20), story["headline"])
                    print("Category: ".ljust(20), story["story_cat"])
                    print("Region: ".ljust(20), story["story_region"])
                    print("Author Name: ".ljust(20), story["author"])
                    print("Date Published: ".ljust(20), story["story_date"])
                    print("Details: ".ljust(20), story["story_details"])
                    i += 1
            else:
                print("\nError! Failed to retrieve stories from ", self.base_url)
                if (len(r.text) <= 500):
                    print(r.text)
                print("Status Code is %s" % r.status_code)
        except Exception:
            print("\nError! Failed to retrieve stories from ", self.base_url)




    # Processes the news input and calls relevant class functions
    def processNewsInput(self, command):
        params = ["*", "*", "*", "*"]  # 0=id  1=cat   2=reg   3=date
        for cmd in command[1:]:
            if len(cmd) == 3 and cmd != "pol" and cmd != "art" and cmd.isalpha():
                params[0] = cmd
            elif cmd == "pol" or cmd == "art" or cmd == "tech" or cmd == "trivia":
                params[1] = cmd
            elif cmd == "uk" or cmd == "w" or cmd == "eu":
                params[2] = cmd
            elif len(cmd) == 10:
                m = bool(re.match('^\d\d/\d\d/\d{4}$', cmd))  # dd/mm/yyyy
                if self.checkDateIsValid(cmd) and m:
                    params[3] = cmd
                else:
                    return

        print("Final news: ", params)
        if params[0] != "*":
            self.getSingleStories(params)
        elif params[0] == "*":
            self.getAllStories(params)

    # Checks if the date provided is a valid date
    def checkDateIsValid(self, cmd):
        day, month, year = cmd.split('/')
        try:
            d = datetime.datetime(int(year), int(month), int(day))
            return True
        except ValueError:
            print("Error! date is not a valid date, plz try again")

        return False


if __name__ == "__main__":
    """
    start client progress
    """
    Client().run_server()
