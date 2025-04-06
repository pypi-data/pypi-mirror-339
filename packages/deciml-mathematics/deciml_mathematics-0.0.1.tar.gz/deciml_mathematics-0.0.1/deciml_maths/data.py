from matrix import matx, matutils, melutils
from deciml.deciml import deciml, Decimal
from compare.cmpr import tmatx, eqval, tdata, tint, tdeciml
from terminate import retrn

class data:
    
    def __init__(self,x,y,chk=True,ret='a')->None:
        try:
            def __dataxy(x,y,chk: bool)->matx:
                def __xcheck(x)->tuple:
                    if (xt:=x.__class__.__name__)=='tuple' or xt=='list':
                        del xt
                        if x[0].__class__.__name__=='matx':return matutils.matxtolx(x,True,'c');
                        else:return matx(x,True,'c');
                    return matx(x,True,'c')
                def __ycheck(y)->tuple:
                    if (yt:=y.__class__.__name__)=='tuple' or yt=='list':
                        if (y1:=y[0].__class__.__name__)=='int' or y1=='float' or y1=='Decimal':return tdeciml.dall(y);
                        elif y1=='matx':return tuple(zip(*matutils.matxtolx(y,True,'c').matx));
                        elif y1=='tuple' or y1=='list':return tdeciml.dall(tuple(zip(*y)));
                        else:return None;
                    if yt=='matx':
                        if y.collen==1:return y.matx;
                        elif y.rowlen==1:return tuple(zip(*y));
                        else:return None;
                match chk:
                    case True:
                        x=__xcheck(x)
                        if x is None:raise Exception("Invalid argument: x");
                        y=__ycheck(y)
                        if y is None:raise Exception("Invalid argument: y");
                    case False:pass;
                    case _:raise Exception;
                return (x,y),x.collen,x.rowlen
            if (ndata:=__dataxy(x,y,chk)) is not None:self.__data,self.__datalen,self.__xvars=ndata;del ndata;
            else:raise Exception;
        except Exception as e:print("Invalid command: data()");retrn(ret,e);

    @property
    def data(self)->tuple[matx,tuple[Decimal,...]]:return (self.getax(),self.getay());
    
    @property
    def datalen(self)->int:return self.__datalen;
    
    @property
    def xvars(self)->int:return self.__xvars;

    # prints the data
    @data.getter
    def pdata(self)->None:
        x=self.__data[0].matx;y=self.__data[1];
        for i in range(self.datalen):print(str(i)+": "+str([str(j) for j in x[i]])[1:-1]+" | "+str(str(y[i])));
        print("\n")

    # returns all x
    def getax(self)->matx:return matx(self.__data[0].matx,False,'c');

    # returns all y
    def getay(self)->matx:return self.__data[1];

    # returns x values from data
    def getx(self,li,chk=True,ret='a') -> matx:
        try:return matutils.gele(self.__data[0],li,True,chk,'c');
        except Exception as e:print("Invalid command: data.getx()");retrn(ret,e);

    # returns y values from data
    def gety(self,li,chk=True,ret='a')->tuple[Decimal,...]:
        try:
            match chk:
                case False:return tuple([self.__data[1][i] for i in li]);
                case True:
                    if (li:=tint.ele(li,self.__datalen)) is None:raise Exception;
                    return tuple([self.__data[1][i] for i in li])
                case _:raise Exception("Invalid argument: chk => bool")
        except Exception as e:print("Invalid command: data.gety()");retrn(ret,e);

    # returns data values from data
    def getd(self,li:list,chk=True,ret='a')->tuple[matx,tuple[Decimal,...]]:
        try:
            match chk:
                case False:return tuple([matutils.gele(self.__data[0],li,True,False,'c'),tuple([self.__data[1][i] for i in li])]);
                case True:
                    if (li:=tint.ele(li,self.__datalen)) is None:raise Exception;
                    return tuple([matutils.gele(self.__data[0],li,True,False,'c'),tuple([self.__data[1][i] for i in li])]);
                case _:raise Exception("Invalid argument: chk => bool")
        except Exception as e:print("Invalid command: data.getd()");retrn(ret,e);

    # return listed x
    def getlx(self,li:list,chk=True,ret='a')->matx:
        try:return matutils.tpose(matutils.gele(self.__data[0],li,False,chk,'c'),False,'c');
        except Exception as e:print("Invalid command: data.getlx()");retrn(ret,e);


