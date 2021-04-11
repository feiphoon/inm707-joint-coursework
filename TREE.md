# File tree

This is our file tree up to a certain depth.

The most important files for marking are listed here. Any discrepancies will only be due to more experiment results being logged or processed.

The `maze` folder contains Task 1, and the `cartpole` folder Task 3. All results for Task 3 are logged in the results folder, under their respective environments, and train and test results (figures, images and models) are in `training_results_....csv` and `best_model_results_....csv` respectively.

```bash
.
├── LICENSE
├── README.md
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── cartpole
│   │   ├── actor_critic.py
│   │   ├── actor_critic_test_v0.ipynb
│   │   ├── actor_critic_test_v1.ipynb
│   │   ├── actor_critic_train.ipynb
│   │   ├── actor_critic_train_analysis_cartpolev0.ipynb
│   │   ├── actor_critic_train_analysis_cartpolev1.ipynb
│   │   ├── best_model_results_v0_20210407-003658.csv
│   │   ├── best_model_results_v1_20210405-225734.csv
│   │   ├── best_models
│   │   │   ├── cartpole-v0
│   │   │   └── cartpole-v1
│   │   ├── log_processing.ipynb
│   │   ├── random_evaluation.ipynb
│   │   ├── README.md
│   │   ├── results
│   │   │   ├── CartPole-v0
│   │   │   └── CartPole-v1
│   │   ├── training_results_v0_20210407-003658.csv
│   │   ├── training_results_v1_20210405-225734.csv
│   │   └── utils.py
│   └── maze
│       ├── exp_orchestrator.py
│       ├── exp_runner.py
│       ├── maze.py
│       ├── policies.py
│       ├── policy_evaluation.ipynb
│       ├── q_maze.py
│       └── README.md
├── tasks.py
└── tests
    ├── __init__.py
    └── test_maze.py
```
