from deciml.deciml import deciml, constant as cnst, algbra as alg, stat, Decimal
from compare.cmpr import eqval, tdict, tdata
from terminate import retrn
from deciml_maths.matrix import matx, matutils
from deciml_maths.data import data


class _Predict:
    
    # returns True for y=1 and False for y=0
    @staticmethod
    def _y(x: matx, d: dict, ret='a') -> int:
        try:
            if (dif := [matutils.msub(x, matx(i, True, 'c'), False, 'c') for i in d["mean"]]) is None:
                raise Exception
            if (cov := matx(d["cov"], True, 'c')) is None:
                raise Exception
            e, pi = cnst.e(), cnst.pi()
            if (dn := alg.mul(alg.pwr(alg.mul(2, pi), alg.div(d["n"], 2)), alg.pwr(matutils.dnant(cov, False, 'c'), 0.5))) is None:
                raise Exception
            h = [alg.mul(d["phi"][i[0]], alg.div(alg.pwr(e, alg.div(matutils.mmult(matutils.mmult(i[1], cov.invse(), False, 'c'), matutils.tpose(i[1]), False, 'c').matx[0][0], -2)), dn)) for i in enumerate(dif)]
            if h is None:
                raise Exception
            if h[0] > h[1]:
                return 0
            else:
                return 1
        except Exception as e:
            print("Invalid command: _Predict._y()")
            retrn(ret, e)
    
    @staticmethod
    def _ally(x: matx, d: dict, ret='a') -> tuple[int, ...]:
        try:
            if (dif := [matutils.saddcnst([alg.mul(-1, j) for j in i], x, False, False, 'c') for i in d["mean"]]) is None:
                raise Exception
            if (cov := matx(d["cov"], True, 'c')) is None:
                raise Exception
            e, pi = cnst.e(), cnst.pi()
            if (dn := alg.mul(alg.pwr(alg.mul(2, pi), alg.div(d["n"], 2)), alg.pwr(matutils.dnant(cov, False, 'c'), 0.5))) is None:
                raise Exception
            r = list()
            d0, d1 = [[alg.mul(d["phi"][i[0]], alg.div(alg.pwr(e, alg.div(k, -2)), dn)) for k in [matutils.mmult(matutils.mmult(j, cov.invse()), matutils.tpose(j)).matx[0][0] for j in matutils.matlxtox(i[1], False, 'c')]] for i in enumerate(dif)]
            for i in range(len(d0)):
                if d0[i] > d1[i]:
                    r.append(0)
                else:
                    r.append(1)
            return tuple(r)
        except Exception as e:
            print("Invalid command: _Predict._ally()")
            retrn(ret, e)


class PGDA(_Predict):
    
    @classmethod
    def y(cls, x: list, d: dict, ret='a') -> int:
        try:
            if tdict.dic(d) is None:
                raise Exception
            x = matx(x, ret='c')
            if x is None:
                raise Exception
            if eqval(d["n"], x.rowlen) is None:
                raise Exception
            return _Predict._y(x, d, 'c')
        except Exception as e:
            print("Invalid command: Predict.y()")
            retrn(ret, e)
    
    @classmethod
    def ally(cls, x: tuple[list | tuple] | list[list | tuple], d: dict, ret='a') -> tuple[int, ...]:
        try:
            if tdict.dic(d) is None:
                raise Exception
            x = matx(x, ret='c')
            if x is None:
                raise Exception
            if eqval(d["n"], x.rowlen) is None:
                raise Exception
            return _Predict._ally(x, d, 'c')
        except Exception as e:
            print("Invalid command: Predict.ally()")
            retrn(ret, e)

    @classmethod
    def clas(cls, x: list, d: dict, ret='a') -> int:
        try:
            if tdict.dic(d) is None:
                raise Exception
            c = dict()
            for i in d.items():
                if (cl := cls.y(x, i[1], 'c')) is None:
                    raise Exception
                if cl == 1:
                    c[i[0][1]] = c.setdefault(i[0][1], 0) + 1
                else:
                    c[i[0][0]] = c.setdefault(i[0][0], 0) + 1
            mx = 0
            mc = 0
            for i in c.items():
                if i[1] > mx:
                    mx = i[1]
                    mc = i[0]
            return mc
        except Exception as e:
            print("Invalid command: Predict.clas()")
            retrn(ret, e)
    
    @classmethod
    def allclas(cls, x: tuple[list | tuple] | list[list | tuple], d: dict, ret='a') -> dict:
        try:
            if tdict.dic(d) is None:
                raise Exception
            r1 = dict()
            x = matutils.matlxtox(x, False, 'c')
            for i in d.items():
                if (cl := cls.ally(x, i[1], 'c')) is not None:
                    for j in enumerate(cl):
                        r1[x[j[0]]] =  r1.setdefault(x[j[0]], []) + [i[0][j[1]], ]
                else:
                    raise Exception
            r = list()
            return tuple([stat.mode(r1[tuple(i)]) for i in x])
        except Exception as e:
            print("Invalid command: Predict.allclas()")
            retrn(ret, e)


