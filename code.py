class Node():
    def __init__(self,p,name):
        self.p=p
        self.name=name
        self.parent=[]
        self.sp=[self]
        self.children=[]
        
def add_directed_edge(Node1,Node2):
    Node1.children.append(Node2)
    Node2.parent.append(Node1)
    Node2.sp.append(Node1)
        
def get_index(position,value,domain):
    index=[]
    l=2**position
    repeat=int(domain/l/2)
    for i1 in range(repeat):
        for i2 in range(1,l+1):
            index.append((i1*2+value)*l+i2-1)
    return(index)

def get_multi(list1,list2,p1,p2):
    same_list=set(list1) & set(list2)
    #ex_list=list(set(list2)-set(list1))
    p_list=[]
    for i1,ni1 in enumerate(p1):
        
        index_list=set(range(2**len(list2)))
        for i0,ni0 in enumerate(list1):
            if ni0 in same_list: 
                value=(i1//2**i0)%2
                index_list=index_list & set(get_index(
                                            list2.index(ni0),
                                            value,
                                            2**len(list2)))
        p_list+=[ni1*p2[x] for x in index_list]
    n_list=[x for x in list2 if x not in list1]+list1
    return(p_list,n_list)

def get_sum(Node,p1,list1):
    domain=[0,1]
    index_N=list1.index(Node)
    total_list=[]
    for i in domain:
        total_list+=[get_index(index_N,i,2**len(list1))]
    p_list=[]

    for i in range(len(total_list[0])):
        p_list.append(sum([p1[total_list[i2][i]] for i2 in range(len(total_list))]))
    n_list=[x for x in list1 if not (x==Node)]
    return(p_list,n_list)

def get_condition(list1,list2,p1,p2):
    p_list=[]
    for i1,ni1 in enumerate(p1):
        
        index_list=set(range(2**len(list2)))
        for i0,ni0 in enumerate(list1):
            if ni0 in list2: 
                value=(i1//2**i0)%2
                index_list=index_list & set(get_index(
                                            list2.index(ni0),
                                            value,
                                            2**len(list2)))
        p_list+=[ni1/p2[x] for x in index_list]
    n_list=[x for x in list1 if x not in list2]
    return(p_list,n_list,list1)

pA=[0.9,0.1]
pB=[.9,.1,.1,.9]
pC=[.9,.1,.1,.9]
pD=[.99,.01,.1,.9,.1,.9,.05,.95]

A=Node(pA,'A')
B=Node(pB,'B')
C=Node(pC,'C')
D=Node(pD,'D')
add_directed_edge(A,B)
add_directed_edge(A,C)
add_directed_edge(B,D)
add_directed_edge(C,D)

p,n=get_multi(A.sp,B.sp,A.p,B.p)
p,n=get_multi(n,C.sp,p,C.p)
p,n=get_multi(n,D.sp,p,D.p)

p1,n1=get_sum(B,p,n)
p1,n1=get_sum(C,p1,n1)
#p,n=get_sum(D,p,n)
p2,n2=get_sum(A,p1,n1)

rp,rn,rn2=get_condition(n1,n2,p1,p2)
print(rp)
print([x.name for x in rn])
print([x.name for x in rn2])

p1,n1=get_sum(A,p,n)
p1,n1=get_sum(C,p1,n1)
p2,n2=get_sum(B,p1,n1)

rp,rn,rn2=get_condition(n1,n2,p1,p2)
print(rp)
print([x.name for x in rn])
print([x.name for x in rn2])

p1,n1=get_sum(A,p,n)
p1,n1=get_sum(B,p1,n1)
p2,n2=get_sum(C,p1,n1)

rp,rn,rn2=get_condition(n1,n2,p1,p2)
print(rp)
print([x.name for x in rn])
print([x.name for x in rn2])


import numpy as np

        
def sample(Node,parent_info=[]):
    parent_size=len(Node.parent)
    parent_info=parent_info
    domain=len(Node.p)
    #Node.p
    index_list=set([x for x in range(domain)])
    if parent_info!=[]:
        for i,parent_value in enumerate(parent_info):
            index_list=index_list & set(get_index(i,parent_value,domain))
    index_list=list(index_list)
    p=Node.p[index_list[0]]
    num=np.random.binomial(1,p,1)[0]
    return(num)

     
# foward sampling     
for i in range(10):
    a=sample(A)
    b=sample(B,[a])
    c=sample(C,[a])
    d=sample(D,[b,c])
    print([a,b,c,d])

#d=0
print('if d=0-----------------')  
i=0
r=0
while i<10:
    a=sample(A)
    b=sample(B,[a])
    c=sample(C,[a])
    d=sample(D,[b,c])
    if d==0:
        i+=1
        print([a,b,c,d])
    else:
        r+=1
print('reject:'+str(r))    
            
 #ordered gibbs

def gibbs_sample(Node,other_value,other_list,p1,list1):
    index_list=set(range(2**len(list1)))
    for i,Node in enumerate(other_list):
        index_list=index_list & set(get_index(
                                            list1.index(Node),
                                            other_value[i],
                                            2**len(list1)))
    p=p1[list(index_list)[0]] 
    result=np.random.binomial(1,p,1)[0]
    return(result)




print('begin ordered gibbs sampling')
a=0
b=0
c=0
d=0

p1,n1=get_sum(A,p,n)
rp1,_,rn1=get_condition(n,n1,p,p1)
p1,n1=get_sum(B,p,n)
rp2,_,rn2=get_condition(n,n1,p,p1)
p1,n1=get_sum(C,p,n)
rp3,_,rn3=get_condition(n,n1,p,p1)
p1,n1=get_sum(D,p,n)
rp4,_,rn4=get_condition(n,n1,p,p1)

i=0
while i<10:
    a=gibbs_sample(A,[b,c,d],[B,C,D],rp1,rn1)
    b=gibbs_sample(B,[a,c,d],[A,C,D],rp2,rn2)
    c=gibbs_sample(C,[a,b,d],[A,B,D],rp3,rn3)
    d=gibbs_sample(D,[a,b,c],[A,B,C],rp4,rn4)
    i+=1
    print([a,b,c,d])
    
