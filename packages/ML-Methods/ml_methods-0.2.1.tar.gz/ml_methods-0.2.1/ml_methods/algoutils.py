import json
from deciml.deciml import deciml, algbra as alg,  Decimal, galgbra as galg, abs
from compare.cmpr import eqval, tdeciml, tdata, tdict, tmatx
from terminate import retrn
from deciml_maths.matrix import matx, matutils
from deciml_maths.data import data


class apn:
    def __init__(self,apn:tuple[Decimal,Decimal],chk=True,ret='a')->None:
        try:
            match chk:
                case False:self.__apn = matx(apn,False,'c');
                case True:
                    apn = matx(apn,True,'c')
                    if apn is None or eqval(apn.rowlen,2) is None or eqval(apn.collen,1) is None:raise Exception;
                    self.__apn = apn
                case _:raise Exception("Invalid argument: chk => bool");
            if self.__apn.mele(0,1,False,'c')==0:self.__dapn=None;
            else:self.__dapn=matx(tuple([alg.mul(self.__apn.mele(0,0,False,'c'),self.__apn.mele(0,1,False,'c')),alg.sub(self.__apn.mele(0,1,False,'c'),1)]),False,'c');
            del apn
            self.val=lambda p:self.__fval(p);
            self.dval=lambda p:self.__fdval(p);
        except Exception as e:print("Invalid command: apn()");retrn(ret,e);

    def __fval(self,p:Decimal)->Decimal:
        try:
            if self.__apn.mele(0,1,False,'c')==0:return self.__apn.mele(0,0,False,'c');
            else:return alg.mul(self.__apn.mele(0,0,False,'c'),alg.pwr(p,self.__apn.mele(0,1,False,'c')));
        except Exception as e:print("Invalid command: apn.val()");retrn('a',e);

    def __fdval(self,p:Decimal)->Decimal:
        try:
            if self.__dapn==None:return Decimal('0.0');
            else:return alg.mul(self.__dapn.mele(0,0,False,'c'),alg.pwr(p,self.__dapn.mele(0,1,False,'c')));
        except Exception as e:print("Invalid command: apn.dval()");retrn('a',e);

class parameter:
    def __init__(self,li:list[list[list]]|tuple[tuple[tuple[Decimal,Decimal],...],...],chk=True,ret='a')->None:
        try:
            par=list();n=list();
            for i in li:
                par1=list()
                for j in i:par1.append(apn(j,chk,'c'));
                n.append(len(par1));par.append(tuple(par1));
            self.__par=tuple(par);self.n=tuple(n);
            del par,n;self.val=lambda p:self.__fval(p);self.dval=lambda p:self.__fdval(p);self.valall=lambda p:self.__fvalall(p);self.dvalall=lambda p:self.__fdvalall(p);
        except Exception as e:print("Invalid command: parameter()");retrn(ret,e);
    
    def __fval(self,p:tuple[Decimal,...])->tuple[tuple[Decimal,...],...]:
        try:
            l=list()
            for i in enumerate(self.__par):
                pv=p[i[0]];li=list();
                for j in i[1]:li.append(j.val(pv));
                l.append(tuple(li))
            return tuple(l)
        except Exception as e:print("Invalid command: parameter.val()");retrn('a',e);
    
    def __fdval(self,p:tuple[Decimal,...])->tuple[tuple[Decimal,...],...]:
        try:
            l=list()
            for i in enumerate(self.__par):
                pv=p[i[0]];li=list();
                for j in i[1]:li.append(j.dval(pv));
                l.append(tuple(li))
            return tuple(l)
        except Exception as e:print("Invalid command: parameter.dval()");retrn('a',e);
    
    def __fvalall(self,p:tuple[Decimal,...])->tuple[Decimal,...]:
        try:
            l=list()
            for i in self.__fval(p):l+=i;
            return tuple(l)
        except Exception as e:print("Invalid command: parameter.valall()");retrn('a',e);
    
    def __fdvalall(self,p:tuple[Decimal,...])->tuple[Decimal,...]:
        try:
            l=list()
            for i in self.__fdval(p):l+=i;
            return tuple(l)
        except Exception as e:print("Invalid command: parameter.dvalall()");retrn('a',e);


