import kaggle
import os

os.environ["KAGGLE_CONFIG_DIR"] = "..\kaggle.json"

# Define dataset (use the dataset URL to find this name)
dataset_name = "psparks/instacart-market-basket-analysis"

# Download the dataset
kaggle.api.dataset_download_files(dataset_name, path="data", unzip=True)

print("Download completed!")