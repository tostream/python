class Solution:
    def dominantIndex(self, nums: List[int]) -> int:
        if len(nums) == 0: return -1

        highest = -1
        secondHighest = -1
        highestIndex = 0
        
        for i,n in enumerate(nums):
            if n >= highest:
                secondHighest = highest
                highest = n
                highestIndex = i
            elif n > secondHighest:
                secondHighest = n
        print(highest)
        print(secondHighest)
        if highest < secondHighest*2:
            highestIndex = -1
        
        return highestIndex
        if len(nums) == 1: return 0
        check = [i for i in nums]
        check.sort()
        if check[-2] * 2 > check[-1]:            
            return -1
        return nums.index(check[-1])
