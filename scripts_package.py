from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
root=Path(__file__).parent; source=root/'coastprofile'; target=root/'coastprofile-0.2.0.zip'
with ZipFile(target,'w',ZIP_DEFLATED) as z:
    for p in source.rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts: z.write(p,Path('coastprofile')/p.relative_to(source))
print(target)