class datautils:
    
    @staticmethod
    def dataval(d:data,x:Decimal,chk=True,ret='a')->data:
        try:
            match chk:
                case False:return data(matutils.maddval(d.getax(),x,False,'c'),d.getay(),False,'c');
                case True:
                    if tdata(d) is None:raise Exception;
                    if str(x:=deciml(x))=='NaN':raise Exception;
                    return data(matutils.maddval(d.getax(),x,False,'c'),d.getay(),False,'c');
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: datautils.dataval()");retrn(ret,e);

    # add the listed x to data
    @staticmethod
    def addata(d:data,*a:matx,chk=True,ret='a')->data:
        try:
            match chk:
                case False:return data(matutils.addmatx(d.getax(),*a,r=False,chk=False,ret='c'),d.getay(),False,'c');
                case True:
                    if tdata(d) is None or tmatx(a,True) is None:raise Exception;
                    for i in a:
                        if eqval(d.datalen,i.collen) is None:raise Exception;
                    return data(matutils.addmatx(d.getax(),*a,r=False,chk=False,ret='c'),d.getay(),False,'c')
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: datautils.addata()");retrn(ret,e);

    # retuns a new data object with x of listed positions
    @staticmethod
    def datalx(d:data,li:list,chk=True,ret='a')->data:
        try:
            match chk:
                case False:return data(d.getlx(li,False,'c'),d.getay(),False,'c');
                case True:
                    if tdata(d) is None:raise Exception;
                    return data(d.getlx(li,True,'c'),d.getay(),False,'c')
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: datautils.datalx()");retrn(ret,e);

    # add multiplication of x at listed positions to data
    @staticmethod
    def multlx(d:data,li:list[list]|str,chk=True,ret='a')->data:
        try:
            match chk:
                case False:return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.mult(d.getax(),li,False,False,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c');
                case True:
                    if tdata(d) is None:raise Exception;
                    return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.mult(d.getax(),li,False,True,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c')
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: datautils.multlx()");retrn(ret,e);

    # add addition of x at listed positions to data
    @staticmethod
    def addlx(d:data,li:list[list]|str,chk=True,ret='a')->data:
        try:
            match chk:
                case False:return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.add(d.getax(),li,False,False,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c');
                case True:
                    if tdata(d) is None:raise Exception;
                    return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.add(d.getax(),li,False,True,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c')
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: datautils.addlx()");retrn(ret,e);

    # add powers of x at listed positions to data
    @staticmethod
    def powlx(d:data,an:list[Decimal]|str,li:list|str,chk=True,ret='a')->data:
        try:
            match chk:
                case False:return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.pow(an,d.getax(),li,False,False,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c');
                case True:
                    if tdata(d) is None:raise Exception;
                    return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.pow(an,d.getax(),li,False,True,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c')
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: datautils.powlx()");retrn(ret,e);

    # append log of x at listed positions to data
    @staticmethod
    def loglx(d:data,an:list[Decimal],li:list|str,chk=True,ret='a')->data:
        try:
            match chk:
                case False:return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.log(an,d.getax(),li,False,False,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c');
                case True:
                    if tdata(d) is None:raise Exception;
                    return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.log(an,d.getax(),li,False,True,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c')
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: datautils.loglx()");retrn(ret,e);

    # append x at listed positions as a power to data
    @staticmethod
    def expolx(d:data,an:list[Decimal],li:list|str,chk=True,ret='a')->data:
        try:
            match chk:
                case False:return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.expo(an,d.getax(),li,False,False,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c');
                case True:
                    if tdata(d) is None:raise Exception;
                    return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.expo(an,d.getax(),li,False,True,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c')
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: datautils.expolx()");retrn(ret,e);
    
    @staticmethod
    def triglx(d:data,n:Decimal,li:list|str,f='cos',chk=True,ret='a')->data:
        try:
            match chk:
                case False:return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.trig(n,d.getax(),li,False,f,False,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c');
                case True:
                    if tdata(d) is None:raise Exception;
                    return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.trig(n,d.getax(),li,False,f,True,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c')
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: datautils.triglx()");retrn(ret,e);
 

a = [[1,2,2],[2,3,4],[7.9999999,3,2]]
b = [3,]
c = [2, ]
y = data(a, [2, 3, 4])
y.pdata
y.getax().pmatx
print(y.getay())
y = datautils.dataval(y, deciml('1.0'))
y.pdata
z = y.getlx([1, 0])
q = datautils.addata(y, z)
q.pdata
y = datautils.powlx(y, [1, 2], [1, 0])
y.pdata
y = datautils.multlx(y, [[1, 0], ])
y.pdata
y = datautils.addlx(y, [[0, 4], ])
y.pdata
y = datautils.loglx(y, [1, 10], [5, 6])
y.pdata
y = datautils.expolx(y, [2, 1], [1, 8])
y = datautils.triglx(y, 1, [1, 8])
n = datautils.datalx(y, [7, 8, 10])
y.pdata
n.pdata
