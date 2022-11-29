

def Dropbox_MakeFilesFolderList(response):
    arr = []
    for file in response.entries:
        arr.append(file.name)
    return arr

def RemoveSourceFromAddress(source,localpath):
   addr = localpath.split("/")
   sourceaddr = source.split("/")
   cleanaddr = []
   for i in range(len(addr)):
      try:
          if sourceaddr[i] != addr[i]:
              cleanaddr.append(addr[i])
      except:
          cleanaddr.append(addr[i])       
   return cleanaddr
