from deciml.deciml import deciml, algbra as alg, constant as cnst, stat, galgbra as galg, Decimal
from compare.cmpr import eqval, eqllen, tdict, tdata, tdeciml, tint
from terminate import retrn
from deciml_maths.matrix import matx, matutils, melutils
from deciml_maths.data import data, datautils
from algoutils import parameter, function, Scale, Calculate, GetData


class _Predict:

    # returns True for y=1 and False for y=0
    @staticmethod
    def _ygp(x:tuple[Decimal,...],p:tuple[Decimal,...],p1:parameter,const=(False,True),ret='a')->int:
        try:
            match const[1]:
                case True:x=(Decimal('1.0'),)+x;
                case False:pass;
                case _:raise Exception("Invalid argument: const => (bool, bool)");
            match const[0]:
                case False:h=alg.div('1',alg.add('1',alg.pwr(cnst.e(),alg.mul('-1',alg.add(*galg.mul(x,p1.valall(p)))))));
                case True:h=alg.div('1',alg.add('1',alg.pwr(cnst.e(),alg.mul('-1',p[0],alg.add(*galg.mul(x,p1.valall(p[1:])))))));
                case _:raise Exception("Invalid argument: const => (bool, bool)");
            if h is None:raise Exception;
            if h<0.5:return 0;
            else:return 1;
        except Exception as e:print("Invalid command: _Predict._ygp()");retrn(ret,e);
    
    @staticmethod
    def _allygp(x:matx,p:tuple[Decimal,...],p1:parameter,const=(False,True),ret='a')->tuple[int,...]:
        try:
            match const[1]:
                case True:x=matutils.maddval(x,Decimal('1.0'),False,'c');
                case False:pass;
                case _:raise Exception("Invalid argument: const => (bool, bool)");
            p=p1.valall(p)
            match const[0]:
                case False:h=galg.divsg('1',galg.addsg('1',galg.pwrsg(cnst.e(),galg.mulsg('-1',matutils.smultfac(p,x,False,False,False,'c')))));
                case True:h=galg.divsg('1',galg.addsg('1',galg.pwrsg(cnst.e(),galg.mulsg(alg.mul('-1',p[0]),matutils.smultfac(p[1:],x,False,False,False,'c')))));
                case _:raise Exception("Invalid argument: const => (bool, bool)");
            li=list()
            for i in h:
                if i<0.5:li.append(0);
                else:li.append(1);
            return tuple(li)
        except Exception as e:print("Invalid command: _Predict._allygp()");retrn(ret,e);

    @staticmethod
    def _y(x:tuple[Decimal,...],p:tuple[Decimal,...],const:tuple[bool,bool],ret='a')->int:
        try:
            match const[1]:
                case True:x=(Decimal('1.0'),)+x;
                case False:pass;
                case _:raise Exception("Invalid argument: const => (bool, bool)");
            match const[0]:
                case False:h=alg.div('1',alg.add('1',alg.pwr(cnst.e(),alg.mul('-1',alg.add(*galg.mul(x,p))))));
                case True:h=alg.div('1',alg.add('1',alg.pwr(cnst.e(),alg.mul('-1',p[0],alg.add(*galg.mul(x,p[1:]))))));
                case _:raise Exception("Invalid argument: const => (bool, bool)");
            if h is None:raise Exception;
            if h<0.5:return False;
            else:return True;
        except Exception as e:print("Invalid command: _Predict._y()");retrn(ret,e);
    
    @staticmethod
    def _ally(x:matx,p:tuple[Decimal,...],const:tuple[bool,bool],ret='a')->tuple[bool,...]:
        try:
            match const[1]:
                case True:x=matutils.maddval(x,deciml('1.0'),False,'c');
                case False:pass;
                case _:raise Exception("Invalid argument: const => (bool, bool)");
            match const[0]:
                case False:h=galg.divsg('1',galg.addsg('1',galg.pwrsg(cnst.e(),galg.mulsg('-1',matutils.smultfac(p,x,False,False,False,'c')))));
                case True:h=galg.divsg('1',galg.addsg('1',galg.pwrsg(cnst.e(),galg.mulsg(alg.mul('-1',p[0]),matutils.smultfac(p[1:],x,False,False,False,'c')))));
                case _:raise Exception("Invalid argument: const => (bool, bool)");
            li = list()
            for i in h:
                if i<0.5:li.append(0);
                else:li.append(1);
            return tuple(li)
        except Exception as e:print("Invalid command: _Predict._ally()");retrn(ret,e);


