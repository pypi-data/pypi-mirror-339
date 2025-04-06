from deciml.deciml import deciml, algbra as alg, constant as cnst, Decimal
from terminate import retrn
from compare.cmpr import eqval, tdata, tdeciml, tint
from deciml_maths.matrix import matx, matutils, matstat
from deciml_maths.data import data, datautils
from algoutils import parameter, function, Scale, Calculate, GetData
from linsys import Method


class _Predict:

    @staticmethod
    def _ygp(x: matx, p: matx, p1: parameter, const=(False, True), ret='a') -> Decimal:
        try:
            match const[1]:
                case True:
                    x = matutils.maddval(x, Decimal('1.0'), False, 'c')
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            x = matutils.dpose(x, p1.n, chk=False, ret='c')
            match const[0]:
                case False:
                    return  p1.val(p)
                case True:
                    p = matx(p, False, 'c')
                    p0 = p.pop(0, False, False, 'c')[0]
                    return alg.mul(p0, alg.addl([matutils.mmult(i[1], x[i[0]], False, 'c').matx[0][0] for i in enumerate(p1.val(p))]))
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
        except Exception as e:
            print("Invalid command: _Predict._ygp()")
            retrn(ret, e)

    @staticmethod
    def _allygp(x: matx, p: matx, p1: parameter, const: tuple[bool, bool], ret='a') -> matx:
        try:
            match const[1]:
                case False:
                    pass
                case True:
                    x = matutils.maddval(x, Decimal('1.0'), False, 'c')
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            x = function(matutils.dpose(x, p1.n, False, False, 'c'), False, 'c')
            match const[0]:
                case False:
                    p = p1.val(p)
                    return matx(tuple([(alg.addl(i), ) for i in x.val(p).matx]), False, 'c')
                case True:
                    p = matx(p, False, 'c')
                    p0 = p.pop(0, False, False, 'c')
                    return matx(tuple([(alg.mul(p0, alg.addl(i)), ) for i in x.val(p).matx]), False, 'c')
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
        except Exception as e:
            print("Invalid command: _Predict._allygp()")
            retrn(ret, e)
    
    # returns predicted value of y for linear regression
    @staticmethod
    def _y(x: matx, p: matx, const: tuple[bool, bool], ret='a') -> Decimal:
        try:
            match const[1]:
                case True:
                    x = matutils.maddval(x, Decimal('1.0'), False, 'c')
                case False:
                    pass
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            match const[0]:
                case False:
                    return matutils.mmult(p, matutils.tpose(x, False, 'c'), False, 'c').matx[0][0]
                case True:
                    p = matx(p, False, 'c')
                    p0 = p.pop(0, False, False, 'c')[0]
                    return alg.mul(p0, matutils.mmult(p, matutils.tpose(x, False, 'c'), False, 'c').matx[0][0])
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
        except Exception as e:
            print("Invalid command: _Predict._y()")
            retrn(ret, e)
    
    # returns actual and predicted y
    @staticmethod
    def _ally(x: matx, p: matx, const: tuple[bool, bool], ret='a') -> matx:
        try:
            match const[1]:
                case False:
                    match const[0]:
                        case False:
                            return matutils.tpose(matutils.mmult(p, matutils.tpose(x), False, 'c'))
                        case True:
                            p = matx(p, False, 'c')
                            p0 = p.pop(0, False, False, 'c')[0]
                            return matutils.tpose(matutils.smult(p0, matutils.mmult(p, matutils.tpose(x), False, 'c'), False, 'c'))
                        case _:
                            raise Exception("Invalid argument: const => (bool, bool)")
                case True:
                    match const[0]:
                        case False:
                            return matutils.tpose(matutils.mmult(p, matutils.tpose(matutils.maddval(x, Decimal('1.0'), False, 'c')), False, 'c'))
                        case True:
                            p = matx(p, False, 'c')
                            p0 = p.pop(0, False, False, 'c')[0]
                            return matutils.tpose(matutils.smult(p0, matutils.mmult(p, matutils.tpose(matutils.maddval(x, Decimal('1.0'), False, 'c')), False, 'c'), False, 'c'))
                        case _:
                            raise Exception("Invalid argument: const => (bool, bool)")
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
        except Exception as e:
            print("Invalid command: _Predict._ally()")
            retrn(ret, e)


class PLinReg(_Predict):
    
    @classmethod
    def allygp(cls, x: list[list | tuple] | tuple[list, tuple], p: list, cfp: list[list[list]] | tuple[tuple[tuple[float | Decimal | int, float | Decimal | int], ...], ...], const=(False, True), ret='a') -> matx:
        try:
            if (x := matx(x, ret='c')) is None or (p1 := parameter(cfp, True, 'c')) is None or (p := matx(p, ret='c')) is None:
                raise Exception
            match const:
                case (True, True):
                    if sum(p1.n) != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 2))
                    if eqval(len(p1.n), p.rowlen - 1) is None:
                        raise Exception
                case (False, True):
                    if sum(p1.n) != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                    if eqval(len(p1.n), p.rowlen) is None:
                        raise Exception
                case (True, False):
                    if sum(p1.n) != x.rowlen:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                    if eqval(len(p1.n), p.rowlen - 1) is None:
                        raise Exception
                case (False, False):
                    if sum(p1.n) != x.rowlen:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen))
                    if eqval(len(p1.n), p.rowlen) is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            return _Predict._allygp(x, p, p1, const, 'c')
        except Exception as e:
            print("Invalid command: PLinReg.allygp()")
            retrn(ret, e)
    
    @classmethod
    def ygp(cls, x: list, p: list, cfp: list[list[list]] | tuple[tuple[tuple[float | Decimal | int, float | Decimal | int], ...], ...], const=(False, True), ret='a') -> Decimal:
        try:
            if (x := matx(x, ret='c')) is None or (p := matx(p, ret='c')) is None or (p1 := parameter(cfp, True, 'c')) is None:
                raise Exception
            match const:
                case (True, True):
                    if sum(p1.n) != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 2))
                    if eqval(len(p1.n), p.rowlen - 1) is None:
                        raise Exception
                case (False, True):
                    if sum(p1.n) != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                    if eqval(len(p1.n), p.rowlen) is None:
                        raise Exception
                case (True, False):
                    if sum(p1.n) != x.rowlen:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                    if eqval(len(p1.n), p.rowlen - 1) is None:
                        raise Exception
                case (False, False):
                    if sum(p1.n) != x.rowlen:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen))
                    if eqval(len(p1.n), p.rowlen) is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            return _Predict._ygp(x, p, p1, const, 'c')
        except Exception as e:
            print("Invalid command: PLinReg.ygp()")
            retrn(ret, e)
    
    @classmethod
    def ally(cls, x: list[list | tuple] | tuple[list | tuple], p: list, const=(False, True), ret='a') -> matx:
        try:
            if (x := matx(x, ret='c')) is None or (p := matx(p, ret='c')) is None:
                raise Exception
            match const:
                case (True, True):
                    if p.rowlen != x.rowlen + 2:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 2))
                case (False, True):
                    if p.rowlen != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                case (True, False):
                    if p.rowlen != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                case (False, False):
                    if p.rowlen != x.rowlen:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen))
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            return _Predict._ally(x, p, const, 'c')
        except Exception as e:
            print("Invalid command: PLinReg.ally()")
            retrn(ret, e)

    @classmethod
    def y(cls, x: list, p: list, const=(False, True), ret='a') -> Decimal:
        try:
            if (p := matx(p, ret='c')) is None or (x := matx(x, ret='c')) is None:
                raise Exception
            match const:
                case (True, True):
                    if p.rowlen != x.rowlen + 2:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 2))
                case (False, True):
                    if p.rowlen != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                case (True, False):
                    if p.rowlen != x.rowlen + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen + 1))
                case (False, False):
                    if p.rowlen != x.rowlen:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(x.rowlen))
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            return _Predict._y(p, x, const, 'c')
        except Exception as e:
            print("Invalid command: PLinReg.y()")
            retrn(ret, e)


