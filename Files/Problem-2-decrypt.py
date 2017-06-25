def answer(l, t):
    # your code here
    ## Have two indecies, both starting at zero and a
    ## current sum value.
    ## Begin loop.
    ## If they are the same index, check if that index
    ## is the desired t value.
    ## If it is, return a list of [strtIndx,endIndx]
    ## Else move endIndx to the right and add the value
    ## there to the current sum.
    ## If the current sum is correct return [strtIndx,
    ## endIndx]
    ## If the current sum is too small, move endIndx
    ## to the right, add the new endIndx to the current
    ## sum.
    ## If the current sum is too large, subtract strtIndx
    ## value from the current sum then move strtIndx to
    ## the right.
    ## If endIndx == len(l), return [-1,-1]

    strtIndx = 0
    endIndx = 0
    currSum = l[0]
    maxLen = len(l)

    while True:
        if strtIndx == endIndx:
            if l[strtIndx] == t:
                return [strtIndx, endIndx]
            else:
                endIndx += 1
                if endIndx == maxLen:
                    return [-1, -1]
                currSum += l[endIndx]
        elif currSum == t:
            return [strtIndx, endIndx]
        elif currSum < t:
            endIndx += 1
            if endIndx == maxLen:
                return [-1, -1]
            currSum += l[endIndx]
        else:
            currSum -= l[strtIndx]
            strtIndx += 1

ls = [[4, 3, 10, 2, 8], [1, 2, 3, 4], [4, 3, 5, 7, 8]]
ks = [12, 15, 12]
ans = [[2, 3], [-1, -1], [0, 2]]

for i in range(len(ls)):
    if answer(ls[i], ks[i]) == ans[i]:
        print("Passed test ", i)
