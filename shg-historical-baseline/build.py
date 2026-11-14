"""Build a TST-branded Master Synthesis.docx from the markdown-style baseline draft.
Usage: python3 -I build.py <draft.txt> <logo.jpg> <out.docx>
Writes raw OOXML (no external libs) so the file stays small."""
import sys, zipfile, re
from xml.sax.saxutils import escape

src, logo, out = sys.argv[1], sys.argv[2], sys.argv[3]
lines = open(src, encoding="utf-8").read().splitlines()

ORANGE, BLUE, GREEN, GREY = "E05729", "0070C0", "548135", "3F403F"
LOGO_W_EMU = int(2.6 * 914400)
LOGO_H_EMU = LOGO_W_EMU // 4  # logo is 4:1

def run(text, rpr=""):
    t = escape(text)
    return f'<w:r>{"<w:rPr>"+rpr+"</w:rPr>" if rpr else ""}<w:t xml:space="preserve">{t}</w:t></w:r>'

def para(text, style=None, ppr_extra="", rpr=""):
    ppr = (f'<w:pStyle w:val="{style}"/>' if style else "") + ppr_extra
    return f'<w:p>{"<w:pPr>"+ppr+"</w:pPr>" if ppr else ""}{runs(text, rpr)}</w:p>'

TAG = re.compile(r"(\[[^\[\]]*\bT[1-4][^\[\]]*\])")
def runs(text, rpr=""):
    # render source-tier tags like [T1] / [L2GP, T3] in smaller grey italics
    out = []
    for part in TAG.split(text):
        if not part:
            continue
        if TAG.fullmatch(part):
            out.append(run(part, rpr + f'<w:i/><w:color w:val="{GREY}"/><w:sz w:val="20"/>'))
        else:
            out.append(run(part, rpr))
    return "".join(out)

def bullet(text, lvl):
    return para(text, "ListParagraph", f'<w:numPr><w:ilvl w:val="{lvl}"/><w:numId w:val="1"/></w:numPr>')

def image(rid, cx, cy, pid, name):
    return (f'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
            f'<wp:docPr id="{pid}" name="{name}" descr="The Share Trust logo"/>'
            '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:nvPicPr><pic:cNvPr id="{pid}" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>')

body = []
# ---- cover page ----
title = lines[0].lstrip("# ").strip()
body.append(f'<w:p><w:pPr><w:spacing w:before="1800" w:after="600"/></w:pPr>{image("rIdLogo", LOGO_W_EMU*14//10, LOGO_H_EMU*14//10, 1, "Logo")}</w:p>')
body.append(para(title, "Title"))
body.append(para("Master Synthesis: Self-Help Groups Research, opening section", "Subtitle"))
body.append(para("Historical Baseline (2023–2026). All ten pillars complete. Prepared November 2026.", None,
                 '<w:spacing w:after="1200"/>'))

i = 1
works = False
for raw in lines[1:]:
    line = raw.rstrip()
    if not line.strip():
        continue
    if line.startswith("[BUILD NOTE"):
        continue  # internal tooling note, not part of the human-facing document
    if line.startswith("AI Disclosure:"):
        body.append(para(line, None, f'<w:pBdr><w:top w:val="single" w:sz="6" w:space="6" w:color="{ORANGE}"/></w:pBdr>',
                         f'<w:i/><w:sz w:val="20"/>'))
        body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
        continue
    if line.startswith("### "):
        body.append(para(line[4:], "Heading2")); continue
    if line.startswith("## "):
        h = line[3:]
        works = h.startswith("Works Referenced")
        body.append(para(h, "Heading1")); continue
    if line.startswith("# "):
        body.append(para(line[2:], "Heading1")); continue
    m = re.match(r"^(\s*)- (.*)$", line)
    if m:
        body.append(bullet(m.group(2), 1 if len(m.group(1)) >= 2 else 0)); continue
    if works:
        body.append(para(line, "Reference")); continue
    body.append(para(line))

sect = ('<w:sectPr><w:headerReference w:type="default" r:id="rIdHdr"/><w:footerReference w:type="default" r:id="rIdFtr"/>'
        '<w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>'
        '<w:titlePg/></w:sectPr>')

NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"')
document = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {NS}><w:body>{"".join(body)}{sect}</w:body></w:document>'

header = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr {NS}>'
          f'<w:p><w:pPr><w:tabs><w:tab w:val="right" w:pos="9360"/></w:tabs></w:pPr>{image("rIdLogoH", LOGO_W_EMU*6//10, LOGO_H_EMU*6//10, 2, "HeaderLogo")}'
          f'<w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:tab/><w:t>Historical Baseline (2023–2026): SHGs Across TST Pillars</w:t></w:r></w:p></w:hdr>')
footer = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr {NS}><w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
          '<w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>'
          '<w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
          '<w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:fldChar w:fldCharType="separate"/></w:r>'
          '<w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>1</w:t></w:r>'
          '<w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>')

