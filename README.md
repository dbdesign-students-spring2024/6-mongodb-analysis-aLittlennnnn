# AirBnB MongoDB Analysis

## Data scrubbing
The [data](/data/listings.csv) set is downloaded from [AirBnB listings data](http://insideairbnb.com/get-the-data.html) containing information of the listings data of Airbnb of New York City for the 12 months leading up to March 7th 2024.

The following is the first 20 rows of the raw data. Only rows with full information are shown since the data is kind of messed up.


The file was too big and contains information not contributing to answering the questions. It also has a lot of empty lines and cells. So I want to first clean the data.
Before importing the data to MongoDB, I used [python file](/scrubbing.py) to help clean up the data. There's two changes I've done through this file to the original data.
- In order to focus on the most important information of this table, I cleaned up the data to contain only the following columns:
```python
['id',
'name',
'host_id',
'host_is_superhost',
'price',
'neighbourhood',
'host_name',
'neighbourhood_group_cleansed',
'review_scores_rating',
'beds',
'review_scores_rating']
```
- I replaced all the empty values with NA to help with future analysis.
```python
for row in reader:
        row = {col:row[col] if row[col] != '' else '#NA' for col in relevant_columns}
        writer.writerow(row)
```

## Import the data into a MongoDB collection
I used the following command to do the importing:
```
[yw6157@i6 ~]$ mongoimport --headerline --type=csv --db=yw6157 --collection=listings --host=class-mongodb.cims.nyu.edu --file=listings_clean.csv --username=yw6157 --password=heH7egqr
```

## Data Analysis in MongoDB
### 1. show exactly two documents from the 'listings' collection in any order: 
I used the following query to show the first two documents from the 'listings' collection, the output is also included.
```
yw6157> db.listings.find({}).limit(2)
[
  {
    _id: ObjectId('660dc16db6515eb20578075c'),
    id: Long('816783428767938211'),
    name: 'Cool studio 3 min from subway!',
    host_id: 47125955,
    host_name: 'Rebeca',
    host_is_superhost: 'f',
    neighbourhood: '#NA',
    neighbourhood_group_cleansed: 'Queens',
    beds: 1,
    price: '$110.00',
    review_scores_rating: 5
  },
  {
    _id: ObjectId('660dc16db6515eb20578075d'),
    id: 35776956,
    name: 'luxury apt in long lsland city  1min to subway',
    host_id: 221012726,
    host_name: 'Lyn',
    host_is_superhost: 'f',
    neighbourhood: '#NA',
    neighbourhood_group_cleansed: 'Queens',
    beds: '#NA',
    price: '#NA',
    review_scores_rating: 2
  }
]
```

### 2. show exactly 10 documents in any order, but "prettyprint" in easier to read format, using the `pretty()` function.
I used the following query to show the first 10 documents from the 'listings' collection using pretty print, and the first three outputs are included.
```
yw6157> db.listings.find({}).limit(10).pretty()
[
  {
    _id: ObjectId('660dc16db6515eb20578075c'),
    id: Long('816783428767938211'),
    name: 'Cool studio 3 min from subway!',
    host_id: 47125955,
    host_name: 'Rebeca',
    host_is_superhost: 'f',
    neighbourhood: '#NA',
    neighbourhood_group_cleansed: 'Queens',
    beds: 1,
    price: '$110.00',
    review_scores_rating: 5
  },
  {
    _id: ObjectId('660dc16db6515eb20578075d'),
    id: 35776956,
    name: 'luxury apt in long lsland city  1min to subway',
    host_id: 221012726,
    host_name: 'Lyn',
    host_is_superhost: 'f',
    neighbourhood: '#NA',
    neighbourhood_group_cleansed: 'Queens',
    beds: '#NA',
    price: '#NA',
    review_scores_rating: 2
  },
  {
    _id: ObjectId('660dc16db6515eb20578075e'),
    id: 52331775,
    name: 'Queen Bedroom A w/Private Bathroom in #608',
    host_id: 305240193,
    host_name: 'June',
    host_is_superhost: 'f',
    neighbourhood: '#NA',
    neighbourhood_group_cleansed: 'Manhattan',
    beds: '#NA',
    price: '#NA',
    review_scores_rating: '#NA'
  }
]
```

### 3. choose two hosts (by reffering to their `host_id` values) who are superhosts (available in the `host_is_superhost` field), and show all of the listings offered by both of the two hosts
   - only show the `name`, `price`, `neighbourhood`, `host_name`, and `host_is_superhost` for each result
1. First I used the following query to get the `host_id` of 2 of the superhosts and get the results.
```
yw6157> db.listings.find({host_is_superhost:"t"},{host_id:1}).limit(2)
[
  { _id: ObjectId('660dc16db6515eb20578076c'), host_id: 174458184 },
  { _id: ObjectId('660dc16db6515eb205780772'), host_id: 52339704 }
]
```
2. Then I used the following query to show the two corresponding documents of the 2 selected hosts by specifying the `host_id`. In order to show only the required fields, I used the projection to limit the fields. There's a total of 4 results and only the first three are shown as required.

```
yw6157> db.listings.find({$or:[{host_id:174458184},{host_id:52339704}]},{_id:0,name:1,price:1,neighbourhood:1,host_name:1,host_is_superhost:1})
[
  {
    name: 'Comfortable and relaxing place',
    host_name: 'Zoraida',
    host_is_superhost: 't',
    neighbourhood: 'Bronx, New York, United States',
    price: '$98.00'
  },
  {
    name: 'Beautiful 3 bedroom APT in Queens NY',
    host_name: 'Angel R.',
    host_is_superhost: 't',
    neighbourhood: '#NA',
    price: '$199.00'
  },
  {
    name: 'Newly renovated 2 Bedroom APT,in Astoria, NYC',
    host_name: 'Angel R.',
    host_is_superhost: 't',
    neighbourhood: 'Queens, New York, United States',
    price: '$189.00'
  }
]
```

### 4. find all the unique `host_name` values
I used the following query and get the outputs.
```
yw6157> db.listings.distinct('host_name')
[
  NaN,               123,                  475,
  '#NA',             '(Ari) HENRY LEE',    '-TheQueensCornerLot',
  '2018Serenity',    '48Lex',              'A',
  'A Group',         'A J',                'A.',
  'A. Beatriz',      'A.B.',               'A.M',
  'A.T.',            'A.V.',               'AFI Apartments',
  'AHm',             'AVacations',         'Aafreen',
  'Aalap',           'Aaliyah',            'Aamer',
  'Aamir',           'Aanchal',            'Aar',
  'Aaron',           'Aba',                'Abass',
  'Abayomi',         'Abbe',               'Abbey',
  'Abby',            'Abbygale',           'Abc',
  'Abdes',           'Abdo',               'Abdon',
  'Abdoulaye',       'Abdul',              'Abdulcelil',
  'Abdullah',        'Abdur Malik',        'Abe',
  'Abe & Gail',      'Abeer',              'Abel',
  'Abena',           'Abhi',               'Abhilasha Ashiv',
  'Abhinaya',        'Abhishek',           'Abi',
  'Abigail',         'Abinav',             'Abir',
  'Abisoye',         'Abosi',              'Abr',
  'Abraham',         'Abul',               'Aby',
  'AcHomeAway',      'Acadia',             'Acclaimed',
  'Ace',             'Ace Hotel Brooklyn', 'Ace Hotel New York',
  'Achiaa',          'Acima',              'Ad',
  'Ada',             'Ada Azra',           'Adal',
  'Adalgisa',        'Adam',               'Adam + Caro',
  'Adamilca',        'Adana',              'Adanna',
  'Adar',            'Adarsh',             'Adashima',
  'Addie',           'Address In NYC',     'Addy',
  'Ade',             'Adekunle',           'Adel & Katie',
  'Adel And Chriss', 'Adelaide',           'Adele',
  'Adelle',          'Adelma',             'Ademi',
  'Ademola',         'Adena',              'Adenomo',
  'Adenrele',
  ... 8718 more items
]
```
Since there's significantly more listings than the number of hosts, we can conclude that there are quite a lot of hosts that have multiple listings.

### 5. find all of the places that have more than 2 `beds` in a neighborhood of your choice (referred to as either the `neighborhood` or `neighbourhood_group_cleansed` fields in the data file), ordered by `review_scores_rating` descending
   - only show the `name`, `beds`, `review_scores_rating`, and `price`
   - if your data set only has blanks for all the neighborhood-related fields, or only one neighborhood value in all documents, you may pick another field to filter by - include an explanation and justification for this in your report.
   - if you run out of memory for this query, try filtering `review_scores_rating` that aren't empty (`$ne`); and lastly, if there's still an issue, you can set the `beds` to match exactly 2.
I found all the places with more than 2 `beds` in `Brooklyn` using the following query and get the results. Only the first 3 are shown as required.
```
yw6157> db.listings.find({neighbourhood_group_cleansed:'Brooklyn',beds:{$gt:2}},{_id:0,name:1,beds:1,review_scores_rating:1,price:1}).sort({review_scores_rating:-1})
[
  {
    name: 'Spacious 2Bd Near Dumbo+W/D',
    beds: 3,
    price: '$232.00',
    review_scores_rating: '#NA'
  },
  {
    name: 'Charming 2 Floor Apartment with Backyard',
    beds: 3,
    price: '$130.00',
    review_scores_rating: '#NA'
  },
  {
    name: '2bd/2full bath w/kitchen & w/d',
    beds: 3,
    price: '$125.00',
    review_scores_rating: '#NA'
  }
]
```
As we can see, most of the results don't have the ratings information, so I added an entra criterion of `review_scores_rating:{$ne:"#NA"}` to find some results that have ratings. Only the first 3 results are shown.
```
yw6157> db.listings.find({neighbourhood_group_cleansed:'Brooklyn',beds:{$gt:2},review_scores_rating:{$ne:"#NA"}},{_id:0,name:1,beds:1,review_scores_rating:1,price:1}).sort({review_scores_rating:-1})
[
  {
    name: 'Home away from home.',
    beds: 3,
    price: '$180.00',
    review_scores_rating: 5
  },
  {
    name: 'Family friendly 2bd  in Boerum/Cobble Hill',
    beds: 3,
    price: '$230.00',
    review_scores_rating: 5
  },
  {
    name: 'Modern, Carroll Garden Townhouse',
    beds: 4,
    price: '$375.00',
    review_scores_rating: 5
  }
]
```
From the results we can see that there're a lot of listings without a rating information. And due to the large data, we can find results even with more restrictions added.

### 6. show the number of listings per host
I used the following query and get the outputs.
```
yw6157> db.listings.aggregate({$group:{_id:"$host_id",listingCount:{$sum:1}}})
[
  { _id: 43461100, listingCount: 1 },
  { _id: 243466968, listingCount: 1 },
  { _id: 58237695, listingCount: 1 }
]
```
Only the first three ids are shown, but from the result I find hosts with listings from 1 to even 65, we can see that the number of listings actually varies a lot.

### 7. find the average `review_scores_rating` per neighborhood, and only show those that are `4` or above, sorted in descending order of rating (see [the docs](https://docs.mongodb.com/manual/reference/operator/aggregation/sort/))
   - if your data set only has blanks in the neighborhood-related fields, or only one neighborhood value in all documents, you may pick another field to break down the listings by - include an explanation and justification for this in your report.
I used the following query and get the results.
```
yw6157> db.listings.aggregate([ { $group: { _id: "$neighbourhood_group_cleansed", averageRating: { $avg: "$review_scores_rating" } } }, { $match: { averageRating: { $gt: 4 } } }, { $sort: { averageRating: -1 } }] );
[
  { _id: 'Staten Island', averageRating: 4.765718954248366 },
  { _id: 'Brooklyn', averageRating: 4.74221756542796 },
  { _id: 'Bronx', averageRating: 4.695215215215216 },
  { _id: 'Queens', averageRating: 4.666091033851784 },
  { _id: 'Manhattan', averageRating: 4.660964896489649 }
]
```
From looking at the raw data, we can definitely not get such information. Among all the neighborhoods, Brooklyn has the highest average rating.

## Extra Credit
 This assignment deserve extra credits because I have successfully setup python mongdb envrionment, and performed the query that finds all the places that have more than 2 beds in the neighborhood 'Brooklyn', and displayed in descending order. I also used the pretty print 'pprint()' function in pymongo to pretty print the results.

 I set up the virtual environment on **i6** and run the file [extra_credit.py](/extra_credit.py) on **i6**.

1. Here I successfully connected to my database:
```
connection = pymongo.MongoClient("class-mongodb.cims.nyu.edu", 27017,
                                username="yw6157",
                                password="heH7egqr",
                                authSource="yw6157")
collection = connection["yw6157"]["listings"]
```
2. Then I have my queries.
```
query = {
    "beds": {"$gt": 2},
    "neighbourhood_group_cleansed":'Brooklyn'
}
projection = {
    "_id": 0,
    "name": 1,
    "beds": 1,
    "review_scores_rating": 1,
    "price": 1
}
```
3. Then I created a list to store all the results retrieved by the cursor and print each of the documents.
```
results = collection.find(query, projection).sort("review_scores_rating", -1)

for document in results:
    pprint.pprint(document)
```
4. The following are the pretty-printed results. There are too many of them, only the first 3 are shown.
 ```
 (.venv) [yw6157@i6 ~]$ python extra_credit.py
{'beds': 3,
 'name': 'Spacious 2Bd Near Dumbo+W/D',
 'price': '$232.00',
 'review_scores_rating': '#NA'}
{'beds': 3,
 'name': 'Charming 2 Floor Apartment with Backyard',
 'price': '$130.00',
 'review_scores_rating': '#NA'}
{'beds': 3,
 'name': '2bd/2full bath w/kitchen & w/d',
 'price': '$125.00',
 'review_scores_rating': '#NA'}
 ```
 We can see that the results are the same with running mongoDB directly.