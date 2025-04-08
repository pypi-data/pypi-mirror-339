import os
import warnings
import torch
import torch.nn as nn
import math

from .buffer import BufferIO

from typing import Optional
from typing import Union
from typing import List

# Padding modes
PADDING_MODES = [
    'zeros',
    'reflect',
    'replicate',
    'circular',
]

class TemporalPad1d(nn.Module):
    def __init__(
            self,
            padding: int,
            in_channels: int,
            buffer: Optional[ Union[ float, torch.Tensor ] ] = None,
            padding_mode: str = 'zeros',
            causal: bool = False,
            ):
        super(TemporalPad1d, self).__init__()

        if not isinstance(padding, int):
            raise ValueError(
                f"""
                padding must be an integer, but got {type(padding)}.
                padding must not be a tuple, because the TemporalPadding
                will automatically determine the amount of left and right
                padding based on the causal flag.
                """
                )

        self.pad_len = padding
        self.causal = causal

        if causal:
            # Padding is only on the left side
            self.left_padding = self.pad_len
            self.right_padding = 0
        else:
            # Padding is on both sides
            self.left_padding = self.pad_len // 2
            self.right_padding = self.pad_len - self.left_padding
        
        if padding_mode == 'zeros':
            self.pad = nn.ConstantPad1d(
                (self.left_padding, self.right_padding),
                0.0,
                )
        elif padding_mode == 'reflect':
            self.pad = nn.ReflectionPad1d(
                (self.left_padding, self.right_padding),
                )
        elif padding_mode == 'replicate':
            self.pad = nn.ReplicationPad1d(
                (self.left_padding, self.right_padding),
                )
        elif padding_mode == 'circular':
            self.pad = nn.CircularPad1d(
                (self.left_padding, self.right_padding),
                )
        else:
            raise ValueError(
                f"""
                padding_mode must be one of {PADDING_MODES},
                but got {padding_mode}.
                """
                )
        
        # Buffer is used for streaming inference
        if buffer is None:
            if in_channels is None:
                buffer = torch.zeros(
                    1,
                    self.pad_len,
                    )
            else:
                buffer = torch.zeros(
                    1,
                    in_channels,
                    self.pad_len,
                    )
        elif isinstance(buffer, (int, float)):
            if in_channels is None:
                buffer = torch.full(
                    size = (1, self.pad_len),
                    fill_value = buffer,
                    )
            else:
                buffer = torch.full(
                    size = (1, in_channels, self.pad_len),
                    fill_value = buffer,
                    )
        elif not isinstance(buffer, torch.Tensor):
            raise ValueError(
                f"""
                The argument 'buffer' must be None or of type float,
                int, or torch.Tensor, but got {type(buffer)}.
                """
                )
        
        # Register buffer as a persistent buffer which is available as self.buffer
        self.register_buffer(
            'buffer',
            buffer,
            )
        
        return
    
    def pad_inference(
            self,
            x: torch.Tensor,
            buffer_io: Optional[ BufferIO ] = None,
            ):

        if not self.causal:
            raise ValueError(
                """
                Streaming inference is only supported for causal convolutions.
                """
                )

        if x.shape[0] != 1:
            raise ValueError(
                f"""
                Streaming inference requires a batch size
                of 1, but batch size is {x.shape[0]}.
                """
                )
        
        if buffer_io is None:
            in_buffer = self.buffer
        else:
            in_buffer = buffer_io.next_in_buffer()
            if in_buffer is None:
                in_buffer = self.buffer
                buffer_io.append_internal_buffer( in_buffer )

        x = torch.cat(
            (in_buffer, x),
            -1,
            )

        out_buffer = x[ ..., -self.pad_len: ]
        if buffer_io is None:
            self.buffer = out_buffer
        else:
            buffer_io.append_out_buffer(out_buffer)

        return x
    
    def forward(
            self,
            x: torch.Tensor,
            inference: bool = False,
            buffer_io: Optional[ BufferIO ] = None,
            ):
        if inference:
            x = self.pad_inference(x, buffer_io=buffer_io)
        else:
            x = self.pad(x)
        return x
    
    def reset_buffer(self):
        self.buffer.zero_()
        if self.buffer.shape[-1] != self.pad_len:
            raise ValueError(
                f"""
                Buffer shape {self.buffer.shape} does not match the expected
                shape (1, {self.in_channels}, {self.pad_len}).
                """
                )