def style(sid, name, ptype="paragraph", ppr="", rpr="", based="Normal", extra=""):
    b = f'<w:basedOn w:val="{based}"/>' if based else ""
    return (f'<w:style w:type="{ptype}" w:styleId="{sid}"><w:name w:val="{name}"/>{b}{extra}'
            f'<w:pPr>{ppr}</w:pPr><w:rPr>{rpr}</w:rPr></w:style>')

FONT = '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri"/>'
styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
          f'<w:docDefaults><w:rPrDefault><w:rPr>{FONT}<w:color w:val="{GREY}"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr></w:rPrDefault>'
          '<w:pPrDefault><w:pPr><w:spacing w:after="160" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
          + style("Normal", "Normal", based=None, extra='<w:qFormat/>')
          + style("Title", "Title", ppr='<w:spacing w:after="240"/>', rpr=f'<w:b/><w:color w:val="{ORANGE}"/><w:sz w:val="52"/>', extra='<w:qFormat/>')
          + style("Subtitle", "Subtitle", ppr='<w:spacing w:after="240"/>', rpr=f'<w:color w:val="{BLUE}"/><w:sz w:val="28"/>', extra='<w:qFormat/>')
          + style("Heading1", "heading 1", ppr='<w:keepNext/><w:spacing w:before="360" w:after="120"/><w:outlineLvl w:val="0"/>',
                  rpr=f'<w:b/><w:color w:val="{ORANGE}"/><w:sz w:val="32"/>', extra='<w:next w:val="Normal"/><w:qFormat/>')
          + style("Heading2", "heading 2", ppr='<w:keepNext/><w:spacing w:before="240" w:after="80"/><w:outlineLvl w:val="1"/>',
                  rpr=f'<w:b/><w:color w:val="{BLUE}"/><w:sz w:val="28"/>', extra='<w:next w:val="Normal"/><w:qFormat/>')
          + style("Heading3", "heading 3", ppr='<w:keepNext/><w:spacing w:before="200" w:after="60"/><w:outlineLvl w:val="2"/>',
                  rpr=f'<w:b/><w:color w:val="{GREEN}"/><w:sz w:val="24"/>', extra='<w:next w:val="Normal"/><w:qFormat/>')
          + style("ListParagraph", "List Paragraph", ppr='<w:spacing w:after="80"/><w:ind w:left="720"/>', extra='<w:qFormat/>')
          + style("Reference", "Reference", ppr='<w:spacing w:after="80"/><w:ind w:left="360" w:hanging="360"/>', rpr='<w:sz w:val="20"/>')
          + '</w:styles>')

numbering = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
             '<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="hybridMultilevel"/>'
             f'<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr><w:rPr><w:color w:val="{ORANGE}"/></w:rPr></w:lvl>'
             f'<w:lvl w:ilvl="1"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="–"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="1440" w:hanging="360"/></w:pPr><w:rPr><w:color w:val="{BLUE}"/></w:rPr></w:lvl>'
             '</w:abstractNum><w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>')

ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
      '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
      '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
      '<Default Extension="xml" ContentType="application/xml"/><Default Extension="jpeg" ContentType="image/jpeg"/>'
      '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
      '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
      '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
      '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
      '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
      '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
      '</Types>')
rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '</Relationships>')
RT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"
docrels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
           f'<Relationship Id="rIdStyles" Type="{RT}styles" Target="styles.xml"/>'
           f'<Relationship Id="rIdNum" Type="{RT}numbering" Target="numbering.xml"/>'
           f'<Relationship Id="rIdHdr" Type="{RT}header" Target="header1.xml"/>'
           f'<Relationship Id="rIdFtr" Type="{RT}footer" Target="footer1.xml"/>'
           f'<Relationship Id="rIdLogo" Type="{RT}image" Target="media/logo.jpeg"/>'
           '</Relationships>')
hdrrels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
           f'<Relationship Id="rIdLogoH" Type="{RT}image" Target="media/logo.jpeg"/></Relationships>')
core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:title>Master Synthesis: Historical Baseline (2023–2026)</dc:title><dc:creator>The Share Trust (AI-assisted draft)</dc:creator>'
        '<dcterms:created xsi:type="dcterms:W3CDTF">2026-11-14T00:00:00Z</dcterms:created></cp:coreProperties>')

with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    z.writestr("[Content_Types].xml", ct)
    z.writestr("_rels/.rels", rels)
    z.writestr("docProps/core.xml", core)
    z.writestr("word/document.xml", document)
    z.writestr("word/styles.xml", styles)
    z.writestr("word/numbering.xml", numbering)
    z.writestr("word/header1.xml", header)
    z.writestr("word/footer1.xml", footer)
    z.writestr("word/_rels/document.xml.rels", docrels)
    z.writestr("word/_rels/header1.xml.rels", hdrrels)
    z.write(logo, "word/media/logo.jpeg", compress_type=zipfile.ZIP_STORED)
print(out, len(body), "paragraphs")
