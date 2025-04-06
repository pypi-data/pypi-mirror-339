from deciml.deciml import algbra as alg, galgbra as galg, trig, htrig, Decimal
from compare.cmpr import tmatx, eqval, tdeciml, eqllen, tint
from terminate import retrn

class matx:
    
    def __init__(self,li:list|tuple,chk=True,ret='a')->None:
        try:
            if (tli:=li.__class__.__name__)=='matx':self.__matx=li.matx;self.__collen=li.collen;self.__rowlen=li.rowlen;self.__sqmatx=li.sqmatx;self.__dnant=None;self.__invse=None;self.__invsednant=None;self.__cofacm=None;self.__adjnt=None;self.__tpose=None;
            else:
                match chk:
                    case True:
                        if tli=='list' or tli=='tuple':
                            if (tli0:=li[0].__class__.__name__)=='tuple' or tli0=='list':
                                if eqllen(li) is None:raise Exception("Invalid argument: li");
                            else:li=li,;
                            if (li:=tdeciml.dall(li)) is None:raise Exception("Invalid argument: li");
                        else:raise Exception("Invalid argument: li => list/tuple/matx");
                    case False:
                        match tli:
                            case 'tuple':
                                if li[0].__class__.__name__=='Decimal':li=li,;
                                elif li[0].__class__.__name__=='tuple':pass;
                                elif li[0].__class__.__name__=='float':li=tdeciml.dall(li),;
                                else:raise Exception("Invalid argument: li");
                            case _:raise Exception("Invalid argument: li => tuple/matx");
                    case _:raise Exception("Invalid argument: chk => bool");
                for i in li:
                    for j in i:
                        if j.__class__.__name__!='Decimal':raise Exception(str(j)+" is not Decimal");
                lc=len(li);lr=len(li[0]);
                if lr==lc:sq=True;
                else:sq=False;
                self.__matx=li;self.__collen=lc;self.__rowlen=lr;self.__sqmatx=sq;self.__dnant=None;self.__invse=None;self.__invsednant=None;self.__cofacm=None;self.__adjnt=None;self.__tpose=None;
        except Exception as e:print("Invalid command: matx()");retrn(ret,e);

    @property
    def matx(self)->tuple:return self.__matx;
    
    @matx.setter
    def matx(self,li:list|tuple)->None:
        try:
            if (tli:=li.__class__.__name__)=='matx':self.__matx=li.matx;self.__collen=li.collen;self.__rowlen=li.rowlen;self.__sqmatx=li.sqmatx;self.__dnant=None;self.__invse=None;self.__invsednant=None;self.__cofacm=None;self.__adjnt=None;self.__tpose=None;
            elif tli=='list' or tli=='tuple':
                if (tli0:=li[0].__class__.__name__)=='tuple' or tli0=='list':
                    if eqllen(li) is None:raise Exception("Invalid argument: li");
                else:li=li,;
                if (li:=tdeciml.dall(li)) is None:raise Exception("Invalid argument: li");
                lc=len(li);lr=len(li[0]);
                if lr==lc:sq=True;
                else:sq=False;
                self.__matx=li;self.__collen=lc;self.__rowlen=lr;self.__sqmatx=sq;self.__dnant=None;self.__invse=None;self.__invsednant=None;self.__cofacm=None;self.__adjnt=None;self.__tpose=None;
            else:raise Exception("Invalid argument: li => list/tuple/matx");
        except Exception as e:print("Invalid command: matx()");retrn('a',e);
    
    @property
    def collen(self)->int:return self.__collen;
    
    @property
    def rowlen(self)->int:return self.__rowlen;
    
    @property
    def sqmatx(self)->bool:return self.__sqmatx;
    
    # prints the value of matx object
    @matx.getter
    def pmatx(self)->None:
        print("matx(")
        for k in [[str(j) for j in i] for i in self.__matx]:print('|'+str(k)[1:-1]+'|');
        print(')\n')
    
    def dnant(self)->Decimal:
        if self.__dnant is None and self.__sqmatx is True:self.__dnant=matutils.dnant(matx(self.__matx,False,'c'),False,'w');return self.__dnant;
        else:return self.__dnant;

    def invsednant(self)->Decimal:
        if self.__invsednant is None and self.__sqmatx is True:self.__invsednant=matutils.invsednant(matx(self.__matx,False,'c'),False,'w');return self.__invsednant;
        else:return self.__invsednant;
    
    def invse(self):
        if self.__invse is None and self.sqmatx is True and self.dnant()!=0:self.__invse=matutils.invse(matx(self.__matx,False,'c'),False,'w');return self.__invse;
        else:return self.__invse;
    
    def adjnt(self):
        if self.__adjnt is None and self.__sqmatx is True:self.__adjnt=matutils.adjnt(matx(self.__matx,False,'c'),False,'w');return self.__adjnt;
        else:return self.__adjnt;

    def tpose(self):
        if self.__tpose is None:self.__tpose=matutils.tpose(matx(self.__matx,False,'c'),False,'w');return self.__tpose;
        else:return self.__tpose;
    
    def cofacm(self):
        if self.__cofacm is None:self.__cofacm=matx(tuple([tuple([matutils.cofac(matx(self.__matx,False,'c'),i,j,False,'c') for j in range(self.__rowlen)]) for i in range(self.__collen)]),False,'w');return self.__cofacm;
        else:return self.__cofacm;

    # returns matx as a list
    def matxl(self)->list:return [list(i) for i in self.__matx];
    
    def pop(self,i:int,r=True,chk=True,ret='a')->tuple[Decimal,...]:
        try:
            match chk:
                case False:pass;
                case True:
                    if (i:=tint.ele(i,self.__collen)) is None:raise Exception;
                case _:raise Exception("Invalid argument: chk => bool");
            match r:
                case True:m=list(self.__matx);p=m.pop(i);self.__matx=tuple(m);self.__collen=self.__collen-1;
                case False:
                    m=self.matxl();p=list();
                    for j in range(self.__collen):p.append(m[j].pop(i));m[j]=tuple(m[j]);
                    self.__matx=tuple(m);self.__rowlen=self.__rowlen-1;
                case _:raise Exception("Invalid argument: r => bool")
            del m
            if self.__collen==self.__rowlen:self.__sqmatx=True;
            else: self.__sqmatx=False;
            return tuple(p)
        except Exception as e:print("Invalid command: matx.pop()");retrn(ret,e);

    # return element at i,j of matrix
    def mele(self,i:int,j:int,chk=True,ret='a')->Decimal:
        try:
            match chk:
                case False:return self.__matx[i][j];
                case True:
                    if (i:=tint.ele(i,self.__collen)) is None or (j:=tint.ele(j,self.__rowlen)) is None:raise Exception;
                    return self.__matx[i][j]
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: matx.mele()");retrn(ret,e);

    # return tuple of i'th row
    def mrow(self,i:int,chk=True,ret='a')->tuple[Decimal,...]:
        try:
            match chk:
                case False:return self.__matx[i];
                case True:
                    if (i:=tint.ele(i,self.__collen)) is None:raise Exception;
                    return self.__matx[i]
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: matx.mrow()");retrn(ret,e);

    # returns tuple of i'th column
    def mcol(self,j:int,chk=True,ret='a')->tuple[Decimal,...]:
        try:
            match chk:
                case False:return tuple([self.__matx[i][j] for i in range(self.__collen)]);
                case True:
                    if (j:=tint.ele(j,self.__rowlen)) is None:raise Exception;
                    return tuple([self.__matx[i][j] for i in range(self.__collen)])
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: matx.mcol()");retrn(ret,e);
    
    def gele(self,a:list|tuple,r=False,chk=True,ret='a')->tuple[tuple[Decimal,...],...]:
        try:
            match chk:
                case False:pass;
                case True:
                    if a is None:raise Exception;
                    match r:
                        case True:a=tint.ele(a,self.__collen);
                        case False:a=tint.ele(a,self.__rowlen);
                        case _:raise Exception("Invalid argument: r => bool");
                case _:raise Exception("Invalid argument: chk => bool");
            match r:
                case True:return tuple([self.__matx[i] for i in a]);
                case False:
                    r=self.__matx[0];r=[[r[i],] for i in a];a=tuple(enumerate(a));
                    for i in self.__matx[1:]:
                        for j in a:r[j[0]].append(i[j[1]]);
                    return tuple([tuple(i) for i in r])
                case _:raise Exception("Invalid argument: r => bool");
        except Exception as e:print("Invalid command: matx.gele()");retrn(ret,e);

