class Solution:
    def isPalindrome(self, x: int) -> bool:
        return str(x) == str(x)[::-1]
        str_x = str(x)
        n = len(str_x) 
        i = 0
        j = n-1
        k = n//2
        while i <= k and j >= k:
            if str_x[i] != str_x[j]:
                return False
            i+=1
            j-=1
        return True
