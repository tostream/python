class Solution:
    def isValid(self, s: str) -> bool:
        open_map = ["(", "{", "["]
        close_map = {")":"(", "}":"{", "]":"["}
        ans = []
        for i in s:
            if i in open_map:
                ans.append(i)
            elif i in close_map:
                if len(ans) == 0:
                    return False
                temp = ans.pop()
                if temp != close_map[i] :
                    return False
        return not len(ans) 