class _ScalePar:

    # scale parameter values for linear regression
    @staticmethod
    def _0to1(c: matx, f: matx, p: matx, const=True, ret='a') -> matx:
        try:
            c = matx(c, False, 'c')
            f = matx(f, False, 'c')
            match const:
                case True:
                    g = f.pop(-1, False, False, 'c')[0]
                    d, p = alg.div(c.pop(-1, False, False, 'c')[0], g), matutils.smult(alg.div(1, g), p, False, 'c')
                    p0 = (alg.add(p.pop(0, False, False, 'c')[0], alg.sub(alg.addl(matutils.smultfac(p.matx[0], c, False, False, 'c').matx[0]), d)), )
                    return matx((p0, ) + matutils.smultfac(f.matx[0], p, False, False, 'c').matx[0], False, 'c')
                case False:
                    p = matutils.smult(alg.div(1, f.pop(-1, False, False, 'c')[0]), p, False, 'c')
                    return matutils.smultfac(f.matx[0], p, False, False, 'c')
                case _:
                    raise Exception("Invalid argument: const => bool")
        except Exception as e:
            print("Invalid command: _ScalePar._0to1()")
            retrn(ret, e)

    @staticmethod
    def _orignl(c: matx, f: matx, p: matx, const=True, ret='a') -> matx:
        try:
            c = matx(c, False, 'c')
            f = matx(f, False, 'c')
            match const:
                case True:
                    p = matutils.smult(f.pop(-1, False, False, 'c')[0], p, False, 'c')
                    p0 = alg.add(p.pop(0, False, False, 'c')[0], c.pop(-1, False, False, 'c')[0])
                    p = matutils.smultfac(tuple([alg.div(1, i) for i in f.matx[0]]), p, False, False, 'c')
                    p0 = alg.sub(p0, matutils.mmult(p, matutils.tpose(c, False, 'c'), False, 'c').matx[0][0])
                    return matx((p0, ) + p.matx[0], False, 'c')
                case False:
                    p = matutils.smult(f.pop(-1, False, False, 'c')[0], p, False, 'c')
                    p = matutils.smultfac(tuple([alg.div(1, i) for i in f.matx[0]]), p, False, False, 'c')
                    return matx(p, False, 'c')
                case _:
                    raise Exception("Invalid argument: const => bool")
        except Exception as e:
            print("Invalid command: _ScalePar._orignl()")
            retrn(ret, e)


class _Calculate(_Predict):

    # returns weights for weighted regression
    @staticmethod
    def _weights(x: matx, xm: tuple[Decimal, ...], t: Decimal, ret='a') -> tuple[Decimal, ...]:
        try:
            e, c = cnst.e(), alg.div(-1, alg.pwr(t, 2))
            return tuple([alg.pwr(e, alg.mul(c, k)) for k in [alg.addl(alg.lmul(j, j)) for j in matutils.saddcnst([alg.mul(-1, i) for i in xm], x, False, False, 'c').matx]])
        except Exception as e:
            print("Invalid command: _Calculate._weights()")
            retrn(ret, e)
    
    # returns coefficient of determination for regression
    @classmethod
    def _coofdet(cls, d: tuple, p: matx, const: tuple[bool, bool], ret='a') -> Decimal:
        try:
            y = _Predict._ally(d[0], p, const, ret='c')
            ym = alg.mul(-1, matstat.amean(d[1], 'all', False, 'c'))
            return alg.div(alg.addl([alg.pwr(i[0], 2) for i in matutils.saddcnst([ym, ], y, False, False, 'c').matx]), alg.addl([alg.pwr(i[0], 2) for i in matutils.saddcnst([ym, ], d[1], False, False, 'c').matx]))
        except Exception as e:
            print("Invalid command: _Calculate._coofdet()")
            retrn(ret, e)
    
    @classmethod
    def _coofdetgp(cls, d: tuple, p: matx, p1: parameter, const: tuple[bool, bool], ret='a') -> Decimal:
        try:
            y = _Predict._allygp(d[0], p, p1, const, ret='c')
            ym = alg.mul(-1, matstat.amean(d[1], 'all', False, 'c'))
            return alg.div(alg.addl([alg.pwr(i[0], 2) for i in matutils.saddcnst([ym, ], y, False, False, 'c').matx]), alg.addl([alg.pwr(i[0], 2) for i in matutils.saddcnst([ym, ], d[1], False, False, 'c').matx]))
        except Exception as e:
            print("Invalid command: _Calculate._coofdetgp()")
            retrn(ret, e)


