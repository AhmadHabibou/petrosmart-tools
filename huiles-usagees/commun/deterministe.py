"""Rend reproductibles les fichiers Office (docx, xlsx, pptx) : horodatages fixes dans l'archive et les proprietes."""
from pathlib import Path
import re
import zipfile

DATE_ZIP = (2026, 11, 18, 0, 0, 0)
DATE_ISO = "2026-11-18T00:00:00Z"


def figer(chemin):
    chemin = Path(chemin)
    with zipfile.ZipFile(chemin) as z:
        entrees = [(i, z.read(i.filename)) for i in z.infolist()]
    tmp = chemin.with_suffix(chemin.suffix + ".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for info, data in entrees:
            if info.filename == "docProps/core.xml":
                txt = data.decode("utf-8")
                txt = re.sub(r"(<dcterms:(created|modified)[^>]*>)[^<]*(</dcterms:\2>)", r"\g<1>" + DATE_ISO + r"\g<3>", txt)
                data = txt.encode("utf-8")
            zi = zipfile.ZipInfo(info.filename, DATE_ZIP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)
    tmp.replace(chemin)
