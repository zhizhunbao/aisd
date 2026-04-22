# Mid Term Test - Questions, Options, and Answers

## Q1

**Question:**
A dataset containing patient medical records is analyzed for predicting the likelihood of developing a specific disease. In this dataset:

Scenario 1: Patients with a higher body mass index (BMI) are less likely to report their weight accurately.

Scenario 2: Missing values for blood pressure readings occur due to random equipment malfunctions.

Scenario 3: Patients who are diagnosed with a terminal illness are less likely to respond to a follow up survey about their general health.

Which of the following best describes the type of missingness in each scenario?

**Options:**
A) Scenario 1: Missing Completely at Random (MCAR), Scenario 2: Missing Not at Random (MNAR), Scenario 3: Missing at Random (MAR)

B) Scenario 1: Missing at Random (MAR), Scenario 2: Missing Completely at Random (MCAR), Scenario 3: Missing Not at Random (MNAR)

C) Scenario 1: Missing at Random (MAR), Scenario 2: Missing Not at Random (MNAR), Scenario 3: Missing Completely at Random (MCAR)

D) Scenario 1: Missing Not at Random (MNAR), Scenario 2: Missing at Random (MAR), Scenario 3: Missing Completely at Random (MCAR)

**Answer:**
B) Scenario 1: Missing at Random (MAR), Scenario 2: Missing Completely at Random (MCAR), Scenario 3: Missing Not at Random (MNAR)

---

## Q2

**Question:**
A machine learning model is being developed to predict customer churn for a subscription service. During the feature engineering process, the data scientist calculates the average number of future customer support tickets for each customer and includes this as a feature. What is the primary risk associated with this approach?

**Options:**
A) Reduced model performance due to irrelevant features.

B) Data leakage, leading to unrealistically high evaluation scores.

C) Increased computational cost during model training.

D) Overfitting of the training data due to high dimensionality.

**Answer:**
B) Data leakage, leading to unrealistically high evaluation scores.

---

## Q3

**Question:**
A machine learning model predicts loan approval based on several features, including income, credit score, and debt-to-income ratio. When using SHAP values to explain a specific loan approval prediction, a feature's SHAP value represents:

**Options:**
A) The feature's correlation with the target variable (loan approval).

B) The feature's impact on the model's accuracy on the entire dataset.

C) The feature's overall importance in the model across all predictions.

D) The feature's contribution to the prediction for that specific loan approval, compared to the average prediction.

**Answer:**
D) The feature's contribution to the prediction for that specific loan approval, compared to the average prediction.

---

## Q4

**Question:**
You are training a model to predict whether an email is spam or not. Your dataset has significantly more non-spam emails than spam emails. You notice your model is very good at identifying non-spam emails, but often misses spam emails. Which of the following is the MOST effective way to improve your model's ability to detect spam emails?

**Options:**
A) Use accuracy as the main metric to evaluate your model's performance.

B) Remove some of the non-spam emails from your training data.

C) Collect more non-spam emails to make the dataset even larger.

D) Give the model more examples of spam emails by creating copies of existing spam emails in your training data and slightly modifying them

**Answer:**
D) Give the model more examples of spam emails by creating copies of existing spam emails in your training data and slightly modifying them

---

## Q5

**Question:**
Consider a scenario where you are training a very large deep learning model on a massive dataset. Which of the following statements BEST describes the key differences between data parallelism, model parallelism, and pipeline parallelism?

**Options:**
A) Data parallelism focuses on optimizing data loading, model parallelism optimizes model architecture, and pipeline parallelism optimizes the training loop.

B) Data parallelism splits the data across multiple GPUs, model parallelism splits the model across multiple GPUs, and pipeline parallelism splits the training process into stages.

C) Data parallelism splits the model across multiple GPUs, model parallelism splits the data across multiple GPUs, and pipeline parallelism splits the training process into stages.

D) Data parallelism is used for small datasets, model parallelism for small models, and pipeline parallelism for sequential data.

**Answer:**
B) Data parallelism splits the data across multiple GPUs, model parallelism splits the model across multiple GPUs, and pipeline parallelism splits the training process into stages.

---

## Q6

**Question:**
A company's online platform experiences a surge in user traffic during peak hours. Which of the following statements BEST describes the key differences between horizontal scaling, vertical scaling, and hybrid scaling?

**Options:**
A) Horizontal scaling is used for small applications, vertical scaling for large applications, and hybrid scaling for cloud-based applications.

B) Horizontal scaling increases the processing power of a single server, vertical scaling adds more servers, and hybrid scaling is a combination of both.

C) Horizontal scaling adds more servers to handle the load, vertical scaling increases the processing power of a single server, and hybrid scaling uses both approaches.

D) Horizontal scaling optimizes database queries, vertical scaling optimizes network bandwidth, and hybrid scaling optimizes application code.

**Answer:**
C) Horizontal scaling adds more servers to handle the load, vertical scaling increases the processing power of a single server, and hybrid scaling uses both approaches.

---

## Q7

**Question:**
A deep learning model is being deployed on a resource-constrained device (e.g., a mobile phone). Which of the following statements BEST describes the key differences between model quantization, pruning, knowledge distillation, and general model compression?

**Options:**
A) Quantization is only used for image models, pruning is only used for text models, knowledge distillation is only used for audio models, and model compression is used for any type of data.

B) Quantization reduces the precision of the model's weights, pruning removes redundant connections or neurons, knowledge distillation trains a smaller model to mimic a larger model, and model compression is a general term for any size reduction.

C) Quantization reduces the model's size by removing redundant layers, pruning reduces the precision of the model's weights, knowledge distillation trains a smaller model to mimic a larger model, and model compression is a general term for any size reduction.

D) Quantization optimizes the model's architecture, pruning optimizes the training process, knowledge distillation optimizes the inference speed, and model compression is a specific algorithm.

**Answer:**
B) Quantization reduces the precision of the model's weights, pruning removes redundant connections or neurons, knowledge distillation trains a smaller model to mimic a larger model, and model compression is a general term for any size reduction.

---

## Q8

**Question:**
Statement: Faithfulness verifies that the LLM's response is consistent with the information provided within the given context or input.

**Options:**
A) True
B) False

**Answer:**
A) True

---

## Q9

**Question:**
In the context of distributed systems and workflow management, what is the primary distinction between a scheduler and an orchestrator?

**Options:**
A) Schedulers are used for real-time processing, while orchestrators are used for batch processing.

B) Schedulers manage hardware resources, while orchestrators manage software dependencies.

C) Schedulers focus on data storage, while orchestrators focus on data processing.

D) Schedulers execute individual tasks based on time or resource availability, while orchestrators manage complex, multi-step workflows.

**Answer:**
D) Schedulers execute individual tasks based on time or resource availability, while orchestrators manage complex, multi-step workflows.

---

## Q10

**Question:**
A Pod in Kubernetes is a group of one or more containers, with shared storage and network resources, and a specification for how to run the containers.

**Options:**
A) True
B) False

**Answer:**
A) True
