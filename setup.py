import os; import os.path as osp

for i in range(1,26):
    fname = 'day' + format(i,'02')
    if not osp.exists(fname):
        os.makedirs(fname)
        os.chdir(fname)
        open('input.txt','w').close()
        os.chdir('../')
