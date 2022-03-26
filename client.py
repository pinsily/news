import requests
import json
import re
import datetime


class Client:
    # Init function to set required class variables
    def __init__(self):
        self.session = requests.Session()
        self.url = "None"
        self.status = "None"
        self.base_url = "http://127.0.0.1:8000/"
        # self.base_url = "https://1001james.pythonanywhere.com/"
        self.json_headers = {'content-type': 'application/json'}
        self.form_headers = {'content-type': 'application/x-www-form-urlencoded'}
        self.category_list = ['tech', 'pol', 'art', 'trivia']
        self.region_list = ['uk', 'w', 'eu']

    def register(self):
        username = input("username: ").strip()
        password = input("password: ").strip()
        data = {"username": username, "password": password}

        response = self.session.post(f'{self.base_url}api/register/',
                                     data=data, headers=self.form_headers, timeout=10)

        if response.json():
            print(f"register res: {response.json().get('msg')}")

    def login(self):
        """
        login
        """
        username = input("username: ").strip()
        password = input("password: ").strip()
        print("logging In....")
        data = {'username': username, 'password': password}

        response = self.session.post(self.base_url + "api/login/", data=data, headers=self.form_headers, timeout=4)

        if response.json():
            print(f"login res: {response.json().get('msg')}")

        if response.status_code == 200:
            self.status = "(" + username + ") "
        else:
            self.url = "None"

    def logout(self):
        """
        logout
        """
        print("\nLoggin out....")

        response = self.session.post(self.base_url + "api/logout/", timeout=10)
        if response.status_code == 200:
            self.status = "None"

        if response.json():
            print(f"login res: {response.json().get('msg')}")

    def post(self):
        """
        post a new
        """
        headline = input("Headline: ")
        category = ""
        while category not in self.category_list:
            category = input("Category (pol, art, trivia, tech): ")

        region = ""
        while region not in self.region_list:
            region = input("Region (eu, w, uk): ")
        details = input("Details: ")
        print("\nPosting Story....")
        data = {'headline': headline, 'category': category, 'region': region, 'details': details}

        response = self.session.post(self.base_url + "api/poststory/", data=json.dumps(data), headers=self.json_headers,
                                     timeout=10)

        if response.json():
            print(f"post res: {response.json().get('msg')}")

    def delete(self, key):
        print(f"\nDeleting Key: {key}....")

        response = self.session.post(self.base_url + "api/deletestory/", data=json.dumps({'story_key': key}),
                                     headers=self.json_headers,
                                     timeout=10)

        if response.json():
            print(f"delete res: {response.json().get('msg')}")

    def detail(self, index):
        data = {
            "key": index
        }
        r = self.session.get(self.base_url + "api/getstory/", data=json.dumps(data), headers=self.form_headers,
                             timeout=10)

        if r.status_code == 200:
            stories = r.json()
            self.print_table(stories)
        else:
            print("\n--- detail nothing!")

    def list(self, index=None):
        """
        list all news
        """
        response = self.session.get(self.base_url + "api/getstory/", data=json.dumps({}), headers=self.form_headers,
                                    timeout=10)

        if response.status_code == 200:
            stories = response.json()
            i = 1

            self.print_table(stories)

        else:
            print("\n--- list nothing!")

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
            if command_name == "query":
                handler(command)
            elif command_name in ["delete", "detail"]:
                handler(command[1])
            else:
                handler()

    def query(self, command):
        """
        query
        """
        data = {}
        for cmd in command[1:]:
            param, value = cmd.split("=")
            data[param] = value

        response = self.session.get(self.base_url + "api/getstory/", data=json.dumps(data), headers=self.form_headers,
                                    timeout=10)

        if response.status_code == 200:
            stories = response.json()

            self.print_table(stories)
        else:
            print("\n--- query nothing!")


    def print_table(self, stories):
        print("{:<8} {:<15} {:<10} {:<8} {:<15} {:<20} {:<10}"
              .format('Key', 'Headline', 'Category', 'Region', 'Author Name', 'Date Published', 'Details'))

        for story in stories["stories"]:
            print("{:<8} {:<15} {:<10} {:<8} {:<15} {:<20} {:<10}"
                  .format(story["key"], story["headline"], story["story_cat"],
                          story["story_region"], story["author"], story["story_date"]
                          , story["story_details"]))


if __name__ == "__main__":
    """
    start client progress
    """
    Client().run_server()
