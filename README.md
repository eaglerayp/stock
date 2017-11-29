# TWSE Stock Predition

1. Fetch stock daily data from bloomberg and store into db?
1. Input: Daily data > 1 year for one stock
1. Output: Training SVM model per stock (binary classfication: stock price +/- tomorrow)

## Usage

After clone this repository, it's necessary to install dependency python package first

```sh
~$ pip install -r requirements.txt
```

Then execute below command to run test case

```sh
~$ python svm.py
```

## Process

### Data preprocessing

1. Transform daily data to n-days diff
1. Lable answer (+/- in following n days)
1. PCA choose main component

### Model Building

1. Call whatever SVM library

### Test

1. Use last month data for testing
1. Choose rate > 90% to trading