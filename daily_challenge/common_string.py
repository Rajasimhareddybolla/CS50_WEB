#Q)  Maximum Product of Word Lengths
#
#Given a string array words, return the maximum value of length(word[i]) * length(word[j]) where the two words do not share common letters. If no such two words exist, return 0.
def max_prodouct(arr):
    leng = []
    for i in range(0,len(arr)):
        #betwween two adjacent strings
        for k in range(0,len(arr)):
            if i != k:
                is_consists = False
                for ch in arr[i]:
                    for a_ch in arr[k]:
                        if ch == a_ch:
                            is_consists = True
                            break
                if not is_consists:    
                    leng.append(len(arr[i])*len(arr[k]))
    if leng:
        return max(leng)
    else:
        return 0
words = ["a","ab","abc","d","cd","bcd","abcd"]
print(max_prodouct(words))