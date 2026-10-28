"""Reduce embedded image resolution in the approved Aud v15, preserving vectors/text."""
from pathlib import Path
import json,hashlib,math,io
import pymupdf
from PIL import Image
HERE=Path(__file__).resolve().parent
SOURCE=HERE/'render_full_map_v15/Aud_Full_Map_v15.pdf'
OUT=HERE/'aud_map_optimized_v15'

def build():
 OUT.mkdir(exist_ok=True)
 before=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
 src=pymupdf.open(SOURCE);source_text=src[0].get_text();source_paths=len(src[0].get_drawings())
 report={'source_bytes':SOURCE.stat().st_size,'source_sha256':before,'source_vector_paths':source_paths,'outputs':{}}
 for name,dpi,quality in [('Aud_Map_v15_Print_300dpi.pdf',300,92),('Aud_Map_v15_Web_200dpi.pdf',200,88)]:
  d=pymupdf.open(SOURCE)
  # Resize each unique image once at its largest placed size; rebuild RGBA atomically.
  # This avoids rewrite_images changing shared pictures/masks repeatedly at smaller uses.
  images={item[0]:item for item in d[0].get_images(full=True)}
  placements={}
  for info in d[0].get_image_info(xrefs=True):
   placements.setdefault(info['xref'],[]).append(pymupdf.Matrix(info['transform']))
  for xref,item in images.items():
   _,smask,iw,ih,*_=item
   uses=placements.get(xref,[])
   if not uses:continue
   scale=min(1,max(max(math.hypot(m.a,m.b)*dpi/72/iw,math.hypot(m.c,m.d)*dpi/72/ih) for m in uses))
   if scale>=.98:continue
   pix=pymupdf.Pixmap(d,xref)
   if pix.colorspace and pix.colorspace.n!=3:pix=pymupdf.Pixmap(pymupdf.csRGB,pix)
   if smask:
    mask=pymupdf.Pixmap(d,smask)
    pix=pymupdf.Pixmap(pix,mask)
   im=Image.frombytes('RGBA' if pix.alpha else 'RGB',[pix.width,pix.height],pix.samples)
   im=im.resize((max(1,math.ceil(iw*scale)),max(1,math.ceil(ih*scale))),Image.Resampling.LANCZOS)
   stream=io.BytesIO();im.save(stream,'PNG',optimize=True)
   d[0].replace_image(xref,stream=stream.getvalue())
  print('Saving',name,flush=True)
  target=OUT/name
  d.save(target,garbage=4,deflate=True,deflate_images=True,deflate_fonts=True,use_objstms=1,compression_effort=100)
  d.close()
  check=pymupdf.open(target)
  assert len(check)==1 and check[0].rect==src[0].rect
  assert check[0].get_text()==source_text,'Selectable text changed'
  assert len(check[0].get_drawings())==source_paths,'Vector path count changed'
  check[0].get_pixmap(matrix=pymupdf.Matrix(2,2)).save(OUT/(target.stem+'_preview.png'))
  report['outputs'][name]={'bytes':target.stat().st_size,'reduction_percent':round((1-target.stat().st_size/SOURCE.stat().st_size)*100,2),'image_dpi':dpi,'compression':'lossless PNG after resampling; alpha preserved','text_and_vector_paths_preserved':True}
 # Web image from the approved source, with enough pixels for zooming and all fine labels.
 width=2400
 pix=src[0].get_pixmap(matrix=pymupdf.Matrix(width/src[0].rect.width,width/src[0].rect.width),alpha=False)
 image=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
 target=OUT/'Aud_Map_v15_Game_2400.webp';image.save(target,'WEBP',quality=90,method=6)
 report['outputs'][target.name]={'bytes':target.stat().st_size,'width':pix.width,'height':pix.height,'webp_quality':90}
 # Comparison crops at high magnification allow reviewing small symbols and type.
 crop=pymupdf.Rect(330,380,535,565)
 for label,path in [('Original',SOURCE),('Print',OUT/'Aud_Map_v15_Print_300dpi.pdf'),('Web',OUT/'Aud_Map_v15_Web_200dpi.pdf')]:
  d=pymupdf.open(path);d[0].get_pixmap(matrix=pymupdf.Matrix(4,4),clip=crop).save(OUT/('Detail_'+label+'.png'))
 assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==before
 (OUT/'compression_report.json').write_text(json.dumps(report,indent=2))
 print(json.dumps(report,indent=2))
if __name__=='__main__':build()