class matutils:

    # returns scalar matrix of size nxn
    @staticmethod
    def sclrm(n:int,el:Decimal,chk=True,ret='a')->matx:
        try:
            match chk:
                case False:pass;
                case True:
                    if (n:=tint.intn(n)) is None or str(el:=Decimal(str(el)))=='NaN':raise Exception;
                case _:raise Exception("Invalid argument: chk => bool");
            m=list()
            for i in range(n):
                l1=list()
                for j in range(n):
                    if i==j:l1.append(el);
                    else:l1.append(Decimal('0.0'));
                m.append(tuple(l1))
            return matx(tuple(m),False,'c')
        except Exception as e:print("Invalid command: matutils.sclrm()");retrn(ret,e);

    # returns matrix of size mxn with equal elements
    @staticmethod
    def eqelm(m:int,n:int,i:Decimal,chk=True,ret='a')->matx:
        try:
            match chk:
                case True:return matx(tuple([tuple([i for _ in range(n)]) for _ in range(m)]),False,'c');
                case False:
                    if (n:=tint.intn(n)) is None or (m:=tint.intn(m)) is None or str(i:=Decimal(str(i)))=='NaN':raise Exception;
                    return matx(tuple([tuple([i for _ in range(n)]) for _ in range(m)]),False,'c')
        except Exception as e:print("Invalid command: matutils.eqelm()");retrn(ret,e);

    @staticmethod
    def addmatx(a:matx,*b:matx,r=False,chk=True,ret='a')->matx:
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx((a,)+b,True) is None:raise Exception;
                    match r:
                        case False:
                            for i in b:
                                if eqval(i.collen,a.collen) is None:raise Exception;
                        case True:
                            for i in b:
                                if eqval(i.rowlen,a.rowlen) is None:raise Exception;
                        case _:raise Exception("Invalid argument: r => bool");
                case _:raise Exception("Invalid argument: chk => bool");
            match r:
                case False:
                    a=list(a.matx)
                    for i in b:
                        l=0
                        for j in i.matx:
                            a[l]=a[l]+j;l+=1;
