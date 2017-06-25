def answer(plaintext):
    # your code here
    uCase = "000001"
    sp = "000000"

    strs = [##"code",
            "Braille",
            "The quick brown fox jumped over the lazy dog"]
    bnry = [##"100100101010100110100010",
            "000001110000111010100000010100111000111000100010",
            "000001011110110010100010000000111110101001010100100100101000000000110000111010101010010111101110000000110100101010101101000000010110101001101100111100100010100110000000101010111001100010111010000000011110110010100010000000111000100000101011101111000000100110101010110110"]

    convDict = {}

    
    for charStrI in range(len(strs)):
        upShift = 0
        print(convDict)
        for i, character in enumerate(strs[charStrI]):
            brSt = (i + upShift) * 6
            if character.isupper():
                upShift += 1
                convDict["UCASE"] = bnry[charStrI][brSt:brSt+6]
                brSt += 6
                convDict[character.lower()] = bnry[charStrI][brSt:brSt+6]
            else:
                convDict[character] = bnry[charStrI][brSt:brSt+6]

    finStr = ""    
    for character in plaintext:
        if character.isupper():
            finStr += convDict["UCASE"]
        finStr += convDict[character.lower()]
    print(convDict)
    testL = []
    for k in convDict:
        testL.append([k,convDict[k]])
    testL = sorted(testL, key=lambda x: x[0])
    for item in testL:
        print(item)
    return finStr


strs = ["code",
            "Braille",
            "The quick brown fox jumped over the lazy dog"]
bnry = ["100100101010100110100010",
            "000001110000111010100000010100111000111000100010",
            "000001011110110010100010000000111110101001010100100100101000000000110000111010101010010111101110000000110100101010101101000000010110101001101100111100100010100110000000101010111001100010111010000000011110110010100010000000111000100000101011101111000000100110101010110110"]

for i in range(len(strs)):
    if answer(strs[i]) == bnry[i]:
        print("Passed", i)
    else:
        print("Failed",i)
        ##print(answer(strs[i]))
        ##print(bnry[i])