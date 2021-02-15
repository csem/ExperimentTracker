from setuptools import setup, find_packages


setup(
    name="csem_experimenttracker",
    version="0.0.1",
    author="CSEM",
    packages=find_packages("src/CSEM_ExperimentTracker"),
    package_dir={"": "src/"},
    entry_points={
        "console_scripts": [
            "clean_folder=CSEM_ExperimentTracker.load_files:delete_empty_folder",
            "save_df = CSEM_ExperimentTracker.load_files:save_df",
        ]
    },
)