# class function:
#     def __init__(self,li:matx,chk=True,ret='a')->None:
#         try:
#             match chk:
#                 case True:
#                     if tmatx(li,True) is None:raise Exception;
#                 case False:pass;
#                 case _:raise Exception("Invalid argument: chk => bool");
#             self.__x=li;self.val=lambda p:self.__fval(p);del li;
#         except Exception as e:print("Invalid command: function()");retrn(ret, e);
#     
#     def __fval(self,p:tuple[tuple[Decimal,...],...])->matx:
#         for i in enumerate([matutils.mmult(i[1], matutils.tpose(p[i[0]]), False, 'c') for i in enumerate(self.__x)]):
#             if i[0] == 0:
#                 x = i[1]
#             else:
#                 x = matutils.addmatx(x, i[1], False, False, 'c')
#         return x


class Calculate:

    @classmethod
    def cmperrpr(cls,p:matx,pn:matx,pr:Decimal,t='relrms',chk=True,ret='a')->bool:
        try:
            match chk:
                case True:
                    if tmatx((p,pn),True) is None:
                        try:p=matx(p,True,'c');pn=matx(pn,True,'c');
                        except:raise Exception("Invalid argument: p,pn => matx");
                    if p.rowlen!=pn.rowlen or p.collen!=1 or pn.collen!=1:raise Exception("Invalid argument: p,pn");
                    if pr.__class__.__name__!='Decimal':
                        pr=deciml(pr);
                        if pr==Decimal('NaN'):raise Exception("Invalid argument: pr => Decimal");
                case False:pass;
                case _:raise Exception("Invalid argument: chk => bool");
            p=p.matx[0];pn=pn.matx[0];
            match t:
                case 'relrms':err=cls.__relrmserr(p,pn);
                case 'meanabs':err=cls.__meanabserr(p,pn);
                case 'meanabsrel':err=cls.__meanabsrelerr(p,pn);
                case 'absrms':err=cls.__absrmserr(p,pn);
                case _:raise Exception("Invalid argument: t => rms/");
            if err<pr:return True;
            else:return False;
        except Exception as e:print("Invalid command: Calculate._cmperrpr()");retrn(ret,e);
    
    @staticmethod
    def __relrmserr(p:tuple,pn:tuple)->Decimal:
        try:return alg.pwr(alg.div(alg.add(*galg.pwrgs(galg.div(galg.sub(p,pn),pn),2)),len(pn)),'0.5');
        except Exception as e:print(e);return None;

    @staticmethod
    def __meanabserr(p:tuple,pn:tuple)->Decimal:
        try:return alg.div(alg.add(*map(abs,galg.sub(p,pn))),len(pn));
        except Exception as e:print(e);return None;

    @staticmethod
    def __meanabsrelerr(p:tuple,pn:tuple)->Decimal:
        try:return alg.div(alg.add(*map(abs,galg.div(galg.sub(p,pn),pn))),len(pn));
        except Exception as e:print(e);return None;

    @staticmethod
    def __absrmserr(p:tuple,pn:tuple)->Decimal:
        try:return alg.pwr(alg.div(alg.add(*galg.pwrgs(galg.sub(p,pn),2)),len(pn)),'0.5');
        except Exception as e:print(e);return None;

