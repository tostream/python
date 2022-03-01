class Solution:
    def countBits(self, n: int) -> List[int]:
        res = [0]
        while len(res) <= n:
            res += [i+1 for i in res]
        return res[:n+1]
        result = []
        for i in range(n+1):
            check=0
            num = i
            while (num>0):
                check += num%2
                num = int(num/2)
            result.append(check)
        return result
