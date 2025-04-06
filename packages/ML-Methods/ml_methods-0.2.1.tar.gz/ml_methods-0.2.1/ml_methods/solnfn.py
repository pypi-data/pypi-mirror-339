from deciml_maths.functions import funcutils, poly
from deciml_maths.matrix import matutils, matx
from deciml.deciml import algbra as alg, abs
from compare.cmpr import eqval, tint
from terminate import retrn


class SolveFn:
    
    @classmethod
    def rootrearr(cls,fn,pos:int,x:list|matx,m=100,pr=0.01,ret='a')->dict:
        try:
            if (x:=matx(x,ret='c')) is None or eqval(x.collen,1) is None or (pos:=tint.int(pos)) is None or (fnr:=funcutils.rearr(fn,pos,'c')) is None:raise Exception;
            xn = list()
            for i in x.matx[0]:
                try:
                    dfnr=abs(fnr.dval(i))
                    if dfnr>0:
                        if dfnr>1:continue;
                    xn.append(i)
                except ArithmeticError:continue;
                except TypeError:continue;
            if len(xn)==0:raise Exception;
            value = dict()
            for i in xn:
                xi=i;c=-1;
                while (c:=c+1)!=m:
                    val=fnr.val(xi);valy=fn.val(val);
                    if str(valy)=='NaN':break;
                    if abs(valy)<pr or c==m:value[str(i)]=(str(val),c,);break;
                    else:xi=val;
            return value
        except Exception as e:print("Invalid command: SolveFn.rootrearr()");retrn(ret,e);
    
    @classmethod
    def lininter(cls,fn,x:list|matx,m=100,pr=0.01,ret='a')->dict:
        try:
            if (x:=matx(x,ret='c')) is None or eqval(x.rowlen,2) is None:raise Exception;
            x=x.matx;value=dict();
            for i in x:
                c=-1;p1=(i[0],fn.val(i[0]));p2=(i[1],fn.val(i[1]));
                if (p1[1]>0 and p2[1]<0) or (p1[1]<0 and p2[1]>0):
                    while (c:=c+1)<m:
                        valx=alg.add(alg.div(alg.mul(alg.sub(p1[0],p2[0]),alg.mul(-1,p1[1])),alg.sub(p1[1],p2[1])),p1[0]);p3=(valx,fn.val(valx));
                        if str(p3[1]) == 'NaN':break;
                        if abs(p3[1])<pr or c==m:value[str(i)]=(str(p3[0]),c,);break;
                        if p1[1]*p3[1]<0:p2=p3;
                        else:p1=p3;
            return value
        except Exception as e:print("Invalid command: SolveFn.lininter()");retrn(ret,e);
    
    @classmethod
    def bchop(cls,fn,x:list|matx,m=100,pr=0.01,ret='a')->dict:
        try:
            if (x:=matx(x,ret='c')) is None or eqval(x.rowlen,2) is None:raise Exception;
            x=x.matx;value=dict();
            for i in x:
                c=-1;p1=(i[0],fn.val(i[0]));p2=(i[1],fn.val(i[1]));
                if (p1[1]>0 and p2[1]<0) or (p1[1]<0 and p2[1]>0):
                    while (c:=c+1)<m:
                        mid=alg.div(alg.add(p1[0],p2[0]),2);p3=(mid,fn.val(mid));
                        if str(p3[1])=='NaN':break;
                        if abs(p3[1])<pr or c==m:value[str(i)]=(str(p3[0]),c,);break;
                        if (p1[1]>0 and p3[1]<0) or (p1[1]<0 and p3[1]>0):p2=p3;
                        else:p1=p3;
            return value
        except Exception as e:print("Invalid command: SolveFn.bchop()");retrn(ret,e);

    @classmethod
    def nrinter(cls,fn,x:list|matx,m=100,pr=0.01,ret='a')->dict:
        try:
            if (x:=matx(x,ret='c')) is None or eqval(x.collen,1) is None:raise Exception;
            value = dict()
            for i in x.matx[0]:
                try:
                    c=-1
                    nx=i;nxv=fn.val(nx);
                    while (c:=c+1)<m:
                        nx=alg.sub(nx,alg.div(nxv,fn.dval(nx)))
                        if (nxv:=fn.val(nx))<pr:value[str(i)]=(str(nx),c,);break;
                except:continue;
            return value
        except Exception as e:print("Invalid command: SolveFn.nrinter()");retrn(ret,e);


for j in range(1):
    d = {'Al_LowCutoff': {'parameters': [16.058881741715595, -8.955601539113559, 1.0939627709012711],
                          'r^2': 0.9983192621607382, 'r^2_adj': 0.9978390513495206},
        'Al_HighCutoff': {'parameters': [15.811508555198088, -8.971596025396138, 1.1032308384019416],
                           'r^2': 0.998828056926424, 'r^2_adj': 0.9984932160482594},
        'Al_MedCutoff': {'parameters': [15.946995875099674, -9.0157831403194, 1.107305156358052],
                          'r^2': 0.9988916677797752, 'r^2_adj': 0.9985750014311395}}
    p = dict()
    for i in d.items():
        p[i[0]] = poly([i[1]["parameters"], [0, 1, 2]])
    for i in p.items():
        p[i[0]] = funcutils.ndpoly(i[1], 1)
    for i in p.items():
        p[i[0]] = SolveFn.nrinter(i[1], [-10, 0, 10], 1000, 0.001)
    print(p)
    p = SolveFn.rootrearr(poly([[4, -4, 1], [0, 1, 2]]), 2, [i - 5 for i in range(10)], 1000, 0.001)
    print(p)