#                     for i in range(a.collen):
#                         r1=a.mrow(i,False,'c')
#                         for k in [j.mrow(i,False,'c') for j in b]:r1+=k;
#                         r.append(r1)
                    return matx(tuple(a),False,'c')
                case True:
                    r=a.matx
                    for i in b:r+=i.matx;
                    return matx(r,False,'c')
                case _:raise Exception("Invalid argument: r => bool");
        except Exception as e:print("Invalid command: matutils.addmatx()");retrn(ret,e);

    @classmethod
    def maddval(cls,a:matx,x:Decimal,chk=True,ret='a')->matx:
        try:
            match chk:
                case False:return cls.addmatx(cls.eqelm(a.collen,1,x,False,'c'),a,r=False,chk=False,ret='c');
                case True:
                    if tmatx(a) is None or str(x:=Decimal(str(x)))=='NaN':raise Exception;
                    return cls.addmatx(cls.eqelm(a.collen,1,x,False,'c'),a,r=False,chk=False,ret='c')
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: matutils.maddval()");retrn(ret,e);

    # convert list x to x
    @staticmethod
    def matlxtox(a:matx,chk=True,ret='a')->tuple:
        try:
            match chk:
                case False:return tuple([matx(i,False,'c') for i in a.matx]);
                case True:
                    if tmatx(a) is None:raise Exception;
                    return tuple([matx(i,False,'c') for i in a.matx])
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: matutils.matlxtox()");retrn(ret,e);

    @staticmethod
    def matxtolx(a:tuple[matx,...]|list,chk=True,ret='a')->matx:
        try:
            x=list()
            match chk:
                case False:return matx(tuple([i.matx[0] for i in a]),False,'c');
                case True:
                    if tmatx(a,True) is None:raise Exception;
                    ar=a[0].rowlen
                    for i in a:
                        if eqval(i.collen,1) is None or eqval(i.rowlen,ar) is None:raise Exception;
                        x.append(i.matx[0])
                    return matx(tuple(x),False,'c')
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: matutils.matxtolx()");retrn(ret,e);

    # returns row or column elements of the matrix
    @staticmethod
    def gele(a:matx,b:list,r=False,chk=True,ret='a')->matx:
        try:return matx(a.gele(b,r,chk,r),False,'c');
        except Exception as e:print("Invalid command: matutils.gele()");retrn(ret,e);

    # returns the transpose of the matrix
    @classmethod
    def tpose(cls,a:matx,chk=True,ret='a')->matx:
        try:
            match chk:
                case False:return matx(tuple(zip(*a.matx)),False,'c');
                case True:
                    if tmatx(a) is None:raise Exception;
                    return matx(tuple(zip(*a.matx)),False,'c')
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: matutils.tpose()");retrn(ret,e);

    # returns the co-factor of the matrix element
    @classmethod
    def cofac(cls,a:matx,b:int,c:int,chk=True,ret='a')->Decimal:
        try:
            match chk:
                case True:
                    if tmatx(a) is None or (b,c:=tint.ele([b,c],a.rowlen)) is None:raise Exception;
                    if a.sqmatx is False:raise Exception("Error: Not a square matrix");
                case False:pass;
                case _:raise Exception("Invalid argument: chk => bool");
            a=matx(a,False,'c');a.pop(c,False,False,'c');a.pop(b,chk=False,ret='c');
            if (p:=alg.div((b+c),2))==int(p):return cls.dnant(a,False,'c');
            else:return alg.mul(-1,cls.dnant(a,False,'c'));
        except Exception as e:print("Invalid command: matutils.cofac()");retrn(ret,e);

    # returns the determinant of the matrix
    @classmethod
    def dnant(cls,a:matx,chk=True,ret='a')->Decimal:
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx(a) is None:raise Exception;
                    if a.sqmatx is False:raise Exception("Error: Not a square matrix");
                case _:raise Exception("Invalid argument: chk => bool");
            a=matx(a,False,'c')
            if (lr:=a.rowlen)==1:return a.mele(0,0,False,'c');
            else:
                ep=None;ele=a.mele(0,0,False,'c');li=a.mrow(0,False,'c');
                if ele==0:
                    for i in range(lr):
                        if i>0:
                            if li[i]!=0:e=li[i];ep=i;
                    if ep is None:return Decimal('0');
                else:ep=0;e=ele;
                for i in range(lr):
                    if i!=ep:ele=li[i];fac=alg.div(alg.mul(-1,ele),e);a.matx=cls.tform(a,i,ep,fac,False,False,'c');
                return alg.mul(e,cls.cofac(a,0,ep,False,'c'))
        except Exception as e:print("Invalid command: matutils.dnant()");retrn(ret,e);

    # returns adjoint matrix of the matrix
    @classmethod
    def adjnt(cls,a:matx,chk=True,ret='a')->matx:
        try:
            match chk:
                case False:return matx(tuple([tuple([cls.cofac(a,j,i,False,'c') for j in range(a.collen)]) for i in range(a.rowlen)]),False,'c');
                case True:
                    if tmatx(a) is None:raise Exception;
                    if a.sqmatx is False:raise Exception("Error: Not a square matrix");
                    return matx(tuple([tuple([cls.cofac(a,j,i,False,'c') for j in range(a.collen)]) for i in range(a.rowlen)]),False,'c')
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: matutils.adjnt()");retrn(ret,e);

    # returns inverse matrix of the matrix
    @classmethod
    def invse(cls,a:matx,chk=True,ret='a')->matx:
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx(a) is None:raise Exception;
                case _:raise Exception("Invalid argument: chk => bool");
            if (det:=cls.dnant(a,False,'c')) is None:raise Exception;
            if det==0:raise Exception("Error: Determinant is 0,\nInverse DNE!");
            return cls.smult(alg.div(1,det),cls.adjnt(a,False,'c'),chk=False,ret='c')
        except Exception as e:print("Invalid command: matutils.invse()");retrn(ret,e);

    # returns inverse matrix of the matrix using matrix transformation
    @classmethod
    def invsednant(cls,a:matx,chk=True,ret='a')->Decimal:
        try:
            match chk:
                case True:
                    if tmatx(a) is None:raise Exception;
                case False:pass;
                case _:raise Exception("Invalid argument: chk => bool");
            a=matx(a,False,'c');det=cls.dnant(a,False,'c');
            if det is None:raise Exception;
            if det==0:raise Exception("Error: Determinant is 0,\nInverse DNE!");
            b=cls.sclrm(a.rowlen,Decimal('1.0'),False,'c')
            l=list()
            for i in range(a.collen):
                ele=a.mele(i,i,False,'c')
                if ele==0:
                    el=0
                    for j in range(i+1,a.rowlen-1):
                        el=a.mele(i,j,False,'c')
                        if el!=0:a.matx=cls.tform(a,i,j,alg.div(1,el),False,False,'c');b.matx=cls.tform(b,i,j,alg.div(el),False,False,'c');break;
                    if el==0:
                        raise Exception("Error: Invalid Matrix Inverse");
                l.append(ele:=a.mele(i,i,False,'c'));row=a.mrow(i,False,'c');col=a.mcol(i,False,'c');
                for j in range(i+1,a.rowlen):
                    el=row[j];e=col[j];a.matx=cls.tform(a,j,i,alg.div(alg.mul(-1,el),ele),False,False,'c');b.matx=cls.tform(b,j,i,alg.div(alg.mul(-1,el),ele),False,False,'c');a.matx=cls.tform(a,j,i,alg.div(alg.mul(-1,e),ele),True,False,'c');b.matx=cls.tform(b,j,i,alg.div(alg.mul(-1,e),ele),True,False,'c');del e;del el;
                del ele
            l=alg.mul(*l)
            if l==0:raise Exception("Error: Invalid Matrix Inverse");
            if l>0:b.matx=cls.smult(alg.pwr(l,alg.div(-1,a.collen)),b,chk=False,ret='c');
            if l<0:b.matx=cls.smult(alg.mul(-1,alg.pwr(alg.mul(-1,l),alg.div(-1,a.collen))),b,chk=False,ret='c');
            return cls.dnant(b,False,'c')
        except Exception as e:print("Invalid command: matutils.invsednant()");retrn(ret,e);

    # returns matrix after row or column tranformation
    @classmethod
    def tform(cls,a:matx,b:int,c:int,d: Decimal,r=False,chk=True,ret='a')->matx:
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx(a) is None or str(d:=Decimal(str(d)))=='NaN':raise Exception;
                case _:raise Exception("Invalid argument: chk => bool");
            if (m:=a.gele([b,c],r,chk,'c')) is None:raise Exception;
            match r:
                case True:
                    a=list(a.matx);a[b]=galg.add(m[0],galg.mulsg(d,m[1]));return matx(tuple(a),False,'c');
                case False:
                    a=list(a.matx)
                    for i in enumerate(galg.add(m[0],galg.mulsg(d,m[1]))):a1=list(a[i[0]]);a1[b]=i[1];a[i[0]]=tuple(a1);
                    return matx(tuple(a),False,'c')
                case _:raise Exception;
        except Exception as e:print("Invalid command: matutils.tform()");retrn(ret,e);

    # returns sum of two matrices
    @staticmethod
    def madd(a:matx,b:matx,sumr=None,chk=True,ret='a')->matx|tuple[Decimal,...]:
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx([a,b],True) is None:raise Exception;
                    if eqval([a.collen,a.rowlen],[b.collen,b.rowlen]) is None:raise Exception;
                case _:raise Exception("Invalid argument: chk => bool");
            r=[galg.add(*i) for i in zip(a.matx,b.matx)];
            match sumr:
                case None:return matx(tuple(r),False,'c');
                case True:return galg.add(*r);
                case False:return tuple([alg.add(*i) for i in r]);
                case _:raise Exception("invalid argument: sumr => None/bool");
        except Exception as e:print("Invalid command: matutils.madd()");retrn(ret,e);
    
    @classmethod
    def saddcnst(cls,a: tuple | list | Decimal,b: matx,r=False,sumr=None,chk=True,ret='a')->matx | tuple[Decimal,...]:
        try:
            match chk:
                case False:pass;
                case True:
                    if r is not None:
                        if (a:=tdeciml.dall(a)) is None:raise Exception;
                    else:
                        if str(a:=Decimal(str(a)))=='NaN':raise Exception;
                    if tmatx(b) is None:raise Exception;
                    match r:
                        case True:
                            if eqval(len(a),b.collen) is None:raise Exception;
                        case False:
                            if eqval(len(a),b.rowlen) is None:raise Exception;
                        case None:pass;
                        case _:raise Exception("Invalid argument: r => bool");
                case _:raise Exception("Invalid argument: chk => bool");
            match r:
                case True:r=[galg.addsg(i[0],i[1]) for i in zip(a,b.matx)];
                case False:r=[galg.add(a,i) for i in b.matx];
                case None:r=[galg.addsg(a,i) for i in b.matx];
                case _:raise Exception("Invalid argument: r => bool/None");
            match sumr:
                case None:return matx(tuple(r),False,'c');
                case True:return galg.add(*r);
                case False:return tuple([alg.add(*i) for i in r]);
                case _:raise Exception("Invalid argument: sumr => None/bool");
        except Exception as e:print("Invalid command: matutils.saddcnst()");retrn(ret,e);

    # returns difference of two matrices
    @staticmethod
    def msub(a:matx,b:matx,sumr=None,chk=True,ret='a')->matx|tuple[Decimal,...]:
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx([a,b],True) is None:raise Exception;
                    if eqval([a.collen,a.rowlen],[b.collen,b.rowlen]) is None:raise Exception;
                case _:raise Exception("Invalid argument: chk => bool");
            r=[galg.sub(*i) for i in zip(a.matx,b.matx)];
            match sumr:
                case None:return matx(tuple(r),False,'c');
                case True:return galg.add(*r);
                case False:return tuple([alg.add(*i) for i in r]);
                case _:raise Exception("invalid argument: sumr => None/bool");
        except Exception as e:print("Invalid command: matutils.msub()");retrn(ret,e);

    # returns matrix after scalar multiplication
    @staticmethod
    def smult(a:Decimal,b:matx,sumr=None,chk=True,ret='a')->matx|tuple[Decimal,...]:
        try:
            match chk:
                case False:pass;
                case True:
                    if str(a:=Decimal(str(a)))=='NaN':raise Exception;
                    if tmatx(b) is None:raise Exception;
                case _:raise Exception("Invalid argument: chk => bool");
            r=[galg.mulsg(a,i) for i in b.matx]
            match sumr:
                case None:return matx(tuple(r),False,'c');
                case True:return galg.add(*r);
                case False:return tuple([alg.add(*i) for i in r]);
                case _:raise Exception("Invalid argument: sumr => None/bool");
        except Exception as e:print("Invalid command: matutils.smult()");retrn(ret,e);

    @classmethod
    def smultfac(cls,a:tuple|list,b:matx,r=True,sumr=None,chk=True,ret='a')->matx|tuple[Decimal,...]:
        try:
            match chk:
                case False:pass;
                case True:
                    if (a:=tdeciml.dall(a)) is None or tmatx(b) is None:raise Exception;
                    match r:
                        case True:
                            if eqval(len(a),b.collen) is None:raise Exception;
                        case False:
                            if eqval(len(a),b.rowlen) is None:raise Exception;
                        case _:raise Exception("Invalid argument: r => bool");
                case _:raise Exception("Invalid argument: chk => bool");
            if r is True:r=[galg.mulsg(i[0],i[1]) for i in zip(a,b.matx)];
            else:r=[galg.mul(a,i) for i in b.matx];
            match sumr:
                case None:return matx(tuple(r),False,'c');
                case True:return galg.add(*r);
                case False:return tuple([alg.add(*i) for i in r]);
                case _:raise Exception("Invalid argument: sumr => None/bool");
        except Exception as e:print("Invalid command: matutils.smultfac()");retrn(ret,e);

    # returns matrix after matrix multiplication
    @classmethod
    def mmult(cls,a:matx,b:matx,t=(False,False),sumr=None,chk=True,ret='a')->matx|tuple[Decimal,...]:
        try:
            match t:
                case (False,False):
                    match chk:
                        case False:r=[matutils.smultfac(i,b,True,True,False,'c') for i in a.matx];
                        case True:
                            if tmatx([a,b],True) is None or eqval(a.rowlen,b.collen) is None:raise Exception;
                            r=[matutils.smultfac(i,b,True,True,False,'c') for i in a.matx]
                        case _:raise Exception("Invalid argument: chk => bool");
                case (False,True):
                    match chk:
                        case False:r=[matutils.smultfac(i,b,False,False,False,'c') for i in a.matx];
                        case True:
                            if tmatx([a,b],True) is None or eqval(a.rowlen,b.rowlen) is None:raise Exception;
                            r=[matutils.smultfac(i,b,False,False,False,'c') for i in a.matx]
                        case _:raise Exception("Invalid argument: chk => bool");
                case (True,False):
                    match chk:
                        case False:r=[matutils.smultfac(i,b,True,True,False,'c') for i in zip(*a.matx)];
                        case True:
                            if tmatx([a,b],True) is None or eqval(a.collen,b.collen) is None:raise Exception;
                            r=[matutils.smultfac(i,b,True,True,False,'c') for i in zip(*a.matx)]
                        case _:raise Exception("Invalid argument: chk => bool");
                case (True,True):
                    match chk:
                        case False:r=[matutils.smultfac(i,b,False,False,False,'c') for i in zip(*a.matx)];
                        case True:
                            if tmatx([a,b],True) is None or eqval(a.collen,b.rowlen) is None:raise Exception;
                            r=[matutils.smultfac(i,b,False,False,False,'c') for i in zip(*a.matx)]
                        case _:raise Exception("Invalid argument: chk => bool");
                case _:raise Exception("Invalid argument: t => (bool, bool)");
            match sumr:
                case None:return matx(tuple(r),False,'c');
                case False:return tuple([alg.add(*i) for i in r]);
                case True:return galg.add(*r);
                case _:raise Exception("Invalid argument: sumr => None/bool");
        except Exception as e:print("Invalid command: matutils.mmult()");retrn(ret,e);
    
    @staticmethod
    def melmult(a:matx,b:matx,t=(False,False),sumr=None,chk=True,ret='a')->matx|tuple[Decimal,...]:
        try:
            match t:
                case (False,False):
                    match chk:
                        case False:r=tuple([galg.mul(*i) for i in zip(a.matx,b.matx)]);
                        case True:
                            if tmatx([a,b],True) is None or eqval([a.collen,a.rowlen],[b.collen,b.rowlen]) is None:raise Exception;
                            r=tuple([galg.mul(*i) for i in zip(a.matx,b.matx)])
                        case _:raise Exception("Invalid argument: chk => bool");
                case (True,False):
                    match chk:
                        case False:r=tuple([galg.mul(*i) for i in zip(zip(*a.matx),b.matx)]);
                        case True:
                            if tmatx([a,b],True) is None or eqval([a.collen,a.rowlen],[b.collen,b.rowlen]) is None:raise Exception;
                            r=tuple([galg.mul(*i) for i in zip(zip(*a.matx),b.matx)])
                        case _:raise Exception("Invalid argument: chk => bool");
                case (False,True):
                    match chk:
                        case False:r=tuple([galg.mul(*i) for i in zip(a.matx,zip(*b.matx))]);
                        case True:
                            if tmatx([a,b],True) is None or eqval([a.collen,a.rowlen],[b.collen,b.rowlen]) is None:raise Exception;
                            r=tuple([galg.mul(*i) for i in zip(a.matx,zip(*b.matx))])
                        case _:raise Exception("Invalid argument: chk => bool");
                case (True,True):
                    match chk:
                        case False:r=tuple([galg.mul(*i) for i in zip(zip(*a.matx),zip(*b.matx))])
                        case True:
                            if tmatx([a,b],True) is None or eqval([a.collen,a.rowlen],[b.rowlen,b.collen]) is None:raise Exception;
                            r=tuple([galg.mul(*i) for i in zip(zip(*a.matx),zip(*b.matx))])
                        case _:raise Exception("Invalid argument: chk => bool");
                case _:raise Exception("Invalid argument: t => (bool, bool)");
            match sumr:
                case None:return matx(r,False,'c');
                case True:return galg.add(*r);
                case False:return tuple([alg.add(*i) for i in r]);
                case _:raise Exception("Invalid argument: sumr => None/bool");
        except Exception as e:print("Invalid command: matutils.melmult()");retrn(ret,e);

    @staticmethod
    def uldcompose(a:matx,chk=True,ret='a')->tuple:
        try:
            match chk:
                case True:
                    if tmatx(a) is None or a.sqmatx is None:raise Exception;
                case False:pass;
                case _:raise Exception("Invalid argument: chk => bool");
            ut=list();lt=list();dia=list();
            for i in range(a.collen):
                ut1=list();lt1=list();
                for j in range(a.rowlen):
                    if j<i:lt1.append(a.mele(i,j,False,'c'));ut1.append(Decimal('0.0'));
                    elif i==j:dia.append(a.mele(i,j,False,'c'));lt1.append(Decimal('0.0'));ut1.append(Decimal('0.0'));
                    else:ut1.append(a.mele(i,j,False,'c'));lt1.append(Decimal('0.0'));
                ut.append(tuple(ut1));lt.append(tuple(lt1));
            return matx(tuple(ut),False,'c'),matx(tuple(lt),False,'c'),matx((tuple(dia),),False,'c')
        except Exception as e:print("Invalid command: matutils.uldcompose()");retrn(ret,e);
    
    @classmethod
    def dpose(cls,a: matx,li: list | tuple,r=False,chk=True,ret='a')->tuple:
        try:
            match chk:
                case True:
                    if tmatx(a) is None:raise Exception;
                    match li.__class__.__name__:
                        case 'list':
                            if (li:=tint.iwgrp(li)) is None:raise Exception;
                    match r:
                        case False:
                            if eqval(sum(li),a.rowlen) is None:raise Exception;
                        case True:
                            if eqval(sum(li),a.collen) is None:raise Exception;
                        case _:raise Exception("Invalid argument: r => bool");
                case False:pass;
                case _:raise Exception("Invalid argument: chk => bool");
            i=0;ln=list();
            for j in li:ln.append([i+k for k in range(j)]);i+=j;
            return tuple([cls.gele(a,i,r,False,'c') for i in ln])
        except Exception as e:print("Invalid command: matutils.dpose()");retrn(ret,e);


