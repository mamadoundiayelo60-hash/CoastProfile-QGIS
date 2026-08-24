from __future__ import annotations
from dataclasses import dataclass
from math import hypot
from typing import Iterable

@dataclass(frozen=True)
class SurveyPoint:
    x: float; y: float; z: float
    hrms: float | None = None; vrms: float | None = None
    fixed: bool = True; fid: int | None = None

@dataclass(frozen=True)
class Profile:
    identifier: str; campaign: str
    points: tuple[SurveyPoint, ...]; chainage: tuple[float, ...]

@dataclass(frozen=True)
class Comparison:
    chainage: tuple[float, ...]; first_z: tuple[float, ...]; second_z: tuple[float, ...]
    erosion_area: float; accretion_area: float; net_area: float; max_erosion: float; max_accretion: float

def decimal(value) -> float | None:
    if value in (None, ""): return None
    try: return float(str(value).replace(",", "."))
    except (TypeError, ValueError): return None

def profile_identifier(value) -> str | None:
    """Normalise un identifiant sans appliquer de nomenclature métier."""
    if value is None: return None
    text=str(value).strip()
    return text or None

def main_spatial_group(points: Iterable[SurveyPoint], link_distance: float=75.0) -> tuple[list[SurveyPoint],list[SurveyPoint]]:
    """Conserve la plus grande composante spatiale et isole les points éloignés."""
    pts=list(points); unseen=set(range(len(pts))); components=[]
    while unseen:
        todo=[unseen.pop()]; component=[]
        while todo:
            i=todo.pop(); component.append(i); neighbours=[]
            for j in unseen:
                if hypot(pts[i].x-pts[j].x,pts[i].y-pts[j].y)<=link_distance: neighbours.append(j)
            for j in neighbours: unseen.remove(j); todo.append(j)
        components.append(component)
    keep=set(max(components,key=len)) if components else set()
    return [p for i,p in enumerate(pts) if i in keep],[p for i,p in enumerate(pts) if i not in keep]

def build_profile(identifier: str, campaign: str, points: Iterable[SurveyPoint], land_to_sea: bool = True) -> Profile:
    pts=list(points)
    if len(pts)<2: raise ValueError("Un profil nécessite au moins deux points.")
    # L'ordre d'acquisition est conservé; seule l'orientation est normalisée.
    if land_to_sea and pts[0].z < pts[-1].z: pts.reverse()
    d=[0.0]
    for a,b in zip(pts,pts[1:]): d.append(d[-1]+hypot(b.x-a.x,b.y-a.y))
    return Profile(identifier,campaign,tuple(pts),tuple(d))

def _interp(xs: tuple[float,...], ys: tuple[float,...], x: float) -> float:
    if x<=xs[0]: return ys[0]
    for i in range(1,len(xs)):
        if x<=xs[i]:
            t=(x-xs[i-1])/(xs[i]-xs[i-1]) if xs[i]!=xs[i-1] else 0
            return ys[i-1]+t*(ys[i]-ys[i-1])
    return ys[-1]

def compare(a: Profile, b: Profile, step: float=1.0) -> Comparison:
    end=min(a.chainage[-1],b.chainage[-1])
    if end<=0: raise ValueError("Aucun segment comparable.")
    n=max(2,int(end/step)+1); xs=tuple(i*end/(n-1) for i in range(n))
    az=tuple(_interp(a.chainage,tuple(p.z for p in a.points),x) for x in xs)
    bz=tuple(_interp(b.chainage,tuple(p.z for p in b.points),x) for x in xs)
    erosion=accretion=0.0
    dif=[y-x for x,y in zip(az,bz)]
    for i in range(1,n):
        area=(dif[i-1]+dif[i])*.5*(xs[i]-xs[i-1])
        if area<0: erosion-=area
        else: accretion+=area
    return Comparison(xs,az,bz,erosion,accretion,accretion-erosion,min(dif),max(dif))
