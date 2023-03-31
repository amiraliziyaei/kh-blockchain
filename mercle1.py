import hashlib
def mercle(trx):
    myhash = []
    while True :
        #trx : list of transaction
        n=0
        x=""
        for i in trx :
            x += i
            n += 1
            if n ==2 :
                myhash.append(hashlib.sha256(x.encode()).hexdigest())
                n = 0
                x = ""
            
            if i == trx[-1] and n == 1 :
                x += i
                myhash.append(hashlib.sha256(x.encode()).hexdigest())
        if len(myhash) > 1 :
            trx=myhash
            myhash=[]
        else :

            return myhash

            break

#test it !
#shortly and clean code 
#great and strong
trx = ['1','2','3','4','5']
print(mercle(trx))
