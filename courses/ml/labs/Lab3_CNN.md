# CST8506 - Lab 3: Convolutional Neural Networks

**Due Date:** Check Brightspace for due dates.

## Introduction

The goal of this lab is to classify handwritten digits dataset (MNIST) using CNN in Keras. All tasks should be performed using Keras and Python. (Refer to documentation: https://keras.io/api/layers/)

For all methods, seed value should be set as the last 3 digits of your student number. If your student number is 12345, seed should be 345 for all operations.

## Steps (all these steps should be done in Python):

1. **Load the dataset** (MNIST set is a large collection of handwritten digits. MNIST: Modified National Institute of Standards and Technology database) https://keras.io/api/datasets/mnist/

2. **Print the number of images** in train and test set.

3. **Print first 5 images** in the train set along with its corresponding number in one frame.

4. **To set the channel**, use reshape function. (if it is RGB, we set 3 as the number of channels; for greyscale, set it as 1. As our images are greyscale, set it as 1)

5. **Normalize the images.**

6. **Apply one-hot encoding** on the y values. This means if the number is 5, it should be represented as `[0 0 0 0 0 1 0 0 0 0]`. As our numbers are from 0 to 9, 5 is at the 6th position. So, sixth position should be 1 and all other positions should be 0.

7. **Print old and new values** for the first 5 instances of y_train.

8. **Build the model.** We will be creating a model as follows (As you are adding layers one after the other sequentially, use Sequential model. As we are using greyscale images, you can use Conv2D for creating Conv layers. Use ReLU (Rectified Linear Unit) as the activation function. Use softmax as the activation function for the last Dense layer to get the probabilities of each output):

   ```
   Input → Conv → MaxPool → Conv → MaxPool → Flatten → Dense → Dense (Output)
   ```

   You can decide the values of parameter like filter size, padding, stride etc. Make sure to explain your parameters. Even if you decide to use default values, you must write those values and its meaning in the answer document.

9. **Compile the model.** (Compiling the model is needed to finalize the model. We need to specify the optimizer, loss function and the metrics at this time).

10. **Print the model summary.**

11. **Fit the model.**

12. **Predict for the test data.**

13. **Print the accuracy of the model.**

14. **As your prediction will be a list of probabilities**, for each row, find the index of the highest probability. For example, in the list of these probabilities, `[8.0525751e-08 1.7561485e-11 4.1590823e-07 6.1171789e-08 1.8435065e-10 6.8201229e-11 4.6666044e-14 9.9999928e-01 2.5774932e-10 1.3494517e-07]`, the highest value is 9.9999928e-01 which is 99.99% at index 7. So, this image is predicted as the number 7.

15. **Print the results** in the format of the first 20 instances:

    | Highest probability | predicted digit | Actual digit |
    |---------------------|-----------------|--------------|
    | [0.9999924] | 7 | 7 |
    | [0.9999807] | 2 | 2 |
    | [0.9963497] | 1 | 1 |

16. **Now, for all the misclassified instances**, print the results in the above format.

## Submission Requirements

In order to get grades:

1. You should be ready with your Python code and results.
2. Submit your jupyter/colab notebook and the answer document to Brightspace. Lab will not be graded if any of these files are missing. Don't zip. Zipped files will not be graded.