class _Grades(_ScalePar, Calculate):
    
    @classmethod
    def _linreg(cls, d: tuple, p: matx, a, m, pr, const: tuple[bool, bool], ret='a') -> tuple[matx, int]:
        try:
            const, c, a = const[0], 0, alg.mul(-1, a)
            m += 1
            while (c := c + 1) != m:
                match const:
                    case False:
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(a, matutils.mmult(d[0], matutils.tpose(matutils.msub(matutils.mmult(p, d[0], False, 'c'), d[1], False, 'c'), False, 'c'), False, 'c'), False, 'c'), False, 'c'), False, 'c')
                    case True:
                        p1 = matx(p, False, 'c')
                        p0 = p1.pop(0, False, False, 'c')[0]
                        dm = matutils.tpose(matutils.msub(matutils.smult(p0, matutils.mmult(p1, d[0], False, 'c'), False, 'c'), d[1], False, 'c'), False, 'c')
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(a, matutils.addmatx(matutils.mmult(matutils.mmult(p1, d[0], False, 'c'), dm, False, 'c'), matutils.mmult(matutils.smult(p0, d[0], False, 'c'), dm, False, 'c'), True, False, 'c'), False, 'c'), False, 'c'), False, 'c')
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")        
                if pn is None:
                    raise Exception
                err = Calculate._cmperrpr(p, pn, pr, 'c')
                match err:
                    case True:
                        return pn, c
                    case False:
                        p.matx = pn
                    case _:
                        raise Exception
            return pn, c - 1
        except Exception as e:
            print("Invalid command: _Grades._linreg()")
            retrn(ret, e)
    
    @classmethod
    def _linregsp(cls, d: tuple, p: matx, a, m, pr, cf: tuple[matx, matx], const: tuple[bool, bool], ret='a') -> tuple[matx, int]:
        try:
            scc, scf = cf
            if const[1] is True:
                cn = matx(scc.matx[0][:-1] + (Decimal('0.0'), ), False, 'c')
            c, a = 0, alg.mul(-1, a)
            m += 1
            while (c := c + 1) != m:
                match const[0]:
                    case False:
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(a, matutils.mmult(d[0], matutils.tpose(matutils.msub(matutils.mmult(p, d[0], False, 'c'), d[1], False, 'c'), False, 'c'), False, 'c'), False, 'c'), False, 'c'), False, 'c')
                    case True:
                        p1 = matx(p, False, 'c')
                        p0 = p1.pop(0, False, False, 'c')[0]
                        dm = matutils.tpose(matutils.msub(matutils.smult(p0, matutils.mmult(p1, d[0], False, 'c'), False, 'c'), d[1], False, 'c'), False, 'c')
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(a, matutils.addmatx(matutils.mmult(matutils.mmult(p1, d[0], False, 'c'), dm, False, 'c'), matutils.mmult(matutils.smult(p0, d[0], False, 'c'), dm, False, 'c'), True, False, 'c'), False, 'c'), False, 'c'), False, 'c')
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")        
                if pn is None:
                    raise Exception
                match const[0]:
                    case False:
                        op = _ScalePar._orignl(scc, scf, p, const[1], 'c')
                        opn = _ScalePar._orignl(scc, scf, pn, const[1], 'c')
                        if op is None or opn is None:
                            raise Exception
                    case True:
                        match const[1]:
                            case False:
                                op = matutils.maddval(_ScalePar._orignl(scc, scf, matx(p.matx[0][1:], False, 'c'), False, 'c'), p.mele(0, 0, False, 'c'), False, 'c')
                                opn = matutils.maddval(_ScalePar._orignl(scc, scf, matx(pn.matx[0][1:], False, 'c'), False, 'c'), p.mele(0, 0, False, 'c'), False, 'c')
                                if op is None or opn is None:
                                    raise Exception
                            case True:
                                op = matutils.maddval(_ScalePar._orignl(cn, scf, matx(p.matx[0][1:], False, 'c'), True, 'c'), p.mele(0, 0, False, 'c'), False, 'c')
                                opn = matutils.maddval(_ScalePar._orignl(cn, scf, matx(pn.matx[0][1:], False, 'c'), True, 'c'), p.mele(0, 0, False, 'c'), False, 'c')
                                if op is None or opn is None:
                                    raise Exception
                            case _:
                                raise Exception("Invalid argument: const => (bool, bool)")
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                err = Calculate._cmperrpr(op, opn, pr, 'c')
                match err:
                    case True:
                        return pn, c
                    case False:
                        p.matx = pn
                    case _:
                        raise Exception
            return pn, c - 1
        except Exception as e:
            print("Invalid command: _Grades._linregsp()")
            retrn(ret, e)

    @classmethod
    def _weilinreg(cls, d: tuple, p: matx, a, m, pr, w: tuple, const: tuple[bool, bool], ret='a') -> tuple[matx, int]:
        try:
            c, a = 0, alg.mul(-1, a)
            m += 1
            while (c := c + 1) != m:
                match const[0]:
                    case False:
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(a, matutils.mmult(matutils.smultfac(w, d[0], False, False, 'c'), matutils.tpose(matutils.msub(matutils.mmult(p, d[0], False, 'c'), d[1], False, 'c'), False, 'c'), False, 'c'), False, 'c'), False, 'c'), False, 'c')
                    case True:
                        p1 = matx(p, False, 'c')
                        p0 = p1.pop(0, False, False, 'c')[0]
                        dm = matutils.tpose(matutils.msub(matutils.smult(p0, matutils.mmult(p1, d[0], False, 'c'), False, 'c'), d[1], False, 'c'), False, 'c')
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(a, matutils.addmatx(matutils.mmult(matutils.smultfac(w, matutils.mmult(p1, d[0], False, 'c'), False, False, 'c'), dm, False, 'c'), matutils.mmult(matutils.smult(p0, matutils.smultfac(w, d[0], False, False, 'c'), False, 'c'), dm, False, 'c'), True, False, 'c'), False, 'c'), False, 'c'), False, 'c')
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                if pn is None:
                    raise Exception
                err = Calculate._cmperrpr(p, pn, pr, 'c')
                match err:
                    case True:
                        return pn, c
                    case False:
                        p.matx = pn
                    case _:
                        raise Exception
            return pn, c - 1
        except Exception as e:
            print("Invalid command: _Grades._weilinreg()")
            retrn(ret, e)

    @classmethod
    def _weilinregsp(cls, d: tuple, p: matx, a, m, pr, w: tuple, cf: tuple[matx, matx], const: tuple[bool, bool], ret='a') -> tuple[matx, int]:
        try:
            scc, scf = cf
            if const[1] is True:
                cn = matx(scc.matx[0][:-1] + (Decimal('0.0'), ), False, 'c')
            c, a = 0, alg.mul(-1, a)
            m += 1
            while (c := c + 1) != m:
                match const[0]:
                    case False:
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(a, matutils.mmult(matutils.smultfac(w, d[0], False, False, 'c'), matutils.tpose(matutils.msub(matutils.mmult(p, d[0], False, 'c'), d[1], False, 'c'), False, 'c'), False, 'c'), False, 'c'), False, 'c'), False, 'c')
                    case True:
                        p1 = matx(p, False, 'c')
                        p0 = p1.pop(0, False, False, 'c')[0]
                        dm = matutils.tpose(matutils.msub(matutils.smult(p0, matutils.mmult(p1, d[0], False, 'c'), False, 'c'), d[1], False, 'c'), False, 'c')
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(a, matutils.addmatx(matutils.mmult(matutils.smultfac(w, matutils.mmult(p1, d[0], False, 'c'), False, False, 'c'), dm, False, 'c'), matutils.mmult(matutils.smult(p0, matutils.smultfac(w, d[0], False, False, 'c'), False, 'c'), dm, False, 'c'), True, False, 'c'), False, 'c'), False, 'c'), False, 'c')
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                if pn is None:
                    raise Exception
                match const[0]:
                    case False:
                        op = _ScalePar._orignl(scc, scf, p, const[1], 'c')
                        opn = _ScalePar._orignl(scc, scf, pn, const[1], 'c')
                        if op is None or opn is None:
                            raise Exception
                    case True:
                        match const[1]:
                            case False:
                                op = matutils.maddval(_ScalePar._orignl(scc, scf, matx(p.matx[0][1:], False, 'c'), False, 'c'), p.mele(0, 0, False, 'c'), False, 'c')
                                opn = matutils.maddval(_ScalePar._orignl(scc, scf, matx(pn.matx[0][1:], False, 'c'), False, 'c'), p.mele(0, 0, False, 'c'), False, 'c')
                                if op is None or opn is None:
                                    raise Exception
                            case True:
                                op = matutils.maddval(_ScalePar._orignl(cn, scf, matx(p.matx[0][1:], False, 'c'), True, 'c'), p.mele(0, 0, False, 'c'), False, 'c')
                                opn = matutils.maddval(_ScalePar._orignl(cn, scf, matx(pn.matx[0][1:], False, 'c'), True, 'c'), p.mele(0, 0, False, 'c'), False, 'c')
                                if op is None or opn is None:
                                    raise Exception
                            case _:
                                raise Exception("Invalid argument: const => (bool, bool)")
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                err = Calculate._cmperrpr(op, opn, pr, 'c')
                match err:
                    case True:
                        return pn, c
                    case False:
                        p.matx = pn
                    case _:
                        raise Exception
            return pn, c - 1
        except Exception as e:
            print("Invalid command: _Grades._weilinregsp()")
            retrn(ret, e)


