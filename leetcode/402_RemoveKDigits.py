class Solution:
    def removeKdigits(self, num: str, k: int) -> str:
        # edge case
        if len(num) <= k: return '0'
        
        stack = []
        for i, digit in enumerate(num):
            while k > 0 and stack and int(stack[-1]) > int(digit):
                # remove the digit
                stack.pop()
                k -= 1
            stack.append(digit)
        
        while k > 0:
            stack.pop()
            k -= 1
            
        ans = ''.join(stack).lstrip('0')
        return ans if ans else '0'

    
    #monotonicstack
