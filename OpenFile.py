def appendFile(absolut_filepath, content):
    with open(absolut_filepath, 'a') as file:
        file.write(content)


def writeFile(absolut_filepath, content):
    with open(absolut_filepath, 'w') as file:
        file.write(content)


def openFileByString(absolut_filepath):
    with open(absolut_filepath, 'r') as file:
        return file.read()


def openFileByLines(absolut_filepath):
    with open(absolut_filepath, 'r') as file:
        return file.readlines()