class _Gradesgp(Calculate):

    @classmethod
    def _linreg(cls, d: tuple, p: matx, p1: parameter, a: Decimal, m: int, pr: Decimal, const=(False, True), ret='a') -> tuple[matx, matx, int]:
        try:
            c, a = 0, alg.mul(-1, a)
            m += 1
            while (c := c + 1) != m:
                match const[0]:
                    case False:
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(a, matutils.mmult(matutils.tpose(d[0].val(p1.dval(p)), False, 'c'), matutils.msub(matx(tuple([(alg.addl(i),) for i in d[0].val(p1.val(p)).matx]), False, 'c'), d[1], False, 'c'), False, 'c'), False, 'c'), False, 'c'), False, 'c')
                    case True:
                        pn = matx(p, False, 'c')
                        p0 = pn.pop(0, False, False, 'c')[0]
                        p1v = p1.val(pn)
                        dm = matutils.msub(matx(tuple([(alg.mul(p0, alg.addl(i)),) for i in d[0].val(p1v).matx]), False, 'c'), d[1], False, 'c')
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(a, matutils.addmatx(matutils.mmult(matx(tuple([alg.addl(i) for i in d[0].val(p1v).matx]), False, 'c'), dm, False, 'c'), matutils.mmult(matutils.smult(p0, matutils.tpose(d[0].val(p1.dval(pn)), False, 'c'), False, 'c'), dm, False, 'c'), True, False, 'c'), False, 'c'), False, 'c'), False, 'c')
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                if pn is None:
                    raise Exception
                match const[0]:
                    case False:
                        pv = p1.val(p)
                        pnv = p1.val(pn)
                        for i in range(len(pv)):
                            if i == 0:
                                ap = pv[i]
                                apn = pnv[i]
                            else:
                                ap.matx = matutils.addmatx(ap, pv[i], False, False, 'c')
                                apn.matx = matutils.addmatx(apn, pnv[i], False, False, 'c')
                    case True:
                        pv = matx(p, False, 'c')
                        pnv = matx(pn, False, 'c')
                        ap0 = matx(pv.pop(0, False, False, 'c'), False, 'c')
                        apn0 = matx(pnv.pop(0, False, False, 'c'), False, 'c')
                        pv = p1.val(pv)
                        pnv = p1.val(pnv)
                        for i in range(len(pv)):
                            if i == 0:
                                ap = matutils.addmatx(ap0, pv[i], False, False, 'c')
                                apn = matutils.addmatx(apn0, pnv[i], False, False, 'c')
                            else:
                                ap.matx = matutils.addmatx(ap, pv[i], False, False, 'c')
                                apn.matx = matutils.addmatx(apn, pnv[i], False, False, 'c')
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                err = Calculate._cmperrpr(ap, apn, pr, 'c')
                match err:
                    case True:
                        return pn, c
                    case False:
                        p.matx = pn
                    case _:
                        raise Exception
            return pn, c - 1
        except Exception as e:
            print("Invalid command: _Gradesgp._linreg()")
            retrn(ret, e)
    
    @classmethod
    def _weilinreg(cls, d: tuple, p: matx, p1: parameter, a: Decimal, m: int, pr: Decimal, w: tuple, const=(False, True), ret='a') -> tuple[matx, matx, int]:
        try:
            c, a = 0, alg.mul(-1, a)
            m += 1
            while (c := c + 1) != m:
                match const[0]:
                    case False:
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(a, matutils.mmult(matutils.tpose(matutils.smultfac(w, d[0].val(p1.dval(p)), chk=False, ret='c'), False, 'c'), matutils.msub(matx(tuple([(alg.addl(i),) for i in d[0].val(p1.val(p)).matx]), False, 'c'), d[1], False, 'c'), False, 'c'), False, 'c'), False, 'c'), False, 'c')
                    case True:
                        pn = matx(p, False, 'c')
                        p0 = pn.pop(0, False, False, 'c')[0]
                        dm = matutils.msub(matx(tuple([(alg.mul(p0, alg.addl(i)),) for i in d[0].val(p1.val(pn)).matx]), False, 'c'), d[1], False, 'c')
                        pn = matutils.madd(p, matutils.tpose(matutils.smult(a, matutils.addmatx(matutils.mmult(matutils.smultfac(w, matx(tuple([alg.addl(i) for i in d[0].val(p1.val(pn)).matx]), False, 'c'), False, False, 'c'), dm, False, 'c'), matutils.mmult(matutils.tpose(matutils.smult(p0, matutils.smultfac(w, d[0].val(p1.dval(pn)), chk=False, ret='c'), False, 'c'), False, 'c'), dm, False, 'c'), True, False, 'c'), False, 'c'), False, 'c'), False, 'c')
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                if pn is None:
                    raise Exception
                match const[0]:
                    case False:
                        pv = p1.val(p)
                        pnv = p1.val(pn)
                        for i in range(len(pv)):
                            if i == 0:
                                ap = pv[i]
                                apn = pnv[i]
                            else:
                                ap.matx = matutils.addmatx(ap, pv[i], False, False, 'c')
                                apn.matx = matutils.addmatx(apn, pnv[i], False, False, 'c')
                    case True:
                        pv = matx(p, False, 'c')
                        pnv = matx(pn, False, 'c')
                        ap0 = matx(pv.pop(0, False, False, 'c'), False, 'c')
                        apn0 = matx(pnv.pop(0, False, False, 'c'), False, 'c')
                        pv = p1.val(pv)
                        pnv = p1.val(pnv)
                        for i in range(len(pv)):
                            if i == 0:
                                ap = matutils.addmatx(ap0, pv[i], False, False, 'c')
                                apn = matutils.addmatx(apn0, pnv[i], False, False, 'c')
                            else:
                                ap.matx = matutils.addmatx(ap, pv[i], False, False, 'c')
                                apn.matx = matutils.addmatx(apn, pnv[i], False, False, 'c')
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                err = Calculate._cmperrpr(ap, apn, pr, 'c')
                match err:
                    case True:
                        return pn, c
                    case False:
                        p.matx = pn
                    case _:
                        raise Exception
            return pn, c - 1
        except Exception as e:
            print("Invalid command: _Gradesgp._weilinreg()")
            retrn(ret, e)

    
