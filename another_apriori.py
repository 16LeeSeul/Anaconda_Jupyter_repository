import itertools
import sys

def prunning(k, item_set_2, a):  # Prunning 하는 함수
    fin = []
    for i in range(len(item_set_2)):
        mi = list(itertools.combinations(set(item_set_2[i]), k))  # combination으로 n-1개의 부분 집합 생성
        sub_set = []
        cnt = 0
        for j in range(len(mi)):
            ans = list(mi[j])
            ans.sort()   # 같은 지 비교를 위해 list 형으로 만든 뒤 정렬
            sub_set = ans
            if sub_set in a:
                cnt += 1    
                if cnt == k:   # 모든 부분 집합이 포함 되어있을 때
                    fin.append(item_set_2[i])  # append
    return fin


def count_set(min_sup, data, unique):   # 빈발 횟수를 세는 함수
    item_set = {}
    item_set1 = {}
    new_set = []
    for trans in data:
        for item in unique:
            if set(item).issubset(set(trans)):     # 아이템이 해당 transaction의 부분집합일 때
                item = tuple(item)   # dictionary의 key 값은 변하지 않는 값만 가능 : tuple로 입력 
                if item in item_set:item_set[item] += 1   # dictionary 의 value 증가
                else: item_set[item] = 1  # dictionary key가 없었을 경우 새로 만듦
    for key, value in item_set.items():
        #if value < min_sup:
            #del item_set[key] : 크기가 달라짐
         if value >= min_sup:
           #  new_set.insert(0,key)
             item_set1[key] = value
    new_set = list(map(list,item_set1.keys()))
    new_set.sort()
    return new_set, item_set1
    

def make_new_set(k, item_set):   # (n+1) 개의 아이템 셋을 만드는 함수 
    new_set=[]
    if k == 2:
        new_set = list(itertools.combinations(item_set, k))   # 두 개를 만들 때는 해당하는 모든 아이템들의 두개씩 부분집합 만듦
        new_set.sort()
    else:
        for i in range(len(item_set)):
            for j in range(i+1, len(item_set)):
                a = list(set(item_set[i]) | set(item_set[j]))  # 세 개 이상부터는 한 줄마다 합집합 해서
                a.sort()
                if len(a) == k:   # 개수가 맞을 시
                    new_set.append(a)  # append
        new_set = sorted(set(map(tuple, new_set)))
    return new_set

def print_txt(item_dic, role):    # 파일을 적는 함수 
    with open(filename_out,role) as f:# 쓸 파일을 염
        for key, value in item_dic.items():   # dictionary를 형식에 맞게 적음
            key = ' '.join(key).replace('\r\n',' ')
            f.write(str(key))   # write은 str만 가능하기 때문에 다 str형으로 바꿔줌
            f.write(' ')
            f.write('(')
            f.write(str(value))
            f.write(')')
            f.write('\n')

# 입력 받은 값 각자 넣어주

min_sup = int(sys.argv[1])   # 외부함수로 받아오기  : 두 번째 값은 min_sup  ( 첫 번째는 코드 이름 )
k = int(sys.argv[2])  # 두 번째는 k
filename = sys.argv[3]    # 세 번째는 열 파일 경로와 이름
filename_out = sys.argv[4]   # 네 번째는 생성할 파일 경로와 이름
 
f = open(filename, 'rt')   # 열어야할 파일을 열어서
readfiles = f.read()
readlines = readfiles.splitlines()
data = [line.split(" ") for line in readlines]   # 줄 별로 받음
data1 = readfiles.split()  # unique 함수를 위해 각각도 찢어줌
f.close


# ITEM 셋들이 하나씩만 가지고 있는 unique 한 list 생성
A = list(set(data1))   # set의 성질을 이용해 하나씩만 포함하는 list 생성
A.sort()  # 정렬

uniqueLength = A.__len__()
item_set1 = []
for i in range(0, uniqueLength):
	item_set1.append(A[i:i+1])   # 각각 하나씩 한 구역을 차지하도록 재정렬
del data1, i, readfiles, readlines,  uniqueLength, f, A # 쓸모 없는 변수들 제거 
[item_set, item_dic] = count_set(min_sup, data, item_set1)   # 첫 번째 item set의 dictionary 생성
a = []
for x in range(len(item_set)):
    a.append(item_set[x][0])   # item set을 list 형태로 만들어줌
if k == 1:   # 첫 번째는 새로 만들어 열어야 하므로 role은  w
    print_txt(item_dic,'w+')

 

i=2
while(len(a) > 2):  
    item_set_2 = make_new_set(i,a)  # 새로운 item set을 만들어줌
    if i>=3:  # 2일 때는 어차피 가지치기를 할 필요가 없으므로 3부터 prunning
        item_set_2 = prunning(i-1, item_set_2, a)  # 새로 생성된 item set에 대하여 prunning 실행
    [a, item_dic] = count_set(min_sup, data, item_set_2)  # prunning 된 item set에 대하여 sup 세고 min_sup보다 낮을 경우 다시 가지치기
    if i == k:   # 첫 번째는 새로 만들어 열어야 하므로 role은  w
        print_txt(item_dic,'w+')
    elif i > k:  # 그 다음은 밑에 추가하므로 role은 a+
        print_txt(item_dic,'a+')
    i+=1