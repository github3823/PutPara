# coding:utf-8
#[\u4e00-\u9fa5]正则中文范围
import re
import os
from tkinter import *
from tkinter.filedialog import askopenfilename
import subprocess
import base64
from title import img
root = Tk()
root.title('LOL打包参数生成工具v1.0')#窗口标题
root.resizable(False,False)#固定窗口大小
tmp = open("tmp.ico","wb+")
tmp.write(base64.b64decode(img))#解码图片
tmp.close()
root.iconbitmap(r'tmp.ico')#左上角图标
os.remove("tmp.ico")
frame=Frame(root)#创建框架
frame.pack(padx = 5,pady = 2)#框架填充xy
v=''
v2=StringVar()#定义entry变量值
def label():
    Label(frame, text='                                 ').grid(row=4, column=0, sticky=W)
    Label(frame, text='                                 ').grid(row=5, column=0, sticky=W)
    Label(frame, text='                                        ').grid(row=6, column=0, sticky=W)
def cleartextgetv(str):
    text.delete(0.0, END)  # 清空text
    text.insert(INSERT, str)  # 插入文本

def ishan(text):
    r = re.compile('[\u4e00-\u9fa5]')
    return r.search(text)
def GetList(f):
    List = []
    for i in f:
        if not i == '\n' and ''.join(i).split():
            List.append(i.strip())
    return List
def GetVer(List):
    Version=['-o','','-n','']
    v=0
    r=re.compile(r'(\d).(\d).(\d).(\d)')#只匹配括号内内容，不匹配‘.’
    for i in List:
        if r.search(i):
            Version[1+v]=''.join(list(r.findall(i)[0]))
            v=v+2
    return ' '.join(Version)
def GetPara(List):
    #[print(i) for i in List]
    r=re.compile(r'将(\w+)下')
    Para=[]
    p = len(List)
    for n,i in enumerate(List):
        head = "/"
        bb = ''
        if r.match(i) and not '根目录' in r.findall(i) and  not 'TCLS' in r.findall(i) :
            bb=''.join(r.findall(i))+head
           # bb=''.join(head)
            #print(bb)
        if i[-1]=='包' and  not 'TCLS' in r.findall(i) and  'TCLS' not in i:
           v = 0
           while(1):
             #print(List[0])
             if n+v+1 >= p:
                 break
             if ishan(''.join(List[n+v+1])):
                 v=v+1
                 continue
             if List[n+v+1][-1] == '包' :
                 #print(List[n+v+1])
                 break
             else:
                 Para.append(bb+List[n+v+1])
                 v=v+1
    p = re.compile(r'\w+\.\w{3}$')
    for x in Para:
        if not p.search(x) or ishan(List[-1]):
            return ''
    return ','.join(Para)
def FUllurl(List):
    v = ''
    label()
    for i in List:
        if '是否需要制作完整包下载链接（会员下载器） 是' in i:
            Label(frame, text='需要制作完整包').grid(row=4, column=0,sticky=W)
        if '是否需要制作手动补丁包                   是' in i:
            Label(frame, text='需要制作手整包').grid(row=5, column=0,sticky=W)
    for y in List:
        if '是否有TCLS更新                           是' in y and 'TCLS\mmog_data.xml' in List[-1]:
            Label(frame, text='建单去掉删除安全文件步骤').grid(row=6, column=0,sticky=W)
            return GetVer(List)
        elif '是否有TCLS更新                           否' in y and 'TCLS\mmog_data.xml' in List[-1]:
            Label(frame, text='建单去掉删TCLScopy').grid(row=6, column=0,sticky=W)
            return GetVer(List) +' -d '+'\''+ GetPara(List)+'TCLS/mmog_data.xml'+'\''
        elif '是否有TCLS更新                           是' in y and not GetPara(List)=='':
            return GetVer(List)+' -d '+'\''+GetPara(List)+'\''
        elif '是否有TCLS更新                           否' in y and not GetPara(List)=='':
            Label(frame, text='建单去掉删TCLScopy').grid(row=6, column=0,sticky=W)
            return GetVer(List)+' -d '+'\''+GetPara(List)+','+'TCLS/mmog_data.xml'+'\''

    return '我是大王'


## def getv(v):#过滤掉汉字
#
#             b = 0
#             c = ''
#             while (1):
#                 if not ishan(v[b]):
#                     # print(aa[b])
#                     c = c + v[b]
#
#                 if b > len(v) - 2:
#                     break
#                 b = b + 1
#             return c
def selectPath():
    def call():
        def copy2clip(txt):
            cmd = 'echo ' + txt.strip() + ' | clip'
            return subprocess.check_call(cmd, shell=True)
        copy2clip(v)
    fname = askopenfilename(filetypes=(("Text files", "*.txt"),('All Files','*.*')))
    v2.set(fname)
    r=re.compile(r'\w+\.txt$')
    if fname=='' or not r.search(fname):
        label()
        cleartextgetv('请选择正确的文本文件')
        return False
    with open(fname, 'r') as f:  # r'C:\Users\gg475\Desktop\正式服3221版本确认信息.txt'
            List = GetList(f.readlines())
        

    v = FUllurl(List)
    CheckVer = re.compile(r'\-\w\s\d{4}\s\-\w\s\d{4}')
    if not CheckVer.search(v) :
        label()
        cleartextgetv('参数有误请确认')
        Button(frame, text='复制', state=DISABLED).grid(row=6, column=1, sticky=W)
    else:
        cleartextgetv(v)
        Button(frame, text='复制', command=call).grid(row=6, column=1)



#testCMD=root.register(test)#需要将函数包装一下，必要的

'''l1=Label(frame,text='打包版本号（纯数字，字母无效）').grid(row=0,column=0)
e1=Entry(frame,textvariable=v1,
         validate='key',#当validate为key的时候，获取输入框内容就不可以用get（），发生任何变动的时候，就会调用validatecommand
         validatecommand=(testCMD,'%P'))#因为只有当validatecommand判断正确后，返回true。才会改变.get()返回的值.所以要用%P
e1.grid(row=0,column=1,pady=10)
Button(frame,text='确认',command=call).grid(row=0,column=2)'''
Label(frame, text='').grid(row=0, column=0)
Button(frame,text='选择版本确认信息文件',command=selectPath,width='20').grid(row=1,column=0,sticky=W)
Label(frame,text='请选择文本文件，如果输出为空，请确认文件类型。\n文本最后一行为中文返回参数错误，请修改！').grid(row=0,column=0,sticky=W)
Entry(frame,textvariable=v2,validate='key',state='readonly',width=45).grid(row=2,column=0,pady=5,sticky=W)#validatecommand=(testCMD,'%P'),
text = Text(frame,width=45, height=10)
text.grid(row=3,column=0,pady=10,columnspan=4,sticky=W)
Label(frame, text='').grid(row=4, column=0,sticky=E)
Label(frame, text='').grid(row=5, column=0,sticky=E)
Label(frame, text='').grid(row=6, column=0,sticky=E)
Button(frame,text='复制',state=DISABLED).grid(row=6,column=1,sticky=W)


root.mainloop()