class _RegMatrix:

    @staticmethod
    def _hessianx(x: matx, xt=None, ret='a') -> matx:
        try:
            xtt = xt.__class__.__name__
            match xtt:
                case 'NoneType':
                    x = matutils.matlxtox(matutils.tpose(x, False, 'c'), False, 'c')
                    upr, dia = list(), list()
                    for i in range(len(x)):
                        upr1, dia1 = list(), list()
                        for j in range(len(x)):
                            if j == i:
                                dia1.append(
                                    matutils.mmult(x[i], matutils.tpose(x[j], False, 'c'), False, 'c').matx[0][0])
                                upr1.append(Decimal('0.0'))
                            elif j > i:
                                upr1.append(
                                    matutils.mmult(x[i], matutils.tpose(x[j], False, 'c'), False, 'c').matx[0][0])
                                dia1.append(Decimal('0.0'))
                            else:
                                upr1.append(Decimal('0.0'))
                                dia1.append(Decimal('0.0'))
                        upr.append(tuple(upr1))
                        dia.append(tuple(dia1))
                case 'matx':
                    return matutils.mmult(matutils.tpose(xt, False, 'c'), x, False, 'c')
                case _:
                    raise Exception("Invalid argument: xt => None/matx")
            upr, dia = matx(tuple(upr), False, 'c'), matx(tuple(dia), False, 'c')
            return matutils.madd(dia, matutils.madd(upr, matutils.tpose(upr, False, 'c'), False, 'c'), False, 'c')
        except Exception as e:
            print("Invalid command: _RegMatrix._hessianx()")
            retrn(ret, e)

    @staticmethod
    def _jacobiany(x: matx, y: matx, ret='a') -> matx:
        try:
            x = matutils.matlxtox(matutils.tpose(x, False, 'c'), False, 'c')
            j = list()
            for i in x:
                j.append((matutils.mmult(i, y, False, 'c').matx[0][0],))
            return matx(tuple(j), False, 'c')
        except Exception as e:
            print("Invalid command: _RegMatrix._jacobiany()")
            retrn(ret, e)


