from __future__ import annotations
from collections import defaultdict
from pathlib import Path
import traceback
from math import ceil, floor, log10
from qgis.PyQt.QtCore import Qt, QRectF, QLineF, QPointF
from qgis.PyQt.QtGui import QColor, QPainter, QPen, QFont, QBrush
from qgis.PyQt.QtWidgets import (QApplication,QMainWindow,QWidget,QVBoxLayout,QFormLayout,QComboBox,QPushButton,QLabel,QListWidget,QFileDialog,QMessageBox,QSplitter,QDoubleSpinBox)
from qgis.core import QgsProject,QgsVectorLayer,QgsWkbTypes
from .core.profiles import SurveyPoint,build_profile,decimal,main_spatial_group,profile_identifier,natural_sort_key

def _enum(owner,scope,name):
    """Retourne un enum Qt avec ou sans portée (compatibilité Qt 5 / Qt 6)."""
    return getattr(getattr(owner,scope,owner),name)

ALIGN_CENTER=_enum(Qt,'AlignmentFlag','AlignCenter')
ALIGN_RIGHT=_enum(Qt,'AlignmentFlag','AlignRight')
ALIGN_VCENTER=_enum(Qt,'AlignmentFlag','AlignVCenter')
HORIZONTAL=_enum(Qt,'Orientation','Horizontal')
ANTIALIASING=_enum(QPainter,'RenderHint','Antialiasing')
CRITICAL=_enum(QMessageBox,'Icon','Critical')

class ProfileChart(QWidget):
    def __init__(self): super().__init__(); self.setMinimumSize(650,420); self.profile=None
    def set_profile(self,p): self.profile=p; self.update()
    def paintEvent(self,event):
        q=QPainter(self); q.setRenderHint(ANTIALIASING,True); q.fillRect(self.rect(),QColor('#ffffff')); p=self.profile
        if not p: q.setPen(QColor('#667085')); q.drawText(self.rect(),ALIGN_CENTER,'Sélectionnez un profil'); return
        left,top,right,bottom=82,54,34,72
        box=QRectF(left,top,self.width()-left-right,self.height()-top-bottom); q.setPen(QPen(QColor('#98a2b3'),1)); q.drawRect(box)
        xs=p.chainage; zs=[x.z for x in p.points]
        def nice_step(span,target=6):
            raw=max(span/target,1e-9); power=10**floor(log10(raw)); fraction=raw/power
            nice=1 if fraction<=1 else 2 if fraction<=2 else 5 if fraction<=5 else 10
            return nice*power
        xstep=nice_step(max(xs),6); xmax=ceil(max(xs)/xstep)*xstep
        ystep=nice_step(max(zs)-min(zs),6); zmin=floor((min(zs)-.15)/ystep)*ystep; zmax=ceil((max(zs)+.15)/ystep)*ystep
        def xy(x,z): return box.left()+x/max(xmax,1)*box.width(), box.bottom()-(z-zmin)/max(zmax-zmin,.1)*box.height()
        q.setPen(QPen(QColor('#cfd6df'),1))
        ycount=int(round((zmax-zmin)/ystep))
        for i in range(ycount+1):
            val=zmin+i*ystep; y=box.bottom()-(val-zmin)/(zmax-zmin)*box.height()
            q.drawLine(QLineF(box.left(),y,box.right(),y))
            q.setPen(QColor('#475467'))
            label=f'{val:.1f}'.replace('.',',') if ystep<1 else f'{val:.0f}'
            q.drawText(QRectF(30,y-10,43,20),ALIGN_RIGHT|ALIGN_VCENTER,label)
            q.setPen(QPen(QColor('#cfd6df'),1))
        # Grille verticale et graduations de distance.
        xcount=int(round(xmax/xstep))
        for i in range(xcount+1):
            value=i*xstep; x=box.left()+value/xmax*box.width()
            q.setPen(QPen(QColor('#d8dde5'),1)); q.drawLine(QLineF(x,box.top(),x,box.bottom()))
            q.setPen(QColor('#475467')); q.drawText(QRectF(x-35,box.bottom()+8,70,20),ALIGN_CENTER,f'{value:.0f}')
        q.setPen(QPen(QColor('#e31a1c'),3))
        for i in range(1,len(xs)):
            a=xy(xs[i-1],zs[i-1]); b=xy(xs[i],zs[i]); q.drawLine(QLineF(a[0],a[1],b[0],b[1]))
        q.setPen(QPen(QColor('#e31a1c'),1)); q.setBrush(QBrush(QColor('#e31a1c')))
        for x,z in zip(xs,zs):
            px,py=xy(x,z); q.drawEllipse(QPointF(px,py),3.8,3.8)
        q.setPen(QColor('#101828')); q.setFont(QFont('Arial',14,600)); q.drawText(QRectF(0,8,self.width(),32),ALIGN_CENTER,f'{p.identifier} — Profil {p.campaign}')
        q.setFont(QFont('Arial',10)); q.drawText(QRectF(box.left(),box.bottom()+34,box.width(),24),ALIGN_CENTER,'Distance (m)')
        q.save(); q.translate(20,box.center().y()); q.rotate(-90); q.drawText(QRectF(-box.height()/2,-12,box.height(),24),ALIGN_CENTER,'Altitude Z (m)'); q.restore()
        # Légende compacte.
        lx=box.right()-118; ly=box.top()+18; q.setPen(QPen(QColor('#e31a1c'),3)); q.drawLine(QLineF(lx,ly,lx+28,ly)); q.setBrush(QColor('#e31a1c')); q.drawEllipse(QPointF(lx+14,ly),3.5,3.5); q.setPen(QColor('#101828')); q.drawText(QPointF(lx+38,ly+5),str(p.campaign))
        q.setPen(QColor('#667085')); q.setFont(QFont('Arial',9)); q.drawText(QPointF(box.left()+8,box.top()+18),f'{len(zs)} points GNSS')