class PLogReg(_Predict):

    @classmethod
    def ygp(cls,x:list,p:list,cfp:tuple[tuple[tuple[Decimal,Decimal],...],...]|list[list[list]],const=(False,True),ret='a')->int:
        try:
            if (p := matx(p,ret='c')) is None:
                raise Exception
            if (x := matx(x,ret='c')) is None:
                raise Exception
            if (p1:=parameter(cfp,True,'c')) is None:
                raise Exception
            match const:
                case (True,True):
                    if sum(p1.n) != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 2))
                    if eqval(len(p1.n),p.rowlen - 1) is None:
                        raise Exception
                case (False,True):
                    if sum(p1.n) != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                    if eqval(len(p1.n),p.rowlen) is None:
                        raise Exception
                case (True,False):
                    if sum(p1.n) != x.rowlen:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                    if eqval(len(p1.n),p.rowlen - 1) is None:
                        raise Exception
                case (False,False):
                    if sum(p1.n) != x.rowlen:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen))
                    if eqval(len(p1.n),p.rowlen) is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            return _Predict._ygp(x,p,p1,const,'c')
        except Exception as e:
            print("Invalid command: PLogReg.ygp()")
            retrn(ret,e)
    
    @classmethod
    def allygp(cls,x: list[list | tuple] | tuple[list,tuple],p: list,cfp: list[list[list]] | tuple[tuple[tuple[float | Decimal | int,float | Decimal | int],...],...],const=(False,True),ret='a') -> tuple[int,...]:
        try:
            if (x := matx(x,ret='c')) is None or (p1 := parameter(cfp,True,'c')) is None or (p := matx(p,ret='c')) is None:
                raise Exception
            match const:
                case (True,True):
                    if sum(p1.n) != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 2))
                    if eqval(len(p1.n),p.rowlen - 1) is None:
                        raise Exception
                case (False,True):
                    if sum(p1.n) != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                    if eqval(len(p1.n),p.rowlen) is None:
                        raise Exception
                case (True,False):
                    if sum(p1.n) != x.rowlen:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                    if eqval(len(p1.n),p.rowlen - 1) is None:
                        raise Exception
                case (False,False):
                    if sum(p1.n) != x.rowlen:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen))
                    if eqval(len(p1.n),p.rowlen) is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            return _Predict._allygp(x,p,p1,const,'c')
        except Exception as e:
            print("Invalid command: PLogReg.allygp()")
            retrn(ret,e)
    
    @classmethod
    def y(cls,x: list,p: list,const=(False,True),ret='a') -> int:
        try:
            if (p := matx(p,ret='c')) is None:
                raise Exception
            if (x := matx(x,ret='c')) is None:
                raise Exception
            match const:
                case (True,True):
                    if p.rowlen != x.rowlen + 2:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 2))
                case (False,True):
                    if p.rowlen != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                case (True,False):
                    if p.rowlen != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                case (False,False):
                    if p.rowlen != x.rowlen:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen))
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            return _Predict._y(x,p,const,'c')
        except Exception as e:
            print("Invalid command: PLogReg.y()")
            retrn(ret,e)
    
    @classmethod
    def ally(cls,x: list[list | tuple] | tuple[list | tuple],p: list,const=(False,True),ret='a') -> tuple[int,...]:
        try:
            if (x := matx(x,ret='c')) is None or (p := matx(p,ret='c')) is None:
                raise Exception
            match const:
                case (True,True):
                    if p.rowlen != x.rowlen + 2:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 2))
                case (False,True):
                    if p.rowlen != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                case (True,False):
                    if p.rowlen != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                case (False,False):
                    if p.rowlen != x.rowlen:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen))
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            return _Predict._ally(x,p,const,'c')
        except Exception as e:
            print("Invalid command: PLogReg.ally()")
            retrn(ret,e)

    @classmethod
    def clas(cls,x: list,d: dict,const=(False,True),ret='a') -> int:
        try:
            if tdict.dic(d) is None:
                raise Exception
            c = dict()
            for i in d.items():
                cl = cls.y(i[1]["parameters"],x,const,'c')
                if cl is None:
                    raise Exception
                if cl == 1:
                    c[i[0][1]] = c.setdefault(i[0][1],0) + 1
                else:
                    c[i[0][0]] = c.setdefault(i[0][0],0) + 1
            mx = 0
            mc = 0
            for i in c.items():
                if i[1] > mx:
                    mx = i[1]
                    mc = i[0]
            return mc
        except Exception as e:
            print("Invalid command: PLogReg.clas()")
            retrn(ret,e)
    
    @classmethod
    def allclas(cls,x: tuple[list | tuple] | list[list | tuple],d: dict,ret='a') -> dict:
        try:
            if tdict.dic(d) is None:
                raise Exception
            r1 = dict()
            x = matutils.matlxtox(x,False,'c')
            for i in d.items():
                if (cl := cls.ally(x,i[1],'c')) is not None:
                    for j in enumerate(cl):
                        r1[x[j[0]]] =  r1.setdefault(x[j[0]],[]) + [i[0][j[1]],]
                else:
                    raise Exception
            r = list()
            return tuple([stat.mode(r1[tuple(i)]) for i in x])
        except Exception as e:
            print("Invalid command: PLogReg.allclas()")
            retrn(ret,e)