def _grades(d: data, p: matx, a: Decimal, m: int, pr: Decimal, scale=False, xmt=None, const=(False, True), ret='a') -> dict:
    try:
        da, txmt = d, xmt.__class__.__name__
        match scale:
            case True:
                match txmt:
                    case 'NoneType':
                        pass
                    case 'tuple':
                        w = _Calculate._weights(matutils.smultfac((f := [alg.div(1, i) for i in scf.matx[0][:-1]]), d.getax(), False, False, 'c'), alg.lmul(xmt[0], f), xmt[1], 'c')
                    case _:
                        raise Exception("Invalid argument: xmt => None/tuple")
                sc = Scale._scale0to1(d, 'c')
                if sc is None:
                    raise Exception
                d, scc, scf = sc["data"], sc["constant"], sc["factor"]
                del sc
                match const[1]:
                    case False:
                        c = matutils.smultfac([alg.div(1, i) for i in scf.matx[0]], scc, False, False, 'c')
                        cy = c.pop(-1, False, False, 'c')
                        d = data(matutils.saddcnst(c.matx[0], d.getax(), False, False, 'c'), matutils.saddcnst(cy, d.getay(), False, False, 'c'), False, 'c')
                    case True:
                        match const[0]:
                            case True:
                                d = data(matutils.maddval(d.getax(), Decimal('1.0'), False, 'c'), matutils.saddcnst((alg.div(scc.mele(0, -1, False, 'c'), scf.mele(0, -1, False, 'c')), ), d.getay(), False, False, 'c'), False, 'c')
                            case False:
                                d = datautils.dataval(d, Decimal('1.0'), False, 'c')
                            case _:
                                raise Exception("Invalid argument: const => (bool, bool)")
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
                match const[0]:
                    case False:
                        p = _ScalePar._0to1(scc, scf, p, const[1], 'c')
                        if p is None:
                            raise Exception
                    case True:
                        match const[1]:
                            case False:
                                p = matutils.maddval(_ScalePar._0to1(scc, scf, matx(p.matx[0][1:], False, 'c'), False, 'c'), p.mele(0, 0, False, 'c'), False, 'c')
                                if p is None:
                                    raise Exception
                            case True:
                                p = matutils.maddval(_ScalePar._0to1(matx(scc.matx[0][:-1] + (Decimal('0.0'), ), False, 'c'), scf, matx(p.matx[0][1:], False, 'c'), True, 'c'), p.mele(0, 0, False, 'c'), True, 'c')
                                if p is None:
                                    raise Exception
                            case _:
                                raise Exception("Invalid argument: const => (bool, bool)")
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
            case False:
                match txmt:
                    case 'NoneType':
                        pass
                    case 'tuple':
                        w = _Calculate._weights(d.data[0], xmt[0], xmt[1], 'c')
                    case _:
                        raise Exception("Invalid argument: xmt => None/tuple")
                match const[1]:
                    case True:
                        d = datautils.dataval(d, Decimal('1.0'), False, 'c')
                    case False:
                        pass
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
            case _:
                raise Exception("Invalid argument: scale => bool")
        d1 = (matutils.tpose(d.getax()), matutils.tpose(d.getay()))
        match scale:
            case True:
                match txmt:
                    case 'NoneType':
                        pn = _Grades._linregsp(d1, p, a, m, pr, (scc, scf), const, 'c')
                    case 'tuple':
                        pn = _Grades._weilinregsp(d1, p, a, m, pr, w, (scc, scf), const, 'c')
                    case _:
                        raise Exception("Invalid argument: xmt => None/tuple")
            case False:
                match txmt:
                    case 'NoneType':
                        pn = _Grades._linreg(d1, p, a, m, pr, const, 'c')
                    case 'tuple':
                        pn = _Grades._weilinreg(d1, p, a, m, pr, w, const, 'c')
                    case _:
                        raise Exception("Invalid argument: xmt => None/tuple")
            case _:
                raise Exception("Invalid argument: scale => bool")
        if pn is None:
            raise Exception
        p, c = pn
        del pn
        match scale:
            case True:
                match const[0]:
                    case False:
                        p = _ScalePar._orignl(scc, scf, p, const[1], 'c')
                        if p is None:
                            raise Exception
                    case True:
                        match const[1]:
                            case False:
                                p = matutils.maddval(_ScalePar._orignl(scc, scf, matx(p.matx[0][1:], False, 'c'), False, 'c'), p.mele(0, 0, False, 'c'), False, 'c')
                                if p is None:
                                    raise Exception
                            case True:
                                p = matutils.maddval(_ScalePar._orignl(matx(scc.matx[0][:-1] + (Decimal('0.0'), ), False, 'c'), scf, matx(p.matx[0][1:], False, 'c'), True, 'c'), p.mele(0, 0, False, 'c'), False, 'c')
                                if p is None:
                                    raise Exception
                            case _:
                                raise Exception("Invalid argument: const => (bool, bool)")
                    case _:
                        raise Exception("Invalid argument: const => (bool, bool)")
            case False:
                pass
            case _:
                raise Exception("Invalid argument: scale => bool")
        dic = dict()
        dic["parameters"] = [str(i) for i in p.matxl()[0]]
        dic["iterations"] = c
        dic["r^2"] = str(_Calculate._coofdet(da.data, p, const, 'c'))
        if dic["r^2"] is None:
            raise Exception
        try:
            dic["r^2_adj"] = str(alg.sub(1, alg.div(alg.mul(alg.sub(1, dic["r^2"]), (s := alg.sub(da.datalen, 1))), alg.sub(s, da.xvars))))
        except ZeroDivisionError:
            dic["r^2_adj"] = 'NaN'
        return dic
    except Exception as e:
        print("Invalid command: _grades()")
        retrn(ret, e)


def _gradesgp(d: data, p: matx, p1: parameter, a: Decimal, m: int, pr: Decimal, xmt=None, const=(False, True), ret='a') -> dict:
    try:
        da = d
        match (txmt := xmt.__class__.__name__):
            case 'NoneType':
                pass
            case 'tuple':
                w = _Calculate._weights(d.data[0], xmt[0], xmt[1], 'c')
            case _:
                raise Exception("Invalid argument: xmt => None/tuple")
        match const[1]:
            case True:
                d = datautils.dataval(d, Decimal('1.0'), False, 'c')
            case False:
                pass
            case _:
                raise Exception("Invalid argument: const => (bool, bool)")
        d = (function(matutils.dpose(d.getax(), p1.n, chk=False, ret='c'), False, 'c'), d.getay())
        match txmt:
            case 'NoneType':
                pn = _Gradesgp._linreg(d, p, p1, a, m, pr, const, 'c')
            case 'tuple':
                pn = _Gradesgp._weilinreg(d, p, p1, a, m, pr, w, const, 'c')
            case _:
                raise Exception("Invalid argument: xmt")
        if pn is None:
            raise Exception
        p = pn[0]
        c = pn[1]
        dic = dict()
        dic["parameters"] = [[str(i) for i in p.matxl()[0]], [[str(j) for j in i.matx[0]] for i in p1.val(p)]]
        dic["iterations"] = c
        dic["r^2"] = str(_Calculate._coofdetgp(da.data, p, p1, const, 'c'))
        if dic["r^2"] is None:
            raise Exception
        try:
            dic["r^2_adj"] = str(alg.sub(1, alg.div(alg.mul(alg.sub(1, dic["r^2"]), (s := alg.sub(da.datalen, 1))), alg.sub(s, da.xvars))))
        except ZeroDivisionError:
            dic["r^2_adj"] = 'NaN'
        return dic
    except Exception as e:
        print("Invalid command: _gradesgp()")
        retrn(ret, e)


