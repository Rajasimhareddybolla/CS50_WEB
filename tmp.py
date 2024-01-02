class Solution(object):
    roman_code={
        "1":"I",
        "5":"V",
        "10":"X",
        "50":"L",
        "100":"C",
        "500":"D",
        "1000":"M"
    }

    def intToRoman(self, num):
        """
        :type num: int
        :rtype: str
        """
        self.num = num
        roman = ""
        updated_no = self.num
        nos = [1000, 500, 100, 50, 10, 5, 1]
        for no in nos:
            if int(updated_no / no) != 0:
                if no ==1:
                    roman += self.roman_code["1"]*updated_no
                    break
                roman += self.roman_code[str(no)]*int(updated_no / no)
                updated_no -= no*int(updated_no / no)
            if updated_no==0:
                break
        return roman
SOl = Solution()
print(SOl.intToRoman(1994))

