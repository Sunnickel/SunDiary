import os
import datetime
import json


banner = """
  ________  ____  ____  _____  ___       ________   __          __        _______   ___  ___  
 /"       )("  _||_ " |(\\"   \|"  \     |"      "\ |" \        /""\      /"      \ |"  \/"  | 
(:   \___/ |   (  ) : ||.\\\\   \    |    (.  ___  :)||  |      /    \    |:        | \   \  /  
 \___  \   (:  |  | . )|: \.   \\\\  |    |: \   ) |||:  |     /' /\  \   |_____/   )  \\\\  \/   
  __/  \\\\   \\\\ \__/ // |.  \    \. |    (| (___\ |||.  |    //  __'  \   //      /   /   /    
 /" \   :)  /\\\\ __ //\ |    \    \ |    |:       :)/\  |\  /   /  \\\\  \ |:  __   \  /   /     
(_______/  (__________) \___|\____\)    (________/(__\_|_)(___/    \___)|__|  \___)|___/      
                                                                                              


        [::] Sun Diary
        [::] Made by Sunnickel
"""
diary_list = """
        Site {} / {}
        --------------------------------------------"""
options_menu = """        
        [1] Add a Diary Entry
        [2] Edit a Diary Entry
        [3] Delete a Diary Entry
"""

file_extensions = "txt"

def getInfosFromConfig(getInfo):
    f = open("config.json", "r")
    config = json.load(f)
    return config[getInfo]


def getOption():
    print(options_menu)
    while True:
        option = input(f"What do you want to do {getInfosFromConfig('name')}? ")
        if option == "1":
            newEntry()
            break
        if option == "2":
            editEntry()
            break
        if option == "3":
            deleteEntry()
            break


def printSite(site):
    site_num = len(os.listdir("entrys"))
    print(diary_list.format(site, site_num))
    file_num = 1
    for file in os.listdir(f"entrys/site{site}"):
        file_time = datetime.datetime.fromtimestamp(os.path.getmtime(f"entrys/site{site}/{file}"))
        print(f"        [{file_num}] {file}                   {file_time.strftime('%d.%m.%Y')}")
        file_num += 1


def getEntry(site=1):
    siteNum = len(os.listdir("entrys"))

    printSite(site)
    if not os.listdir("entrys/site1"):
        print("        No entries")
        choice = input("\nDo you want to make a new entry? (y/n) ")
        if choice == "y":
            newEntry()
        elif choice == "n":
            exit()
    entry = ""

    while not entry.isnumeric():
        print("\nIf you want to go to another site, enter < or >")
        entry = input(f"Which entry would you like to select {getInfosFromConfig('name')}? ")
        if entry == "<":
            if siteNum == 1:
                for i in range(20):
                    print()
                printSite(site)
                print("\n        You are already on the first site!")
            else:
                site -= 1
                printSite(site)
        if entry == ">":
            if siteNum == siteNum:
                for i in range(20):
                    print()
                printSite(site)
                print("\n        You are already on the last site!")
            else:
                site += 1
                printSite(site)
        if entry.isnumeric():
            return {"entry": entry, "site": site}


def newEntry():
    today = datetime.date.today()
    todayFormatted = f"{today.day}.{today.month}.{today.year}"
    entryNum = 1
    for file in os.listdir("entrys/site1"):
        if file is today:
            print("        The entry already exists")
            choice = input("        Do you want to edit the entry?")[0]
            if choice == "y":
                editEntry()
                break
            elif choice == "n":
                getEntry()
                break
    siteNum = len(os.listdir("entrys"))
    for file in os.listdir(f"entrys/site{siteNum}"):
        entryNum += 1
    if entryNum == 10:
        os.mkdir(f"entrys/site{siteNum + 1}")
    with open(f"entrys/site{siteNum}/Entry_{entryNum}.{file_extensions}", "w") as f:
        birthday = ""
        if getInfosFromConfig("birthday") == todayFormatted:
            birthday = "Happy Birthday!"
        f.write(f"{todayFormatted}\n{getInfosFromConfig('name')}\n------------------\n{birthday}\n")
    os.system(f"notepad entrys/site{siteNum}/Entry_{entryNum}.{file_extensions}")


def editEntry():
    for i in range(20):
        print()
    print("Which entry would you like to edit?")
    entry = getEntry()
    siteNum = entry["site"]
    entryNum = entry["entry"]
    os.system(f"notepad entrys/site{siteNum}/Entry_{entryNum}.{file_extensions}")


def deleteEntry():
    for i in range(20):
        print()
    print("Which entry would you like to delete?")
    entry = getEntry()
    siteNum = entry["site"]
    entryNum = entry["entry"]
    os.system(f"del entrys/site{siteNum}/Entry_{entryNum}.{file_extensions}")


def firstEntry():
    for dir in os.listdir():
        if dir == "entrys":
            return
    os.mkdir("entrys")
    os.mkdir("./entrys/site1")
    open("config.json", "w")
    name = input("What is your name? ")
    birthday = input("When is your birthday? ")

    with open("config.json", "w") as configFile:
        info = json.dumps({"name": name, "birthday": birthday})
        configFile.write(info)


if __name__ == '__main__':
    print(banner)
    firstEntry()
    getOption()
