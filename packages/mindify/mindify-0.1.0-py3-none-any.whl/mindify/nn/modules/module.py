import torch
import torch.nn as nn
import torch.nn.functional as F
from funasr.models.conformer.encoder import ConformerEncoder

import mindify.audio.nn as ann


class TDNNBlock(nn.Module):
    """An implementation of TDNN.

    Arguments
    ---------
    in_channels : int
        Number of input channels.
    out_channels : int
        The number of output channels.
    kernel_size : int
        The kernel size of the TDNN blocks.
    dilation : int
        The dilation of the TDNN block.
    activation : torch class
        A class for constructing the activation layers.
    groups : int
        The groups size of the TDNN blocks.

    Example
    -------
    inp_tensor = torch.rand([8, 120, 64]).transpose(1, 2)
    layer = TDNNBlock(64, 64, kernel_size=3, dilation=1)
    out_tensor = layer(inp_tensor).transpose(1, 2)
    out_tensor.shape
    torch.Size([8, 120, 64])
    """

    def __init__(
            self,
            in_channels,
            out_channels,
            kernel_size,
            dilation,
            activation=nn.ReLU,
            groups=1,
    ):
        super().__init__()
        self.conv = nn.Conv1d(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=kernel_size,
            dilation=dilation,
            # 保持时间维度尺寸不变
            padding=dilation * (kernel_size - 1) // 2,
            groups=groups,
        )
        self.activation = activation()
        self.norm = nn.BatchNorm1d(out_channels)

    def forward(self, x):
        """Processes the input tensor x and returns an output tensor."""
        return self.norm(self.activation(self.conv(x)))


class Res2NetBlock(nn.Module):
    """An implementation of Res2NetBlock w/ dilation.

    Arguments
    ---------
    in_channels : int
        The number of channels expected in the input.
    out_channels : int
        The number of output channels.
    scale : int
        The scale of the Res2Net block.
    kernel_size: int
        The kernel size of the Res2Net block.
    dilation : int
        The dilation of the Res2Net block.

    Example
    -------
    inp_tensor = torch.rand([8, 120, 64]).transpose(1, 2)
    layer = Res2NetBlock(64, 64, scale=4, dilation=3)
    out_tensor = layer(inp_tensor).transpose(1, 2)
    out_tensor.shape
    torch.Size([8, 120, 64])
    """

    def __init__(
            self, in_channels, out_channels, scale=8, kernel_size=3, dilation=1
    ):
        super().__init__()
        assert in_channels % scale == 0
        assert out_channels % scale == 0

        in_channel = in_channels // scale
        hidden_channel = out_channels // scale

        self.blocks = nn.ModuleList(
            [
                TDNNBlock(
                    in_channel,
                    hidden_channel,
                    kernel_size=kernel_size,
                    dilation=dilation,
                )
                for i in range(scale - 1)
            ]
        )
        self.scale = scale

    def forward(self, x):
        """Processes the input tensor x and returns an output tensor."""
        y = []
        for i, x_i in enumerate(torch.chunk(x, self.scale, dim=1)):
            if i == 0:
                y_i = x_i
            elif i == 1:
                y_i = self.blocks[i - 1](x_i)
            else:
                y_i = self.blocks[i - 1](x_i + y_i)
            y.append(y_i)
        y = torch.cat(y, dim=1)
        return y


class SEBlock(nn.Module):
    """An implementation of squeeze-and-excitation block.

    Arguments
    ---------
    in_channels : int
        The number of input channels.
    se_channels : int
        The number of output channels after squeeze.
    out_channels : int
        The number of output channels.

    Example
    -------
    inp_tensor = torch.rand([8, 120, 64]).transpose(1, 2)
    se_layer = SEBlock(64, 16, 64)
    lengths = torch.rand((8,))
    out_tensor = se_layer(inp_tensor, lengths).transpose(1, 2)
    out_tensor.shape
    torch.Size([8, 120, 64])
    """

    def __init__(self, in_channels, se_channels, out_channels):
        super().__init__()

        self.conv1 = nn.Conv1d(
            in_channels=in_channels, out_channels=se_channels, kernel_size=1
        )
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv1d(
            in_channels=se_channels, out_channels=out_channels, kernel_size=1
        )
        self.sigmoid = nn.Sigmoid()

    def forward(self, x, lengths=None):
        """Processes the input tensor x and returns an output tensor."""
        L = x.shape[-1]
        if lengths is not None:
            mask = ann.length_to_mask(lengths * L, max_len=L, device=x.device)
            mask = mask.unsqueeze(1)
            total = mask.sum(dim=2, keepdim=True)
            s = (x * mask).sum(dim=2, keepdim=True) / total
        else:
            s = x.mean(dim=2, keepdim=True)

        s = self.relu(self.conv1(s))
        s = self.sigmoid(self.conv2(s))

        return s * x