class _ScalePar:

    # scale parameter values for logistic regression
    @staticmethod
    def _0to1(c: matx,f: matx,p: matx,const=True,ret='a') -> matx:
        try:
            p = matx(p,False,'c')
            match const:
                case True:
                    p0 = (alg.add(p.pop(0,False,False,'c')[0],alg.addl(matutils.smultfac(p.matx[0],c,False,False,'c').matx[0])),)
                    p = p0 + matutils.smultfac(f.matx[0],p,False,False,'c').matx[0]
                    return matx(p,False,'c')
                case False:
                    p = matutils.smultfac(f.matx[0],p,False,False,'c').matx[0]
                    return matx(p,False,'c')
                case _:
                    raise Exception("Invalid argument: const => bool")
        except Exception as e:
            print("Invalid command: _ScalePar._0to1()")
            retrn(ret,e)
    
    @staticmethod
    def _orignl(c: matx,f: matx,p: matx,const=True,ret='a') -> matx:
        try:
            p = matx(p,False,'c')
            match const:
                case True:
                    p0 = p.pop(0,False,False,'c')[0]
                    p = matutils.smultfac(tuple([alg.div(1,i) for i in f.matx[0]]),p,False,False,'c')
                    p0 -= matutils.mmult(p,c,(False,True),chk=False,ret='c').matx[0][0]
                    return matx((p0,) + p.matx[0],False,'c')
                case False:
                    p = matutils.smultfac(tuple([alg.div(1,i) for i in f.matx[0]]),p,False,False,'c')
                    return matx(p,False,'c')
                case _:
                    raise Exception("Invalid argument: const => bool")
        except Exception as e:
            print("Invalid command: _ScalePar._orignl()")
            retrn(ret,e)


