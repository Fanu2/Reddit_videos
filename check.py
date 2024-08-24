import sys

if sys.version_info.major != 3 or sys.version_info.minor not in [10, 11]:
    print(
        "Hey! Congratulations, you've made it so far (which is pretty rare with no Python 3.10). Unfortunately, this program only works on Python 3.10. Please install Python 3.10 and try again."
    )
    sys.exit()
