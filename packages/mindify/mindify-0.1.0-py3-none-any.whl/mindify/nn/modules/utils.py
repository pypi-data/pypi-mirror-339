import torch


def length_to_mask(length, max_len=None, dtype=None, device=None):
    """根据序列长度生成二进制掩码矩阵（0/1矩阵），用于标识有效数据区域

    实现参考：https://discuss.pytorch.org/t/how-to-generate-variable-length-mask/23397/3

    参数
    ---------
    length : torch.LongTensor
        包含每个序列长度的1维张量，例如 shape=(batch_size,)
    max_len : int, 可选
        生成掩码的最大长度（第二维度尺寸），默认为length中的最大值
    dtype : torch.dtype, 可选
        输出掩码的数据类型，默认与length类型相同
    device : torch.device, 可选
        输出掩码所在的设备，默认与length所在设备相同

    返回
    -------
    mask : torch.Tensor
        二进制掩码矩阵，shape=(batch_size, max_len)
        有效位置为1，填充位置为0

    示例
    -------
    length = torch.tensor([1, 2, 3])
    mask = length_to_mask(length)
    print(mask)
    tensor([[1, 0, 0],
            [1, 1, 0],
            [1, 1, 1]])

    length = torch.tensor([2, 3, 1])
    mask = length_to_mask(length, max_len=4)
    print(mask)
    tensor([[1, 1, 0, 0],
            [1, 1, 1, 0],
            [1, 0, 0, 0]])
    """
    # 确保输入是1维张量
    assert len(length.shape) == 1, "ensure length is one-dimensional"

    # 计算最大长度（当未指定max_len时）
    if max_len is None:
        max_len = length.max().long().item()  # 将张量转换为Python标量

    # 核心实现逻辑：
    # 1. 生成0到max_len-1的位置索引矩阵（广播机制）
    # 2. 将每个位置的索引与对应序列长度比较
    # 3. 当位置索引 < 序列长度时，该位置标记为True（即有效位置）
    # shape: (batch_size, max_len)
    row_vector = torch.arange(
        max_len,
        device=length.device,  # 保持设备一致
        dtype=length.dtype  # 保持数据类型一致（通常为torch.int64）
    )  # 生成 [0, 1, 2, ..., max_len-1]

    # 扩展为二维矩阵并进行广播比较
    mask = row_vector.expand(len(length), max_len) < length.unsqueeze(1)

    # 转换最终输出的数据类型和设备
    # 注意：这里使用torch.as_tensor确保类型和设备正确，同时避免不必要的数据拷贝
    mask = torch.as_tensor(mask, dtype=dtype, device=device)

    return mask