class SERes2NetBlock(nn.Module):
    """An implementation of building block in ECAPA-TDNN, i.e.,
    TDNN-Res2Net-TDNN-SEBlock.

    Arguments
    ---------
    in_channels: int
        Expected size of input channels.
    out_channels: int
        The number of output channels.
    res2net_scale: int
        The scale of the Res2Net block.
    se_channels : int
        The number of output channels after squeeze.
    kernel_size: int
        The kernel size of the TDNN blocks.
    dilation: int
        The dilation of the Res2Net block.
    activation : torch class
        A class for constructing the activation layers.
    groups: int
        Number of blocked connections from input channels to output channels.

    Example
    -------
    x = torch.rand(8, 120, 64).transpose(1, 2)
    conv = SERes2NetBlock(64, 64, res2net_scale=4)
    out = conv(x).transpose(1, 2)
    out.shape
    torch.Size([8, 120, 64])
    """

    def __init__(
        self,
        in_channels,
        out_channels,
        res2net_scale=8,
        se_channels=128,
        kernel_size=1,
        dilation=1,
        activation=torch.nn.ReLU,
        groups=1,
    ):
        super().__init__()
        self.out_channels = out_channels
        self.tdnn1 = TDNNBlock(
            in_channels,
            out_channels,
            kernel_size=1,
            dilation=1,
            activation=activation,
            groups=groups,
        )
        self.res2net_block = Res2NetBlock(
            out_channels, out_channels, res2net_scale, kernel_size, dilation
        )
        self.tdnn2 = TDNNBlock(
            out_channels,
            out_channels,
            kernel_size=1,
            dilation=1,
            activation=activation,
            groups=groups,
        )
        self.se_block = SEBlock(out_channels, se_channels, out_channels)

        self.shortcut = None
        if in_channels != out_channels:
            self.shortcut = nn.Conv1d(
                in_channels=in_channels,
                out_channels=out_channels,
                kernel_size=1,
            )

    def forward(self, x, lengths=None):
        """Processes the input tensor x and returns an output tensor."""
        residual = x
        if self.shortcut:
            residual = self.shortcut(x)

        x = self.tdnn1(x)
        x = self.res2net_block(x)
        x = self.tdnn2(x)
        x = self.se_block(x, lengths)

        return x + residual


class MultiHeadAttentionBlock(nn.Module):
    """多头注意力模块，适配ECAPA的维度"""

    def __init__(self, embed_dim, num_heads):
        super().__init__()
        self.attention = nn.MultiheadAttention(
            embed_dim=embed_dim,
            num_heads=num_heads,
            batch_first=True
        )
        self.layer_norm = nn.LayerNorm(embed_dim)

    def forward(self, x, lengths=None):
        # 输入形状: [B, C, T]
        B, C, T = x.size()

        # 转换为注意力需要的形状 [B, T, C]
        x_in = x.permute(0, 2, 1)

        # 创建注意力mask（处理变长序列）
        if lengths is not None:
            max_len = T
            mask = torch.arange(max_len).expand(len(lengths), max_len) >= (lengths * max_len).long().unsqueeze(1)
            mask = mask.to(x.device)
        else:
            mask = None

        # 多头注意力
        attn_out, _ = self.attention(
            query=x_in,
            key=x_in,
            value=x_in,
            key_padding_mask=mask
        )

        # 残差连接 + 层归一化
        out = self.layer_norm(x_in + attn_out)

        # 恢复原始维度 [B, C, T]
        return out.permute(0, 2, 1)


