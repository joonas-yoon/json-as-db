# Benchmark

details on: https://gist.github.com/joonas-yoon/7a67039b90d0554b26a5abdcba23343b

## Loads from file

file_path is `generated_10k.json` which is JSON file containing 10,000 items.

|`jad.load(file_path)`|`pd.read_json(file_path)`|
|:-|:-|
|149.11810 ms|153.71676 ms|


## Appending data

Measure the time calling method to append 1,000 times.

|`db.add(data)`|`df.append(data, ignore_index=True)`|
|:-|:-|
|8.96103 ms|2760.27654 ms|


## Searching items

by increasing `i` from `0` to `10000`, search items with given `i`.

|`db.find(Key('index') > i)`|`df[df['index'] > i]`|
|:-|:-|
|9.87914 ms|2.59354 ms|

