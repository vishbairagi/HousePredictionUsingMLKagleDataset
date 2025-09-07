# HousePredictionUsingMLKagleDataset

This repository contains a machine learning project aimed at predicting house prices using the Kaggle dataset. The project utilizes various machine learning algorithms to build a predictive model.

## Project Structure

The repository includes the following files:

- `app.py` - The main application script.
- `house_price_model.pkl` - The trained machine learning model.
- `house_price_train.py` - Script for training the machine learning model.
- `house_price_ui.py` - User interface script for interacting with the model.
- `predictions.db` - Database file to store predictions.
- `train.csv` - The dataset used for training the model.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- Required Python libraries (pandas, numpy, scikit-learn, flask, matplotlib)

### Installation


```bash
git clone https://github.com/vishbairagi/HousePredictionUsingMLKagleDataset.git
cd HousePredictionUsingMLKagleDataset

pip install -r requirements.txt



python house_price_train.py


python app.py
Dataset

The dataset used for training the model is train.csv, which contains various features related to house properties. Ensure the dataset is in the same directory as the scripts.

Model Training

The house_price_train.py script processes the dataset, selects features, and trains a predictive model using scikit-learn.

Database

The predictions.db file is an SQLite database used to store predictions made by the model. This allows tracking and analyzing past predictions.

License

This project is licensed under the MIT License - see the LICENSE
 file for details.
