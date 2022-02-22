class Solution:
    def charHash(self,input_str: str) -> int:
        hash_map={'A':1,
                  'B':2,
                  'C':3,
                  'D':4,
                  'E':5,
                  'F':6,
                  'G':7,
                  'H':8,
                  'I':9,
                  'J':10,
                  'K':11,
                  'L':12,
                  'M':13,
                  'N':14,
                  'O':15,
                  'P':16,
                  'Q':17,
                  'R':18,
                  'S':19,
                  'T':20,
                  'U':21,
                  'V':22,
                  'W':23,
                  'X':24,
                  'Y':25,
                  'Z':26
                 }
        return hash_map[input_str]
    
    def titleToNumber(self, columnTitle: str) -> int:
        ans, pos = 0, 0
        for letter in reversed(columnTitle):
            digit = self.charHash(letter)
            ans += digit * 26**pos
            pos += 1
            
        return ans