class melutils:

    @staticmethod
    def add(a:matx,li:list[list]|tuple[list]|str,r=False,chk=True,ret='a')->matx:
        try:
            if li!='all':
                l=list()
                for i in li:
                    for j in i:
                        if j not in l:l.append(j);
                d=dict()
                for i in enumerate(a.gele(l,r,chk,'c')):d[l[i[0]]]=i[1];
                return matx(tuple([galg.add(*[d[j] for j in i]) for i in li]),False,'c')
            else:
                match r:
                    case False:return matx(tuple([alg.add(*i) for i in a.matx]),False,'c');
                    case True:return matx(galg.add(*a.matx),False,'c');
                    case _:raise Exception("Invalid argument: r => bool");
        except Exception as e:print("Invalid command: melutils.add()");retrn(ret,e);
    
    @staticmethod
    def mult(a:matx,li:list[list]|tuple[list]|str,r=False,chk=True,ret='a')->matx:
        try:
            if li!='all':
                l=list()
                for i in li:
                    for j in i:
                        if j not in l:l.append(j);
                d=dict()
                for i in enumerate(a.gele(l,r,chk,'c')):d[l[i[0]]]=i[1];
                return matx(tuple([galg.mul(*[d[j] for j in i]) for i in li]),False,'c')
            else:
                match r:
                    case False:return matx(tuple([alg.mul(*i) for i in a.matx]),False,'c');
                    case True:return matx(galg.mul(*a.matx),False,'c');
                    case _:raise Exception("Invalid argument: r => bool");
        except Exception as e:print("Invalid command: melutils.mult()");retrn(ret,e);

    @staticmethod
    def pow(an:list|tuple[Decimal,Decimal],a:matx,li:list|tuple|str,r=False,chk=True,ret='a')->matx:
        try:
            match chk:
                case False:pass;
                case True:
                    match an.__class__.__name__:
                        case 'tuple':
                            if (an:=tdeciml.dall(an)) is None:raise Exception;
                        case 'list':
                            if (an:=tdeciml.dall(an)) is None:raise Exception;
                        case _:raise Exception("Invalid argument: a => tuple/list");
                    if eqval(len(an),2) is None:raise Exception;
                case _:raise Exception("Invalid argument: chk => bool");
            if li!='all':
                if an[0]!=1:return matx(tuple([galg.pwrgs(galg.mulsg(an[0],i),an[1]) for i in a.gele(li,r,chk,'c')]),False,'c');
                else:return matx(tuple([galg.pwrgs(i,an[1]) for i in a.gele(li,r,chk,'c')]),False,'c');
            else:
                if an[0]!=1:return matx(tuple([galg.pwrgs(galg.mulsg(an[0],i),an[1]) for i in a.matx]),False,'c');
                else:return matx(tuple([galg.pwrgs(i,an[1]) for i in a.matx]),False,'c');
        except Exception as e:print("Invalid command: melutils.pow()");retrn(ret,e);

    @staticmethod
    def log(an:list|tuple[Decimal,Decimal],a:matx,li:list|tuple|str,r=False,chk=True,ret='a')->matx:
        try:
            match chk:
                case False:pass;
                case True:
                    match an.__class__.__name__:
                        case 'tuple':
                            if (an:=tdeciml.dall(an)) is None:raise Exception;
                        case 'list':
                            if (an:=tdeciml.dall(an)) is None:raise Exception;
                        case _:raise Exception("Invalid argument: a => tuple/list");
                    if eqval(len(an),2) is None:raise Exception;
                case _:raise Exception("Invalid argument: chk => bool");
            if li!='all':
                if an[0]!=1:return matx(tuple([tuple([alg.log(alg.mul(j,an[0]),an[1]) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                else:return matx(tuple([tuple([alg.log(j,an[1]) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
            else:
                if an[0]!=1:return matx(tuple([tuple([alg.log(alg.mul(j,an[0]),an[1]) for j in i]) for i in a.matx]),False,'c');
                else:return matx(tuple([tuple([alg.log(j,an[1]) for j in i]) for i in a.matx]),False,'c');
        except Exception as e:print("Invalid command: melutils.log()");retrn(ret,e);

    @staticmethod
    def expo(an:list|tuple[Decimal,Decimal],a:matx,li:list|tuple|str,r=False,chk=True,ret='a')->matx:
        try:
            match chk:
                case False:pass;
                case True:
                    match an.__class__.__name__:
                        case 'tuple':
                            if (an:=tdeciml.dall(an)) is None:raise Exception;
                        case 'list':
                            if (an:=tdeciml.dall(an)) is None:raise Exception;
                        case _:raise Exception("Invalid argument: a => tuple/list");
                    if eqval(len(an),2) is None:raise Exception;
                case _:raise Exception("Invalid argument: chk => bool");
            if li!= 'all':
                if an[1]!=1:return matx(tuple([tuple([alg.pwr(an[0],alg.mul(j,an[1])) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                else:return matx(tuple([tuple([alg.pwr(an[0],j) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
            else:
                if an[1]!=1:return matx(tuple([tuple([alg.pwr(an[0],alg.mul(j,an[1])) for j in i]) for i in a.matx]),False,'c');
                else:return matx(tuple([tuple([alg.pwr(an[0],j) for j in i]) for i in a.matx]),False,'c');
        except Exception as e:print("Invalid command: melutils.expo()");retrn(ret,e);

    @staticmethod
    def trig(n:Decimal,a:matx,li:list|tuple|str,r=False,f='cos',chk=True,ret='a')->matx:
        try:
            match chk:
                case False:pass;
                case True:
                    if str(n:=Decimal(str(n)))=='NaN':raise Exception;
                case _:raise Exception("Invalid argument: chk => bool");
            if li!='all':
                if n!=1:
                    match f:
                        case 'cos':return matx(tuple([tuple([trig.cos(alg.mul(n,j)) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'sin':return matx(tuple([tuple([trig.sin(alg.mul(n,j)) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'tan':return matx(tuple([tuple([trig.tan(alg.mul(n,j)) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'sec':return matx(tuple([tuple([trig.sec(alg.mul(n,j)) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'cosec':return matx(tuple([tuple([trig.cosec(alg.mul(n,j)) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'cot':return matx(tuple([tuple([trig.cot(alg.mul(n,j)) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'acos':return matx(tuple([tuple([trig.acos(alg.mul(n,j)) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'asin':return matx(tuple([tuple([trig.asin(alg.mul(n,j)) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'atan':return matx(tuple([tuple([trig.atan(alg.mul(n,j)) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'asec':return matx(tuple([tuple([trig.asec(alg.mul(n,j)) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'acosec':return matx(tuple([tuple([trig.acosec(alg.mul(n,j)) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'acot':return matx(tuple([tuple([trig.acot(alg.mul(n,j)) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'sinh':return matx(tuple([tuple([htrig.sinh(alg.mul(n,j)) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'cosh':return matx(tuple([tuple([htrig.cosh(alg.mul(n,j)) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'tanh':return matx(tuple([tuple([htrig.tanh(alg.mul(n,j)) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'cosech':return matx(tuple([tuple([htrig.cosech(alg.mul(n,j)) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'sech':return matx(tuple([tuple([htrig.sech(alg.mul(n,j)) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'coth':return matx(tuple([tuple([htrig.coth(alg.mul(n,j)) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                else:
                    match f:
                        case 'cos':return matx(tuple([tuple([trig.cos(j) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'sin':return matx(tuple([tuple([trig.sin(j) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'tan':return matx(tuple([tuple([trig.tan(j) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'sec':return matx(tuple([tuple([trig.sec(j) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'cosec':return matx(tuple([tuple([trig.cosec(j) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'cot':return matx(tuple([tuple([trig.cot(j) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'acos':return matx(tuple([tuple([trig.acos(j) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'asin':return matx(tuple([tuple([trig.asin(j) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'atan':return matx(tuple([tuple([trig.atan(j) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'asec':return matx(tuple([tuple([trig.asec(j) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'acosec':return matx(tuple([tuple([trig.acosec(j) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'acot':return matx(tuple([tuple([trig.acot(j) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'sinh':return matx(tuple([tuple([htrig.sinh(j) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'cosh':return matx(tuple([tuple([htrig.cosh(j) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'tanh':return matx(tuple([tuple([htrig.tanh(j) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'cosech':return matx(tuple([tuple([htrig.cosech(j) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'sech':return matx(tuple([tuple([htrig.sech(j) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                        case 'coth':return matx(tuple([tuple([htrig.coth(j) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
            else:
                if n!=1:
                    match f:
                        case 'cos':return matx(tuple([tuple([trig.cos(alg.mul(n,j)) for j in i]) for i in a.matx]),False,'c');
                        case 'sin':return matx(tuple([tuple([trig.sin(alg.mul(n,j)) for j in i]) for i in a.matx]),False,'c');
                        case 'tan':return matx(tuple([tuple([trig.tan(alg.mul(n,j)) for j in i]) for i in a.matx]),False,'c');
                        case 'sec':return matx(tuple([tuple([trig.sec(alg.mul(n,j)) for j in i]) for i in a.matx]),False,'c');
                        case 'cosec':return matx(tuple([tuple([trig.cosec(alg.mul(n,j)) for j in i]) for i in a.matx]),False,'c');
                        case 'cot':return matx(tuple([tuple([trig.cot(alg.mul(n,j)) for j in i]) for i in a.matx]),False,'c');
                        case 'acos':return matx(tuple([tuple([trig.acos(alg.mul(n,j)) for j in i]) for i in a.matx]),False,'c');
                        case 'asin':return matx(tuple([tuple([trig.asin(alg.mul(n,j)) for j in i]) for i in a.matx]),False,'c');
                        case 'atan':return matx(tuple([tuple([trig.atan(alg.mul(n,j)) for j in i]) for i in a.matx]),False,'c');
                        case 'asec':return matx(tuple([tuple([trig.asec(alg.mul(n,j)) for j in i]) for i in a.matx]),False,'c');
                        case 'acosec':return matx(tuple([tuple([trig.acosec(alg.mul(n,j)) for j in i]) for i in a.matx]),False,'c');
                        case 'acot':return matx(tuple([tuple([trig.acot(alg.mul(n,j)) for j in i]) for i in a.matx]),False,'c');
                        case 'sinh':return matx(tuple([tuple([htrig.sinh(alg.mul(n,j)) for j in i]) for i in a.matx]),False,'c');
                        case 'cosh':return matx(tuple([tuple([htrig.cosh(alg.mul(n,j)) for j in i]) for i in a.matx]),False,'c');
                        case 'tanh':return matx(tuple([tuple([htrig.tanh(alg.mul(n,j)) for j in i]) for i in a.matx]),False,'c');
                        case 'cosech':return matx(tuple([tuple([htrig.cosech(alg.mul(n,j)) for j in i]) for i in a.matx]),False,'c');
                        case 'sech':return matx(tuple([tuple([htrig.sech(alg.mul(n,j)) for j in i]) for i in a.matx]),False,'c');
                        case 'coth':return matx(tuple([tuple([htrig.coth(alg.mul(n,j)) for j in i]) for i in a.matx]),False,'c');
                else:
                    match f:
                        case 'cos':return matx(tuple([tuple([trig.cos(j) for j in i]) for i in a.matx]),False,'c');
                        case 'sin':return matx(tuple([tuple([trig.sin(j) for j in i]) for i in a.matx]),False,'c');
                        case 'tan':return matx(tuple([tuple([trig.tan(j) for j in i]) for i in a.matx]),False,'c');
                        case 'sec':return matx(tuple([tuple([trig.sec(j) for j in i]) for i in a.matx]),False,'c');
                        case 'cosec':return matx(tuple([tuple([trig.cosec(j) for j in i]) for i in a.matx]),False,'c');
                        case 'cot':return matx(tuple([tuple([trig.cot(j) for j in i]) for i in a.matx]),False,'c');
                        case 'acos':return matx(tuple([tuple([trig.acos(j) for j in i]) for i in a.matx]),False,'c');
                        case 'asin':return matx(tuple([tuple([trig.asin(j) for j in i]) for i in a.matx]),False,'c');
                        case 'atan':return matx(tuple([tuple([trig.atan(j) for j in i]) for i in a.matx]),False,'c');
                        case 'asec':return matx(tuple([tuple([trig.asec(j) for j in i]) for i in a.matx]),False,'c');
                        case 'acosec':return matx(tuple([tuple([trig.acosec(j) for j in i]) for i in a.matx]),False,'c');
                        case 'acot':return matx(tuple([tuple([trig.acot(j) for j in i]) for i in a.matx]),False,'c');
                        case 'sinh':return matx(tuple([tuple([htrig.sinh(j) for j in i]) for i in a.matx]),False,'c');
                        case 'cosh':return matx(tuple([tuple([htrig.cosh(j) for j in i]) for i in a.matx]),False,'c');
                        case 'tanh':return matx(tuple([tuple([htrig.tanh(j) for j in i]) for i in a.matx]),False,'c');
                        case 'cosech':return matx(tuple([tuple([htrig.cosech(j) for j in i]) for i in a.matx]),False,'c');
                        case 'sech':return matx(tuple([tuple([htrig.sech(j) for j in i]) for i in a.matx]),False,'c');
                        case 'coth':return matx(tuple([tuple([htrig.coth(j) for j in i]) for i in a.matx]),False,'c');
        except Exception as e:print("Invalid command: melutils.trig()");retrn(ret,e);

class matstat:
    
    @staticmethod
    def amean(a:matx,el='row',chk=True,ret='a')->tuple[Decimal,...]|Decimal:
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx(a) is None: raise Exception;
                case _:raise Exception("Invalid argument: a => matx");
            match el:
                case 'row':return galg.divgs([alg.add(*i) for i in a.matx],a.rowlen);
                case 'col':return galg.divgs(galg.add(*a.matx),a.collen);
                case 'all':return alg.div(alg.add(*[alg.add(*i) for i in a.matx]),a.rowlen*a.collen);
                case _:raise Exception("Invalid argument: el => 'row'/'col'/'all");
        except Exception as e:print("Invalid command: matstat.amean()");retrn(ret,e);
    
    @classmethod
    def gmean(cls,a:matx,el='row',chk=True,ret='a')->tuple[Decimal,...]|Decimal:
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx(a) is None:raise Exception;
                case _:raise Exception("Invalid argument: a => matx");
            match el:
                case 'row':return galg.pwrgs([alg.mul(*i) for i in a.matx],alg.div('1',a.rowlen));
                case 'col':return galg.pwrgs(galg.mul(*a.matx),alg.div('1',a.collen));
                case 'all':return alg.pwr(alg.mul(*[alg.mul(*i) for i in a.matx]),alg.div('1',a.rowlen*a.collen));
                case _:raise Exception("Invalid argument: el => 'row'/'col'/'all");
        except Exception as e:print("Invalid command: matstat.gmean()");retrn(ret,e);

    @classmethod
    def hmean(cls,a:matx,el='row',chk=True,ret='a')->tuple[Decimal,...]|Decimal:
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx(a) is None:raise Exception;
                case _:raise Exception("Invalid argument: a => matx");
            match el:
                case 'row':return galg.divsg(a.rowlen,[alg.add(*galg.divsg('1',i)) for i in a.matx]);
                case 'col':return galg.divsg(a.collen,galg.add(*[galg.divsg('1',i) for i in a.matx]));
                case 'all':return alg.div(a.rowlen*a.collen,alg.add(*[alg.add(*galg.divsg('1',i)) for i in a.matx]));
                case _:raise Exception("Invalid argument: el => 'row'/'col'/'all");
        except Exception as e:print("Invalid command: matstat.hmean()");retrn(ret,e);

    @classmethod
    def qmean(cls,a: matx,el='row',chk=True,ret='a')->tuple[Decimal,...]|Decimal:
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx(a) is None: raise Exception;
                case _:raise Exception("Invalid argument: a => matx");
            match el:
                case 'row':return galg.pwrgs(galg.divgs([alg.add(*galg.pwrgs(i,'2')) for i in a.matx],a.rowlen),'0.5');
                case 'col':return galg.pwrgs(galg.divgs(galg.add(*[galg.pwrgs(i,'2') for i in a.matx]),a.collen),'0.5');
                case 'all':return alg.pwr(alg.div(alg.add(*[alg.add(*galg.pwrgs(i,'2')) for i in a.matx]),a.rowlen*a.collen),'0.5');
                case _:raise Exception("Invalid argument: el => 'row'/'col'/'all");
        except Exception as e:print("Invalid command: matstat.qmean()");retrn(ret,e);
    
    @classmethod
    def var(cls,a: matx,el='row',samp=True,chk=True,ret='a')->tuple[Decimal,...]|Decimal:
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx(a) is None:raise Exception;
                case _:raise Exception("Invalid argument: a => matx");
            match el:
                case 'row':
                    match samp:
                        case True:d=(ar:=a.rowlen)-1;
                        case False:d=(ar:=a.rowlen);
                        case _:raise Exception("Invalid argument: samp => bool");
                    return galg.divgs([alg.sub(alg.add(*galg.pwrgs(i,'2')),alg.div(alg.pwr(alg.add(*i),'2'),ar)) for i in a.matx],d);
                case 'col':
                    match samp:
                        case True:d=(ac:=a.collen)-1;
                        case False:d=(ac:=a.collen);
                        case _:raise Exception("Invalid argument: samp => bool");
                    return galg.divgs(galg.sub(galg.add(*[galg.pwrgs(i,'2') for i in a.matx]),galg.divgs(galg.pwrgs(galg.add(*a.matx),ac),'2')),d);
                case 'all':
                    match samp:
                        case True:d=(n:=a.rowlen*a.collen)-1;
                        case False:d=(n:=a.rowlen*a.collen);
                        case _:raise Exception("Invalid argument: samp => bool");
                    return alg.div(alg.sub(alg.add(*[alg.add(*galg.pwrgs(i,'2')) for i in a.matx]),alg.div(alg.pwr(alg.add(*[alg.add(*i) for i in a.matx]),'2'),n)),d);
                case _:raise Exception("Invalid argument: el => 'row'/'col'/'all");
        except Exception as e:print("Invalid command: matstat.var()");retrn(ret,e);
    
    @classmethod
    def sd(cls,a: matx,el='row',samp=True,chk=True,ret='a')->tuple[Decimal,...]|Decimal:
        try:
            if el!='all':return galg.pwrgs(cls.var(a,el,samp,chk,'c'),'0.5');
            else:return alg.pwr(cls.var(a,el,samp,chk,'c'),'0.5');
        except Exception as e:print("Invalid command: matstat.sd()");retrn(ret,e);

# print("1")
# z=[1,2,3]
# a1 = [z,[5,2, int(6)], [5, 5, 8]]
# b = [[1, 3, 6], [8, 5, 6], [7, 4, 5]]
# a = matx(a1)
# a.pmatx
# print(a.dnant())
# a.pmatx
# matutils.saddcnst((1, 2, 3), a).pmatx
# melutils.add(a, [[0,1], [0,1,2]]).pmatx
# melutils.add(a, [[0,1], [0,1,2]], True).pmatx
# melutils.pow([1, 2], a, [0,2]).pmatx
# melutils.trig(100, a, [0, 1], f='cos').pmatx
# x = matutils.dpose(a, [1,2], True)
# for i in x:
#     i.pmatx
# a.matx = a.matx
# a.pmatx
# print(a.matxl())
# a.pmatx
# a.tpose().pmatx
# print(a.mele(0, 0))
# a.pmatx
# print(a.rowlen, a.collen)
# a1 = [0, 0, 0]
# a.pmatx
# c = a.matxl()
# c[0] = [0, 0, 0]
# a.pmatx
# print(c)
# a.matx = [[1, 2, 3], [5, 0, 6], [5, 5, 8]]
# a.pmatx
# print("2")
# b = matx(b)
# a.pmatx
# b.pmatx
# matutils.melmult(a, b).pmatx
# print(matutils.melmult(a, b, (True, False), False))
# print(matutils.melmult(a, b, (False, True), True))
# matutils.melmult(a, b, (True, True)).pmatx
# matutils.addmatx(a, b, matx([[1,],[1,],[1,]])).pmatx
# matutils.smultfac(tuple([2, 1, 2]), a).pmatx
# matutils.gele(a, [0, 1]).pmatx
# matutils.gele(a, [1, 0], True).pmatx
# print(a.sqmatx)
# c = [0, 0]
# print(matx(c).sqmatx)
# print(a.dnant(), b.dnant())
# a.invse().pmatx
# b.invse().pmatx
# print(b.invsednant(), matutils.dnant(b.invse()))
# matutils.madd(a, b).pmatx
# matutils.mmult(a, b).pmatx
# a = matx([11, 10, 100])
# matutils.matlxtox(a)
# matutils.maddval(a, Decimal('1.0')).pmatx
# matutils.matxtolx([matx([1,2,3]), matx([2,3,4])], False).pmatx
# a = matx([[1,2], [5,3]])
# a.pmatx
# print(matstat.amean(a), matstat.amean(a, 'col'), matstat.amean(a, 'all'))
# print(matstat.gmean(a), matstat.gmean(a, 'col'), matstat.gmean(a, 'all'))
# print(matstat.hmean(a), matstat.hmean(a, 'col'), matstat.hmean(a, 'all'))
# print(matstat.qmean(a), matstat.qmean(a, 'col'), matstat.qmean(a, 'all'))
# print(matstat.sd(a, samp=False), matstat.sd(a, 'col', False), matstat.sd(a, 'all'))
# a.cofacm().pmatx

