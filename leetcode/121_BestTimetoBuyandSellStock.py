class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        end = len(prices) -1
        high_price = 0
        ans = 0        
        low_price = 0
        for i in range(end,-1,-1):
            high_price = max(high_price, prices[i])
            ans = max(ans , high_price - prices[i] )
                
        return ans
