

def FindLatest(arr):
    newarr = []
    for a in arr:
        try:
            newarr.append(int(a))
        except:
            pass
    sorted_list = sorted(newarr, reverse=True , key=int)
    return str(sorted_list[0])

