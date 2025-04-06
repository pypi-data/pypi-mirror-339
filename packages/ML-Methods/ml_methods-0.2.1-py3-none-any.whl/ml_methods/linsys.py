from deciml.deciml import abs, algbra as alg, Decimal
from compare.cmpr import eqval, tdeciml, tint
from terminate import retrn
from deciml_maths.matrix import matx, matutils
from algoutils import Calculate


class _Calculate:

    @staticmethod
    def _ulp(ut: matx, lt: matx, x: matx, c: matx, ret='a') -> matx:
        try:
            xn = list()
            for i in range(lt.collen):
                pn1 = 0
                for j in range(lt.rowlen):
                    if j < i:
                        pn1 = alg.add(pn1, alg.mul(lt.mele(i, j, False, 'c'), x.mele(0, j, False, 'c')))
                xn.append((pn1,))
            x = matutils.matlxtox(matutils.msub(matx(tuple(xn), False, 'c'), c, False, 'c'), False, 'c')
            for i in range(ut.collen):
                if i > 0:
                    xn.matx = matutils.addmatx(matutils.madd(matutils.mmult(xn, matx(tuple([(j,) for j in ut.mrow(ut.collen - 1 - i, False, 'c')[ut.collen - i:]]), False, 'c'), False, 'c'), x[-(i + 1)], False, 'c'), xn, chk=False, ret='c')
                else:
                    xn = x[-1]
            return xn
        except Exception as e:
            print("Invalid command: _Calculate._ulp()")
            retrn(ret, e)

    @staticmethod
    def _lup(lt: matx, ut: matx, x: matx, c: matx, ret='a') -> matx:
        try:
            xn = list()
            for i in range(ut.collen):
                pn1 = 0
                for j in range(ut.rowlen):
                    if j > i:
                        pn1 = alg.add(pn1, alg.mul(ut.mele(i, j, False, 'c'), x.mele(0, j, False, 'c')))
                xn.append((pn1,))
            x = matutils.matlxtox(matutils.msub(matx(tuple(xn), False, 'c'), c, False, 'c'), False, 'c')
            for i in range(lt.collen):
                if i > 0:
                    xn.matx = matutils.addmatx(xn, matutils.madd(matutils.mmult(xn, matx(tuple([(j,) for j in lt.mrow(i, False, 'c')[:i]]), False, 'c'), False, 'c'), x[i], False, 'c'), chk=False, ret='c')
                else:
                    xn = x[0]
            return xn
        except Exception as e:
            print("Invalid command: _Calculate._lup()")
            retrn(ret, e)

