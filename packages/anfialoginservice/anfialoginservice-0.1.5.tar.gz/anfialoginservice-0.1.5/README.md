How to use it?

This small program builds a config.txt file where user and password are stored. It is intended to be used with Microsoft. Then, it executes the login with pywinauto. It can also retrieve server and database names for SQL server, and can also be configured for FTP. Intended for usage inside my organization.

To use it, first of all declare variables. Right now, the config file is configured to accept Microsoft username and password, server name and database name, and ftp info. Call user, password... = anfialoginservice.get_login_info_from_config(). If you don't need all variables, for example, type user, password, *rest = anfialoginservice.get_login_info_from_config().

Then, if you want to auto-login, you can do it with simulate_user_login(), currently only for Microsoft ID access prompts. You must start a thread to do so.

from threading import Thread

    auth_thread = Thread(target=als.simulate_user_login, args=(user, password, etc...))

    auth_thread.start()

Then execute the rest of the code that will trigger the login request.