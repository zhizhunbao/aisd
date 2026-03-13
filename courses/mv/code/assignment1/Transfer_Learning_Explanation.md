**Subject:** Assignment 1 — Explanation of Transfer Learning Usage

Dear Professor,

Thank you for the feedback on my Assignment 1. I'd like to explain how Transfer Learning is applied in my implementation.

---

### What is Transfer Learning?

Transfer Learning reuses a model pre-trained on a large dataset (ImageNet, ~1.2M images) as the starting point for a new task, instead of training from scratch. The idea is that low-level features learned from ImageNet (edges, textures, shapes) are general-purpose and transfer well to other vision tasks, including flower classification.

### How I Used It in My Code

In my config files, I set the `init_cfg` parameter in the backbone to load **ImageNet pretrained checkpoints**:

**ResNet-18:**
```python
init_cfg=dict(type='Pretrained', checkpoint='torchvision://resnet18')
```

**MobileNet V2:**
```python
init_cfg=dict(type='Pretrained',
    checkpoint='https://download.openmmlab.com/mmclassification/v0/mobilenet_v2/...')
```

This means the backbone weights are initialized from ImageNet pretrained models, and then **fine-tuned** on the Oxford Flowers 17 dataset.

### The Transfer Learning Process

1. **Download pretrained weights** — ResNet-18 (~44MB) from PyTorch; MobileNet V2 (~14MB) from OpenMMLab
2. **Initialize the backbone** — Load these weights as the model's starting point (instead of random initialization)
3. **Fine-tune on Flowers 17** — Train on our target dataset; all layers are updated with a smaller learning rate

### What Transfers vs. What is New

- **Transferred:** The backbone weights — encoding general visual features from 1.2M ImageNet images
- **New:** The classification head (`LinearClsHead`) — mapping features to 17 flower classes (randomly initialized since ImageNet has 1,000 classes)
- **Fine-tuned:** Both backbone and head are updated during training; backbone is slightly adjusted for flower-specific features

### Why Transfer Learning Matters Here

Flowers 17 is very small (~60 images/class, ~1,000 total). Without pretrained weights, the model lacks sufficient data to learn good features from scratch, leading to poor accuracy and high overfitting risk. Transfer learning provides rich initial features, faster convergence, and better generalization.

### Supporting Design Choices

- **ImageNet normalization** — `mean=[123.675, 116.28, 103.53]`, `std=[58.395, 57.12, 57.375]` must match what the pretrained model expects
- **Smaller learning rate** — ResNet-18 uses `lr=0.01` (10× smaller than ImageNet's 0.1); MobileNet V2 uses `lr=0.001` to avoid destroying pretrained features
- **Data augmentation** — `RandomResizedCrop` and `RandomFlip` complement transfer learning to prevent overfitting

---

Thank you for your time. Please let me know if you have any further questions.

Best regards,
[Your Name]
