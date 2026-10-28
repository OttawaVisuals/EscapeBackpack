"""Solver for the hnefatafl puzzle (PZ-008): all pieces slide like rooks, custodial capture, king escapes to a corner.
solutions(att, dfn, king, black_moves, order) returns every escape path; order e.g. "BKBKBK" (black moves first, king moves 3 times).
Checked 17 Oct 2026 against board_layout.py: the four black moves leave exactly one escape in four king moves, F6 H6 H7 K7 K11 (2134)."""
import sys, itertools
sys.path.insert(0,'.')
from board_layout import ATTACKERS, DEFENDERS, THRONE, CORNERS, SIZE
DIRS=[(1,0),(-1,0),(0,1),(0,-1)]
def slides(pos, occ, king=False):
    x,y=pos; out=[]
    for dx,dy in DIRS:
        nx,ny=x+dx,y+dy
        while 0<=nx<SIZE and 0<=ny<SIZE and (nx,ny) not in occ:
            if (nx,ny) in CORNERS and not king: break
            out.append((nx,ny)); nx+=dx;ny+=dy
    return out
class S:
    def __init__(s,att,dfn,king): s.att=frozenset(att); s.dfn=frozenset(dfn); s.king=king
    def occ(s): return s.att|s.dfn|{s.king}
def capture(att,dfn,king,dest,side,rules):
    # custodial capture by mover at dest; side 'a' captures defenders, 'd' (incl king as hammer) captures attackers
    if not rules: return att,dfn
    for dx,dy in DIRS:
        n=(dest[0]+dx,dest[1]+dy); f=(dest[0]+2*dx,dest[1]+2*dy)
        if side=='a':
            if n in dfn and (f in att or f in CORNERS): dfn=dfn-{n}
        else:
            if n in att and (f in dfn or f==king or f in CORNERS): att=att-{n}
    return att,dfn
def king_moves(st):
    return slides(st.king, st.occ(), king=True)
def king_dead(st):
    # four sides hostile; the board edge counts as hostile (ticket rule, 16 Oct 2026)
    return all((not (0<=st.king[0]+dx<SIZE and 0<=st.king[1]+dy<SIZE)) or ((st.king[0]+dx,st.king[1]+dy) in st.att) for dx,dy in DIRS)
def solutions(att,dfn,king,black_moves,order,rules=False,nk=3):
    # order: sequence like 'BKBKBK' ; black_moves list consumed in order
    res=[]
    def rec(st,i,bi,path):
        if i==len(order): return
        t=order[i]
        if t=='B':
            fr,to=black_moves[bi]
            if fr not in st.att or to in st.occ(): return
            if to not in slides(fr,st.occ()): return
            a=st.att-{fr}|{to}; d=st.dfn
            a,d=capture(a,d,st.king,to,'a',rules)
            ns=S(a,d,st.king)
            if king_dead(ns): return
            rec(ns,i+1,bi+1,path)
        else:
            for m in king_moves(st):
                a,d=capture(st.att,st.dfn,m,m,'d',rules)
                ns=S(a,d,m)
                np_=path+[m]
                if m in CORNERS:
                    if order[i+1:].count('K')==0 or True:
                        # must be exactly the last king move
                        if st_count(order,i)==nk: res.append(tuple(np_))
                    continue
                if st_count(order,i)==nk: continue
                rec(ns,i+1,bi,np_)
    def st_count(order,i): return order[:i+1].count('K')
    rec(S(att,dfn,king),0,0,[])
    return res
if __name__=='__main__':
    from board_layout import BLACK_MOVES, coord_label
    def lab(p): return ' '.join(coord_label(*q) for q in [(5,5)]+list(p))
    def code(path):
        pts=[(5,5)]+list(path); return ''.join(str(abs(a[0]-b[0])+abs(a[1]-b[1])) for a,b in zip(pts,pts[1:]))
    r=solutions(ATTACKERS,DEFENDERS,THRONE,BLACK_MOVES,'BKBKBKBK',True,nk=4)
    print('board_layout.py with its four black moves, 4 king moves:',[(lab(p),code(p)) for p in r])
    for nk,order in ((3,'BKBKBK'),(2,'BKBK'),(1,'BK')):
        print('  escapes in',nk,'king moves:',len(solutions(ATTACKERS,DEFENDERS,THRONE,BLACK_MOVES[:nk],order,True,nk=nk)))
    print('  without the last black move:',len(solutions(ATTACKERS,DEFENDERS,THRONE,BLACK_MOVES[:3],'BKBKBKK',True,nk=4)),'escapes')
