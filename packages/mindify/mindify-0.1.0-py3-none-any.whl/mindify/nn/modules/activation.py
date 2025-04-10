import math

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchmetrics import Accuracy


class AMSoftmax(nn.Module):
    def __init__(self, embedding_dim, num_classes, margin=0.35, scale=30., label_smoothing=0.0):
        """
        Additive Margin Softmax Loss (AM-Softmax) 实现

        参数理论范围:
            - margin ∈ [0, π/2)  # 0 ≤ margin < 1.5708 弧度（约90度）
            - scale > 0          # 典型值范围[20, 60]

        经验参数设置:
            - 人脸识别: margin=0.35(20°), scale=30
            - 细粒度分类: margin=0.2(11.5°), scale=30
            - 过大margin(>0.5)会导致优化困难

        参数协同:
            - margin增大时需适当增加scale补偿相似度压缩
            - 例: margin=0.5时建议scale=40

        参数说明:
            embedding_dim (int): 特征嵌入维度
            num_classes (int): 分类类别总数
            margin (float, optional): 决策边界间隔，控制类间距离. 默认0.35
            scale (float, optional): 相似度缩放因子，放大分类置信度. 默认30.0
            label_smoothing (float, optional): 标签平滑系数. 默认0.0

        维度说明:
            - 权重矩阵形状: [embedding_dim, num_classes]
            - 输入特征形状: [batch_size, embedding_dim]
            - 标签形状: [batch_size]
        """
        super(AMSoftmax, self).__init__()
        # 参数校验
        assert margin >= 0 and margin < math.pi/2, f"Margin需在[0, π/2)范围内, 当前值{margin}"

        # 核心参数初始化
        self.margin = margin
        self.scale = scale
        self.label_smoothing = label_smoothing
        self.embedding_dim = embedding_dim
        self.num_classes = num_classes

        # 分类权重矩阵 (使用Xavier正态分布初始化)
        self.weight = nn.Parameter(torch.randn((embedding_dim, num_classes)), requires_grad=True)
        nn.init.xavier_normal_(self.weight, gain=1)  # 保持输入输出方差一致

        # 评估指标 (使用torchmetrics.Accuracy)
        self.accuracy = Accuracy(task="multiclass", num_classes=num_classes, top_k=1)

    def forward(self, x, labels):
        """
        前向传播过程

        输入参数:
            x (Tensor): 特征矩阵, 形状[batch_size, embedding_dim]
            labels (Tensor): 真实标签, 形状[batch_size]

        返回:
            loss (Tensor): 损失值, 形状[1]
            acc (Tensor): 当前batch准确率, 形状[1]

        计算流程:
            1. 特征和权重矩阵L2归一化
            2. 计算余弦相似度矩阵
            3. 对目标类别应用margin修正
            4. 缩放后计算交叉熵损失
        """
        # ============== 特征归一化 ==============
        # 输入特征L2归一化: 沿特征维度计算
        # 数学公式: x_norm = x / ||x||_2
        # 维度变化: [B, D] -> [B, D]
        x_norm = F.normalize(x, p=2, dim=1)

        # 权重矩阵L2归一化: 沿每个类别的权重向量归一化
        # 数学公式: w_norm = W / ||W||_2 (逐列归一化)
        # 维度变化: [D, C] -> [D, C]
        w_norm = F.normalize(self.weight, p=2, dim=0)

        # ============== 余弦相似度计算 ==============
        # 矩阵相乘得到余弦相似度
        # 数学公式: cosine = x_norm @ w_norm.T (自动转置)
        # 维度变化: [B, D] * [D, C] -> [B, C]
        cosine = torch.mm(x_norm, w_norm)

        # ============== Margin修正 ==============
        # 创建margin掩码矩阵 (仅目标位置有margin值)
        # scatter_参数说明:
        #   - dim=1: 按行填充
        #   - index=labels.view(-1,1): 目标列索引
        #   - src=self.margin: 填充值
        # 维度变化: [B, C] -> [B, C]
        margin_mask = torch.zeros_like(cosine, device=x.device)
        margin_mask.scatter_(1, labels.view(-1, 1), self.margin)

        # 对目标类别余弦值进行margin修正
        # 数学公式: cos(θ) - margin (仅对目标类别)
        cosine_m = cosine - margin_mask

        # ============== 缩放与损失计算 ==============
        # 相似度缩放: 扩大类间差异
        # 维度保持: [B, C] -> [B, C]
        logits = self.scale * cosine_m

        # 交叉熵损失计算 (内置log_softmax)
        # 数学公式: loss = -log(exp(s(cosθ_y - m)) / Σ exp(s·cosθ_j))
        loss = F.cross_entropy(logits, labels, label_smoothing=self.label_smoothing)

        # 准确率计算 (detach避免梯度回传)
        acc = self.accuracy(logits.detach(), labels.detach())

        return loss, acc


