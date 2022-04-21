import os


def cwd(path):
    path = path.format(os.getcwd())
    return path


class Folders:
    database = cwd(r"{}/database")


class Files:
    icon = cwd(r"{}/logo.ico")
    db = cwd(r"{}/surveyfiles.db")