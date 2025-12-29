# EDA spike for v1 MVP

## Dataset = housing Data

## file_type =csv

## data_shape

(rows,columns): (20640,9)

## columns

['longitude', 'latitude', 'housing_median_age', 'total_rooms',
'total_bedrooms', 'population', 'households', 'median_income',
'median_house_value']

## Missing values

only total_bedrooms has missing values i.e. 207 missing values out of all the rows

## Data type of each columns

Column Non-Null Count Dtype

0 longitude 20640 non-null float64
1 latitude 20640 non-null float64
2 housing_median_age 20640 non-null float64
3 total_rooms 20640 non-null float64
4 total_bedrooms 20433 non-null float64
5 population 20640 non-null float64
6 households 20640 non-null float64
7 median_income 20640 non-null float64
8 median_house_value 20640 non-null float64

## total description of our data

| index | longitude            | latitude           | housing_median_age  | total_rooms         | total_bedrooms     | population          | households         | median_income       | median_house_value  |
| ----- | -------------------- | ------------------ | ------------------- | ------------------- | ------------------ | ------------------- | ------------------ | ------------------- | ------------------- |
| count | 20640\.0             | 20640\.0           | 20640\.0            | 20640\.0            | 20433\.0           | 20640\.0            | 20640\.0           | 20640\.0            | 20640\.0            |
| mean  | -119\.56970445736432 | 35\.63186143410853 | 28\.639486434108527 | 2635\.7630813953488 | 537\.8705525375618 | 1425\.4767441860465 | 499\.5396802325581 | 3\.8706710029069766 | 206855\.81690891474 |

## Simple rules for columns and data

1. longitue: range = -180 to +180
2. latitude: range = -90 to +90
3. housing_median_age >=0
4. total_rooms >=0
5. total_bedrooms >=0
6. population >=0
7. median_income >= 0
8. median_house_value >=0
9. households > 0

## required columns

all columns are required although total_bedrooms can be neglected but still we can derive good information from that so lets keep it that way

## required values

all columns must be non-null except total_bedrooms which we will handle by filling up with median value of that column

## handling missing values

since only total_bedrooms has missing values we will use median for filling up those rows

## charts for v1

Total 3 charts and 3 KPI's. Hasn't decided on which charts yet

## KPI's

1. Total rows loaded
2. Total missing values
3. Columns missing values

## Charts

1. scatter plot: median_income vs median_house_value
2. histogram: median_house_value
3. Map-like view: average median_house_value binned by lat/long

## Job status fields

- status = pending/processing/succeeded/failed
- created_at,started_at,finished_at
- error_messages (if failed)
