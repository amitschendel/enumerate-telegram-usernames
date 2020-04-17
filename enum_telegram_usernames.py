import requests
from bs4 import BeautifulSoup
import sys
import json

URL = "https://t.me/"

if len(sys.argv) != 3:
    exit("Usage: python3 enum_telegram_usernames.py input_file output_file")


def main(input_path, output_path):
    with open(input_path, 'r') as input_file, open(output_path, 'w') as output_file:
        output_json = []
        for username in input_file.readlines():
            # send a request for each username
            username = username.strip()
            res = requests.get(URL+username)
            soup = BeautifulSoup(res.text, 'html.parser')
            # extracting the title from the response
            title = soup.title.string
            if ':' in title:
                tele_type = ''
                description = soup.find(
                    "meta", property="og:description")["content"]
                name = soup.find("meta", property="og:title")["content"]
                print(f"name: {name}")
                # check if the username is a group or a user
                if f"You can contact @{username} right away." == description:
                    tele_type = "user"
                    print(f"valid user: {username}")
                    output_json.append(
                        {
                            "name": name,
                            "username": username,
                            "type": tele_type
                        }
                    )
                else:
                    tele_type = "group"
                    print(f"valid group: {username}")
                    group_url = URL + username
                    print(f"group url: {group_url}")
                    output_json.append(
                        {
                            "name": name,
                            "username": username,
                            "groupUrl": group_url,
                            "type": tele_type
                        }
                    )
        # write output to file as json
        json.dump(output_json, output_file, indent=4)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
