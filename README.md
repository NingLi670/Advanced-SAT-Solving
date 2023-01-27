Use the command to run our SAT solver:

`python main.py -i [CNF instance path] -d xx -r xx -m xx -b xx -s xx`

### Parameter Explanation:

#### Different Heuristics

Use `-d` to change the heuristic algorithm.
`-d 0`: Use VSIDS as heuristic algorithm.
`-d 1`: Use LRB as heuristic algorithm.
`-d 2`: Use CHB as heuristic algorithm.

#### Restart

Use `-r`to decide whether to use restart.
`-r 0`: No restart.
`-r 1`: Restart
Use `-m` to change the bandit algorithm.
`-m 0`: No bandit algorithm.
`-m 1`: MOSS
`-m 2`: UCB

#### Preprocess:

`-b`: Whether to use bounded variable elimination and the maximum number of clauses(Refer to the report for more information).
`-s`: Whether to use subsumption.
I recommand you to choose one parameter combination from these three combinations:
`-b 0 -s 0`: No preprocessing
`-b 100 -s 0`: Only use bounded variable elimination
`-b 0 -s 1`: Only use subsumption