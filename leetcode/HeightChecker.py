class Solution:
    def heightChecker(self, heights: List[int]) -> int:
        checker=list(i for i in heights)
        checker.sort()
        counter = 0
        for i in range(len(heights)):
            if heights[i] != checker[i]:
                counter += 1
                
        return counter