def _regmatrix(d: data, pmpr: tuple[matx, int, Decimal], weigh=False, xmt=None, method='inverse', const=True, ret='a') -> dict:
    try:
        match weigh:
            # performs linear regression using matrix method
            case False:
                match const:
                    case True:
                        d1 = datautils.dataval(d, Decimal('1.0'), False, 'c')
                    case False:
                        d1 = d
                    case _:
                        raise Exception("Invalid argument: const=bool")
                x, y = d1.data
                y.matx, x.matx = _RegMatrix._jacobiany(x, y, 'c'), _RegMatrix._hessianx(x, ret='c')
            # performs weighted linear regression using matrix method
            case True:
                if (w := _Calculate._weights(d.getax(), xmt[0], xmt[1], 'c')) is None:
                    raise Exception
                match const:
                    case True:
                        d1 = datautils.dataval(d, Decimal('1.0'), False, 'c')
                    case False:
                        d1 = d
                    case _:
                        raise Exception("Invalid argument: const=bool")
                x, y = d1.data
                xt = matutils.smultfac(w, x, True, False, 'c')
                y.matx, x.matx = _RegMatrix._jacobiany(xt, y, 'c'), _RegMatrix._hessianx(x, xt, 'c')
                del xt
            case _:
                raise Exception("Invalid argument: weigh => bool")
        match method:
            case 'inverse':
                p = Method._inverse(x, y, 'c')
                if p is None:
                    raise Exception
            case 'uttform':
                p = Method._uttform(x, y, 'c')
                if p is None:
                    raise Exception
            case 'gauseidel':
                p = Method._gauseidel(x, y, pmpr, 'c')
                if p is None:
                    raise Exception
                dic = dict()
                dic["parameters"] = [str(i) for i in p[0].matxl()[0]]
                dic["iterations"] = p[1]
                dic["r^2"] = str(_Calculate._coofdet(d.data, p[0], (False, const), 'c'))
                if dic["r^2"] is None:
                    raise Exception
                try:
                    dic["r^2_adj"] = str(alg.sub(1, alg.div(alg.mul(alg.sub(1, dic["r^2"]), (s := alg.sub(d.datalen, 1))), alg.sub(s, d.xvars))))
                except ZeroDivisionError:
                    dic["r^2_adj"] = 'NaN'
                return dic
            case 'tridia':
                p = Method._tridia(x, y, 'c')
                if p is None:
                    raise Exception
        dic = dict()
        dic["parameters"] = [str(i) for i in p.matxl()[0]]
        dic["r^2"] = str(_Calculate._coofdet(d.data, p, (False, const), 'c'))
        if dic["r^2"] is None:
            raise Exception
        try:
            dic["r^2_adj"] = str(alg.sub(1, alg.div(alg.mul(alg.sub(1, dic["r^2"]), (s := alg.sub(d.datalen, 1))), alg.sub(s, d.xvars))))
        except ZeroDivisionError:
            dic["r^2_adj"] = 'NaN'
        return dic
    except Exception as e:
        print("Invalid command: _regmatrix()")
        retrn(ret, e)


class LinReg:
    
    @staticmethod
    def gradesgp(d: data, p: list | matx, cfp: list[list[list]] | tuple[tuple[tuple[float | Decimal | int, float | Decimal | int], ...], ...], a: float, m=100, pr=0.01, const=(False, True), ret='a') -> dict:
        try:
            if tdata(d) is None:
                raise Exception
            if (p := matx(p, True, 'c')) is None or (a := tdeciml.decip(a)) is None or (pr := tdeciml.decip(pr)) is None or (m := tint.intn(m)) is None or (p1 := parameter(cfp, True, 'c')) is None:
                raise Exception
            match const:
                case (True, True):
                    if sum(p1.n) != d.xvars + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 2))
                    if eqval(len(p1.n), p.rowlen - 1) is None:
                        raise Exception
                case (False, True):
                    if sum(p1.n) != d.xvars + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
                    if eqval(len(p1.n), p.rowlen) is None:
                        raise Exception
                case (True, False):
                    if sum(p1.n) != d.xvars:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
                    if eqval(len(p1.n), p.rowlen - 1) is None:
                        raise Exception
                case (False, False):
                    if sum(p1.n) != d.xvars:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars))
                    if eqval(len(p1.n), p.rowlen) is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            return _gradesgp(d, p, p1, a, m, pr, const=const, ret='c')
        except Exception as e:
            print("Invalid command: LinReg.gradesgp()")
            retrn(ret, e)
    
    @staticmethod
    def grades(d: data, p: list, a: float, m=100, pr=0.01, scale=False, const=(False, True), ret='a') -> dict:
        try:
            if tdata(d) is None:
                raise Exception
            if (p := matx(p, True, 'c')) is None or eqval(p.collen, 1) is None or (a := tdeciml.decip(a)) is None or (pr := tdeciml.decip(pr)) is None or (m := tint.intn(m)) is None:
                raise Exception
            if const == (True, True):
                if p.rowlen != d.xvars + 2:
                    raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 2))
            elif const == (True, False) or const == (False, True):
                if p.rowlen != d.xvars + 1:
                    raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
            elif const == (False, False):
                if p.rowlen != d.xvars:
                    raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars))
            else:
                raise Exception("Invalid argument: const => (bool, bool)")
            return _grades(d, p, a, m, pr, scale, const=const, ret='c')
        except Exception as e:
            print("Invalid command: LinReg.grades()")
            retrn(ret, e)

    @staticmethod
    def matrix(d: data, p=None, m=100, pr=0.01, method='inverse', const=True, ret='a') -> dict:
        try:
            if tdata(d) is None:
                raise Exception
            if p is not None:
                if (pr := tdeciml.decip(pr)) is None or (p := matx(p, ret='c')) is None or eqval(p.collen, 1) is None:
                    raise Exception
                match const:
                    case True:
                        if p.rowlen != d.xvars + 1:
                            raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
                    case False:
                        if p.rowlen != d.xvars:
                            raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars))
                    case _:
                        raise Exception("Invalid argument: const => bool")
            return _regmatrix(d, (p, m, pr), method=method, const=const, ret='c')
        except Exception as e:
            print("Invalid command: LinReg.matrix()")
            retrn(ret, e)


