import torch
import torch.nn as nn
import torch.nn.functional as F


class AttentiveStatisticsPooling(nn.Module):
    """基于注意力机制的统计池化层，用于提取时域特征的加权统计量

    本层通过注意力机制学习每个时间步的权重，计算加权均值和标准差，
    最终输出拼接后的统计特征（形状 [N, 2*C, 1]）

    参数
    ---------
    channels : int
        输入特征的通道数（对应特征维度）
    attention_channels : int, 可选（默认128）
        注意力中间层的通道数
    global_context : bool, 可选（默认True）
        是否使用全局上下文信息（拼接全局均值/标准差）

    示例
    -------
    # 输入形状：[批大小, 通道数, 时间步长]
    inp_tensor = torch.rand([8, 64, 120])  # [N, C, L]
    asp_layer = AttentiveStatisticsPooling(64)
    lengths = torch.tensor([0.8, 0.7, 0.9, 1.0, 0.6, 1.0, 0.9, 0.8])  # 相对长度
    out_tensor = asp_layer(inp_tensor, lengths)
    print(out_tensor.shape)
    torch.Size([8, 128, 1])

    # 当不指定lengths时（假设所有时间步有效）
    out_tensor = asp_layer(inp_tensor)
    print(out_tensor.shape)
    torch.Size([8, 128, 1])
    """

    def __init__(self, channels, attention_channels=128, global_context=True):
        super().__init__()
        self.eps = 1e-12  # 数值稳定用的小量
        self.global_context = global_context

        # TDNN块处理输入特征（时延神经网络层）
        if global_context:
            # 当使用全局上下文时，输入为原始特征+全局均值+全局标准差（3倍通道）
            self.tdnn = TDNNBlock(channels * 3, attention_channels, 1, 1)
        else:
            # 否则直接使用原始特征
            self.tdnn = TDNNBlock(channels, attention_channels, 1, 1)

        # 注意力计算模块
        self.tanh = nn.Tanh()  # 激活函数
        self.conv = nn.Conv1d(
            in_channels=attention_channels,
            out_channels=channels,  # 输出通道与输入特征通道一致
            kernel_size=1
        )

    def forward(self, x, lengths=None):
        """前向传播过程

        参数
        ---------
        x : torch.Tensor
            输入特征张量，形状为 [N, C, L]
            (批大小, 通道数, 时间步长)
        lengths : torch.Tensor, 可选
            各样本有效长度的比例（0.0~1.0），形状为 [N,]

        返回
        -------
        pooled_stats : torch.Tensor
            拼接后的加权统计量，形状为 [N, 2*C, 1]
        """
        L = x.shape[-1]  # 获取时间步长

        # 定义统计量计算函数
        def _compute_statistics(x, m, dim=2, eps=self.eps):
            """计算加权均值和标准差
            参数：
                x: 输入特征 [N, C, L]
                m: 注意力权重 [N, C, L]
                dim: 计算维度（时间维度）
            """
            mean = (m * x).sum(dim)  # 加权均值
            std = torch.sqrt(
                (m * (x - mean.unsqueeze(dim)).pow(2)).sum(dim).clamp(eps)
            )  # 加权标准差（clamp防止数值不稳定）
            return mean, std

        # 处理长度掩码
        if lengths is None:
            # 如果未提供长度，假设所有时间步有效
            lengths = torch.ones(x.shape[0], device=x.device)

        # 生成二进制掩码 [N, 1, L]
        # 将相对长度转换为绝对长度（lengths * L），然后生成掩码
        mask = length_to_mask(lengths * L, max_len=L, device=x.device)
        mask = mask.unsqueeze(1)  # 增加通道维度

        # 全局上下文处理
        if self.global_context:
            # 计算全局统计量（不考虑注意力权重）
            total = mask.sum(dim=2, keepdim=True).float()  # 有效时间步总数
            global_mean, global_std = _compute_statistics(x, mask / total)

            # 扩展全局统计量到每个时间步
            global_mean = global_mean.unsqueeze(2).repeat(1, 1, L)  # [N, C, L]
            global_std = global_std.unsqueeze(2).repeat(1, 1, L)  # [N, C, L]

            # 拼接原始特征+全局均值+全局标准差
            attn = torch.cat([x, global_mean, global_std], dim=1)  # [N, 3*C, L]
        else:
            attn = x  # 直接使用原始特征

        # 通过注意力网络
        attn = self.tdnn(attn)  # TDNN特征变换
        attn = self.tanh(attn)  # 非线性激活
        attn = self.conv(attn)  # 1x1卷积生成注意力权重

        # 掩码处理：将填充位置的注意力权重设为负无穷
        attn = attn.masked_fill(mask == 0, float("-inf"))

        # 生成注意力权重（时间维度softmax归一化）
        attn = F.softmax(attn, dim=2)  # [N, C, L]

        # 计算最终加权统计量
        mean, std = _compute_statistics(x, attn)

        # 拼接统计量 [N, 2*C, 1]
        pooled_stats = torch.cat((mean, std), dim=1).unsqueeze(2)

        return pooled_stats


class MultiHeadAttentionPooling(nn.Module):
    def __init__(self, d_model: int, num_heads: int = 4, dropout: float = 0.1):
        super().__init__()
        assert d_model % num_heads == 0, "d_model必须能被num_heads整除"

        self.d_model = d_model
        self.num_heads = num_heads
        self.head_dim = d_model // num_heads

        # 可学习的查询向量
        self.query = nn.Parameter(torch.randn(1, 1, d_model))  # [1, 1, d_model]

        # 多头注意力层（调整为支持新维度）
        self.attention = nn.MultiheadAttention(
            embed_dim=d_model,
            num_heads=num_heads,
            dropout=dropout,
            batch_first=False  # 强制使用 (seq_len, batch, embed_dim)
        )

        # 层归一化
        self.layer_norm = nn.LayerNorm(d_model)

        self._reset_parameters()

    def _reset_parameters(self):
        nn.init.xavier_uniform_(self.query)

    def forward(self, x: torch.Tensor, lengths=None) -> torch.Tensor:
        """
        Args:
            x: 输入序列, shape [batch_size, d_model, seq_len]
        Returns:
            池化后的特征向量, shape [batch_size, d_model]
        """
        batch_size = x.size(0)

        # 调整输入维度到 [seq_len, batch_size, d_model]
        x = x.permute(2, 0, 1)  # [seq_len, batch, d_model]

        # 扩展可学习query到batch维度
        query = self.query.expand(-1, batch_size, -1)  # [1, batch, d_model]

        # 注意力计算
        attn_output, _ = self.attention(
            query=query,  # [1, batch, d_model]
            key=x,  # [seq_len, batch, d_model]
            value=x,  # [seq_len, batch, d_model]
        )

        # 调整维度并归一化
        output = attn_output.squeeze(0)  # [batch, d_model]
        output = self.layer_norm(output)
        output = output.unsqueeze(2)

        return output
