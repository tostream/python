class Solution:
    def countBits(self, n: int) -> List[int]:
        result = []
        for i in range(n+1):
            check=0
            num = i
            while (num>0):
                check += num%2
                num = int(num/2)
            result.append(check)
        return result
