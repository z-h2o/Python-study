def is_palindrome(text):
    """判断是否为回文"""
    import re

    clean = text.lower()
    # clean = re.sub(r"[^a-z0-9]", "", text.lower())
    print(clean, clean[::-1], clean == clean[::-1])
    return clean == clean[::-1]


is_palindrome("ABcBA")
