from datetime import datetime
import requests
import config
import csv
import os

headers = {"Authorization": f"Bearer {config.BEARER_TOKEN}"}
accounts = []


def start():
    print("- - - Twitter Followers Checker - - -")
    get_nicknames_file()


def get_nicknames_file():
    file_path = str(input("Drop file with nicknames here: "))
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            accounts.append(line.rstrip())
    check_excel()


def check_excel():
    a = str(input("Do you already have an excel file? y/n\n"))
    if a == "y":
        b = str(input("Drop file here: "))
        main(b)
    elif a == "n":
        create_excel()
    else:
        print("Sorry, can't understand you")
        check_excel()

def create_excel():
    head = ["Nickname", "Followers", "Time"]
    with open("Followers.csv", "w", encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(head)
        print("Excel file was created")
    main("Followers.csv")


def main(excel_file):
    for account in accounts:
        nickname = account.partition("com/")[2]
        req = requests.get(f"https://api.twitter.com/2/users/by/username/{nickname}", headers=headers)
        data = req.json()
        user_id = data["data"]["id"]
        req = requests.get(f"https://api.twitter.com/2/users/{user_id}?user.fields=public_metrics,created_at",
                           headers=headers)
        data = req.json()
        body = [nickname, data["data"]['public_metrics']['followers_count'], datetime.now().strftime("%H:%M:%S")]
        with open(excel_file, "a", newline="", encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(body)
    completed()


def completed():
    print("Data was saved, opening excel ...")
    os.system("start EXCEL.EXE Followers.csv")

start()
