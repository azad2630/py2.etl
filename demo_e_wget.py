import wget

IRIS_download_URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"
wget.download(IRIS_download_URL, out='IRIS.csv')