class _Calculate(_Predict):

    # misclassifications after classification
    @classmethod
    def _misclassed(cls,d: tuple,p: matx,const: tuple[bool,bool],ret='a') -> dict:
        try:
            dic = dict()
            dic.setdefault('0',[0,0,[]])
            dic.setdefault('1',[0,0,[]])
            py = _Predict._ally(d[0],p,const,'c')
            for i in enumerate(py):
                y = str(d[1].mele(i[0],0,False,'c'))
                if i[1] == 0:
                    dic[y][0] += 1
                    if y == '1':
                        dic[y][1] += 1
                        dic[y][2].append(tuple([str(j) for j in d[0].mrow(i[0],False,'c')]))
                else:
                    dic[y][0] += 1
                    if y == '0':
                        dic[y][1] += 1
                        dic[y][2].append(tuple([str(j) for j in d[0].mrow(i[0],False,'c')]))
            return dic
        except Exception as e:
            print("Invalid command: _Calculate._misclassed()")
            retrn(ret,e)


class _Grades(_ScalePar,Calculate):
    
    @classmethod
    def _logreg(cls,d: tuple,p: matx,a: Decimal,m: int,pr: Decimal,const: tuple[bool,bool],ret='a') -> tuple[matx,int]:
        try:
            c,a = 0,alg.mul(-1,a)
            m += 1
            while (c := c + 1) != m:
                match const[0]:
                    case False:
                        e = cnst.e()
                        h = melutils.pow((Decimal('1.0'),Decimal('-1.0')),matutils.madd(matutils.eqelm(1,d[0].rowlen,Decimal('1.0'),False,'c'),melutils.expo((e,Decimal('-1.0')),matutils.mmult(p,d[0],chk=False,ret='c'),[0,],True,False,'c'),False,'c'),[0,],True,False,'c')
                        pn = matutils.madd(p,matutils.tpose(matutils.smult(a,matutils.mmult(d[0],matutils.msub(h,d[1],False,'c'),(False,True),chk=False,ret='c'),False,'c'),False,'c'),False,'c')
                    case True:
                        p1 = matx(p,False,'c')
                        p0 = p1.pop(0,False,False,'c')[0]
                        e = cnst.e()
                        h = melutils.pow((Decimal('1.0'),Decimal('-1.0')),matutils.madd(matutils.eqelm(1,d[0].rowlen,Decimal('1.0'),False,'c'),melutils.expo((e,Decimal('-1.0')),matutils.smult(p0,matutils.mmult(p1,d[0],chk=False,ret='c'),False,'c'),[0,],True,False,'c'),False,'c'),[0,],True,False,'c')
                        pn = matutils.madd(p,matutils.tpose(matutils.smult(a,matutils.addmatx(matutils.mmult(matutils.mmult(p1,d[0],chk=False,ret='c'),matutils.msub(h,d[1],False,'c'),(False,True),chk=False,ret='c'),matutils.mmult(matutils.smult(p0,d[0],False,'c'),matutils.msub(h,d[1],False,'c'),(False,True),chk=False,ret='c'),r=True,chk=False,ret='c'),False,'c'),False,'c'),False,'c')
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")        
                if pn is None:
                    raise Exception
                err = Calculate._cmperrpr(p,pn,pr)
                match err:
                    case True:
                        p.matx = pn
                        return p,c
                    case False:
                        p.matx = pn
                    case _:
                        raise Exception
            return p,c - 1
        except Exception as e:
            print("Invalid command: _Grades._logreg()")
            retrn(ret,e)
    
    @classmethod
    def _logregsp(cls,d: tuple,p: matx,a,m,pr,cf: tuple[matx,matx],const: tuple[bool,bool],ret='a') -> tuple[matx,int]:
        try:
            scc = cf[0]
            scf = cf[1]
            c,a = 0,alg.mul(-1,a)
            m += 1
            while (c := c + 1) != m:
                match const[0]:
                    case False:
                        e = cnst.e()
                        h = melutils.pow((Decimal('1.0'),Decimal('-1.0')),matutils.madd(matutils.eqelm(1,d[0].rowlen,Decimal('1.0'),False,'c'),melutils.expo((e,Decimal('-1.0')),matutils.mmult(p,d[0],chk=False,ret='c'),[0,],True,False,'c'),False,'c'),[0,],True,False,'c')
                        pn = matutils.madd(p,matutils.tpose(matutils.smult(a,matutils.mmult(d[0],matutils.msub(h,d[1],False,'c'),(False,True),chk=False,ret='c'),False,'c'),False,'c'),False,'c')
                    case True:
                        p1 = matx(p,False,'c')
                        p0 = p1.pop(0,False,False,'c')[0]
                        e = cnst.e()
                        h = melutils.pow((Decimal('1.0'),Decimal('-1.0')),matutils.madd(matutils.eqelm(1,d[0].rowlen,Decimal('1.0'),False,'c'),melutils.expo((e,Decimal('-1.0')),matutils.smult(p0,matutils.mmult(p1,d[0],chk=False,ret='c'),False,'c'),[0,],True,False,'c'),False,'c'),[0,],True,False,'c')
                        pn = matutils.madd(p,matutils.tpose(matutils.smult(a,matutils.addmatx(matutils.mmult(matutils.mmult(p1,d[0],chk=False,ret='c'),matutils.msub(h,d[1],False,'c'),(False,True),chk=False,ret='c'),matutils.mmult(matutils.smult(p0,d[0],False,'c'),matutils.msub(h,d[1],False,'c'),(False,True),chk=False,ret='c'),r=True,chk=False,ret='c'),False,'c'),False,'c'),False,'c')
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")       
                if pn is None:
                    raise Exception
                match const[0]:
                    case False:
                        op = _ScalePar._orignl(scc,scf,p,const[1],'c')
                        opn = _ScalePar._orignl(scc,scf,pn,const[1],'c')
                        if op is None or opn is None:
                            raise Exception
                    case True:
                        op = matutils.maddval(_ScalePar._orignl(scc,scf,matx(p.matx[0][1:],False,'c'),const[1],'c'),p.mele(0,0,False,'c'),False,'c')
                        opn = matutils.maddval(_ScalePar._orignl(scc,scf,matx(pn.matx[0][1:],False,'c'),const[1],'c'),p.mele(0,0,False,'c'),False,'c')
                        if op is None or opn is None:
                            raise Exception
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                err = Calculate._cmperrpr(op,opn,pr)
                match err:
                    case True:
                        p.matx = pn
                        return p,c
                    case False:
                        p.matx = pn
                    case _:
                        raise Exception
            return p,c - 1
        except Exception as e:
            print("Invalid command: _Grades._logregsp()")
            retrn(ret,e)


