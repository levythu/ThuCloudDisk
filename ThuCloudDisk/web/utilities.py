def sanitize(original, sep="/"):
    lists=original.split(sep)
    laStack=[]
    for elem in lists:
        if elem=="" or elem==".":
            continue
        if elem=="..":
            if len(laStack)>0:
                laStack.pop()
        else:
            laStack.append(elem)
    res=""
    if original.startswith(sep):
        res=res+sep
    res=res+sep.join(laStack)
    if original.endswith(sep) and not (original.startswith(sep) and len(laStack)==0):
        res=res+sep

    return res

def setClear(original, sep="/"):
    if original==sep:
        return ""
    return original

if __name__ == '__main__':
    print sanitize("")
    print sanitize("/")
    print sanitize("//")
    print sanitize("//asd/d")
    print sanitize("asd/ds/")
    print sanitize("asd/ds/asd")
    print sanitize("asd/ds/.././asd")
    print sanitize("/../../.././asd/")
    print sanitize("/..///addr/.././asd")
