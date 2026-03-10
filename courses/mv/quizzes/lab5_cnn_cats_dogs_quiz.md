# Lab 5 Quiz: Cats vs Dogs CNN Classification

> 基于 CST8508 Lab 5 实验内容生成。涵盖 CNN 架构、数据预处理、训练流程和模型评估。

---

## Multiple Choice Questions (MCQ)

**Question 1** (1 point)
In Lab 5, `datasets.ImageFolder` determines class labels by:

Question 1 options:
A) Reading a separate CSV label file
B) Using the names of subdirectories (e.g., `Cat/`, `Dog/`)
C) Sorting filenames alphabetically and assigning 0/1
D) Reading EXIF metadata from each image

---

**Question 2** (1 point)
Why is `transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])` used in the pipeline?

Question 2 options:
A) It converts images to grayscale
B) It rescales pixel values using ImageNet mean and std to speed up convergence
C) It randomly flips images for augmentation
D) It resizes images to 128×128

---

**Question 3** (1 point)
In `SimpleCNN`, after three `MaxPool2d(2, 2)` operations on a 128×128 input, the spatial dimension becomes:

Question 3 options:
A) 8×8
B) 32×32
C) 16×16
D) 64×64

---

**Question 4** (1 point)
Why is `Dropout(p=0.5)` placed between `fc1` and `fc2` in `SimpleCNN`?

Question 4 options:
A) To speed up training by skipping half the neurons permanently
B) To reduce overfitting by randomly zeroing 50% of activations during training
C) To increase the number of trainable parameters
D) To normalize the output of `fc1`

---

**Question 5** (1 point)
In the training loop, `optimizer.zero_grad()` must be called before `loss.backward()` because:

Question 5 options:
A) PyTorch accumulates gradients by default; not zeroing them would mix gradients from different batches
B) It resets the model weights to zero
C) It clears the training history dictionary
D) It is required to move tensors to the GPU

---

**Question 6** (1 point)
What is the purpose of `model.eval()` before the validation loop?

Question 6 options:
A) It freezes all model weights permanently
B) It switches Dropout and BatchNorm to inference mode (no random dropout, frozen running stats)
C) It moves the model to CPU
D) It resets the optimizer state

---

**Question 7** (1 point)
In Lab 5's `load_dataset`, two separate `datasets.ImageFolder` instances are created. Why?

Question 7 options:
A) To double the dataset size through duplication
B) So the train split uses augmentation transforms and the test split uses only resize+normalize
C) Because `ImageFolder` cannot hold more than 10,000 images
D) To avoid loading corrupted images

---

**Question 8** (1 point)
The final layer `fc2 = nn.Linear(256, 2)` outputs 2 values. What do these represent when used with `CrossEntropyLoss`?

Question 8 options:
A) The pixel coordinates of the detected animal
B) Raw logit scores for class Cat (index 0) and class Dog (index 1)
C) The probability that the image is corrupted
D) The train and validation accuracy

---

**Question 9** (1 point)
After 10 epochs, the model achieved ~88% validation accuracy. Which metric from `classification_report` best measures performance when the dataset is nearly balanced (2478 Cat / 2522 Dog)?

Question 9 options:
A) Precision only
B) Recall only
C) F1-score (harmonic mean of precision and recall)
D) Support count

---

**Question 10** (1 point)
`urllib.request.urlretrieve` is used in the Setup cell. What would be the consequence of NOT checking `if not ZIP_PATH.exists()` before downloading?

Question 10 options:
A) The download would fail silently
B) The dataset would be downloaded and overwritten every time the cell runs (~786 MB each time)
C) The kernel would crash due to memory overflow
D) The zip file would be corrupted

---

## True / False Questions

**Question 11** (1 point)
`transforms.RandomHorizontalFlip()` is applied to both training and test data in Lab 5.

Question 11 options:
True
False

---

**Question 12** (1 point)
`torch.no_grad()` during evaluation reduces memory usage and speeds up inference by disabling gradient computation.

Question 12 options:
True
False

---

**Question 13** (1 point)
`nn.CrossEntropyLoss` in PyTorch internally combines `Softmax` and negative log-likelihood loss, so no explicit `Softmax` is needed in the model's `forward`.

Question 13 options:
True
False

---

**Question 14** (1 point)
Setting `shuffle=True` in the test `DataLoader` improves model accuracy.

Question 14 options:
True
False

---

**Question 15** (1 point)
`PIL.Image.verify()` decodes the full pixel data of an image to check for corruption.

Question 15 options:
True
False

---

## Short Answer / Coding Questions

**Question 16** (2 points)
The current `SimpleCNN` uses three `Conv2d` layers sharing a **single** `self.pool = nn.MaxPool2d(2, 2)` object. Is this correct? Explain why or why not.

---

**Question 17** (2 points)
Change the model to output **5 classes** instead of 2 (e.g., for a multi-pet dataset). Write only the two lines of code that need to be modified inside `SimpleCNN.__init__`.

---

## Answer Key

| # | Answer |
|---|--------|
| 1 | B |
| 2 | B |
| 3 | C |
| 4 | B |
| 5 | A |
| 6 | B |
| 7 | B |
| 8 | B |
| 9 | C |
| 10 | B |
| 11 | False — `RandomHorizontalFlip` is in `train_transform` only |
| 12 | True |
| 13 | True |
| 14 | False — shuffling test data has no effect on accuracy |
| 15 | False — `verify()` only checks the file header/trailer, not the full pixel data |
| 16 | Yes, it is correct. `MaxPool2d` has no learnable parameters; it is a stateless operation. The same instance can be reused multiple times in `forward` without any issue. |
| 17 | `self.fc2 = nn.Linear(256, 5)` — change the output size from 2 to 5. No other line needs changing. |
