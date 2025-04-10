<p align="center">
  <img src="ensemble_logo.jpg" alt="Logo" width="400">
  <br /> <br / >
</p>

# NdLinear: Multi-Dimensional Linear Layer for Representation Learning

## Overview

You have found **NdLinear** by [Ensemble AI](https://ensemblecore.ai/). We proudly present this PyTorch module designed as an innovative linear transformation layer. 
It preserves the multi-dimensional structure of data, enhances representational power, and is parameter-efficient. 
Unlike conventional embedding layers, NdLinear transforms tensors across a collection of vector spaces, 
capturing multivariate structure and dependencies typically lost in standard fully connected layers.
Read our [paper](https://arxiv.org/abs/2503.17353).

## Key Features

- **Structure Preservation:** Retains the original data format and shape.
- **Parameter Efficiency:** Reduces parameter count while improving performance.
- **Minimal Overhead:** Maintains the same complexity as conventional linear layers.
- **Flexible Integration:** Seamlessly replaces existing linear layers.

## Installation

To integrate NdLinear into your projects, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/ensemble-core/NdLinear.git
cd NdLinear
pip install . 
```

Alternatively, if packaged, install via pip:

```bash
pip install ndlinear
```

## Usage

NdLinear can be utilized in various neural network architectures such as CNNs, RNNs, and Transformers.

### Example 1: Replacing a Standard Linear Layer with NdLinear

```python
import torch
from ndlinear import NdLinear

input_tensor = torch.randn(32, 28, 28, 3)  # Batch of images

ndlinear_layer = NdLinear(input_dims=(28, 28, 3), hidden_size=(64, 64, 6))

output = ndlinear_layer(input_tensor)
```

### Example 2: Transformer

In transformer architectures, you might need to manipulate multi-dimensional tensors for efficient linear operations. Here's how you can use `NdLinear` with a 3D input tensor:

```python
import torch 
from ndlinear import NdLinear

input_tensor = torch.randn(32, 28, 28) 

# Reshape the input tensor for linear operations
input_tensor = input_tensor.reshape(-1, 28, 1)  # New shape: (batch_size * num_tokens, token_dim, 1)

# Define an NdLinear layer with suitable input and hidden dimensions
ndlinear_layer = NdLinear(input_dims=(28, 1), hidden_size=(32, 1))

# Perform the linear transformation
output = ndlinear_layer(input_tensor)

# Reshape back to the original dimensions after processing
output = output.reshape(batch_size, num_tokens, -1)  # Final output shape: (32, 28, 32)
```

This example illustrates how `NdLinear` can be integrated into transformer models by manipulating the tensor shape, thereby maintaining the structure necessary for further processing and achieving efficient projection capabilities.

### Example 3: Multilayer Perceptron 

This example demonstrates how to use the `NdLinear` layers in a forward pass setup, making integration into existing MLP structures simple and efficient.

```python 
import torch
from ndlinear import NdLinear

input_tensor = torch.randn(32, 128)

# Define the first NdLinear layer for the MLP with input dimensions (128, 8) and hidden size (64, 8)
layer1 = NdLinear(input_dims=(128, 8), hidden_size=(64, 8))

# Define the second NdLinear layer for the MLP with input dimensions (64, 8) and hidden size (10, 2)
layer2 = NdLinear(input_dims=(64, 8), hidden_size=(10, 2))

x = F.relu(layer1(input_tensor))

output = layer2(x)
```

### Example 4: Edge Case

When `input_dims` and `hidden_size` are one-dimensional, `NdLinear` functions as a conventional `nn.Linear` layer, serving as an edge case where `n=1`.

```python
from ndlinear import NdLinear

# Defining NdLinear with one-dimensional input and hidden sizes
layer1 = NdLinear(input_dims=(32,), hidden_size=(64,))
```

## Examples of Applications

NdLinear is versatile and can be used in:

- **Image Classification:** Run `cnn_img_classification.py`.
- **Time Series Forecasting:** Use `ts_forecast.py`.
- **Text Classification:** Launch `txt_classify_bert.py`.
- **Vision Transformers:** Execute `vit_distill.py`.

## Explore and Discover

We invite you to visit [Ensemble AI](https://ensemblecore.ai/) and experience the innovative capabilities we offer. 
Dive in, explore, and see how NdLinear can make a difference in your projects. We're excited to have you try it out!

## Community Engagement

Join the community and enhance your projects using NdLinear in Hugging Face, Kaggle, and GitHub.

[//]: # (## Citation)

[//]: # ()
[//]: # (If you find NdLinear useful in your research, please cite our work:)

[//]: # ()
[//]: # (```bibtex)

[//]: # (@article{reneau2025ndlinear,)

[//]: # (  title={NdLinear Is All You Need for Representation Learning},)

[//]: # (  author={Reneau, Alex and Hu, Jerry Yao-Chieh and Zhuang, Zhongfang and Liu, Ting-Chun},)

[//]: # (  journal={Ensemble AI},)

[//]: # (  year={2025},)

[//]: # (  note={\url{https://arxiv.org/abs/2503.17353}})

[//]: # (})

[//]: # (```)

## Contact

For questions or collaborations, please contact [Alex Reneau](mailto:alex@ensemblecore.ai).

## License

This project is distributed under the Apache 2.0 license. View the [LICENSE](https://github.com/ensemble-core/NdLinear/blob/main/LICENSE) file for more details.
