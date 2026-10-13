# Font sources

Fonts used by the PDF (Typst, `font-paths: [assets/fonts]`) and embedded in
the EPUB (`epub-fonts` in `_quarto.yml`). All are under the SIL Open Font
License 1.1; the license texts sit next to the files. Fetched 2026-10-13 from
the official Adobe GitHub releases; the OTF files are copied unmodified.

| Family | Release | Archive | Archive SHA-256 |
|---|---|---|---|
| Source Serif 4 (body) | [4.005R](https://github.com/adobe-fonts/source-serif/releases/tag/4.005R) | https://github.com/adobe-fonts/source-serif/releases/download/4.005R/source-serif-4.005_Desktop.zip | `549fdb8f9a682bd06944298621404969f6de77c2e422ff3b8244a1dcd6a0c425` |
| Source Sans 3 (headings, captions, running heads) | [3.052R](https://github.com/adobe-fonts/source-sans/releases/tag/3.052R) | https://github.com/adobe-fonts/source-sans/releases/download/3.052R/OTF-source-sans-3.052R.zip | `a4ebbdea20b08ccbd7bf3665a9462454eefdd01d9a6307129d3b3d4672981074` |

License files: `OFL-SourceSerif4.md` is `LICENSE.md` from the Source Serif
archive; `OFL-SourceSans3.md` is
https://raw.githubusercontent.com/adobe-fonts/source-sans/3.052R/LICENSE.md
(the OTF archive ships without it).

Files (SHA-256):

```
7776ddb9f3eb58683e59f28d558d8896b768c2d0c80799fb3f1c56c54dfd98c9  SourceSans3-Bold.otf
430b9f0eb1170be0981706d14b6cf87122efba9d86c373bbdf69daf276421462  SourceSans3-It.otf
bbfab2c58d46defe8a194634744660ee15d560dcf3d7a8c7bb509936acc618c7  SourceSans3-Light.otf
08df266400933d3178d081a45f94a08814c3e55b4b7dd2e0ff69cb1329f13ab6  SourceSans3-Regular.otf
81204ed282543df2d93db214c98b5ec1c9ce735c4c82e4323d5ae5ee69c6b8b7  SourceSans3-SemiboldIt.otf
36f1cd2c344aa3109e64429bce41a41e4b2b923beb2db19b8dbf9bb56f05a4f9  SourceSans3-Semibold.otf
ebb5394e1e11e09480619c9bb10f020aded9530833edcbdb735a4702ae6fa09e  SourceSerif4-BoldIt.otf
f5fb9a7b1611353fdfebcf8b1e46c7d9108470f25999b841816d8b643b1856ff  SourceSerif4-Bold.otf
f8062257f4693e438a8e317c9fe2b4393f0d4eed84d897edcbfd733c30a1c1a1  SourceSerif4-It.otf
edf160d0d584deee8a3bb2c3371b2a7624ca63580fbe02c57c1f4c91e84d8787  SourceSerif4-Regular.otf
fc22addcea5d5ab982dfef6d388fff6bdb3e31ae46c37e0015b8312e634a6e9b  SourceSerif4-SemiboldIt.otf
25e034392847d9965c92f98971b3646436b7ab919ece9118b0c0e5ec94c02efc  SourceSerif4-Semibold.otf
89ad2c4f66dd29127527493e729c31e731f111cf10faf5774c3db9275ed0c22c  OFL-SourceSans3.md
75784a295293a8992f5a8d99210566e0064a012e6dab6731305e3787f15896c7  OFL-SourceSerif4.md
```

The Noto Sans files (`NotoSans-*.ttf`, `OFL-NotoSans.txt`) are used only for
D2 diagram labels (`scripts/render_diagram.rb`).