class EcapaTDNN(nn.Module):
    """ECAPA-TDNN说话人嵌入模型，用于提取语音的说话人特征

    核心创新点：
    - 增强的通道注意力机制
    - 多尺度Res2Net结构
    - 多层特征聚合
    - 注意力统计池化

    论文：《ECAPA-TDNN: Emphasized Channel Attention, Propagation and Aggregation in TDNN Based Speaker Verification》
    论文链接：https://arxiv.org/abs/2005.07143

    参数说明
    ---------
    in_channels : int
        输入特征的维度（如MFCC的80维）
    embedding_dim : int, 默认192
        最终嵌入向量的维度
    activation : torch类, 默认ReLU
        激活函数类型
    channels : list[int], 默认[512,512,512,512,1536]
        各层的输出通道数配置
    kernel_sizes : list[int], 默认[5,3,3,3,1]
        各层的卷积核尺寸
    dilations : list[int], 默认[1,2,3,4,1]
        各层的膨胀系数（控制感受野）
    attention_channels : int, 默认128
        注意力层的通道数
    res2net_scale : int, 默认8
        Res2Net模块的分组数（多尺度）
    se_channels : int, 默认128
        SE注意力机制的通道数
    global_context : bool, 默认True
        是否使用全局上下文
    groups : list[int], 默认[1,1,1,1,1]
        各层的分组卷积配置

    示例
    -------
    # 输入形状：[批大小, 时间步数, 特征维度]
    input_feats = torch.rand([5, 120, 80])  # 5个样本，120帧，80维MFCC
    model = ECAPA_TDNN(80, embedding_dim=192)
    outputs = model(input_feats)
    print(outputs.shape)
    torch.Size([5, 1, 192])  # 输出形状：[批大小, 1, 嵌入维度]

    # 处理变长序列示例
    input_feats = torch.rand([3, 100, 80])
    lengths = torch.tensor([0.8, 1.0, 0.5])  # 相对长度
    outputs = model(input_feats, lengths)
    print(outputs.shape)
    torch.Size([3, 1, 192])
    """

    def __init__(
            self,
            in_channels: int = 80,
            embedding_dim: int = 192,
            activation=torch.nn.LeakyReLU,
            channels: list[int] = [512, 512, 512, 512, 1536],
            kernel_sizes: list[int] = [5, 3, 3, 3, 1],
            dilations: list[int] = [1, 2, 3, 4, 1],
            attention_channels=128,
            res2net_scale=8,
            se_channels=128,
            global_context=True,
            groups: list[int] = [1, 1, 1, 1, 1],
    ):
        super().__init__()
        # 参数校验
        assert len(channels) == len(kernel_sizes), "通道数与卷积核数必须一致"
        assert len(channels) == len(dilations), "通道数与膨胀系数数必须一致"

        self.mel_spectrogram = ann.MelSpectrogram(n_mels=in_channels)
        self.channels = channels
        self.blocks = nn.ModuleList()

        # 初始TDNN层（时间延迟神经网络），原论文 Conv1D(k=5, d=1) + ReLU + NB
        # 输入形状：[N, input_size, T] -> [N, 512, T]
        self.blocks.append(
            TDNNBlock(
                in_channels,  # 输入特征维度（如80）
                channels[0],  # 输出通道（512）
                kernel_sizes[0],  # 卷积核大小5
                dilations[0],  # 膨胀系数1
                activation,  # 激活函数
                groups[0],  # 分组卷积数
            )
        )

        # 构建SE-Res2Net模块堆叠层，论文里是3个, 等于 len(channels) - 2
        # SE-Res2Block(k=3,d=2),SE-Res2Block(k=3,d=3), SE-Res2Block(k=3,d=4),
        for i in range(1, len(channels) - 1):
            self.blocks.append(
                SERes2NetBlock(
                    in_channels=channels[i - 1],  # 输入通道（前一层的输出）
                    out_channels=channels[i],  # 输出通道（512）
                    res2net_scale=res2net_scale,  # Res2Net分组数（多尺度）
                    se_channels=se_channels,  # SE注意力中间层维度
                    kernel_size=kernel_sizes[i],  # 卷积核大小（3）
                    dilation=dilations[i],  # 膨胀系数（2/3/4）
                    activation=activation,  # 激活函数
                    groups=groups[i],  # 分组卷积数
                )
            )

        # 多层级特征聚合（Multi-layer Feature Aggregation）
        # 输入：前几层输出的拼接 [N, 512*3, T] -> [N, 1536, T]
        self.mfa = TDNNBlock(
            in_channels=sum(channels[1:-1]),  # 512*3=1536
            out_channels=channels[-1],  # 1536
            kernel_size=kernel_sizes[-1],  # 1x1卷积
            dilation=dilations[-1],  # 膨胀系数1
            activation=activation,
            groups=groups[-1],
        )

        # 注意力统计池化层（Attentive Statistics Pooling）
        # 输入：[N, 3072, T] -> [N, 3072, 1]
        self.pooling = ann.AttentiveStatisticsPooling(
            channels[-1],
            attention_channels=attention_channels,
            global_context=global_context,
        )
        # self.asp = MultiHeadAttentionPooling(channels[-1], num_heads=num_heads)
        # 批归一化处理，[N, 3072, 1] -> [N, 3072, 1]
        self.pooling_bn = nn.BatchNorm1d(channels[-1] * 2)

        # 最终线性变换层（降维到目标嵌入维度）
        # 输入：[N, 3072, 1] -> [N, 192, 1]
        self.fc = nn.Conv1d(
            in_channels=channels[-1]*2,  # 3072
            out_channels=embedding_dim,  # 192
            kernel_size=1,  # 1x1卷积
        )

    def forward(self, input):
        """前向传播过程

        参数
        ---------
        # x : torch.Tensor
        #     输入语音特征，形状为 [batch, time, features]
        #     例如：[32, 200, 80] 表示32个样本，200帧，80维特征
        # lengths : torch.Tensor, 可选
        #     各样本的有效长度比例（0.0~1.0），形状为 [batch]
        x: torch.Tensor
              输入语音序列，形状为 [batch, time]
        返回
        -------
        x : torch.Tensor
            说话人嵌入向量，形状为 [batch, embedding_dim]
        """
        with torch.no_grad():
            # [batch, time] -> [batch, channels(in_channels), time]
            x = self.mel_spectrogram(input)

        # 调整维度顺序以适应卷积层
        # [B, T, D] -> [B, D, T] (D=特征维度，T=时间步)
        # x = x.transpose(1, 2)

        # 各层特征保存列表（用于后续特征聚合）
        xl = []
        for layer in self.blocks:
            x = layer(x)
            xl.append(x)  # 保存各层输出

        # 多层级特征聚合（拼接中间层输出）
        # xl[1:] 取第1到第3层的SE-Res2Block的输出（各层形状[N,512,T]），第一层的输出不用
        # 拼接后形状 [N, 512*3, T] = [N, 1536, T]
        x = torch.cat(xl[1:], dim=1)
        x = self.mfa(x)  # 通过TDNN块 [N,1536,T] -> [N,1536,T]

        # 注意力统计池化
        x = self.pooling(x)  # [N, 3072, 1]
        x = self.pooling_bn(x)  # 批归一化

        # 最终线性变换
        x = self.fc(x)  # [N, 192, 1]

        # 调整输出维度 [B, D, 1] -> [B, 1, D] -> [B, D]
        # x = x.transpose(1, 2)
        x = x.squeeze(-1)
        return x


