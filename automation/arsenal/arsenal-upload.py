import dropbox
import json
import os

configfolder = '/etc/arsenal'
configfile = '/etc/arsenal/config.json'

if not os.path.exists(configfolder):
    os.makedirs(configfolder)

if not os.path.exists(configfile):
    f = open(configfile, "a")
    f.write("[]")
    f.close()



def GetWholeDropboxList(dbx, appname):
    print("Getting")
    newpath = "/"+appname
    entries = []
    response = dbx.files_list_folder(path=newpath,recursive=True)
    entries.extend(response.entries)
    Left = response.has_more
    Cursor = response.cursor
    while Left:
        result = dbx.files_list_folder_continue(Cursor)
        Left = result.has_more
        Cursor = result.cursor
        entries.extend(result.entries)
    print(len(entries))
    return entries
    

def Dropbox_Upload_Whole_Live_Folder(path, appname): 
    dbd = '/' + appname
    for root, dirs, files in os.walk(path):
        for filename in files:
            local_path = os.path.join(root, filename)
            relative_path = os.path.relpath(local_path, path)
            dropbox_path = os.path.join(dbd, relative_path)
            with open(local_path, 'rb') as f:
               print("Real Link " + local_path)
               print("Dropbox Link " + dropbox_path)
               dbx.files_upload(open(local_path, "rb").read(), dropbox_path)

def RemoveSourceFromAddress(source,addr):
   sourceaddr = source.split("/")
   cleanaddr = []
   for i in range(len(addr)):
      try:
          if sourceaddr[i] != addr[i]:
              cleanaddr.append(addr[i])
      except:
          cleanaddr.append(addr[i])       
   return cleanaddr

def CompareMissingFiles(local,remote):
  localfilelist = []
  for localfile in local:
    addr = "/".join(localfile)
    localfilelist.append(addr)
  #print(localfilelist)
  remotefilelist = []
  for remotefile in remote:
    addr = "/".join(remotefile)
    remotefilelist.append(addr)
  #print(remotefilelist)
  
  missingfiles = []
  for localfile in localfilelist:
      for remotefile in remotefilelist:
           #print("Checking if " + localfile + " is " + remotefile)
           if remotefile == localfile:
              print("Existing " + localfile)
              break            
      else:
          print("Missing " + localfile)
          #return missingfiles
          missingfiles.append(localfile)
          
  print("Missing Files")
  for fim in missingfiles:
    #print(fim)
    pass
  return missingfiles        


def UploadToDropboxList(missingfiles,appname,source):
   print("Going to Upload")
   #print(missingfiles)
   for addr in missingfiles:
       #print(addr)
       localpath = os.path.join(source,addr)
       #print(localpath)
       dbd = '/' + appname
       dropbox_path = os.path.join(dbd, addr)
       with open(localpath, 'rb') as f:
               #print("Real Link " + localpath)
               #print("Dropbox Link " + dropbox_path)
               #dbx.files_upload(open(local_path, "rb").read(), dropbox_path)
               pass




dbx = dropbox.Dropbox("un4M5SV-S6oAAAAAAAAAAf4uaRk4usNoEuOAx0hPTR5kOB2ZYr_UN9KKS6v9ble1")
dbxapps = []
response = dbx.files_list_folder(path="")
# recursive=True
for file in response.entries:
    dbxapps.append(file.name)


print("Apps on Dropbox")
for app in dbxapps:
   print("--" + app)


obj = open(configfile)
data = json.load(obj)




for conns in data:
  print("Outward Syncing Connections")
  print("App Name  :  " + conns["appname"])
  print("Source Location : " + conns["source"])
  destinations  = conns["destination"]
  print("Destinations : ")
  for dest in destinations:
      print("----" + dest["cloud"])
      if dest["cloud"] == "Dropbox":
          print("Checking Dropbox  Checking files Recursive")
          if conns["appname"] in dbxapps:
              entries = GetWholeDropboxList(dbx, conns["appname"])
              dpxfiles = []
              for file in entries:
                  #print(file.path_display)
                  path = file.path_display
                  addr = path.split("/")
                  for a in addr:
                     #print(a)
                     pass
                  addr.pop(0)
                  addr.pop(0)
                  if file.__class__.__name__ == "FileMetadata":
                     dpxfiles.append(addr)
              #dpxfiles.pop(0)
              #print(dpxfiles)
              locallist = []
              for root, dirs, files in os.walk(conns["source"]):
                 for filename in files:
                     local_path = os.path.join(root, filename)
                     addr = local_path.split("/")
                     addr = RemoveSourceFromAddress(conns["source"], addr)
                     locallist.append(addr)
              #print(locallist)
              missingf = CompareMissingFiles(locallist,dpxfiles)
              UploadToDropboxList(missingf,conns["appname"],conns["source"])
          else:
              print("App not found - Creating App")
              Dropbox_Upload_Whole_Live_Folder(conns["source"], conns["appname"])
      