# class _LogReggp(Calculate):
    # returns parameter using gradient descent for linear regression and grouped parameters
#     @staticmethod
#     def _logreggp(d: tuple,p: matx,p1: parameter,a: Decimal,m: int,pr: Decimal,const: tuple[bool,bool],ret='a') -> matx:
#         try:
#             c = 0
#             while (c := c + 1) <= m:
#                 match const[0]:
#                     case False:
#                         pn = matutils.madd(p,matutils.tpose(matutils.smult(-a,matutils.mmult(matutils.tpose(d[0].val(p1.dval(p)),False,'c'),matutils.msub(matx(tuple([(sum(i),) for i in d[0].val(p1.val(p)).matx]),False,'c'),d[1],False,'c'),False,'c'),False,'c'),False,'c'),False,'c')
#                     case True:
#                         pn = matx(p,False,'c')
#                         p0 = pn.pop(0,False,False,'c')[0]
#                         p1v = p1.val(pn)
#                         dm = matutils.msub(matx(tuple([(p0 * sum(i),) for i in d[0].val(p1v).matx]),False,'c'),d[1],False,'c')
#                         pn = matutils.madd(p,matutils.tpose(matutils.smult(-a,matutils.addmatx(matutils.mmult(matx(tuple([sum(i) for i in d[0].val(p1v).matx]),False,'c'),dm,False,'c'),matutils.mmult(matutils.smult(p0,matutils.tpose(d[0].val(p1.dval(pn)),False,'c'),False,'c'),dm,False,'c'),True,False,'c'),False,'c'),False,'c'),False,'c')
#                     case _:
#                         raise Exception("Invalid argument: const => (bool,bool)")
#                 if pn is None:
#                     raise Exception
#                 match const[0]:
#                     case False:
#                         pv = p1.val(p)
#                         pnv = p1.val(pn)
#                         for i in range(len(pv)):
#                             if i == 0:
#                                 ap = pv[i]
#                                 apn = pnv[i]
#                             else:
#                                 ap.matx = matutils.addmatx(ap,pv[i],False,False,'c')
#                                 apn.matx = matutils.addmatx(apn,pnv[i],False,False,'c')
#                     case True:
#                         pv = matx(p,False,'c')
#                         pnv = matx(pn,False,'c')
#                         ap0 = matx(pv.pop(0,False,False,'c'),False,'c')
#                         apn0 = matx(pnv.pop(0,False,False,'c'),False,'c')
#                         pv = p1.val(pv)
#                         pnv = p1.val(pnv)
#                         for i in range(len(pv)):
#                             if i == 0:
#                                 ap = matutils.addmatx(ap0,pv[i],False,False,'c')
#                                 apn = matutils.addmatx(apn0,pnv[i],False,False,'c')
#                             else:
#                                 ap.matx = matutils.addmatx(ap,pv[i],False,False,'c')
#                                 apn.matx = matutils.addmatx(apn,pnv[i],False,False,'c')
#                     case _:
#                         raise Exception("Invalid argument: const => (bool, bool)")
#                 err = Calculate._cmperrpr(ap,apn,pr,'c')
#                 match err:
#                     case True:
#                         return pn,c
#                     case False:
#                         p.matx = pn
#                     case _:
#                         raise Exception
#             return pn,c - 1
#         except Exception as e:
#             retrn(ret,e)


