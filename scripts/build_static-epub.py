#!/usr/bin/env python3
# Program altered by Peter F. Whyte, 2021-12-17
# to produce file suitable for Dorothea Press EPUB

from roman_numerals import convert_to_numeral

WORK_LIST = [
    "preface-first",
    "preface-second",
    "main",
]

TITLES = {
    "preface-first": "Preface 1st Edition",
    "preface-second": "Preface 2nd Edition",
    "main": "Main Text",
}

for WORK in WORK_LIST:
    print("processing: " + WORK)
    SRC = f"../text/young-tutorial-greek-{WORK}.txt"
    DEST = f"../docs/young-tutorial-greek-{WORK}.xhtml"

    TITLE = TITLES[WORK]

    HEADER = f"""\
    <?xml version="1.0" encoding="utf-8"?>
    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" epub:prefix="z3998: http://www.daisy.org/ns/z3998/authoring/, dp: ../Text/dp-vocab.xhtml" xml:lang="grc" lang="grc">
    <head>
    <title>{TITLE}</title>
    <link href="../Styles/dp.css" rel="stylesheet" type="text/css"/>
    </head>
    <body epub:type="bodymatter">
    """

    FOOTER = """\
    </body>
    </html>
    """

    with open(SRC, encoding="utf-8") as f:
        with open(DEST, "w", encoding="utf-8") as g:
            prev_section = None
            prev_chapter = None
            print(HEADER, file=g)
            for line in f:
                parts = line.strip().split(maxsplit=1)
                ref = parts[0].split(".")
                if len(ref) == 2:
                    section = None
                    chapter, verse = ref
                else:
                    section, chapter, verse = ref
                if prev_section != section:
                    if prev_section is not None:
                        print("   </section>""", file=g)
                        print("   </section>""", file=g)
                    print("""   <section epub:type="chapter" id="ch-{chapter}" role="doc-chapter" class="greek chapter">""", file=g)
                    prev_section = section
                    prev_chapter = None
                if prev_chapter != chapter:
                    if prev_chapter is not None:
                        if prev_chapter == "0":
                            if section is None:
                                #print("""    </section>3""", file=g)
                                print("""  """, file=g)
                        else:
                            print("""    </section>""", file=g)
                    if chapter == "0":
                        if section is None:
                            # preamble
                            print("""    <header>""", file=g)
                    else:
                        if chapter == "title":
                            # subscription
                            #print("""    <section class="subscription">""", file=g)
                            print("""  """, file=g)
                        elif chapter == "subtitle":
                            # epilogue
                            print("""    <section class="epilogue">""", file=g)
                        else:
                            #print({chapter})
                            if not chapter == "text":
                                print(f"""    <section epub:type="chapter" id="ch-{chapter}" role="doc-chapter" class="greek chapter">""", file=g)
                                if len(parts) > 1:
                                    print(f"""      <header><p class="chapter-number">{chapter}</p><h2 class="chapter-title" epub:type="title" lang="en" xml:lang="en" title="{chapter}. {parts[1]}">{parts[1]}</h2></header>""", file=g)
                                else:
                                    print(f"""      <header><p class="chapter-number">{chapter}</p></header>""", file=g)
                            else:
                               print(f"""    <section epub:type="chapter" id="ch-{chapter}" role="doc-chapter" class="greek chapter">""", file=g) 
                    prev_chapter = chapter
                    next
                if chapter == "0" and verse == "0":
                    # section_title
                    print(f"""    <p epub:type="title" class="part-number" lang="en" xml:lang="en" title="{parts[1]}">{parts[1]}</p>""", file=g)
                else:
                    if chapter != "0" and verse == "0":
                        # epilogue_title
                        print(f"""<h1 epub:type="title" class="part-title">{parts[1]}</h1>""", file=g)
                        print(f"""</header>""", file=g)
                    else:
                        # HANDLE VERSE
                        if not (verse == "title" or chapter == "0" or chapter == "text"):
                            #print(f"""      <p><span class="para-nbr" id="par-{verse}">{verse}</span>""", end="&nbsp;", file=g)
                            print(f""" <p>{parts[1]}</p>""", file=g)
                        else:
                            if chapter == "text":
                                print(f"""   <p>{parts[1]}</p>""", file=g)
            print("""    </section>""", file=g)

            if section is not None:
                print("""    </section>""", file=g)
            print(FOOTER, file=g)