class _Calculate(_Predict):

    # misclassifications after classification
    @classmethod
    def _misclassed(cls, d: tuple, d1: dict, const: tuple[bool, bool], ret='a') -> dict:
        try:
            dic, y = dict(), _Predict._ally(d[0], d1, 'c')
            dic.setdefault("0", [0, 0, []])
            dic.setdefault("1", [0, 0, []])
            for i in range(d[1].collen):
                if d[1].mele(i, 0, False, 'c') == 0:
                    dic["0"][0] += 1
                    if y[i] == 1:
                        dic["0"][1] += 1
                        dic["0"][2].append([str(j) for j in d[0][i].matxl()[0]])
                else:
                    dic["1"][0] += 1
                    if y[i] == 0:
                        dic["1"][1] += 1
                        dic["1"][2].append([str(j) for j in d[0][i].matxl()[0]])
            return dic
        except Exception as e:
            print("Invalid command: _Calculate._misclassed()")
            retrn(ret, e)

    # returns mean x and phi for GDA
    @staticmethod
    def _meanx_phi(d: tuple, ret='a') -> dict:
        try:
            y1, y2 = 0, 0
            d = (matutils.matlxtox(d[0], False, 'c'), d[1])
            lx = d[0][0].rowlen
            x1, x2 = matutils.eqelm(1, lx, Decimal('0.0'), False, 'c'), matutils.eqelm(1, lx, Decimal('0.0'), False, 'c')
            for i in range(d[1].collen):
                if d[1].mele(i, 0, False, 'c') == 0:
                    y1 += 1
                    x1.matx = matutils.madd(x1, d[0][i], False, 'c')
                else:
                    x2.matx = matutils.madd(x2, d[0][i], False, 'c')
                    y2 += 1
            y1, y2 = deciml(y1), deciml(y2)
            return {"mean": [matutils.smult(1 / y1, x1, False, 'c').matxl()[0], matutils.smult(1 / y2, x2, False, 'c').matxl()[0]],
                    "phi": [y1 / (y1 + y2), y2 / (y1 + y2)]}
        except Exception as e:
            print("Invalid command: _Calculate._meanx_phi()")
            retrn(ret, e)

    # returns covariance and n for GDA
    @staticmethod
    def _cov_n(d: tuple, x1: matx, x2: matx, ret='a') -> dict:
        try:
            d = (matutils.matlxtox(d[0], False, 'c'), d[1])
            xl = d[0][0].rowlen
            cov = matutils.eqelm(xl, xl, Decimal('0.0'), False, 'c')
            for i in range(d[1].collen):
                if d[1].mele(i, 0, False, 'c') == 0:
                    xd = matutils.msub(d[0][i], x1, False, 'c')
                    cov.matx = matutils.madd(cov, matutils.mmult(matutils.tpose(xd, False, 'c'), xd, False, 'c'), False, 'c')
                else:
                    xd = matutils.msub(d[0][i], x2, False, 'c')
                    cov.matx = matutils.madd(cov, matutils.mmult(matutils.tpose(xd, False, 'c'), xd, False, 'c'), False, 'c')
            return {"cov": matutils.smult(alg.div(1, d[1].collen), cov, False, 'c').matxl(), "n": xl}
        except Exception as e:
            print("Invalid command: _Calculate._cov_n()")
            retrn(ret, e)


def _gda(d: data, ret='a') -> dict:
    try:
        d = d.data
        if (dic1 := _Calculate._meanx_phi(d, 'c')) is None:
            raise Exception
        if (dic2 := _Calculate._cov_n(d, matx(dic1["mean"][0]), matx(dic1["mean"][1]), 'c')) is None:
            raise Exception
        dic1.update(dic2)
        if (miscl := _Calculate._misclassed(d, dic1, None, 'c')) is None:
            raise Exception
        dic1.setdefault("misclassifications", miscl)
        dic1.update({"mean": [[str(j) for j in i] for i in dic1["mean"]], "cov": [[str(j) for j in i] for i in dic1["cov"]], "phi": [str(i) for i in dic1["phi"]]})
        return dic1
    except Exception as e:
        print("Invalid command: _gda()")
        retrn(ret, e)


class GDA:
    
    @staticmethod
    def gda(d: data, ret='a') -> dict:
        try:
            if tdata(d) is None:
                raise Exception
            return _gda(d, 'c')
        except Exception as e:
            print("Invalid command: GDA.gda()")
            retrn(ret, e)

    @classmethod
    def gdagc(cls, d: dict, ret='a') -> dict:
        try:
            dic = dict()
            for i in d.items():
                dic[i[0]] = cls.gda(i[1], 'c')
            return dic
        except Exception as e:
            print("Invalid command: GDA.gdagc()")
            retrn(ret, e)


a = GDA.gda(
   data([[10, 10, 10], [5, 7, 9], [4, 2, 7], [5, 9, 1], [20, 20, 20], [21, 25, 22], [14, 18, 12], [12, 15, 11]],
        [[0], [0], [0], [0], [1], [1], [1], [1]]))
print(a)