class Scale:

    @staticmethod
    def factrintrx(x:matx,i=[Decimal('0'),Decimal('1')],ret=True)->dict:
        try:
            x1,x2=list(zip(*[(min(i),max(i)) for i in matutils.tpose(x).matx]));f=galg.divgs(galg.sub(x2,x1),(d:=alg.sub(i[1],i[0])));c=galg.divgs(galg.sub(galg.mulsg(i[1],x1),galg.mulsg(i[0],x2)),d);del x1,x2,d;return {"values":matx(tuple(map(lambda i:galg.div(galg.sub(i,c),f),x.matx)),False,'c'),"factor":f,"constant":c};
        except Exception as e:print("Invalid command: Scale.factrintrx()");retrn(ret,e);

    @classmethod
    def factrintr(cls,x:matx,i=[Decimal('0'),Decimal('1')],distribution="any distribution",ret=True)->dict:
        try:
            pass;
        except Exception as e:print("Invalid command: Scale.factrintr()");retrn(ret, e);
    
    @staticmethod
    def meansdx(x: matx, m=Decimal('0.0'), sd=Decimal('1.0'), ret=True) -> dict:
        try:
            pass
        except Exception as e:
            print("Invalid command: Scale.meansdx()")
            retrn(ret, e)
    
    @classmethod
    def meansd(x: matx, m=Decimal('0.0'), sd=Decimal('1.0'), ret=True) -> dict:
        try:
            pass
        except Exception as e:
            print("Invalid command: Scale.meansd()")
            retrn(ret, e)

    # scale matx between [0, 1]
    @classmethod
    def _scale0to1x(cls, x: matx, ret='a') -> dict:
        try:
            x = matutils.tpose(x, False, 'c')
            mx = list()
            mn = list()
            for i in x.matx:
                mn.append(min(i))
            x = matutils.msub(x, matx(tuple([tuple([mn[i] for _ in range(x.rowlen)]) for i in range(x.collen)]), False, 'c'), False, 'c')
            for i in x.matx:
                mx.append(max(i))
            x = matutils.tpose(matutils.smultfac(tuple([1/ i for i in mx]), x, True, False, 'c'), False, 'c')
            if x is None:
                raise Exception
            return {"constant": matx(tuple(mn), False, 'c'), "factor": matx(tuple(mx), False, 'c'), "values": x}
        except Exception as e:
            print("Invalid command: Scale._scale0to1x()")
            retrn(ret, e)

    # scale data values between [0,1]
    @classmethod
    def _scale0to1(cls, d: data, ret='a') -> dict:
        try:
            x = cls._scale0to1x(d.getax(), 'c')
            y = cls._scale0to1x(d.getay(), 'c')
            if x is None or y is None:
                raise Exception
            return {"constant": matutils.addmatx(x["constant"], y["constant"], chk=False, ret='c'),
                    "factor": matutils.addmatx(x["factor"], y["factor"], chk=False, ret='c'),
                    "data": data(x["values"], y["values"], False, 'c')}
        except Exception as e:
            print("Invalid command: Scale._scale0to1()")
            retrn(ret, e)


class _Output:
    # save the regression output
    @classmethod
    def _save(cls, li: str, d: dict, k: str) -> None:
        try:
            with open(li, 'r') as f:
                dic = json.load(f)
            dic[k] = cls.__chktuple(d)
            with open(li, 'w') as f:
                json.dump(dic, f)
        except Exception as e:
            print("Invalid command: _Output._save()")
            retrn('c', e)

    @classmethod
    def __chktuple(cls, d: dict) -> dict:
        try:
            dic = dict()
            for i in d.keys():
                if type(d[i]) == dict:
                    if type(i) != tuple:
                        dic.update({i: cls.__chktuple(d[i])})
                    else:
                        dic.update({str(i): cls.__chktuple(d[i])})
                else:
                    if type(i) != tuple:
                        dic.update({i: d[i]})
                    else:
                        dic.update({str(i): d[i]})
            return dic
        except Exception as e:
            print("Invalid command: _Output._chktuple()")
            retrn('c', e)


