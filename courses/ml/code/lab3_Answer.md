# CST8506 - Lab 3

## Classification by CNN

**Student Name:** Peng Wang

**Student Number:** 041107730


**For every step, include screenshot of the code and the corresponding results in this document (screenshot from colab/jupyter notebook). Also, in your words, explain your code and results. If there is no explanation, no marks will be given. No need to write long paragraphs, but one or 2 lines per step. Even if you are using default parameters, you must mention the default values and its meaning.**


## 1. Load data

**Code:**

![](../code/lab3/lab3_images/lab3_cnn_step01_code.png)

**Result:**

![](../code/lab3/lab3_images/lab3_cnn_step01_result.png)

**Number of images in the train set:** 60,000

**Number of images in the test set:** 10,000

**Explanation:** I loaded the MNIST dataset using `mnist.load_data()`. This function downloads the dataset and splits it into training and test sets automatically. The training set has 60,000 handwritten digit images, and the test set has 10,000 images for evaluation.

**First 5 images (all images in one row, parallel):**

**Code:**

![](../code/lab3/lab3_images/lab3_cnn_step03_code.png)

**Result:**

![](../code/lab3/lab3_images/step3_first_5_images.png)

**Explanation:** I used `plt.subplots(1, 5)` to create a row of 5 plots. Each image is displayed using `imshow()` with `cmap='gray'` for grayscale. The first 5 training images show digits 5, 0, 4, 1, 9.


## 2. Reshape

**Code:**

![](../code/lab3/lab3_images/lab3_cnn_step04_code.png)

**Result:**

![](../code/lab3/lab3_images/lab3_cnn_step04_result.png)

**Explanation:** I reshaped the data from (60000, 28, 28) to (60000, 28, 28, 1) to add a channel dimension. CNNs require input in the format (samples, height, width, channels).

**Why channels=1?** MNIST images are grayscale - each pixel has only one brightness value (0-255). Grayscale images have 1 channel, while RGB color images have 3 channels (Red, Green, Blue). Since MNIST contains black-and-white handwritten digits, I used channels=1.


## 3. Normalize

**Code:**

![](../code/lab3/lab3_images/lab3_cnn_step05_code.png)

**Result:**

![](../code/lab3/lab3_images/lab3_cnn_step05_result.png)

**Explanation:** I normalized pixel values by dividing by 255.0, converting the range from [0, 255] to [0, 1]. This helps the neural network train faster and more stably because smaller input values lead to better gradient flow.


## 4. Encoding

**Code:**

![](../code/lab3/lab3_images/lab3_cnn_step06_code.png)

**Result:**

![](../code/lab3/lab3_images/lab3_cnn_step07_result.png)

**Explanation:** I applied One-Hot encoding using `to_categorical()`. This converts integer labels (0-9) to binary vectors. For example, digit 5 becomes [0,0,0,0,0,1,0,0,0,0]. This format is required for the softmax output layer which predicts probabilities for each class.


## 5. Model

**Code:**

![](../code/lab3/lab3_images/lab3_cnn_step08_code.png)

**Result:**

![](../code/lab3/lab3_images/lab3_cnn_step08_result.png)

**Model Architecture:**

```
Input(28,28,1) → Conv2D(32) → MaxPool → Conv2D(64) → MaxPool → Flatten → Dense(128) → Dense(10)
```

**Parameter Explanation:**

| Parameter | Value | My Explanation |
|-----------|-------|----------------|
| filters | 32, 64 | Number of feature detectors. First layer learns 32 simple patterns, second learns 64 complex patterns |
| kernel_size | (3,3) | Size of the sliding window that scans the image. 3x3 is a common choice for small images |
| activation | 'relu' | ReLU outputs max(0, x). It adds non-linearity and helps the network learn complex patterns |
| padding | 'same' | Adds zeros around the image edges so output size equals input size |
| pool_size | (2,2) | MaxPooling keeps the largest value in each 2x2 region, reducing image size by half |
| Dense units | 128, 10 | 128 neurons for learning combinations, 10 neurons for 10 digit classes |
| softmax | output | Converts outputs to probabilities that sum to 1 |


## 6. Compile model

**Code:**

![](../code/lab3/lab3_images/lab3_cnn_step09_code.png)

**Result:**

![](../code/lab3/lab3_images/lab3_cnn_step09_result.png)

**Explanation:** I compiled the model with these settings:
- **optimizer='adam'**: Adam automatically adjusts learning rate during training. It's faster than basic gradient descent.
- **loss='categorical_crossentropy'**: This loss function measures how wrong our predictions are for multi-class problems.
- **metrics=['accuracy']**: Tracks what percentage of predictions are correct during training.


## 7. Model summary

**Code:**

![](../code/lab3/lab3_images/lab3_cnn_step10_code.png)

**Result:**

![](../code/lab3/lab3_images/lab3_cnn_step10_result.png)

**Explanation:** The model has 421,642 trainable parameters. Most parameters (401,536) are in the first Dense layer because it connects 3,136 flattened features (7×7×64) to 128 neurons. Each connection has a weight to learn.


## 8. Fit, predict and print accuracy

**Code:**

![](../code/lab3/lab3_images/lab3_cnn_step11_code.png)

**Training Result:**

![](../code/lab3/lab3_images/lab3_cnn_step11_result.png)

**Training History:**

![](../code/lab3/lab3_images/step11_training_history.png)

**Explanation:** I trained the model with:
- **batch_size=128**: Updates weights after every 128 images. Larger batches are faster but use more memory.
- **epochs=10**: Goes through the entire training set 10 times. More epochs can improve accuracy but may overfit.
- **validation_split=0.1**: Uses 10% of training data to check if model generalizes well.

**Accuracy Result:**

![](../code/lab3/lab3_images/lab3_cnn_step13_result.png)

**Final Results:**
- **Test Accuracy: 99.01%**
- **Test Loss: 0.0378**

The model correctly classifies 99 out of 100 handwritten digits!


## 9. Predictions of first 20 instances in the given format

**Code:**

![](../code/lab3/lab3_images/lab3_cnn_step15_code.png)

**Result:**

![](../code/lab3/lab3_images/lab3_cnn_step15_result.png)

**Explanation:** I used `np.argmax()` to find which class has the highest probability. For example, if probabilities are [0.01, 0.01, 0.98, 0, 0, 0, 0, 0, 0, 0], argmax returns 2 (the digit "2"). All 20 predictions shown are correct (marked OK).


## 10. Misclassifications

**Code:**

![](../code/lab3/lab3_images/lab3_cnn_step16_code.png)

**Result:**

![](../code/lab3/lab3_images/lab3_cnn_step16_result.png)

**Misclassified Images:**

![](../code/lab3/lab3_images/step16_misclassified_images.png)

**Results:**
- **Total misclassified:** 99 out of 10,000
- **Misclassification rate:** 0.99%

**Explanation:** The model made 99 mistakes. Looking at the misclassified images, many are poorly written or ambiguous - even humans might struggle to read them. For example, some 4s look like 9s, and some 2s look like 7s. The model's confidence is often lower for these difficult cases.
