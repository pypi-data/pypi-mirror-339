"""ResNet model implementation using MLX.

This module provides an implementation of the ResNet architecture
using MLX for acceleration.
"""

from typing import List, Optional, Type, Union

import mlx.core as mx
import mlx.nn as nn


class BasicBlock(nn.Module):
    """Basic residual block for ResNet.

    This implements the basic residual block used in ResNet-18 and ResNet-34.

    Attributes:
        expansion: Expansion factor for the number of output channels.
        conv1: First convolutional layer.
        bn1: First batch normalization layer.
        conv2: Second convolutional layer.
        bn2: Second batch normalization layer.
        downsample: Optional downsampling layer for skip connection.
    """

    expansion: int = 1

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        stride: int = 1,
        downsample: Optional[nn.Module] = None,
    ) -> None:
        """Initialize a new BasicBlock.

        Args:
            in_channels: Number of input channels.
            out_channels: Number of output channels.
            stride: Stride for the first convolutional layer.
            downsample: Optional downsampling layer for skip connection.
        """
        super().__init__()

        self.conv1 = nn.Conv2d(
            in_channels,
            out_channels,
            kernel_size=3,
            stride=stride,
            padding=1,
            bias=False,
        )
        self.bn1 = nn.BatchNorm(out_channels)
        self.conv2 = nn.Conv2d(
            out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False
        )
        self.bn2 = nn.BatchNorm(out_channels)
        self.downsample = downsample

    def __call__(self, x: mx.array) -> mx.array:
        """Forward pass through the block.

        Args:
            x: Input tensor.

        Returns:
            mx.array: Output tensor.
        """
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = nn.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)

        if self.downsample is not None:
            identity = self.downsample(x)

        out = out + identity
        out = nn.relu(out)

        return out


class Bottleneck(nn.Module):
    """Bottleneck residual block for ResNet.

    This implements the bottleneck residual block used in ResNet-50 and deeper variants.

    Attributes:
        expansion: Expansion factor for the number of output channels.
        conv1: First convolutional layer (1x1).
        bn1: First batch normalization layer.
        conv2: Second convolutional layer (3x3).
        bn2: Second batch normalization layer.
        conv3: Third convolutional layer (1x1).
        bn3: Third batch normalization layer.
        downsample: Optional downsampling layer for skip connection.
    """

    expansion: int = 4

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        stride: int = 1,
        downsample: Optional[nn.Module] = None,
    ) -> None:
        """Initialize a new Bottleneck.

        Args:
            in_channels: Number of input channels.
            out_channels: Number of output channels.
            stride: Stride for the second convolutional layer.
            downsample: Optional downsampling layer for skip connection.
        """
        super().__init__()

        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm(out_channels)
        self.conv2 = nn.Conv2d(
            out_channels,
            out_channels,
            kernel_size=3,
            stride=stride,
            padding=1,
            bias=False,
        )
        self.bn2 = nn.BatchNorm(out_channels)
        self.conv3 = nn.Conv2d(
            out_channels, out_channels * self.expansion, kernel_size=1, bias=False
        )
        self.bn3 = nn.BatchNorm(out_channels * self.expansion)
        self.downsample = downsample

    def __call__(self, x: mx.array) -> mx.array:
        """Forward pass through the block.

        Args:
            x: Input tensor.

        Returns:
            mx.array: Output tensor.
        """
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = nn.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = nn.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)

        if self.downsample is not None:
            identity = self.downsample(x)

        out = out + identity
        out = nn.relu(out)

        return out


class ResNet(nn.Module):
    """ResNet model implementation using MLX.

    This class implements the ResNet architecture using MLX for acceleration.

    Attributes:
        block: Type of residual block to use.
        layers: Number of blocks in each layer.
        num_classes: Number of output classes.
    """

    def __init__(
        self,
        block: Type[Union[BasicBlock, Bottleneck]],
        layers: List[int],
        num_classes: int = 1000,
        zero_init_residual: bool = False,
    ) -> None:
        """Initialize a new ResNet.

        Args:
            block: Type of residual block to use.
            layers: Number of blocks in each layer.
            num_classes: Number of output classes.
            zero_init_residual: Whether to zero-initialize the residual connections.
        """
        super().__init__()

        self.in_channels = 64
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm(64)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.layer1 = self._make_layer(block, 64, layers[0])
        self.layer2 = self._make_layer(block, 128, layers[1], stride=2)
        self.layer3 = self._make_layer(block, 256, layers[2], stride=2)
        self.layer4 = self._make_layer(block, 512, layers[3], stride=2)

        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * block.expansion, num_classes)

    def _make_layer(
        self,
        block: Type[Union[BasicBlock, Bottleneck]],
        channels: int,
        blocks: int,
        stride: int = 1,
    ) -> nn.Sequential:
        """Create a layer of residual blocks.

        Args:
            block: Type of residual block to use.
            channels: Number of output channels.
            blocks: Number of blocks in the layer.
            stride: Stride for the first block.

        Returns:
            nn.Sequential: Sequential layer of residual blocks.
        """
        downsample = None

        if stride != 1 or self.in_channels != channels * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(
                    self.in_channels,
                    channels * block.expansion,
                    kernel_size=1,
                    stride=stride,
                    bias=False,
                ),
                nn.BatchNorm(channels * block.expansion),
            )

        layers = []
        layers.append(block(self.in_channels, channels, stride, downsample))

        self.in_channels = channels * block.expansion

        for _ in range(1, blocks):
            layers.append(block(self.in_channels, channels))

        return nn.Sequential(*layers)

    def __call__(self, x: mx.array) -> mx.array:
        """Forward pass through the network.

        Args:
            x: Input tensor.

        Returns:
            mx.array: Output tensor.
        """
        x = self.conv1(x)
        x = self.bn1(x)
        x = nn.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = mx.reshape(x, (x.shape[0], -1))
        x = self.fc(x)

        return x


def ResNet18(num_classes: int = 1000) -> ResNet:
    """Create a ResNet-18 model.

    Args:
        num_classes: Number of output classes.

    Returns:
        ResNet: ResNet-18 model.
    """
    return ResNet(BasicBlock, [2, 2, 2, 2], num_classes=num_classes)


def ResNet34(num_classes: int = 1000) -> ResNet:
    """Create a ResNet-34 model.

    Args:
        num_classes: Number of output classes.

    Returns:
        ResNet: ResNet-34 model.
    """
    return ResNet(BasicBlock, [3, 4, 6, 3], num_classes=num_classes)


def ResNet50(num_classes: int = 1000) -> ResNet:
    """Create a ResNet-50 model.

    Args:
        num_classes: Number of output classes.

    Returns:
        ResNet: ResNet-50 model.
    """
    return ResNet(Bottleneck, [3, 4, 6, 3], num_classes=num_classes)