class AAMSoftmax(nn.Module):
    def __init__(self, embedding_dim, num_classes, margin=0.2, scale=30.0, label_smoothing=0.0):
        """
        Additive Angular Margin Softmax Loss (AAM-Softmax) 实现

        ██████ 核心数学原理 ██████
        通过角度空间添加间隔: cos(θ + m) = cosθ·cosm - sinθ·sinm
        相比AM-Softmax的余弦空间间隔，具有更好的几何解释性

        参数理论范围:
            - margin ∈ [0, π/2)  # 0 ≤ margin < 1.5708 弧度（约90度）
            - scale > 0          # 典型值范围[20, 60]

        经验参数设置:
            - 人脸识别: margin=0.35(20°), scale=64
            - 语音识别: margin=0.2(11.5°), scale=30
            - 过大margin(>0.5)会导致训练不稳定

        参数说明:
            embedding_dim (int): 特征嵌入维度
            num_classes (int): 分类类别总数
            margin (float): 角度间隔参数，控制决策边界弧度. 默认0.2
            scale (float): 相似度缩放因子，放大类间差异. 默认30.0
            label_smoothing (float): 标签平滑系数. 默认0.0

        维度说明:
            - 权重矩阵形状: [embedding_dim, num_classes]
            - 输入特征形状: [batch_size, embedding_dim]
            - 标签形状: [batch_size]
        """
        super(AAMSoftmax, self).__init__()
        # 参数校验
        assert margin >= 0 and margin < math.pi/2, f"Margin需在[0, π/2)范围内, 当前值{margin}"

        # 核心参数初始化
        self.margin = margin
        self.scale = scale
        self.label_smoothing = label_smoothing
        self.embedding_dim = embedding_dim
        self.num_classes = num_classes

        # 分类权重矩阵 (Xavier正态分布初始化)
        self.weight = nn.Parameter(torch.randn(embedding_dim, num_classes), requires_grad=True)
        nn.init.xavier_normal_(self.weight, gain=1)  # 保持输入输出方差一致

        # 预计算三角函数值（注册为buffer确保设备一致性）
        self.register_buffer('cos_m', torch.cos(torch.tensor(margin)))
        self.register_buffer('sin_m', torch.sin(torch.tensor(margin)))

        # 评估指标 (使用torchmetrics.Accuracy)
        self.accuracy = Accuracy(task="multiclass", num_classes=num_classes, top_k=1)

    def forward(self, x, labels):
        """
        前向传播过程

        输入参数:
            x (Tensor): 特征矩阵, 形状[batch_size, embedding_dim]
            labels (Tensor): 真实标签, 形状[batch_size] (值域: 0 ≤ labels < num_classes)

        返回:
            loss (Tensor): 损失值, 形状[1]
            acc (Tensor): 当前batch准确率, 形状[1]

        计算流程:
            1. 特征和权重L2归一化 → 2. 计算余弦相似度
            3. 计算角度修正后的余弦值 → 4. 构建目标类掩码
            5. 缩放相似度 → 6. 计算交叉熵损失
        """
        # ============== 特征归一化 ==============
        # 输入特征L2归一化 (沿特征维度)
        # 数学公式: x_norm = x / ||x||₂
        # 维度变化: [B, D] → [B, D] (B: batch_size, D: embedding_dim)
        x_norm = F.normalize(x, p=2, dim=1)

        # 权重矩阵L2归一化 (沿每个类别向量)
        # 数学公式: w_norm = W / ||W||₂ (逐列归一化)
        # 维度变化: [D, C] → [D, C] (C: num_classes)
        w_norm = F.normalize(self.weight, p=2, dim=0)

        # ============== 余弦相似度计算 ==============
        # 矩阵相乘计算原始余弦相似度
        # 数学公式: cosine = x_norm @ w_norm.T
        # 维度变化: [B, D] * [D, C] → [B, C]
        cosine = torch.mm(x_norm, w_norm)

        # ============== 角度间隔修正 ==============
        # 计算sinθ (基于cos²θ + sin²θ = 1)
        # clamp操作: 防止反向传播时梯度爆炸
        # 维度保持: [B, C] → [B, C]
        sine = torch.sqrt(1.0 - torch.pow(cosine, 2)).clamp(min=1e-6)

        # 应用角度加法公式: cos(θ + m) = cosθ·cosm - sinθ·sinm
        # 维度保持: [B, C] → [B, C]
        phi = cosine * self.cos_m - sine * self.sin_m

        # ============== 目标类掩码构建 ==============
        # 创建one-hot编码矩阵（仅目标位置为1）
        # scatter_参数解析:
        #   - dim=1: 按行填充
        #   - index=labels.view(-1,1): 目标列索引
        #   - src=1.0: 填充值
        # 维度变化: [B, C] → [B, C]
        one_hot = torch.zeros_like(cosine, device=x.device)
        one_hot.scatter_(1, labels.view(-1, 1), 1.0)

        # 混合修正后的余弦值（仅目标类应用phi）
        # 数学公式: output = one_hot * phi + (1 - one_hot) * cosine
        # 物理意义: 仅对目标类计算cos(θ+m)，其他类保持cosθ
        output = one_hot * phi + (1.0 - one_hot) * cosine

        # ============== 相似度缩放 ==============
        # 放大类间差异（增强损失函数的区分性）
        # 维度保持: [B, C] → [B, C]
        logits = output * self.scale

        # ============== 损失计算 ==============
        # 交叉熵损失（内置log_softmax + nll_loss）
        # 数学公式: loss = -log( exp(s·cos(θ_y + m)) / Σ exp(s·cosθ_j) )
        loss = F.cross_entropy(logits, labels, label_smoothing=self.label_smoothing)

        # 准确率计算（分离计算图防止梯度传播）
        acc = self.accuracy(logits.detach(), labels.detach())

        return loss, acc