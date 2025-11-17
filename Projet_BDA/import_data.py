import kagglehub

# Download latest version
path = kagglehub.dataset_download("novandraanugrah/bitcoin-historical-datasets-2018-2024")

print("Path to dataset files:", path)