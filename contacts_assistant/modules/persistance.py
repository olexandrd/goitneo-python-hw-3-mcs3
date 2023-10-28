import pickle
from pathlib import Path


class AddressBookFile:
    def __init__(self, filename):
        self.filename = filename
        
    def save(self, filename, contacts):
        folder_path = Path.joinpath(Path.cwd(), ".data")
        folder_path.mkdir(exist_ok=True)
        file_path = Path.joinpath(folder_path, filename)
        with open(file_path, "wb") as file:
            pickle.dump(contacts, file)

    def load(self, filename):
        path = Path.joinpath(Path.cwd(), ".data", filename)
        if path.exists():
            with open(path, "rb") as file:
                content = pickle.load(file)
                return content.data


if __name__ == "__main__":
    print("Do not execute this file.")