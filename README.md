# Traffic anomaly detection using LSTM Neural Network
Tool for predicting network traffic for Traffic Monitoring and Analysis (TMA) subject of Master in Cybersecurity at UPC (2022/23)

# Dataset download

## Download and generate MAWI dataset
To generate the MAWI dataset you copy the python notebook located in "python_notebooks" directory to Google Drive. Open "download_mawi_dataset.ipynb" with Google Collab and adjust "date" and "date_dest" parameters to choose the datasets range that will be dowloaded.

- PCAP files will be saved in a directory with the following format: ```/year/month/<pcap_file>```
- After that, it will be sampled with [pcapsampler](https://github.com/groud/pcapsampler) by groud GitHub user.
- Sampled pcap files will be parsed to CSV with [tshark](https://tshark.dev/) command line (filtering only tcp packets).

## Download and generate CAIDA dataset
We have trained the model with MAWI dataset. However, we have tested the precission of the model also with CAIDA dataset. To download the dataset you should follow the next steps:

To generate "time_series_df.csv" dataframe you should follow next steps:
- Install python from: https://www.python.org/downloads/
- Install python requirements: `$ pip install -r requirements.txt`
- Execute "caida_downloader.py": `$ python caida_downloader.py`
- Execute "time_series_generator.py": `$ python time_series_generator.py`

# Dataset processing and model creation
The code is located in "python_notebooks" directory. You should copy "lstm_model.ipynb" notebook to Google Drive. It should be placed in the same folder as where you have downloaded the dataset.

## Dataset processing
We have loaded the previous downloaded datasets and processed in the following way:
1. Dataset reading.
2. Dataset adaptation: choosen parameters as window size and interval size.
3. Dataset analysis: stadistical analysis of the model.

## Model creation
We have created an LSTM model that will read first n time steps to predict the next one. For that task, we have used well-known maching learning libraries as [Keras](https://keras.io/) ans [Sklearn](https://scikit-learn.org/stable/).

We have divided the dataset in two parts:
1. Training dataset: To train the model.
2. Test dataset: Data to test the performance of the model with unseen data.

We have also tested the model with other datasets. The performance decrease significatly. Therefore, it is necessary to retrain the model, but this process require less effort as the model has been pre-trained (fine-tuning).

## Dataset labeling
To label the dataset we have mesaured the slope between two consecutive points. If this slope is equal or higher than that threshold the point is marked as an detection. We consider that the anomaly could have an error. Then, each anomaly is a range between [detection - error, detection + error].

# Sources

## External tools and libs
- https://github.com/groud/pcapsampler
- https://tshark.dev/
- https://keras.io/
- https://scikit-learn.org/stable/

## State of art papers
- https://dl.ifip.org/db/conf/cnsm/cnsm2019/1570563478.pdf
- https://arxiv.org/pdf/1911.11552v1.pdf
