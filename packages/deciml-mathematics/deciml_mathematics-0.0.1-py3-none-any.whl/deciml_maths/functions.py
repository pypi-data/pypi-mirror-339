import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from deciml.deciml import deciml, algbra as alg, galgbra as galg, Decimal, getpr
from terminate import retrn


class axn:
    
    def __init__(self,__f1:Decimal,__f2:Decimal,__pr=getpr())->None:
        self.__f=tuple(map(deciml,(__f1,__f2)));self.__df=(alg.mul(*self.__f,pr=__pr),alg.sub(self.__f[1],'1',pr=__pr));del __f1,__f2,__pr;
        self.f=lambda __a,__pr=getpr():alg.mul(self.__f[0],alg.pwr(__a,self.__f[1],__pr),pr=__pr)
        self.df=lambda __a,__pr=getpr():alg.mul(self.__df[0],alg.pwr(__a,self.__df[1],__pr),pr=__pr)

    def getf(self)->tuple[Decimal,Decimal]:return self.__f;

    def getdf(self)->tuple[Decimal,Decimal]:return self.__df;

class poly:
    
    def __init__(self,*__f:tuple[Decimal,Decimal]|list,pr=getpr())->None:
        self.__f=tuple(map(lambda x:axn(*x,pr),__f));del __f,pr;
        self.f=lambda __a,__pr=getpr():alg.add(*map(lambda i:i.f(__a,__pr),self.__f),pr=__pr)
        self.df=lambda __a,__pr=getpr():alg.add(*map(lambda i:i.df(__a,__pr),self.__f),pr=__pr)

    def getf(self)->tuple[tuple[Decimal,Decimal],...]:return tuple(map(lambda i:i.getf(),self.__f));

    def getdf(self)->tuple[tuple[Decimal,Decimal],...]:return tuple(map(lambda i:i.getdf(),self.__f));

class apolyn:
    
    def __init__(self,__a:Decimal,__n:Decimal,*__f:tuple[Decimal,Decimal]|list,pr=getpr())->None:
        self.__an=axn(__a,__n,pr);self.__f=poly(*__f,pr=pr);del __a,__n,__f,pr;
        self.f=lambda __a,__pr=getpr():self.__an.f(self.__f.f(__a,__pr),__pr)
        self.df=lambda __a,__pr=getpr():alg.mul(self.__an.df(self.__f.f(__a,__pr),__pr),self.__f.df(__a,__pr),pr=__pr)

    def getf(self)->tuple[tuple[Decimal,Decimal],tuple[tuple[Decimal,Decimal],...]]:return self.__an.getf(),self.__f.getf();

    def getdf(self)->tuple[tuple[Decimal,Decimal],tuple[tuple[Decimal,Decimal],...],tuple[tuple[Decimal,Decimal],...]]:return self.__an.getdf(),self.__f.getf(),self.__f.getdf();

class funcutils:
    
    @staticmethod
    def rearr(__a,__pos:int,__pr=getpr())->apolyn:
            ta = __a.__class__.__name__
            a=__a.getf()
            match ta:
                case 'poly':p=(a:=list(a)).pop(__pos);return apolyn(alg.pwr(alg.div('1',p[0],__pr),(pw:=alg.div('1',p[1],__pr)),__pr),pw,*a,pr=__pr);
                case _:return None;
    @staticmethod
    def ndpoly(p: poly,n: int) -> poly | None:
        try:
            for _ in range(n):
                p = poly(*p.getdf())
                if p is None:return None;
            return p
        except Exception as e:print("Invalid command: funcutils.ndpoly()");retrn('c',e);


# a=poly((2,3),(1,-2))
# print(a.f(1),a.df(1),a.getdf())
# a=apolyn(2,1,(1,2),(2,1))
# print([a.f(1),a.df(1)],a.getf())
# print(a.getdf())
