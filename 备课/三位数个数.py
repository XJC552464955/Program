count = 0
for i in range(1,5):
    for j in range(1, 5):
        for k in range(1, 5):
            if(i!=j and i!=k and j!=k):
                print(str(i)+str(j)+str(k))
                count+=1
print("数量:"+str(count))