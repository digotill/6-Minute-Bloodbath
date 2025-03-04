import pickle
import os


class SaveLoadSystem:
    def __init__(self, file_extension, save_folder):
        self.file_extension = file_extension  # File extension for saved data (e.g., ".save")
        self.save_folder = save_folder  # Folder where save files are stored (e.g., "save_data")

    def save_data(self, data, name):
        # Save data to a file using pickle
        data_file = open(self.save_folder + "/" + name + self.file_extension, "wb")
        pickle.dump(data, data_file)  # Serialize and write data to file

    def load_data(self, name):
        # Load data from a file using pickle
        data_file = open(self.save_folder + "/" + name + self.file_extension, "rb")
        data = pickle.load(data_file)  # Deserialize data from file
        return data

    def check_for_file(self, name):
        # Check if a save file exists
        return os.path.exists(self.save_folder + "/" + name + self.file_extension)

    def load_game_data(self, files_to_load, default_data):
        # Load multiple game data files, using default values if files don't exist
        # files_to_load: List of file names to load (e.g., ["entities", "number"])
        # default_data: List of default values corresponding to files_to_load (e.g., [[], 1])
        variables = []
        for index, file in enumerate(files_to_load):
            if self.check_for_file(file):
                variables.append(self.load_data(file))  # Load existing file
            else:
                variables.append(default_data[index])  # Use default value if file doesn't exist

        # Return as tuple if multiple variables, otherwise return single value
        if len(variables) > 1:
            return tuple(variables)
        else:
            return variables[0]

    def save_game_data(self, data_to_save, file_names):
        # Save multiple game data files
        # data_to_save: List of data to save (e.g., [entities, number])
        # file_names: List of file names corresponding to data_to_save (e.g., ["entities", "number"])
        for index, file in enumerate(data_to_save):
            self.save_data(file, file_names[index])  # Save each piece of data to its corresponding file