class WeiLinReg:

    @staticmethod
    def gradesgp(d: data, p: list | matx, a: float, cfp: list[list[list]] | tuple[tuple[tuple[float | Decimal | int, float | Decimal | int], ...], ...], x: list[Decimal] | tuple[Decimal, ...], t=float("inf"), m=100, pr=0.01, const=(False, True), ret='a') -> dict:
        try:
            if tdata(d) is None or (p := matx(p, ret='c')) is None or (a := tdeciml.decip(a)) is None or (pr := tdeciml.decip(pr)) is None or (m := tint.intn(m)) is None or str(t := deciml(t)) == 'NaN' or (p1 := parameter(cfp, True, 'c')) is None:
                raise Exception
            xn = list()
            for i in x:
                if str(i1 := deciml(i)) == 'NaN':
                    raise Exception("Invalid argument: x => tuple/list")
                xn.append(i1)
            x = tuple(xn)
            del xn
            if len(x) != d.xvars:
                raise Exception(str(x.rowlen) + " != " + str(d.xvars))
            match const:
                case (True, True):
                    if sum(p1.n) != d.xvars + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 2))
                    if eqval(len(p1.n), p.rowlen - 1) is None:
                        raise Exception
                case (False, True):
                    if sum(p1.n) != d.xvars + 1:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
                    if eqval(len(p1.n), p.rowlen) is None:
                        raise Exception
                case (True, False):
                    if sum(p1.n) != d.xvars:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
                    if eqval(len(p1.n), p.rowlen - 1) is None:
                        raise Exception
                case (False, False):
                    if sum(p1.n) != d.xvars:
                        raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars))
                    if eqval(len(p1.n), p.rowlen) is None:
                        raise Exception
                case _:
                    raise Exception("Invalid argument: const => (bool, bool)")
            return _gradesgp(d, p, p1, a, m, pr, (x, t), const, ret=True)
        except Exception as e:
            print("Invalid command: WeiLinReg.gradesgp()")
            retrn(ret, e)
    
    @staticmethod
    def grades(d: data, p: list, a: float, x: list, t=float("inf"), m=100, pr=0.01, scale=False, const=(False, True), ret='a') -> dict:
        try:
            if tdata(d) is None or (p := matx(p, True, True)) is None or eqval(p.collen, 1) is None or (a := tdeciml.decip(a)) is None or (pr := tdeciml.decip(pr)) is None or (m := tint.intn(m)) is None or eqval(x.rowlen, d.xvars) is None or eqval(x.collen, 1) is None or str(t := deciml(t)) == 'NaN':
                raise Exception
            xn = list()
            for i in x:
                if str(i1 := deciml(i)) == 'NaN':
                    raise Exception("Invalid argument: x => tuple/list")
                xn.append(i1)
            x = tuple(xn)
            del xn
            if len(x) != d.xvars:
                raise Exception(str(x.rowlen) + " != " + str(d.xvars))
            if const == (True, True):
                if p.rowlen != d.xvars + 2:
                    raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 2))
            elif const == (True, False) or const == (False, True):
                if p.rowlen != d.xvars + 1:
                    raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
            elif const == (False, False):
                if p.rowlen != d.xvars:
                    raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars))
            else:
                raise Exception("Invalid argument: const => (bool, bool)")
            return _grades(d, p, a, m, pr, scale, (x, t), const=const, ret='c')
        except Exception as e:
            print("Invalid command: WeiLinReg.grades()")
            retrn(ret, e)

    @staticmethod
    def matrix(d: data, x: list, t=float('inf'), p=None, m=100, pr=0.01, method='inverse', const=True, ret='a') -> dict:
        try:
            if tdata(d) is None or str(t := deciml(t)) == 'NaN':
                raise Exception
            xn = list()
            for i in x:
                if str(i1 := deciml(i)) == 'NaN':
                    raise Exception("Invalid argument: x => tuple/list")
                xn.append(i1)
            x = tuple(xn)
            del xn
            if len(x) != d.xvars:
                raise Exception(str(x.rowlen) + " != " + str(d.xvars))
            if p is not None:
                if (p := matx(p, ret='c')) is None or eqval(p.collen, 1) is None or (pr := tdeciml.decip(pr)) is None:
                    raise Exception
                match const:
                    case True:
                        if p.rowlen != d.xvars + 1:
                            raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars + 1))
                    case False:
                        if p.rowlen != d.xvars:
                            raise Exception("number of parameters: " + str(p.rowlen) + " != " + str(d.xvars))
                    case _:
                        raise Exception("Invalid argument: const => bool")
            return _regmatrix(d, (p, m, pr), True, (x, t), method=method, const=const, ret='c')
        except Exception as e:
            print("Invalid command: WeiLinReg.matrix()")
            retrn(ret, e)


print('1')
b = LinReg.matrix(data([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]], [[6], [12], [18], [25], [26]]), method='inverse')
print(b)
b = LinReg.matrix(data([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]], [[6], [12], [18], [25], [26]]), method='tridia')
print(b)
b = LinReg.matrix(data([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]], [[6], [12], [18], [25], [26]]), [1,1,1,1], pr=0.01, method='gauseidel')
print(b)
b = LinReg.grades(data([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]], [[6], [12], [18], [25], [26]]),
                   [1, 1, 1], 0.01, 100, scale=True, const=(False, False), ret='c')
print(b)
a = 0.00196
c = (False, True)
b = LinReg.grades(data([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]], [[6], [12], [18], [25], [26]]), [0, 1, 1, 1], a, 1000, 0.01, const=c, ret=True)
print(b)
print(PLinReg.y([2,3,6], b["parameters"], c))
print('2')
c = WeiLinReg.matrix(data([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]], [[6], [12], [18], [25], [26]]), [2, 6, 4])
print(c)
c = WeiLinReg.gradesgp(
   data([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]], [[6], [12], [18], [25], [26]]), [1, 1, 1],
   0.0008, [[[1, 1 ], ] for _ in range(3)], [2, 4, 6], const=(False, False))
print(c)
PLinReg.allygp([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]],  c["parameters"][0], [[[1,1], ] for i in range(3)], (False, False)).pmatx
PLinReg.ally([[1, 2, 3], [2, 4, 6], [3, 6, 9], [10, 12, 12], [15, 12, 10]],  c["parameters"][0] , (False, False)).pmatx


a = LinReg.matrix(GetData.regdata([0,1,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,1,1], [14.44,18.45,5.45,10.77,11.21,8.31,13.09,19.72,18.06,8.13,6.26,5.31,19.83,7,9.77,19.83,9.87,6.31,17.01,4.59], [13.93,3.16,8.51,10.04,10.02,9.5,2.66,9.61,9.24,9.32,4.19,10.89,3.33,7.27,5.66,13.03,8.06,8.99,10.6,8.08]))
print(a)