def _grades(d: data,p: matx,a: Decimal,m: int,pr: Decimal,scale: bool,const: tuple[bool,bool],ret='a') -> dict:
    try:
        da = d.data
        match scale:
            case True:
                sc = Scale._scale0to1x(d.getax(),'c')
                if sc is None:
                    raise Exception
                d,scc,scf = data(sc["values"],d.getay(),False,'c'),sc["constant"],sc["factor"]
                del sc
                match const[0]:
                    case False:
                        match const[1]:
                            case True:
                                d = datautils.dataval(d,Decimal('1.0'),False,'c')
                            case False:
                                c = matutils.smultfac([alg.div(1,i) for i in scf.matx[0]],scc,False,False,'c')
                                d = data(matutils.saddcnst(c,d.getax(),False,False,'c'),d.getay(),False,'c')
                            case _:
                                raise Exception("Invalid argument: const => (bool,bool)")
                    case True:
                        match const[1]:
                            case True:
                                d = datautils.dataval(d,Decimal('1.0'),False,'c')
                            case False:
                                c = matutils.smultfac([alg.div(1,i) for i in scf.matx[0]],scc,False,False,'c')
                                d = data(matutils.saddcnst(c,d.getax(),False,False,'c'),d.getay(),False,'c')
                            case _:
                                raise Exception("Invalid argument: const => (bool, bool)")
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                match const[0]:
                    case False:
                        p = _ScalePar._0to1(scc,scf,p,const[1],'c')
                        if p is None:
                            raise Exception
                    case True:
                        p = matutils.maddval(_ScalePar._0to1(scc,scf,matx(p.matx[0][1:],False,'c'),const[1],'c'),p.mele(0,0,False,'c'),False,'c')
                        if p is None:
                            raise Exception
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
            case False:
                match const[1]:
                    case True:
                        d = datautils.dataval(d,deciml('1.0'),False,'c')
                    case False:
                        pass
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
            case _:
                raise Exception("Invalid argument: scale => bool")
        d1 = (matutils.tpose(d.getax()),matutils.tpose(d.getay()))
        match scale:
            case True:
                p1 = _Grades._logregsp(d1,p,a,m,pr,(scc,scf),const,'c')
            case False:
                p1 = _Grades._logreg(d1,p,a,m,pr,const,'c')
            case _:
                raise Exception("Invalid argument: scale => bool")
        if p is None:
            raise Exception
        p,c = p1
        del p1
        match scale:
            case True:
                match const[0]:
                    case False:
                        p = _ScalePar._orignl(scc,scf,p,const[1],'c')
                        if p is None:
                            raise Exception
                    case True:
                        p = matutils.maddval(_ScalePar._orignl(scc,scf,matx(p.matx[0][1:],False,'c'),const[1],'c'),p.mele(0,0,False,'c'),False,'c')
                        if p is None:
                            raise Exception
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
            case False:
                pass
            case _:
                raise Exception("Invalid argument: scale => bool")
        dic = {"parameters": p.matxl()[0],"iterations": c,}
        miscl = _Calculate._misclassed(da,p,const,'c')
        if miscl is None:
            raise Exception
        dic.update({"misclassifications": miscl})
        dic.update({"parameters": [str(i) for i in dic["parameters"]]})
        return dic
    except Exception as e:
        print("Invalid command: _grades()")
        retrn(ret,e)


