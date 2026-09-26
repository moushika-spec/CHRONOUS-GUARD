import pandas as pd

from config import (
    RAW_DATA_PATH,
    SAMPLING_FREQUENCY,
    WINDOW_SIZE,
    STEP_SIZE,
    ROLLING_WINDOW_SIZE,
    FEATURE_OUTPUT_FILE
)

from data_loader import IMSDataLoader

from preprocessing import SignalPreprocessor

from feature_extractor import (
    VibrationFeatureExtractor
)

from rolling_statistics import RollingZScore


class EdgeSignalPipeline:

    def __init__(self, data_directory):

        self.loader = IMSDataLoader(
            data_directory
        )

        self.preprocessor = SignalPreprocessor(
            SAMPLING_FREQUENCY
        )

        self.feature_extractor = (
            VibrationFeatureExtractor()
        )

        self.rms_zscore = RollingZScore(
            ROLLING_WINDOW_SIZE
        )

        self.kurtosis_zscore = RollingZScore(
            ROLLING_WINDOW_SIZE
        )

    def process(self):

        all_features = []

        global_window_index = 0

        for file_data in self.loader.stream_files():

            file_name = file_data[
                "file_name"
            ]

            raw_signal = file_data[
                "signal"
            ]

            # Select first vibration channel
            if raw_signal.ndim > 1:

                vibration_signal = (
                    raw_signal[:, 0]
                )

            else:

                vibration_signal = raw_signal

            # Clean
            vibration_signal = (
                self.preprocessor.clean_signal(
                    vibration_signal
                )
            )

            # Detrend
            vibration_signal = (
                self.preprocessor.detrend_signal(
                    vibration_signal
                )
            )

            # Create windows
            windows = (
                self.preprocessor.create_windows(
                    vibration_signal,
                    WINDOW_SIZE,
                    STEP_SIZE
                )
            )

            for window in windows:

                features = (
                    self.feature_extractor
                    .extract_features(window)
                )

                # Rolling Z-score for RMS
                rms_statistics = (
                    self.rms_zscore.update(
                        features["rms"]
                    )
                )

                # Rolling Z-score for Kurtosis
                kurtosis_statistics = (
                    self.kurtosis_zscore.update(
                        features["kurtosis"]
                    )
                )

                feature_record = {

                    "file_name": file_name,

                    "window_index":
                    global_window_index,

                    "mean":
                    features["mean"],

                    "rms":
                    features["rms"],

                    "std":
                    features["std"],

                    "kurtosis":
                    features["kurtosis"],

                    "peak":
                    features["peak"],

                    "crest_factor":
                    features["crest_factor"],

                    "rolling_rms_mean":
                    rms_statistics[
                        "rolling_mean"
                    ],

                    "rolling_rms_std":
                    rms_statistics[
                        "rolling_std"
                    ],

                    "rms_z_score":
                    rms_statistics[
                        "z_score"
                    ],

                    "rolling_kurtosis_mean":
                    kurtosis_statistics[
                        "rolling_mean"
                    ],

                    "rolling_kurtosis_std":
                    kurtosis_statistics[
                        "rolling_std"
                    ],

                    "kurtosis_z_score":
                    kurtosis_statistics[
                        "z_score"
                    ]

                }

                all_features.append(
                    feature_record
                )

                global_window_index += 1

        return all_features


def main():

    pipeline = EdgeSignalPipeline(
        RAW_DATA_PATH
    )

    features = pipeline.process()

    dataframe = pd.DataFrame(
        features
    )

    dataframe.to_csv(
        FEATURE_OUTPUT_FILE,
        index=False
    )

    print(
        "\n================================="
    )

    print(
        "EDGE SIGNAL PIPELINE COMPLETED"
    )

    print(
        "================================="
    )

    print(
        f"Windows Processed: {len(dataframe)}"
    )

    print(
        f"Output File: {FEATURE_OUTPUT_FILE}"
    )

    print(
        "\nGenerated Features:"
    )

    print(
        dataframe.head()
    )


if __name__ == "__main__":

    main()