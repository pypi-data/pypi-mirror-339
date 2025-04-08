def reverse_string(s: str) -> str:
    """
    反转字符串

    参数:
        s (str): 需要反转的字符串

    返回:
        str: 反转后的字符串

    异常:
        TypeError: 如果输入不是字符串类型，则抛出此异常
    """
    # 类型检查
    if not isinstance(s, str):
        raise TypeError("输入必须是字符串类型")

    # 字符串反转逻辑
    try:
        return s[::-1]
    except Exception as e:
        # 捕获潜在的异常并提供更友好的错误信息
        raise RuntimeError(f"字符串反转时发生错误: {e}")



def count_vowels(s: str) -> int:
    """
    统计字符串中元音字母的数量。

    参数:
        s (str): 输入字符串。

    返回:
        int: 元音字母的数量。

    注意:
        如果输入不是字符串类型，将抛出 ValueError。
    """
    # 定义元音字母集合，提升查找效率
    VOWELS = set('aeiouAEIOU')

    # 输入验证，确保输入是字符串类型
    if not isinstance(s, str):
        raise ValueError("输入必须是字符串类型")

    # 使用生成器表达式统计元音字母数量
    return sum(1 for char in s if char in VOWELS)



def is_palindrome(s: str) -> bool:
    """
    判断给定字符串是否为回文字符串。

    参数:
        s (str): 输入字符串，可以包含空格和标点符号。

    返回:
        bool: 如果字符串是回文，则返回 True；否则返回 False。

    注意:
        1. 忽略大小写。
        2. 忽略空格和标点符号。
        3. 空字符串被视为回文。
    """
    if not isinstance(s, str):
        raise ValueError("输入必须是字符串类型")

    # 过滤掉非字母数字字符，并转换为小写
    cleaned = ''.join(c.lower() for c in s if c.isalnum())

    # 使用双指针法判断回文
    left, right = 0, len(cleaned) - 1
    while left < right:
        if cleaned[left] != cleaned[right]:
            return False
        left += 1
        right -= 1
    return True