# def _gradesgp(d: data,p: matx,p1:parameter,a: Decimal,m: int,pr: Decimal,const: tuple[bool,bool],ret='a') -> dict:
#     try:
#         match const[1]:
#             case True:
#                 d = datautils.dataval(d,Decimal('1.0'),False,'c')
#             case False:
#                 pass
#             case _:
#                 raise Exception("Invalid argument: const => (bool, bool)")
#         d1 = (function(tuple([matutils.dpose(i,p1.n,chk=False,ret='c') for i in d.data[0]]),'c'),d.getay())
#         c = -1
#         while (c := c + 1) < m:
#             match const[0]:
#                 case True:
#                     pass
#                 case _:
#                     raise Exception("Invalid argument: const => (bool,bool)")
#         dic1 = {"parameters": p.matxl()[0],"iterations": c,}
#         miscl = _Calculate._misclassed(d.data,dic1,ret='c')
#         if miscl is None:
#             raise Exception
#         dic1.update({"misclassifications": miscl})
#         dic1.update({"parameters": [str(i) for i in dic1["parameters"]]})
#         return dic1
#     except Exception as e:
#         retrn(ret,e)


class LogReg:

#     @staticmethod
#     def gradesgp(d: data,p: list | matx,a: float,cfp: list | tuple,m=100,pr=0.01,const=(False,True),ret='a') -> dict:
#         try:
#             if tdata(d) is None:
#                 raise Exception
#             if (p := matx(p,ret='c')) is None:
#                 raise Exception
#             if (a := tdeciml.decip(a)) is None:
#                 raise Exception
#             if (pr := tdeciml.decip(pr)) is None:
#                 raise Exception
#             if (m := tint.intn(m)) is None:
#                 raise Exception
#             match const:
#                 case (True,True):
#                     if sum(p1.n) != d.xvars + 1:
#                         raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 2))
#                     if eqval(len(p1.n),p.rowlen - 1) is None:
#                         raise Exception
#                 case (False,True):
#                     if sum(p1.n) != d.xvars + 1:
#                         raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
#                     if eqval(len(p1.n),p.rowlen) is None:
#                         raise Exception
#                 case (True,False):
#                     if sum(p1.n) != d.xvars:
#                         raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
#                     if eqval(len(p1.n),p.rowlen - 1) is None:
#                         raise Exception
#                 case (False,False):
#                     if sum(p1.n) != d.xvars:
#                         raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars))
#                     if eqval(len(p1.n),p.rowlen) is None:
#                         raise Exception
#                 case _:
#                     raise Exception("Invalid argument: const => (bool,bool)")
#             if (p1 := parameter(cfp)) is None:
#                 raise Exception
#             r = _gradesgp(d,p,p1,a,m,pr,const,'c')
#             if r is None:
#                 raise Exception
#             return r
#         except Exception as e:
#             retrn(ret,e)
    
    @staticmethod
    def grades(d: data,p: list,a: float,m=100,pr=0.01,scale=False,const=(False,True),ret='a') -> dict:
        try:
            if tdata(d) is None:
                raise Exception
            if (p := matx(p,True,'c')) is None or eqval(p.collen,1) is None or str(a := tdeciml.decip(a)) == 'NaN' or str(pr := tdeciml.decip(pr)) == 'NaN' or (m := tint.intn(m)) is None:
                raise Exception
            if const == (True,True):
                if p.rowlen != d.xvars + 2:
                    raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 2))
            elif const == (True,False) or const == (False,True):
                if p.rowlen != d.xvars + 1:
                    raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
            elif const == (False,False):
                if p.rowlen != d.xvars:
                    raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars))
            else:
                raise Exception("Invalid argument: const => (bool, bool)")
            return _grades(d,p,a,m,pr,scale,const,'c')
        except Exception as e:
            print("Invalid command: LogReg.grades()")
            retrn(ret,e)

    @classmethod
    def gradesgc(cls,d: dict,p: dict,a: float,m=100,pr=0.01,scale=False,const=(False,True),ret='a') -> dict:
        try:
            if tdict.matchkeys(d,p) is None or  eqllen(list(p.values())) is None or tdata(list(d.values()),True) is None:
                raise Exception
            dic = dict()
            match scale:
                case False:
                    for i in d.items():
                        dic[i[0]] = cls.grades(i[1],p[i[0]],a,m,pr,False,const,'c')
                    return dic
                case True:
                    for i in d.items():
                        dic[i[0]] = cls.grades(i[1],p[i[0]],a,m,pr,True,const,'c')
                    return dic
                case _:
                    raise Exception
        except Exception as e:
            print("Invalid command: LogReg.gradesgc()")
            retrn(ret,e)


