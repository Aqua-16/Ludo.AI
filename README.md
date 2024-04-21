# LudoAI

## Introduction

LudoAI is a **Reinforcement Learning Project**, aimed at creating artificially intelligent agents that are capable of autonomously playing against other autonomous agents, as well as human opponents.


https://github.com/Aqua-16/LudoAI/assets/123102778/d403b164-0a42-43bc-80cb-35491f37d29d


## Installation and Dependencies

The following dependencies are required to train an agent:-

- NumPy
- Matplotlib
- OpenCV

All requirements have been clearly mentioned in the `requirements.txt`. Just do the following:-
```
python -m venv ludo
env_name\Scripts\activate
git clone https://github.com/Aqua-16/LudoAI.git
cd LudoAI
pip install -r requirements.txt
```

**Note:** *This is only applicable to the Windows Terminal.*

## Training

The model can be trained using the following command:-

```
python train.py
```

The parameters currently set are done so after extensive tuning. But, feel free to change them and experiment with your own values. For reference, the training graphs are attached below. The AI has been trained against itself as well as agents with pseudo random movements.
This allows it to capture a wider array of possible moves, both optimal and sub-optimal.

![Figure_1](https://github.com/Aqua-16/LudoAI/assets/123102778/523779c0-16b4-45df-8054-d46514864f5f)

As can be seen from the figure, even against 3 opponents, the model achieves a win rate above **50%**. With a single opponent though, the AI wins nearly **75%** of the time.

## Gameplay

It is also possible to play against the AI agent using a CLI for giving player commands. After the training phase, the weights are saved into a `.npz` file. This can be fed into the `play.py` file to then play against the AI agent. 
Currently, a demo AI agent is loaded into the `play.py` file. So, it can be tested right away! Just do the following:-

```
python play.py
```

---
Thank you for checking out my project!
