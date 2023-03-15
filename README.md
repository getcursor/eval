### HumanEval for GPT-3.5/GPT-4 

Results are [here](https://twitter.com/amanrsanger/status/1635751764577361921). Forked from [OpenAI's repo](https://github.com/openai/human-eval).

To generate the completions (after pip installing the requirements), run:
```
mkdir results
python run.py
```

Then to evaluate the completion results, run
```
pip3 install -e .
python -m human_eval.evaluate_functional_correctness results/name_of_results_file
```
