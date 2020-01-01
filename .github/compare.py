import os,sys, glob, errno
import pandas as pd

def diffCsv():
    info=""
    for file in sorted(glob.glob('*.csv')):
        info=info+"\n----------------------------------"
        info=info+"\nFILE %s" % file
        info=info+"\nSize %s" % os.stat(file).st_size
        data=pd.read_csv(file)
        info=info+"\nShape %s" % str(data.shape)
        info=info+"\nColumns %s" % data.dtypes
    return info

##main##
pull_branches=[sys.argv[1],sys.argv[2]]

f=dict()
i=1
os.system("git checkout master > /dev/null 2>&1")
for fileName in [".internal/SourceInfo.txt",".internal/DestinInfo.txt"]:
    if not os.path.exists(os.path.dirname(fileName)):
        try:
            os.makedirs(os.path.dirname(fileName))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    f[i]= open(fileName,"w+")
    i=i+1
i=1
for branch in pull_branches:
    os.system("git checkout {0} > /dev/null 2>&1".format(branch))
    info=diffCsv()
    os.system("git checkout master > /dev/null 2>&1")
    f[i].write(info)
    f[i].close()
    i=i+1

os.system("git checkout master > /dev/null 2>&1")
os.system("diff -u .internal/SourceInfo.txt .internal/DestinInfo.txt")


    