d = LogReg.gradesgc(
   {(0,1): data([[10, 10, 10], [5, 7, 9], [4, 2, 7], [5, 9, 1], [20, 20, 20], [21, 25, 22], [14, 18, 12], [12, 15, 11]], [[0], [0], [0], [0], [1], [1], [1], [1]])}, {(0,1): [1, -6, 1, 1, 1]}, 0.01, 1000, const=(True, True))
print(d)
print(PLogReg.y([5, 7, 9], d[(0,1)]["parameters"], const=(True, True)), PLogReg.y([14, 18, 12], d[(0,1)]["parameters"], const=(True, True)))

a = GetData.regdata([0,1,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,1,1], [14.44,18.45,5.45,10.77,11.21,8.31,13.09,19.72,18.06,8.13,6.26,5.31,19.83,7,9.77,19.83,9.87,6.31,17.01,4.59], [13.93,3.16,8.51,10.04,10.02,9.5,2.66,9.61,9.24,9.32,4.19,10.89,3.33,7.27,5.66,13.03,8.06,8.99,10.6,8.08])
b = LogReg.grades(a, [0.632952961307885,0.342184583474655,-0.486518049871918], 0.00001, 100)
print(b)
print(PLogReg.ally(a.getax().matx, [0.632952961307885,0.342184583474655,-0.486518049871918]))