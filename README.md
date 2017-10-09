This tool uses a Genetic Algorithm to fit a sum of exponentials to a data curve and plot the results.


To run download curveFitGA.py, geno.py, and functions.py

Set the permissions in curveFitGA.py to Allow executing file as Program(the other two files should need no modification).

run with the -h or --help flag for information


Parameters

"data", "input for the program in csv format. First column must be time. Remaining columns are data sets. Columns must be equal length. No Header."

"output_name", "specify file output name, if no path is included the file will output where the script is located"

"-a", "--arity", default=1, "The number of exponential terms to fit. Default is one."

"-v", "--verbosity", default=False, action='store_true', help="Enabling verbosity will provide more output during evolution"

"-g", "--params", default=[-10, 10, 100, 1000, 100, 0.4, 0.3, 0.9, 0.3, 0.1], "optional parameter list for genetic algorithm:"


GA parameters

min: The minimum value for terms in the curve formula

max: The maximum value for terms in the curve formula

pop: The number of solutions considered each generation

gen: The maximum number of generations to search for a solution

stop_num: The number of generations to stop after seeing no improvement in the solution

mut_rate: The likelyhood that any solution will be mutated in a given generation 

mut_amount: The max range for mutating a formula term * random(1 + mut_amount, 1 - mut_amount)

mut_decay: The rate at which mutation amounts decays, improvements in solution reset mut_amount to default. Per gen: mut_amount = mut_amount * mut_decay
 
death_rate: The percentage of the popluation that gets replaced each generation due to fitness proportioanl selection(roulette wheel fitness)

elitism: The percentage of the population that gets replace in favor of the most fit solution(random sampling between generation best and all time best)



