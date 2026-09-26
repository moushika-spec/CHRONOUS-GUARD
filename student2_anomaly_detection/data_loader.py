# type:ignore
import pandas as pd

from config import INPUT_FILE


class FeatureLoader:

    def load(self):

        dataframe = pd.read_csv(
            INPUT_FILE
        )

        return dataframe