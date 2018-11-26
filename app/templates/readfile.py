pen=open("group.txt","w")
pen.write("[")
cnt=0
with open("mymedword.txt",encoding='utf-8') as f:
    while True:
        line=f.readline()
        if not line:
            break
        if cnt!=0:
            pen.write(",")
        pen.write("'")
        pen.write(line.split(' ')[0])
        pen.write("'")
        cnt+=1
        if cnt>=3700:
            print("error")
            break
        #print(line.split(' ')[0])
pen.write("]")
pen.close()