# Cactpot Solver (The Only One Probably <3)
## Usage
```
♥ python . <board>
```
Where `board` is a 9-character string of unique digits and `?` characters representing the known values of a mini cactpot board. Values are given left-to-right, top-to-bottom
## Examples
```
♥ python . 123456789
Average Payouts:
    180   108   180   119   180    
      ↘    ↓     ↓     ↓    ↙
        ┌─────┬─────┬─────┐
10000 → │  1  │  2  │  3  │
        ├─────┼─────┼─────┤
  180 → │  4  │  5  │  6  │
        ├─────┼─────┼─────┤
 3600 → │  7  │  8  │  9  │
        └─────┴─────┴─────┘
...
```
```
♥ python . 12??5?7?9
Average Payouts:
    180   121   146   568   169    
      ↘    ↓     ↓     ↓    ↙
        ┌─────┬─────┬─────┐
 2662 → │  1  │  2  │  ?  │
        ├─────┼─────┼─────┤
  105 → │  ?  │  5  │  ?  │
        ├─────┼─────┼─────┤
 1021 → │  7  │  ?  │  9  │
        └─────┴─────┴─────┘

```

