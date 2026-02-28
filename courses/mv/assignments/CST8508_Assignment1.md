# CST8508 — Machine Vision — Assignment 1

## Introduction

This is an assignment that aims at giving you hands-on exposure to training deep-learning models for computer vision tasks. We will be utilizing the [OpenMMLab](https://github.com/open-mmlab) project for assignments.

## Learning Outcomes

For this assignment, you will be training an image classification model using [mmpretrain](https://github.com/open-mmlab/mmpretrain). The main learning outcomes from this assignment are:

- Familiarize yourself with a tech stack that allows you to comfortably train computer vision deep learning models using OpenMMLab projects (Google Colab, Google Colab Prime, faculty server, personal GPU-enabled machine, EC2, whatever works for you!)
- It is strongly discouraged to use Windows or MacOS for your environment setup. OpenMMLab (and almost all ML projects) are designed to work in Linux, and might or might not work in other OS.
- Familiarize yourself with the structure of OpenMMLab projects (learn one, all the others become much easier to learn)

## Instructions

1. **Download the dataset (20%)**
   You must first download the dataset. We will be using the [Oxford Flowers dataset](https://www.robots.ox.ac.uk/~vgg/data/flowers/17/) for this assignment.

   You will then prepare the dataset such that it is compatible with mmpretrain structure for training image classification models. For this dataset, I will ask you to prepare it in the SubFolder format so that you do not have to create any annotation files. You can find more information about the SubFolder format [here](https://mmpretrain.readthedocs.io/en/latest/user_guides/dataset_prepare.html). Successfully preparing the dataset in this format is worth **20%** of the assignment grade.

2. **Setup mmpretrain**
   Setup mmpretrain in your environment. You can refer to the documentation here:
   - Latest: <https://mmpretrain.readthedocs.io/en/latest/get_started.html>
   - Stable: <https://mmpretrain.readthedocs.io/en/stable/get_started.html>

   Make sure to run the "Verify the installation section" in the documentation to ensure you have a working environment before you move on.

3. **Understand config file structure**
   At this point, you have your dataset prepared, and the environment ready. You will now learn about the config file structure. Refer to the documentation [here](https://mmpretrain.readthedocs.io/en/latest/user_guides/config.html). You must read this carefully and make sure you fully understand it.

4. **Train two models (50%)**
   Now that you have a good understanding of the config files, I want you to select two models of your choice and [train](https://mmpretrain.readthedocs.io/en/latest/user_guides/train.html) them for image classification. The successful training of two models is worth **50%** of the assignment grade.

5. **Evaluate your models (20%)**
   Evaluate your models using whatever metric you see fit at this point. You can either use overall accuracy, F1 score, or just visual comparisons. We haven't dived deep into evaluation metrics yet, so I will leave this part to be flexible. This evaluation is worth **20%** of the assignment grade. [This documentation](https://mmpretrain.readthedocs.io/en/latest/user_guides/inference.html) would likely prove relevant to you when learning how to run inference using your trained models.

6. **Lessons learned (10%)**
   Write a summary of the challenges you faced with this assignment, how you solved them, lessons learned, and any other thoughts you have. This is worth **10%** of your assignment grade.

## What to Submit on Brightspace

- Generated training log files.
- Report showing your evaluation analysis and lessons learned.
