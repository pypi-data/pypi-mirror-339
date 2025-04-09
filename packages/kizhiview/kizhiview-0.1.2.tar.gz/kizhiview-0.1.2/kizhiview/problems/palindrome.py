def get_methods():
    return [
        (
            "Method 1: Reverse the string",
            '''def is_palindrome(s):
    return s == s[::-1]'''
        ),
        (
            "Method 2: Using while loop",
            '''def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True'''
        ),
    ]

def show():
    methods = get_methods()
    for title, code in methods:
        print(f"\n{title}\n{code}\n")
