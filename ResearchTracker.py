import json
import os
from datetime import datetime

# ---------------- FILE HANDLING ---------------- #

DATA_FILES = {
    "publications": "publications.json",
    "patents": "patents.json",
    "funds": "funds.json"
}

def load_data(file):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return json.load(f)

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


# ---------------- DATA CLASSES ---------------- #

class Publication:
    def __init__(self, title, category, author):
        self.title = title
        self.category = category
        self.author = author
        self.date = str(datetime.now().date())

    def to_dict(self):
        return self.__dict__


class Patent:
    def __init__(self, title, inventor):
        self.title = title
        self.inventor = inventor
        self.status = "Filed"

    def approve(self):
        self.status = "Approved"

    def to_dict(self):
        return self.__dict__


class FundRequest:
    def __init__(self, member, amount, purpose):
        self.member = member
        self.amount = amount
        self.purpose = purpose
        self.status = "Pending"

    def approve(self):
        self.status = "Granted"

    def to_dict(self):
        return self.__dict__


# ---------------- SYSTEM CONTROLLER ---------------- #

class ResearchTrackerSystem:

    def __init__(self):
        self.publications = load_data(DATA_FILES["publications"])
        self.patents = load_data(DATA_FILES["patents"])
        self.funds = load_data(DATA_FILES["funds"])

    # -------- DASHBOARD -------- #
    def dashboard(self):
        print("\n------ DASHBOARD ------")
        print("Total Publications:", len(self.publications))
        print("Total Patents Filed:", len(self.patents))
        print("Approved Patents:",
              sum(1 for p in self.patents if p["status"] == "Approved"))

        categories = {}
        for p in self.publications:
            categories[p["category"]] = categories.get(p["category"], 0) + 1
        print("Publications by Category:", categories)

    # -------- PUBLICATIONS -------- #
    def add_publication(self):
        title = input("Title: ")
        category = input("Category (Journal/Conference/Scopus/etc): ")
        author = input("Author: ")
        pub = Publication(title, category, author)
        self.publications.append(pub.to_dict())
        save_data(DATA_FILES["publications"], self.publications)
        print("Publication added successfully.")

    def view_publications(self):
        for i, p in enumerate(self.publications, 1):
            print(f"{i}. {p['title']} | {p['category']} | {p['author']}")

    # -------- PATENTS -------- #
    def file_patent(self):
        title = input("Patent Title: ")
        inventor = input("Inventor Name: ")
        patent = Patent(title, inventor)
        self.patents.append(patent.to_dict())
        save_data(DATA_FILES["patents"], self.patents)
        print("Patent filed successfully.")

    def approve_patent(self):
        for i, p in enumerate(self.patents, 1):
            print(f"{i}. {p['title']} | Status: {p['status']}")
        choice = int(input("Select patent to approve: ")) - 1
        self.patents[choice]["status"] = "Approved"
        save_data(DATA_FILES["patents"], self.patents)
        print("Patent approved.")

    # -------- FUND REQUESTS -------- #
    def request_fund(self):
        member = input("Member Name: ")
        amount = float(input("Amount Requested: "))
        purpose = input("Purpose: ")
        fund = FundRequest(member, amount, purpose)
        self.funds.append(fund.to_dict())
        save_data(DATA_FILES["funds"], self.funds)
        print("Fund request submitted.")

    def approve_fund(self):
        for i, f in enumerate(self.funds, 1):
            print(f"{i}. {f['member']} | {f['amount']} | {f['status']}")
        choice = int(input("Select fund request to approve: ")) - 1
        self.funds[choice]["status"] = "Granted"
        save_data(DATA_FILES["funds"], self.funds)
        print("Funds granted.")

    # -------- MENU -------- #
    def menu(self):
        while True:
            print("""
------ RESEARCH TRACKER ------
1. View Dashboard
2. Add Publication
3. View Publications
4. File Patent
5. Approve Patent (Dept)
6. Request Research Funds
7. Grant Research Funds (Dept)
0. Exit
""")
            choice = input("Enter choice: ")

            if choice == "1":
                self.dashboard()
            elif choice == "2":
                self.add_publication()
            elif choice == "3":
                self.view_publications()
            elif choice == "4":
                self.file_patent()
            elif choice == "5":
                self.approve_patent()
            elif choice == "6":
                self.request_fund()
            elif choice == "7":
                self.approve_fund()
            elif choice == "0":
                print("Exiting system...")
                break
            else:
                print("Invalid choice!")


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    system = ResearchTrackerSystem()
    system.menu()