class Conformer(torch.nn.Module):
    def __init__(self, n_mels=80, num_blocks=6, output_size=256, embedding_dim=192, input_layer="conv2d2",
                 pos_enc_layer_type="rel_pos"):
        super(Conformer, self).__init__()

        self.mel_spectrogram = ann.MelSpectrogram(n_mels=n_mels)

        self.conformer = ConformerEncoder(input_size=n_mels, num_blocks=num_blocks,
                                          output_size=output_size, input_layer=input_layer,
                                          pos_enc_layer_type=pos_enc_layer_type)
        self.pooling = ann.AttentiveStatisticsPooling(output_size)
        self.bn = nn.BatchNorm1d(output_size * 2)
        self.fc = torch.nn.Linear(output_size * 2, embedding_dim)

    def forward(self, input):
        with torch.no_grad():
            # [batch, time] -> [batch, channels(in_channels), time]
            x = self.mel_spectrogram(input)

        x = x.squeeze(1).permute(0, 2, 1)
        lens = torch.ones(x.shape[0]).to(x.device)
        lens = torch.round(lens * x.shape[1]).int()
        x, masks, _ = self.conformer(x, lens)
        x = x.permute(0, 2, 1)
        x = self.pooling(x)
        x = self.bn(x)
        x = x.permute(0, 2, 1)
        x = self.fc(x)
        x = x.squeeze(1)
        return x

