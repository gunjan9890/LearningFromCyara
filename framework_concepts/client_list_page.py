from interview_prep.framework_concepts.home_page import HomePage


class ClientListPage(HomePage):

    @classmethod
    def open_page(cls):
        print("Assuming user is on HomePage, click on Clients Menu")

    @classmethod
    def is_page_open(cls):
        print("Check if Client List Page is opened")
        print("return False")
        return False

ClientListPage.navigate_to_page()