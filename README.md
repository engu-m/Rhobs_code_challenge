# Rhobs_code_challenge

The goal of this project is to compute some metrics on some external sample data stored in a MongoDB database for RHOBS, a HR-tech company.

## Installation

To install the project, clone the repository on your local machine, create a python virtual environment, then run in the working directory the following command : `pip install requirements.txt`.
To connect to the database, you will have to fill in the file `credentials.json` with relevant information given by the company RHOBS.

## Assignments

The code written in `mission.py` has 3 purposes : 
  1. Compute the number of listeners by music. 
  2. Compute the average age by music. 
  3. Display the pyramid age: the function should take 2 parameters a city and slice size. Compute the pyramid only for that city. The slice size is the number of years by which you aggregate people (for example 10 by 10 or 3y by 3y).

## Results

Results to each assignment are as follow :
1.
 ```javascript
 {'country': 18971,
 'blues': 20817,
 'hiphop': 28043,
 'metal': 27774,
 'rock': 34472,
 'disco': 34297,
 'pop': 32249,
 'reggae': 19127,
 'jazz': 24304,
 'gabber': 18525,
 'trance': 18173,
 'eurodance': 23487,
 'classical': 21306}
 ```
 
 2.
 ```javascript
 {'country': 42,
 'blues': 50,
 'hiphop': 39,
 'metal': 38,
 'rock': 43,
 'disco': 43,
 'pop': 41,
 'reggae': 39,
 'jazz': 47,
 'gabber': 38,
 'trance': 40,
 'eurodance': 39,
 'classical': 47}
 ```
 
