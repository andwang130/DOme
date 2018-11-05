import os,shutil
import re
A=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
def fenzu():
     mkdir_path=os.getcwd()
     print(mkdir_path)
     path=os.getcwd().split('\\')[-1]
     root =os.walk("./")
     files=[]
     num_list=[]
     for i in root:
         print(i)
         files=i[2]
         break
     long_path="名字超过长度"
     if not os.path.exists(long_path):
         os.makedirs(long_path)
     for i in files:
         old_name=i;
         if len(i)>30:
             phone=re.findall("(\d{1,5}-\d{1,8})&",i)
             if not phone:
                 phone = re.findall("(\d{3,11})&", i)
             if phone:
                 i=i.replace(phone[0]+"&","")
             if(len(i)>30):
                shutil.move(mkdir_path + "\\" +old_name, mkdir_path + "\\" + long_path + "\\" + i)
             else:
                 shutil.move(mkdir_path + "\\" + old_name, mkdir_path + "\\" + i)
     root = os.walk("./")
     for i in root:
         files = i[2]
         break
     print(files)
     try:
        files.remove("fenzu.py")
     except:
        files.remove("fenzu.exe")
     if len(files)<95:
         return
     if (len(files)%95)>0:
         num=int(len(files)/95)-1
         num_list+=[95 for i in range(0,num)]
         new_num=len(files)-(num*95)
         num_list.append(int(new_num/2))
         num_list.append(new_num-int(new_num/2))
     else:
         num = int(len(files) / 95)
         num_list += [95 for i in range(0, num)]
     strat=0
     flage=0
     for i in num_list:
         fpath=path+A[flage]
         if not os.path.exists(fpath):
             os.makedirs(fpath)
         for x in range(0,i):
             shutil.move(mkdir_path+"\\"+files[strat+x],mkdir_path+"\\"+fpath+"\\"+files[strat+x])
         flage+=1
         strat+=i
fenzu()