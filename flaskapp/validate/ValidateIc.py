import re


def validateNRIC(str):
        if (len(str) != 9):
            return False
        
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        
        if(regex.search(str) is not None):
            return False
        
        str = str.upper()
        
        icList = []
        for i in str:
            icList.append(i)
            
        icList[1] = int(icList[1], 10) * 2
        icList[2] = int(icList[2], 10) * 7
        icList[3] = int(icList[3], 10) * 6
        icList[4] = int(icList[4], 10) * 5
        icList[5] = int(icList[5], 10) * 4
        icList[6] = int(icList[6], 10) * 3
        icList[7] = int(icList[7], 10) * 2
        
        weight = 0
        for i in range(1,8,1):
            weight = weight+icList[i]
        
        if (icList[0]=='T' or icList[0]=='G'):
            offset = 4
        else:
            offset = 0
        
        temp = (offset + weight) % 11
        
        
        st = ["J","Z","I","H","G","F","E","D","C","B","A"]
        fg = ["X","W","U","T","R","Q","P","N","M","L","K"]
        
        if (icList[0]=='S' or icList[0]=='T'):
            theAlpha = st[temp]
        elif (icList[0]=='F' or icList[0]=='G'):
            theAlpha = fg[temp]
        
        if (icList[8] != theAlpha):
            return False
        else:
            return True
        