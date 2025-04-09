#WAP on if list of elements size is 4 or above 4 thoese elements only need to be print

def listsize(l):

    result =[]
    for ele in range(len(l)):
    
        if len(l[ele]) >= 4:
            #print(l[ele])
            result.append(l[ele])
    print(result)
l=input("Enter any string:").split()
listsize(l)
        