class Method(_Calculate, Calculate):
    
    @staticmethod
    def _inverse(a: matx, b: matx, ret='a') -> matx:
        try:
            return matutils.mmult(matutils.tpose(b, False, 'c'), matutils.invse(a, False, 'c'), False, 'c')
        except Exception as e:
            print("Invalid command: Method._inverse()")
            retrn(ret, e)

    @staticmethod
    def _uttform(a: matx, b: matx, ret='a') -> matx:
        try:
            for i in range(a.collen):
                an = list(a.matx)
                bn = list(b.matx)
                acol = matutils.gele(a, [i, ], False, False, 'c').matx[0]
                acm = max([acol[j] for j in range(len(acol)) if j > i - 1])
                for j in range(a.collen):
                    if a.mele(0, j, False, 'c') == acm:
                        an.insert(i, an.pop(j))
                        bn.insert(i, bn.pop(j))
                        break
                a.matx = matx(tuple(an), False, 'c')
                b.matx = matx(tuple(bn), False, 'c')
                ai = a.mele(i, i, False, 'c')
                if ai == 0:
                    raise Exception
                for j in range(a.collen):
                    if j > i:
                        facx = alg.mul(-1, alg.div(a.mele(j, i, False, 'c'), ai))
                        a.matx = matutils.tform(a, j, i, facx, True, False, 'c')
                        b.matx = matutils.tform(b, j, i, facx, True, False, 'c')
            x = matx((alg.div(b.mele(b.collen - 1, 0, False, 'c'), a.mele(a.collen - 1, a.rowlen - 1)),), False, 'c')
            del an, acm, acol, facx, ai
            for i in range(a.collen):
                if i == 0:
                    continue
                an = matx(tuple([(a.mele(a.collen - 1 - i, a.rowlen - 1 + j - i + 1, False, 'c'),) for j in range(i)]), False, 'c')
                x.matx = matutils.addmatx(matutils.smult(alg.div(1, a.mele(a.collen - 1 - i, a.rowlen - 1 - i, False, 'c')), matutils.msub(matx(b.mrow(b.collen - 1 - i, False, 'c'), False, 'c'), matutils.mmult(x, an, False, 'c'), False, 'c'), False, 'c'), x, r=False, chk=False, ret='c')
            del an
            return x
        except Exception as e:
            print("Invalid command: Method._uttform()")
            retrn(ret, e)

    @classmethod
    def _gauseidel(cls, a: matx, b: matx, xmpr: tuple[matx, int, Decimal], ret='a') -> tuple[matx, int]:
        try:
            x = xmpr[0]
            m = xmpr[1]
            pr = xmpr[2]
            for i in range(a.rowlen):
                row = None
                el = 0
                ele = a.mele(i, i, False, 'c')
                fac = [Decimal('1.0') for _ in range(a.collen - 1)]
                if ele == 0:
                    for j in range(a.collen):
                        if j != i:
                            el = a.mele(j, i, False, 'c')
                            if el != 0:
                                if row == None:
                                    row = j
                                if abs(el) < abs(a.mele(row, i, False, 'c')):
                                    row = j
                    if row is None:
                        raise Exception
                    el = a.mele(row, i, False, 'c')
                    a.matx = matutils.tform(a, i, row, alg.div(-1, el), True, False, 'c')
                    b.matx = matutils.tform(b, i, row, alg.div(-1, el), True, False, 'c')
                else:
                    fac.insert(i, alg.div(-1, ele))
                    a.matx = matutils.smultfac(tuple(fac), a, chk=False, ret='c')
                    b.matx = matutils.smultfac(tuple(fac), b, chk=False, ret='c')
            a.matx = matutils.madd(a, matutils.sclrm(a.rowlen, Decimal('1.0'), False, 'c'), False, 'c')
            a = matutils.uldcompose(a, False, 'c')
            ut = a[0]
            lt = a[1]
            del a
            uts = 0
            lts = 0
            for i in range(ut.collen):
                for j in range(lt.rowlen):
                    if j > i:
                        uts += ut.mele(i, j, False, 'c')
                    elif j < i:
                        lts += lt.mele(i, j, False, 'c')
            if abs(lts) > abs(uts):
                c = 0
                m += 1
                while (c := c + 1) != m:
                    xn = _Calculate._lup(lt, ut, x, b)
                    if xn is None:
                        raise Exception
                    err = Calculate._cmperrpr(x, xn, pr, 'c')
                    match err:
                        case True:
                            x.matx = xn
                            break
                        case False:
                            x.matx = xn
                        case _:
                            raise Exception
            else:
                c = 0
                m += 1
                while (c := c + 1) != m:
                    xn = _Calculate._ulp(ut, lt, x, b)
                    if xn is None:
                        raise Exception
                    err = Calculate._cmperrpr(x, xn, pr, 'c')
                    match err:
                        case True:
                            x.matx = xn
                            break
                        case False:
                            x.matx = xn
                        case _:
                            raise Exception
            if c == m + 1:
                return x, c - 1
            return x, c
        except Exception as e:
            print("Invalid command: Method._gauseidel()")
            retrn(ret, e)

    @staticmethod
    def _tridia(a: matx, b: matx, ret='a') -> matx:
        try:
            for i in range(int(alg.div(a.rowlen, 2)) + 1):
                elea = a.mele(i + 1, i, False, 'c')
                cola = a.mcol(i, False, 'c')
                for j in range(a.collen):
                    if j > i + 1:
                        a.matx = matutils.tform(a, j, i + 1, alg.div(alg.mul(-1, cola[j]), elea), True, False, 'c')
                        b.matx = matutils.tform(b, j, i + 1, alg.div(alg.mul(-1, cola[j]), elea), True, False, 'c')
                elec = a.mele(a.collen - 2 - i, a.rowlen - 1 - i, False, 'c')
                colc = a.mcol(a.rowlen - 1 - i, False, 'c')
                for j in range(a.collen):
                    if j < a.collen - 2 - i:
                        a.matx = matutils.tform(a, j, a.collen - 2 - i, alg.div(alg.mul(-1, colc[j]), elec), True, False, 'c')
                        b.matx = matutils.tform(b, j, a.collen - 2 - i, alg.div(alg.mul(-1, colc[j]), elec), True, False, 'c')
            del elea, elec, cola, colc, j
            x = a
            y = matutils.tpose(b, False, 'c').matx[0]
            a = list()
            b = list()
            c = list()
            for i in range(x.collen):
                if i == 0:
                    a.append(Decimal('0.0'))
                    b.append(x.mele(i, i, False, 'c'))
                    c.append(x.mele(i, i + 1, False, 'c'))
                elif i == x.collen - 1:
                    a.append(x.mele(i, i - 1, False, 'c'))
                    b.append(x.mele(i, i, False, 'c'))
                    c.append(Decimal('0.0'))
                else:
                    a.append(x.mele(i, i - 1, False, 'c'))
                    b.append(x.mele(i, i, False, 'c'))
                    c.append(x.mele(i, i + 1, False, 'c'))
            del x
            theta = [Decimal('0.0'), ]
            phi = [Decimal('0.0'), ]
            for i in range(len(a)):
                dn = alg.add(alg.mul(a[i], theta[i]), b[i])
                theta.append(- c[i] / dn)
                phi.append(alg.div(alg.sub(y[i], alg.mul(a[i], phi[i])), dn))
            theta.pop(0)
            phi.pop(0)
            x = [Decimal('0.0'), ]
            for i in range(len(theta)):
                x.insert(0, alg.add(alg.mul(x[0], theta[-(i + 1)]), phi[-(i + 1)]))
            x.pop(-1)
            return matx(tuple(x), False, 'c')
        except Exception as e:
            print("Invalid command: Method._tridia()")
            retrn(ret, e)

