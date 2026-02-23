# Reinforcement Learning Quiz – Antonin Raffin

---

## Question 1

**According to Antonin Raffin, what makes Reinforcement Learning difficult?**

- There is a sensitivity to hyperparameters and the random seed.
- Algorithms can be sample inefficient, meaning that a lot of interaction with the environment is necessary for learning.
- Data collection is done by the agent rather than a human.
- The appropriate reward function can be tricky to determine.
- ✅ **All of these answers**

---

## Question 2

**What is reward hacking in RL?**

- ✅ **A phenomenon where an algorithm maximizes reward without learning the desired behavior.**
- It is an ad hoc process that results in a poor reward function.
- It is the process of iteratively determining the optimal reward function.
- All of these answers.
- None of these answers.

---

## Question 3

**What does Antonin Raffin recommend as RL best practices?**

- All of these answers. ✅
- Use recommended hyperparameters for a particular algorithm.
- Don't rely on a previously successful algorithm to be successful on a new problem.
- Save a record of all experiment parameters, including random seed, in order to exactly reproduce experiments.
- Do quantitative evaluation when comparing, which involves arriving at results through multiple runs.

---

## Question 4

**What questions does Antonin Raffin recommend an RL practitioner ask when solving a new problem?**

- None of these answers (questions).
- Do you really need RL?
- Is RL compatible with any requirements for safety guarantees?
- Is RL compatible with any requirements for stability guarantees?
- ✅ **All of these answers (questions).**

---

## Question 5

**According to Antonin Raffin, what is involved in defining a custom task for RL to solve?**

- Define the observation space.
- Define the reward function.
- Define the termination conditions.
- Define the action space.
- ✅ **All of these answers.**

---

## Question 6

**According to Antonin Raffin, what is involved in defining the observation space?**

- Normalize values.
- Ensure there is enough information in observations to solve the task.
- Don't break assumptions, especially the Markov assumption.
- None of these answers.
- ✅ **All of these answers.**

---

## Question 7

**According to Antonin Raffin, what is involved in defining the action space?**

- Determine whether discrete or continuous actions are appropriate for the domain.
- Be careful with continuous action spaces, and ensure they are normalized.
- Use trial and error to evaluate the interactions between complexity (large action space) and performance (faster learning).
- Consider the interactions between complexity (large action space) and performance (faster learning).
- ✅ **All of these answers.**

---

## Question 8

**What does Antonin Raffin recommend regarding determining the reward function?**

- Consider primary rewards (for main goal) and secondary rewards (for desirable way to achieve main goal).
- Be careful to avoid reward hacking.
- Consider sparse rewards (only for achieving the task) and shaped rewards (to encourage progress in learning).
- Start with a simple reward function for a custom task, and do reward shaping from there.
- ✅ **All of these answers.**

---

## Question 9

**What are Antonin Raffin's recommendations for choosing the RL algorithm?**

- Choose more time-tested, older algorithms if possible.
- All of these answers.
- None of these answers.
- Choose more recently developed algorithms which offer the best optimizations.
- ✅ **Consider your actions and whether the algorithm is designed for continuous or discrete actions.**

---

## Question 10

**According to Antonin Raffin, what can you do if your RL system does not work the first time?**

- Increase the training budget (timesteps allocated for training) as part of your experimentation.
- Ensure you used a trusted implementation of the algorithm (stable-baselines3, for example).
- Check your work regarding following best practices.
- Simplify, and then gradually add complexity.
- ✅ **All of these answers.**
