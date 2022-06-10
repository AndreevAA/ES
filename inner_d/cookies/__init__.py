import os


# Собственный Cookies
class Cookies:
    auth_file = None

    def __init__(self):
        self.auth_file = "cookie/auth.txt"

    def is_auth_opened(self):
        if os.path.exists(self.auth_file):
            return True
        return False

    def set_auth_opened(self, user_id, user_login):
        self._delete_cookies_file(self.auth_file)
        self._write_cookies_to_file(self.auth_file, str(user_id) + " " + str(user_login) + "\n")

        print("SUCCESS_WRITE")

    def set_auth_closed(self):
        self._delete_cookies_file(self.auth_file)

    def _write_cookies_to_file(self, file_path, content):
        wf = open(file_path, 'w')
        wf.write(content)
        wf.close()

    def _delete_cookies_file(self, file_path):
        print("DELETING")
        if os.path.exists(file_path):
            os.remove(
                os.path.join(file_path)
            )

    def get_auth_cookie(self):
        return str(open(self.auth_file).read()).split()