class CoastProfileWindow(QMainWindow):
    def __init__(self,iface):
        super().__init__(iface.mainWindow()); self.iface=iface; self.profiles={}; self.setWindowTitle('CoastProfile — Profils côtiers'); self.resize(1180,720); self.setMinimumSize(850,540); self._ui()
    def _ui(self):
        root=QWidget(); self.setCentralWidget(root); lay=QVBoxLayout(root)
        title=QLabel('<h2>CoastProfile</h2><span style="color:#667085">De la campagne GNSS au suivi morphologique multiannuel</span>'); lay.addWidget(title)
        split=QSplitter(HORIZONTAL); lay.addWidget(split,1)
        left=QWidget(); ll=QVBoxLayout(left); form=QFormLayout(); self.layers=QComboBox(); self.group=QComboBox(); self.date=QComboBox(); self.zfield=QComboBox(); self.distance=QDoubleSpinBox(); self.distance.setRange(1,5000); self.distance.setValue(75); self.distance.setSuffix(' m'); form.addRow('Couche de points',self.layers); form.addRow('Champ identifiant',self.group); form.addRow('Champ campagne/date',self.date); form.addRow('Source de l’altitude',self.zfield); form.addRow('Seuil d’isolement',self.distance); ll.addLayout(form)
        self.layers.currentIndexChanged.connect(self._fields); load=QPushButton('Créer les profils'); load.clicked.connect(self.load_profiles); ll.addWidget(load)
        ll.addWidget(QLabel('Profils détectés')); self.list=QListWidget(); self.list.currentTextChanged.connect(self.show_profile); ll.addWidget(self.list,1)
        exp=QPushButton('Exporter le profil en PNG'); exp.clicked.connect(self.export_png); ll.addWidget(exp); close=QPushButton('Fermer'); close.clicked.connect(self.close); ll.addWidget(close)
        batch=QPushButton('Exporter tous les profils dans un dossier'); batch.clicked.connect(self.export_all); ll.insertWidget(ll.count()-2,batch)
        self.status=QLabel('Prêt. Les données sources ne sont jamais modifiées.'); self.status.setWordWrap(True); ll.addWidget(self.status); split.addWidget(left)
        self.chart=ProfileChart(); split.addWidget(self.chart); split.setSizes([320,850])
    def reset_results(self):
        """Vide les résultats calculés sans toucher aux couches sources QGIS."""
        self.profiles.clear()
        self.list.clear()
        self.chart.set_profile(None)
        self.status.setText('Prêt. Cliquez sur « Créer les profils » pour lancer une nouvelle analyse.')
    def closeEvent(self,event):
        self.reset_results()
        super().closeEvent(event)
    def refresh_layers(self):
        current=self.layers.currentData(); self.layers.blockSignals(True); self.layers.clear()
        for lyr in QgsProject.instance().mapLayers().values():
            if isinstance(lyr,QgsVectorLayer) and lyr.geometryType()==QgsWkbTypes.PointGeometry: self.layers.addItem(lyr.name(),lyr.id())
        i=self.layers.findData(current); self.layers.setCurrentIndex(max(0,i)); self.layers.blockSignals(False); self._fields()
    def _layer(self): return QgsProject.instance().mapLayer(self.layers.currentData())
    def _fields(self):
        lyr=self._layer(); self.group.clear(); self.date.clear(); self.zfield.clear(); self.zfield.addItem('Géométrie Z',None)
        if not lyr:return
        names=[f.name() for f in lyr.fields()]; self.group.addItems(names); self.date.addItems(names)
        for name in names: self.zfield.addItem(name,name)
        lowered={n.lower():n for n in names}
        for box,cands in ((self.group,['profil','profile_id','id_profil','transect','identifiant','id']), (self.date,['date','campagne','annee','année','year'])):
            for c in cands:
                if c in lowered: box.setCurrentText(lowered[c]); break
        for c in ('z','altitude','elevation','élévation','height'):
            if c in lowered: self.zfield.setCurrentIndex(self.zfield.findData(lowered[c])); break
    def load_profiles(self):
        try:
            lyr=self._layer()
            if not lyr: return
            if lyr.crs().isGeographic():
                QMessageBox.warning(self,'CRS non métrique','La couche utilise un CRS géographique. Reprojetez-la dans un CRS métrique avant de calculer les distances.')
                return
            groups=defaultdict(list); campaigns=defaultdict(set); gf=self.group.currentText(); df=self.date.currentText(); zf=self.zfield.currentData(); names=lyr.fields().names(); skipped=0
            for f in lyr.getFeatures():
                g=f.geometry()
                if not g or g.isEmpty(): skipped+=1; continue
                # vertices() est stable pour PointZ et MultiPointZ sous QGIS 3/4.
                try: pt=next(g.vertices())
                except StopIteration: skipped+=1; continue
                z=decimal(f[zf]) if zf else decimal(pt.z())
                if z is None or z!=z: skipped+=1; continue
                raw=f[gf]
                if raw is None: skipped+=1; continue
                ident=profile_identifier(raw)
                if ident is None: skipped+=1; continue
                state=str(f['État']) if 'État' in names else 'FIXE'
                groups[ident].append(SurveyPoint(float(pt.x()),float(pt.y()),float(z),decimal(f['HRMS']) if 'HRMS' in names else None,decimal(f['VRMS']) if 'VRMS' in names else None,state.upper().startswith('FIX'),f.id()))
                if df in names and f[df] not in (None,''):
                    value=f[df]; campaign=value.toString('yyyy') if hasattr(value,'toString') else str(value).strip(); campaigns[ident].add(campaign)
            self.profiles={}; self.list.clear()
            mixed=0
            for ident in sorted(groups,key=natural_sort_key):
                pts,isolated=main_spatial_group(groups[ident],self.distance.value()); skipped+=len(isolated)
                values=campaigns.get(ident,set()); campaign=next(iter(values)) if len(values)==1 else ('multi' if values else 'campagne'); mixed+=int(len(values)>1)
                if len(pts)>1: self.profiles[ident]=build_profile(ident,campaign,pts); self.list.addItem(ident)
            total=sum(len(p.points) for p in self.profiles.values())
            note=f' · {mixed} profil(s) avec plusieurs campagnes' if mixed else ''
            self.status.setText(f'{len(self.profiles)} profils créés à partir de {total} points · {skipped} point(s) écarté(s){note}. Orientation terre → mer.')
            if self.list.count(): self.list.setCurrentRow(0)
            else: QMessageBox.warning(self,'Aucun profil','Aucun groupe ne contient au moins deux points 3D. Vérifiez le champ identifiant et la présence des altitudes Z.')
        except Exception as exc:
            details=traceback.format_exc(); self.status.setText(f'Échec : {exc}')
            box=QMessageBox(self); box.setIcon(CRITICAL); box.setWindowTitle('CoastProfile — lecture impossible'); box.setText(str(exc)); box.setDetailedText(details); (box.exec if hasattr(box,'exec') else box.exec_)()
    def show_profile(self,name):
        p=self.profiles.get(name); self.chart.set_profile(p)
        if p:
            ids=[x.fid for x in p.points if x.fid is not None]; lyr=self._layer(); lyr.selectByIds(ids); self.iface.mapCanvas().zoomToSelected(lyr); self.iface.mapCanvas().refresh()
    def export_png(self):
        if not self.chart.profile: return
        path,_=QFileDialog.getSaveFileName(self,'Exporter le profil',f'{self.chart.profile.identifier}_{self.chart.profile.campaign}.png','PNG (*.png)')
        if path: self.chart.grab().save(path,'PNG'); self.status.setText(f'Graphique exporté : {path}')
    def export_all(self):
        if not self.profiles: return
        folder=QFileDialog.getExistingDirectory(self,'Choisir le dossier de destination')
        if not folder: return
        previous=self.list.currentItem().text() if self.list.currentItem() else None; done=0
        for ident,p in self.profiles.items():
            self.chart.set_profile(p); QApplication.processEvents()
            safe=ident.replace('/','_').replace(' ','_'); path=str(Path(folder)/f'{safe}_{p.campaign}.png')
            if self.chart.grab().save(path,'PNG'): done+=1
        if previous: self.list.setCurrentRow(list(self.profiles).index(previous))
        self.status.setText(f'{done} graphiques exportés dans : {folder}')
        QMessageBox.information(self,'Export terminé',f'{done} graphiques ont été enregistrés dans le dossier sélectionné.')
