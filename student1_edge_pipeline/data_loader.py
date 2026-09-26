from pathlib import Path
import numpy as np


class IMSDataLoader:

    def __init__(self, data_directory):

        self.data_directory = Path(data_directory)

    def get_data_files(self):

        """
        Find actual vibration files inside all
        subfolders of the IMS dataset.
        """

        files = []

        # Search inside 1st_test, 2nd_test, 3rd_test
        for test_folder in self.data_directory.iterdir():

            if test_folder.is_dir():

                for file in test_folder.iterdir():

                    if file.is_file():

                        files.append(file)

        return sorted(files)

    def load_file(self, file_path):

        try:

            data = np.loadtxt(file_path)

            if data.size == 0:

                return None

            if data.ndim == 1:

                data = data.reshape(-1, 1)

            return data

        except Exception as error:

            print(
                f"Could not load file: {file_path}"
            )

            print(error)

            return None

    def stream_files(self):

        files = self.get_data_files()

        print(
            f"Found {len(files)} actual vibration files."
        )

        for file_path in files:

            signal_data = self.load_file(
                file_path
            )

            if signal_data is None:

                continue

            yield {

                "file_name": file_path.name,

                "signal": signal_data

            }