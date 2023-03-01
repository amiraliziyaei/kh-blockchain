import hashlib
class root:
    def __init__(self, tnxs):
        self.mempool = tnxs
        self.hashes = []
        self.root = []
    def get_root(self):
        for j in self.mempool:
            x = j["hash"]
            self.hashes.append(x)
        myhash = []
        num = 0
        while True :
            n=0
            x=""
            if num == 0:
                for i in self.hashes:
                    self.hashes[num]= hashlib.sha256(i.encode()).hexdigest()
                    num += 1
            for i in self.hashes :
                x += i
                n += 1
                if n ==2 :
                    myhash.append(hashlib.sha256(x.encode()).hexdigest())
                    n = 0
                    x = ""
                if i == self.hashes[-1] and n == 1 :
                    x += i
                    myhash.append(hashlib.sha256(x.encode()).hexdigest())
            if len(myhash) > 1 :
                trx=myhash
                myhash=[]
            else :
                return myhash[0]
            break
