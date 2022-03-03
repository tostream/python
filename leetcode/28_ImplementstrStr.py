class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        try:
            return haystack.index(needle)
        except Exception:
            return -1
        for i in range(len(haystack) - len(needle)+1):
        if haystack[i:i+len(needle)] == needle:
            return i
        return -1
    
