def finder_volv(data):
    '''
    find volv generator
    '''
    curr = 0
    last = len(data)
    while curr < last:
        if data[curr] in 'ёуеыаоэяию':
            yield curr
        curr += 1
    yield curr

def finder_cons(data):
    '''
    find cons generator
    '''
    curr = 0
    last = len(data)
    while curr < last:
        if data[curr] in 'йцкнгшщзхфвпрлджчсмтб':
            yield curr
        curr += 1
    yield curr


def sp_max(data:str)->list[str]:
    volves = finder_volv(data)
    res = list()
    start = 0
    middle = next(volves)
    i = 0
    for end in volves:
        res.append(data[start:end])
        i += 1
        start = middle + 1
        middle = end
    return res

def combinations(data:str):
    data = data.lower()
    pos_vol = list(finder_volv(data))[:-1]
    pos_cons = list(finder_cons(data))[:-1]

    n = len(pos_cons)
    poses = {i: [i] for i in range(n)}
    indexes = []

    tmp_cons = list(poses.keys())
    cons_num = 2 ** len(tmp_cons)
    for i in range(cons_num):
        tmp = bin(cons_num + i)[2:]
        if tmp.count('1') == 3:
            indexes.append([])
            for j in range(1, len(tmp)):
                if tmp[j] == '1':
                    indexes[-1].append(tmp_cons[j - 1])
    res = []
    for tmp in indexes:
        tmp = [pos_cons[j] for x in tmp for j in poses[x]] + pos_vol
        tmp.sort()
        if len({data[i] for i in tmp}) < 3:
            continue
        res.append(''.join(data[i] for i in tmp))
    return res


def get_comb(data:str):
    res = []
    for x in sp_max(data):
        res.extend(combinations(x))
    return res

