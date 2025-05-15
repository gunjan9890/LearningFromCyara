
class CustomBasePage:

    @classmethod
    def navigate_to_page(cls):
        if not cls.is_page_open():
            if cls is not CustomBasePage:
                parent = cls.__bases__[0]
                parent.navigate_to_page()
            cls.open_page()

    @classmethod
    def open_page(cls):
        print("Opened Base Page")

    @classmethod
    def is_page_open(cls):
        print("checks if the browser is launched")
        print("return False")
        return True