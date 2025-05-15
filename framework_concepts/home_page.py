from interview_prep.framework_concepts.ui_page import CustomBasePage


class HomePage(CustomBasePage):

    @classmethod
    def is_page_open(cls):
        print("chceks if HomePage is open")
        print("returns False")

    @classmethod
    def open_page(cls):
        print("Assuming user is logged in. Click on Home Logo")