def inverse(a: list | tuple | matx, b: list | tuple | matx, ret='a') -> matx:
    try:
        if (a := matx(a, True, 'c')) is None or (b := matx(b, True, 'c')) is None:
            raise Exception
        return Method._inverse(a, b, 'c')
    except Exception as e:
        print("Invalid command: inverse()")
        retrn(ret, e)

def uttform(a: list | tuple | matx, b: list | tuple | matx, ret='a') -> matx:
    try:
        if (a := matx(a, True, 'c')) is None or (b := matx(b, True, 'c')) is None:
            raise Exception
        return Method._uttform(a, b, 'c')
    except Exception as e:
        print("Invalid command: uttform()")
        retrn(ret, e)

def gauseidel(a: list | tuple | matx, b: list | tuple | matx, x: list | tuple | matx, m: int, pr: float, ret='a') -> matx:
    try:
        if (a := matx(a, True, 'c')) is None or (b := matx(b, True, 'c')) is None or (b := matx(b, True, 'c')) is None or eqval([x.rowlen, a.collen, 1], [a.rowlen, b.collen, b.rowlen]) is None or (m := tint.intn(m)) is None or (pr := tdeciml.decip(pr)) is None:
            raise Exception
        return Method._gauseidel(a, b, (x, m, pr), 'c')
    except Exception as e:
        print("Invalid command: gauseidel()")
        retrn(ret, e)

def tridia(a: list | tuple | matx, b: list | tuple | matx, ret='a') -> matx:
    try:
        if (a := matx(a, True, 'c')) is None or (b := matx(b, True, 'c')) is None:
            raise Exception
        return Method._tridia(a, b, 'c')
    except Exception as e:
        print("Invalid command: tridia()")
        retrn(ret, e)