class _getData:
    # transform json data into data object for regression
    @staticmethod
    def _regression(li: str) -> data:
        try:
            with open(li, 'r') as f:
                dic = json.load(f)
            x = list()
            y = list()
            for i in dic["points"].values():
                x.append(i[0])
                y.append([i[1]])
            return data(x, y)
        except Exception as e:
            print("Invalid command: _getData._regression()")
            retrn('c', e)

    # transform json data into data object for classification
    @classmethod
    def _classification(cls, li: str) -> dict:
        try:
            with open(li, 'r') as f:
                dic = json.load(f)
            d = dict()
            for i, j in dic["classes"].items():
                for k, l in dic["classes"].items():
                    if k > i:
                        d[(i, k)] = cls._clasdata(j, l)
            return d
        except Exception as e:
            print("Invalid command: _getData._classification()")
            retrn('c', e)

    @staticmethod
    def _clasdata(x1: list, x2: list) -> data:
        try:
            return data(x1 + x2, [[0.0] for _ in range(len(x1))] + [[1.0] for _ in range(len(x2))])
        except Exception as e:
            print("Invalid command: _getData._clasdata()")
            retrn('c', e)

    @staticmethod
    def _regdata(y: list, x: tuple) -> data:
        try:
            lx = list()
            for i in x:
                lx.append(i)
            return data(matutils.tpose(matx(lx)).matx, y)
        except Exception as e:
            print("Invalid command: _getData._regdata()")
            retrn('c', e)


class Results(_Output):
    @classmethod
    def save(cls, d: dict, li: str, k: str, ret='a') -> None:
        try:
            _Output._save(li, d, k)
        except Exception as e:
            print("Invalid command: Results.save()")
            retrn(ret, e)


class GetData(_getData):
    @classmethod
    def regression(cls, li: str, ret='a') -> data:
        try:
            return _getData._regression(li)
        except Exception as e:
            print("Invalid command: GetData.regression()")
            retrn(ret, e)

    @classmethod
    def classification(cls, li: str, ret='a') -> dict:
        try:
            return _getData._classification(li)
        except Exception as e:
            print("Invalid command: GetData.classification()")
            retrn(ret, e)

    @classmethod
    def regdata(cls, y: list, *x: list, ret='a') -> data:
        try:
            return _getData._regdata(y, x)
        except Exception as e:
            print("Invalid command: GetData.regdata()")
            retrn(ret, e)

    @classmethod
    def clasdata(cls, c0: list, c1: list, ret='a') -> data:
        try:
            return _getData._clasdata(c0, c1)
        except Exception as e:
            print("Invalid command: GetData.clasdata()")
            retrn(ret, e)


class Parameter:
    @staticmethod
    def parlogreg(d: dict, p: list, ret='a') -> dict:
        try:
            if tdict.dic(d) is None:
                raise Exception
            if (p := tdeciml.dall(p)) is None:
                raise Exception
            if tdata(list(d.values()), True) is None:
                raise Exception
            pd = dict()
            for i in enumerate(d.keys()):
                pd[i[1]] = p[i[0]]
            return pd
        except Exception as e:
            print("Invalid command: Parameter.parlogreg()")
            retrn(ret, e)

    @staticmethod
    def parlogregter(d: dict, ret='a') -> dict:
        try:
            if tdict.dic(d) is None:
                raise Exception
            if tdata(list(d.values()), True) is None:
                raise Exception
            pd = dict()
            for i in d.keys():
                print("class: " + str(i) + "\n")
                p = list()
                for j in range(d[i].xvars + 1):
                    par = input("parameter " + str(j) + "\n")
                    try:
                        par = deciml(str(par))
                    except ValueError:
                        raise Exception(str(par) + " is not float")
                    if par is None:
                        raise Exception
                    p.append(par)
                if p is None:
                    raise Exception
                pd[i] = p
            return pd
        except Exception as e:
            print("Invalid command: Parameter.parlogregter()")
            retrn(ret, e)


# d = GetData.clasdata([[0, 1, 2], [2, 1, 2], [2, 1, 5]], [[2, 4, 5], [5, 6, 8]])
# d.pdata
# p = Parameter.parlogregter({('0', '1'): d})
# print(p)
# p = Parameter.parlogreg({('0', '1'): d}, [[1,2,3],])
# print(p)
# d = GetData.regdata([1, 2, 3, 4], [1, 2, 3, 4], [2, 4, 6, 8], [1, 4, 9, 16], [4, 5, 9, 8])
# d.pdata
print(Scale.factrintrx(matx([[1,2,3],[2,3,9],[3,4,6]])))
