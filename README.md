### HumanEval for GPT-3.5/GPT-4 

Results are [here](https://twitter.com/amanrsanger/status/1635751764577361921). Forked from [OpenAI's repo](https://github.com/openai/human-eval).

To give it a go, after pip installing the requirements, run the following commands 
```
mkdir results
python3 run.py
evaluate_functional_correctness results/name_of_results_file
```

The file `run.py` uses OpenAI's api to generate completions to the code in human eval.
Then `evaluate-functional_correctness` runs the code through test cases to verify they pass. This code is entirely created by OpenAI.
