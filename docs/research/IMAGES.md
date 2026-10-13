# Images: generated illustrations, diagrams and real photos

Research date: 2026-10-13. Prices, model IDs and terms change often; every claim below links to the
source it was checked against (see [Sources](#sources)). Items marked **(tested)** were run against
the live API today. This is research, not legal advice; for the cover and for anything borderline,
ask a lawyer in Brazil and the US.

---

## 1. Recommendation in one screen

| Figure type | Tool | Why |
|---|---|---|
| Technical / process diagrams (pipelines, "how a token is predicted", agent loops, timelines) | **Diagrams as code: D2 (primary) + Graphviz (graphs/trees)**, exported to SVG → PDF for print, PNG for EPUB | Reproducible, diffable, vector, and the labels live in text files you can translate. One source → PT-BR and EN builds. |
| Conceptual / metaphor illustrations (chapter openers, "the model as autocomplete", "context window as a desk") | **AI image model, label-free**, then labels overlaid as real text in an SVG template per language | Models still misspell; bilingual books would need two generations per figure anyway. |
| Real people and events | **Wikimedia Commons first**, then Flickr CC (via Commons when possible), US-federal public-domain sources, written permission from press offices, and paid editorial licences (Getty/AP) only as a last resort | Free licences that allow commercial use; machine-readable licence metadata. |
| Likenesses of real people | **Never generate.** Use real photos or nothing. | Misleading, provider-policy and personality-rights risk. |

Model picks (as of 2026-10-13):

- **Default generator:** OpenAI `gpt-image-2.5-flare` (pinned snapshot `gpt-image-2.5-flare-2026-09-08`), `quality: medium` for drafts, `high` for finals, `size: 2048x1536` or `1536x2048` for print. **(tested)**
- **Second opinion / style alternative:** Google `gemini-nano-banana-2.1` at 2K ($0.050/image), or `gemini-3-pro-image` (Nano Banana Pro) when a figure truly needs baked-in text ($0.134 at 1K/2K).
- **Vector line art:** Recraft v4.1 vector models via OpenRouter (`recraft/recraft-v4.1-vector`, `...-pro-vector`) produce SVG output that can be edited in Inkscape, which suits line-art spot illustrations.
- **Do not build on:** `gpt-image-1` (older, most expensive per token), `gemini-2.5-flash-image` (Google lists shutdown on 2026-10-02), and Imagen 4 (deprecated, shutdown listed for 2026-08-17, and absent from the live model list today).

Expected budget: ~60 illustrations × ~4 drafts × ≤$0.21 ≈ **under $50** in API spend. Cost isn't the constraint. The work is art direction and consistency.

---

## 2. Generated illustrations (a)

### 2.1 What the keys can reach today

I listed models live from each API on 2026-10-13 (`/v1/models` for OpenAI, `v1beta/models` for Gemini, `/api/v1/models?output_modalities=image` for OpenRouter).

**OpenAI** (Images API `POST /v1/images/generations`, or the Responses API `image_generation` tool)

| Model | Token price (image in / out per 1M) | Per-image, 1024×1024 (low / med / high) | Notes |
|---|---|---|---|
| `gpt-image-2.5-flare` | $8 / $30 | not published as a table. **Measured:** low 1024² = 196 output tokens ≈ **$0.006**; medium 1536×1024 = 343 tokens ≈ **$0.011** | Released 2026-09-08. "Fast everyday generation". Quality up to `xhigh`/`max`. |
| `gpt-image-2.5-sunburst` | $8 / $30 | same rates, uses more tokens | Precision editing/retouching sibling. |
| `gpt-image-2` | $8 / $30 | $0.006 / $0.053 / $0.211 | Max edge 3840 px, total 0.65–8.3 MP, both edges multiples of 16, ratio ≤ 3:1. Above 2560×1440 is "experimental". |
| `gpt-image-1.5` | $8 / $32 | $0.009 / $0.034 / $0.133 | |
| `gpt-image-1-mini` | $2.5 / $8 | $0.005 / $0.011 / $0.036 | Cheap drafts. |
| `gpt-image-1` | $10 / $40 | $0.011 / $0.042 / $0.167 | Legacy. |

Parameters: `model, prompt, n, size, quality (low|medium|high|xhigh|max|auto), background (transparent|opaque|auto), output_format (png|jpeg|webp), output_compression, moderation (auto|low), stream, partial_images`. **There is no `seed` parameter**, so you can't reproduce an image exactly. You reproduce it by keeping the pinned snapshot ID, the exact prompt, the parameters and the original file. Response: `data[0].b64_json`, `data[0].generation_id`, plus `usage`, `size`, `quality`, `background`, `output_format`. **(tested)**

**Google Gemini API** (`POST v1beta/models/{model}:generateContent`, `generationConfig.responseModalities:["IMAGE"]`, `imageConfig.{aspectRatio, imageSize:"1K"|"2K"|"4K"}`; uppercase K required)

| Model ID | Per image (standard) | Batch | Sizes |
|---|---|---|---|
| `gemini-nano-banana-2.1` (Nano Banana 2.1) | 1K $0.0336, 2K $0.0504, 4K $0.113 | half | 1K/2K/4K. Google recommends it for new projects. |
| `gemini-3.1-flash-image` (Nano Banana 2) | 0.5K $0.045, 1K $0.067, 2K $0.101, 4K $0.151 | half | 0.5K–4K |
| `gemini-3-pro-image` (Nano Banana Pro) | 1K/2K $0.134, 4K $0.24 | half | Thinking always on. Strongest text rendering. |
| `gemini-3.1-flash-lite-image` | 1K $0.0336 | $0.0168 | 1K only. No grounding. **(tested)** |
| `gemini-2.5-flash-image` | $0.039 | $0.0195 | Deprecated, shutdown 2026-10-02. |

No free API tier for image models. Every output carries a **SynthID** watermark. Response: `candidates[0].content.parts[].inlineData{mimeType,data}`. **The tested output was JPEG** (1200×896 for 4:3 at 1K) even though nothing was requested, so save it as `.jpg`. No seed parameter either.

**OpenRouter** (one key, many vendors; `POST /api/v1/images` returning `data[].b64_json`, or chat completions). Notable image-output models listed today: `openai/gpt-image-2.5-flare|sunburst`, `openai/gpt-image-2`, `google/gemini-nano-banana-2.1`, `google/gemini-3-pro-image`, `black-forest-labs/flux-3-image`, `flux.2-pro|max|flex`, `recraft/recraft-v4.1[-pro][-vector]` and `recraft-v4-styles*` (vector/SVG and style-locked variants), `bytedance-seed/seedream-5-0-*`, `qwen/qwen-image-3[-pro]`, `x-ai/grok-imagine-image-2.0`, `microsoft/mai-image-2.6`, `krea/krea-2-*`. OpenRouter's terms say output ownership is whatever **each model's own terms** say, so you have to read the upstream licence for any non-OpenAI/Google model before using it commercially (FLUX in particular has had separate licences per variant).

**HF:** the token is useful for open-weight models via Inference Providers, but nothing there beats the above for this use, and licences vary per model card. Skip it unless you want a fully local pipeline.

### 2.2 Test results (2026-10-13)

Scratch files: `/tmp/claude-1026/-mnt-data-Projects-ai-book-2026/a99c0f7c-c2d5-41cf-8ba5-c586f177de60/scratchpad/img-test/`. Total spend ≈ $0.09.

1. **Label-free concept art, same prompt, both vendors.** `gpt-image-2.5-flare` low 1024² took 11 s and ≈$0.006. `gemini-3.1-flash-lite-image` 1K took 4 s and ≈$0.034. Both followed the two-colour hex palette and "no text" instruction, and both kept their contrast after `magick -colorspace Gray`.
2. **Baked-in PT-BR labels** ("Texto de entrada", "Previsão do próximo token", "Atenção à sequência"). `gpt-image-2.5-flare` medium rendered all three correctly, with diacritics. `gemini-3.1-flash-lite-image` rendered the accents but wrote **"Previsão do do próximo token"**. This is the failure mode that argues for overlaying text yourself.
3. **Provenance metadata.** Both outputs embed **C2PA** manifests (`digitalSourceType = trainedAlgorithmicMedia`; claim generator "OpenAI Media Service API" / "Google C2PA Core Generator Library"). Keep the originals with their manifests in the archive. Print and EPUB exports will strip them, and that's fine; the YAML record below is your provenance.

Minimal working calls (keys stay in env, never echoed):

```bash
# OpenAI
( . ~/.config/zsh/secrets
  curl -s https://api.openai.com/v1/images/generations \
    -H "Authorization: Bearer $OPENAI_API_KEY" -H "Content-Type: application/json" \
    -d '{"model":"gpt-image-2.5-flare-2026-09-08","prompt":"...","size":"2048x1536","quality":"high","output_format":"png"}' \
  | tee resp.json | jq -r '.data[0].b64_json' | base64 -d > fig.png
  jq '{usage, generation_id: .data[0].generation_id}' resp.json )

# Gemini
( . ~/.config/zsh/secrets
  curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-nano-banana-2.1:generateContent" \
    -H "x-goog-api-key: $GEMINI_API_KEY" -H "Content-Type: application/json" \
    -d '{"contents":[{"parts":[{"text":"..."}]}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"4:3","imageSize":"2K"}}}' \
  | tee resp.json | jq -r '.candidates[0].content.parts[]|select(.inlineData)|.inlineData.data' | head -1 | base64 -d > fig.jpg
  jq '{modelVersion, responseId, usageMetadata}' resp.json )
```

### 2.3 Text in images and bilingual editions

- Vendors claim better text rendering (Google: "legible, stylized text for infographics, menus, diagrams"). OpenAI's own guide still says the model "can still struggle with precise text placement and clarity". Test 2 above shows both outcomes.
- With two editions, any baked-in label means two generations. The two images would then differ in composition, so PT and EN figures would not match.
- **Rule: generate art with "no text, no letters, no numbers" in the prompt, and add labels yourself.** Put the raster in an SVG template (`<image href="art.png"/>` + `<text>` elements read from `labels.pt.yml` / `labels.en.yml`), and render with `rsvg-convert` or Inkscape CLI, both of which are installed. If a model sneaks in pseudo-text, edit it out with the Sunburst/Nano Banana edit endpoints or in an image editor.
- Anything that is really a diagram (boxes, arrows, axes, numbers) should not be generated at all. Draw it as code (section 3).

### 2.4 Rights, copyright and KDP

**Who owns outputs**
- OpenAI (API customers, Services Agreement §4.1): customer "owns all Output", and OpenAI assigns its rights "if any". Outputs generated for other users are not yours (§4.4). OpenAI's consumer Terms page returned 403 to automated fetches today. The API is governed by the Services Agreement anyway.
- Google Gemini API Additional Terms (effective 2026-03-23, updated 2026-04-28): "Google won't claim ownership over that content"; "You're responsible for your use of generated content". Use is for "professional or business purposes".
- OpenRouter: ownership follows each upstream model's terms.

**Copyrightability (this matters for the book, not for your right to use the images)**
- US: the Copyright Office's Part 2 report (2025-01-29) concludes that prompts alone don't make you the author of the output. Human selection, arrangement and modification can be protected. *Thaler v. Perlmutter* (D.C. Cir. 2025-03-18) held that human authorship is required, and the Supreme Court **denied cert on 2026-03-02**. If you register the book in the US, disclaim the AI-generated images.
- Brazil: Lei 9.610/98 art. 11 says "Autor é a pessoa física criadora de obra literária, artística ou científica". Purely generated images likely have no author and no protection. PL 2338/2023 (the AI bill, including a copyright section) is still pending in the Câmara as of mid-2026.
- Practical consequence: anyone could probably copy the raw AI art from your book. Your text, your layouts, your overlaid labels and your composites stay protected. That's acceptable for interior art. It's another reason to make the cover's key elements human-made, or human-composited at least.

**KDP AI disclosure (KDP Content Guidelines)**
- You must disclose AI-generated "text, images, or translations" when publishing or republishing. "AI-generated images include cover and interior images and artwork". Content counts as AI-generated "even if you applied substantial edits afterwards".
- AI-*assisted* work (you created it and used AI to edit, refine, error-check, or brainstorm) does not need disclosure.
- For this book: answer **yes, AI-generated images**, in both editions. If the translation of either edition was done by an LLM, the "translations" item may also apply; check how the EN text is produced.
- Diagrams-as-code that you write or review are your work. If an LLM drafted the D2 source, that is at least AI-assisted, and arguably generated. When in doubt, disclose, since disclosure is cheap.
- You also certify that AI content meets the IP rules, so keep logos, real faces and recognisable art styles of living artists out of the prompts.

---

## 3. Diagrams as code

| Tool | Strengths | Weaknesses | Verdict |
|---|---|---|---|
| **D2** (v0.9.0, 2026-09-07, MPL-2.0) | Clean declarative syntax; themes; ELK/dagre layouts; `sketch: true` gives a hand-drawn Excalidraw look; SVG/PNG/PDF export; single Go binary (not installed yet) | Fine positioning sometimes fights the layout engine | **Primary.** Best ratio of looks to effort for flows, architectures and agent loops. |
| **Graphviz** (`dot`, installed) | Rock-solid layout of trees and DAGs; SVG/PDF; stable for decades | Dated default look (fixable with attributes) | **Secondary** for trees (tokenizer BPE merges, decision trees) and big graphs. |
| **Mermaid** (CLI 12.0.0) | Ubiquitous; renders on GitHub | Needs headless Chromium; SVG labels use `<foreignObject>` by default, which breaks in rsvg/Inkscape/EPUB readers (set `htmlLabels: false`); limited style control | Only for quick drafts. |
| **Excalidraw** (v0.18.1, MIT) | The friendly hand-drawn look lay readers like | GUI-first; `.excalidraw` JSON is diffable but translation means editing JSON | Use D2 `sketch` mode for that look instead. |
| **TikZ** | Best typographic quality; precise | Steep learning curve; needs a LaTeX toolchain (none installed) | Only if the book goes LaTeX. |
| **Typst** (v0.15.1) + `cetz` (v0.5.2) / `fletcher` | Native if the book is typeset in Typst; same fonts as body text | Couples figures to Typst | Choose it if the build moves to Typst. The book uses Pandoc-style spans (`[termo]{.glossario}`), so the build is probably Pandoc. Keep figures as standalone SVG/PDF, which works with any build. |

**Translation workflow:** one `fig-xx.d2` source with placeholder labels, plus `fig-xx.labels.yml` holding `pt:` and `en:` keys. A small `scripts/figures.rb` substitutes the labels, renders `build/figures/{pt,en}/fig-xx.svg`, converts to PDF (print) and 2× PNG (EPUB), and runs the grayscale check. Commit the sources. Don't commit rendered output.

---

## 4. House visual style spec

**Page assumptions:** 6×9 in trim, text block ≈ 4.5–4.75 in, so 300 DPI needs ≥ **1425 px** for full text width and ≥ 1875 px for full bleed. KDP print requires ≥ 300 DPI, recommends ≤ 600 DPI, and wants images at 100% size. Kindle requires sRGB, **no transparency** (flatten onto paper colour), no CMYK, and wants images with text to fill ≥ 80% of screen width. Kindle's e-reader preview is grayscale.

**Palette** (chosen by lightness so it survives grayscale and e-ink; CIE L* computed):

| Token | Hex | L* | Use |
|---|---|---|---|
| ink | `#1B2238` | 14 | Outlines, text, arrows |
| navy | `#2B3A67` | 25 | Primary fills |
| teal | `#2F7F86` | 49 | Secondary fills |
| gray | `#8A8F98` | 59 | Muted / "inactive" elements |
| amber | `#E3A23B` | 71 | The **one** highlight per figure |
| sand | `#E9DFC9` | 89 | Panels, background blocks (≥ 10% gray when printed, per KDP's minimum fill) |
| paper | `#FBF9F4` | 98 | Background (never transparent) |

Rules: adjacent fills must differ by **≥ 20 L***. Never use colour as the only signal; pair it with a label, pattern (hatch/dots) or line style. For an alarm/"danger" accent, use rust `#B5523B` (L* 47), but never next to teal, because they turn into the same gray.

**Lines and type (at final print size):** main strokes 1.5 pt, secondary 0.75 pt, minimum 0.5 pt. Round caps and joins. One arrowhead style. Corner radius 4 pt. Labels in one OFL sans with full PT glyphs (IBM Plex Sans or Inter): 8.5 pt regular, 7 pt minimum, titles 10 pt semibold. No text inside AI art.

**AI art prompt prefix (keep constant, version it):**

```
STYLE v1: flat editorial vector illustration, thick uniform ink outlines (#1B2238),
limited palette navy #2B3A67, teal #2F7F86, amber #E3A23B accent, sand #E9DFC9 panels,
off-white #FBF9F4 background, generous whitespace, no gradients, no textures,
no text, no letters, no numbers, no logos, no real people, high contrast,
reads clearly in grayscale.
```

Also pass a reference image (a previously approved figure) on every call. Both OpenAI edits/Responses and Gemini (up to 14 references) support this, and it keeps the series consistent.

**QA per figure:** `magick fig.png -colorspace Gray fig-gray.png`, then view it at 100% and at Kindle size. Check DPI = px / printed inches ≥ 300. Flatten alpha. Convert to sRGB. Run a spell-check on the label YAML.

---

## 5. Real photos (b)

### 5.1 Sources, in order of preference

1. **Wikimedia Commons.** Free licences only (CC0, PD, CC BY, CC BY-SA, some GFDL/FAL). Machine-readable metadata via the API. Coverage check today:
   - **Sam Altman:** several TechCrunch / Village Global photos, CC BY 2.0, up to 3327×5000.
   - **Dario Amodei:** TechCrunch Disrupt 2023, CC BY 2.0, 4000×2667; UK Prime Minister's office, CC BY 2.0.
   - **Jensen Huang:** a 2026-04-30 Stanford series.
   - **Linus Torvalds:** LinuxCon Europe 2014, CC BY-SA 4.0, 3282×4922.
   - **Demis Hassabis:** Nobel Week 2024, CC BY-SA 4.0, **tagged `personality`**.
   - **Andrej Karpathy:** a problem. The CC BY 3.0 photo is only 490×665 (≈1.6×2.2 in at 300 DPI), and a "CC0" 2016 photo uploaded by a third party looks like licence laundering. Expect to ask him or his team directly.
2. **Flickr CC.** Many Commons files came from Flickr (TechCrunch, Village Global, governments). Prefer the Commons copy: Commons runs a licence-review bot/template that records the licence at upload time, which protects you if the Flickr owner later changes it. If you take from Flickr directly, screenshot and record the licence on the date you take it. Only CC BY, CC BY-SA, CC0, PDM and "US Government Work" allow commercial use. Skip anything NC or ND, and remember the book is commercial.
3. **US federal government works** are public domain (17 U.S.C. §105): White House, NASA, Congress, military photographers. Caveats: PD covers copyright only. These sources usually add "may not be used to imply endorsement", and faces still carry personality rights. Photos made by contractors or wire photographers on .gov sites are **not** PD.
4. **Brazilian government.** Agência Brasil content was historically CC BY 3.0 BR with credit "Nome do fotógrafo/Agência Brasil". Commons notes that this blanket licence **does not cover content after 2017-02-23**, so check each item.
5. **Official press kits / newsrooms** (OpenAI, Anthropic, NVIDIA, Google). These are usually licensed for editorial/press use, without a clear grant for a commercial book. Email the press office and ask for written permission naming the book, both editions, print + e-book, and worldwide distribution. Store the email (PDF) next to the image.
6. **Getty Images / AP / Reuters / dpa.** Rights-managed. A book needs a paid editorial licence priced by print run, territory and placement (interior vs cover). Never use a Getty "embed", a screenshot or a search-engine copy. Use these only when nothing free exists for an essential event photo.

### 5.2 CC BY / BY-SA in a commercial book

- All CC licences allow commercial use and inclusion in **collections** ("anthologies, encyclopedias"). The licence of the photo doesn't change the book's licence (CC FAQ). **Placing a BY-SA photo in the book does not make the book BY-SA.**
- ShareAlike kicks in only if you **adapt** the photo: a composite, a drawn-over illustration, a substantial creative edit. Then the adapted image (not the book) must be released under BY-SA (or a compatible licence), with that stated in the credit. Keep BY-SA photos unadapted.
- Format changes are not adaptations under CC 4.0 (CC FAQ: changes made to use the work "in any format or medium… are not considered adaptations"). Grayscale conversion and resizing are safe. Cropping is ambiguous, so treat it as a modification and **say so in the credit**: CC BY/BY-SA 4.0 §3(a)(1)(B) requires indicating modifications. Do it for 2.0/3.0 files too for consistency.
- Attribution must include: creator (the *author*, not the uploader), title if supplied, source link, licence name **and licence link**, and the modification notice. It can be given "in any reasonable manner" for the medium. In print, that means a short credit near the image plus a full entry in a back-matter "Créditos das imagens / Image credits" page with full URLs.
- Credit string formats (TASL + modification):
  - EN caption: `Photo: Krd / Wikimedia Commons, CC BY-SA 4.0 (cropped, grayscale)`
  - PT legenda: `Foto: Krd / Wikimedia Commons, CC BY-SA 4.0 (recortada, em tons de cinza)`
  - Back matter: `"LinuxCon Europe Linus Torvalds 03" by Krd, https://commons.wikimedia.org/wiki/File:LinuxCon_Europe_Linus_Torvalds_03.jpg, licensed under CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/. Cropped and converted to grayscale.`
  - Public domain: `Foto: Casa Branca (Pete Souza) / domínio público`. No ©.

### 5.3 Pitfalls

- **Personality / image rights.** Copyright licences don't license the face. Brazil: Código Civil art. 20 bars commercial use of a person's image without authorisation, and STJ Súmula 403 grants damages for unauthorised commercial use without proof of harm. Editorial use in a nonfiction book about public figures, accompanying text about them, is the normal and defensible case (STF ADI 4815 allowed unauthorised biographies). Riskier uses: the **cover**, marketing material, ads, or any layout implying endorsement. US: state right-of-publicity laws target advertising and trade use. Commons marks some files with `{{Personality rights}}`, which the API exposes as `Restrictions: personality`. Treat that tag as "interior/editorial only; cover needs consent".
- **Freedom of panorama.** US §120(a) covers buildings only (including public interiors), **not** sculptures or murals. Brazil Lei 9.610 art. 48 is broad: "obras situadas permanentemente em logradouros públicos podem ser representadas livremente". For a book sold in both markets, use the stricter (US) rule for artworks in shot. Conference stage screens showing slides or video are someone else's copyrighted content. Incidental is fine; avoid shots where the screen is the subject.
- **Logos and trademarks.** Incidental logos in event photos are fine editorially. Don't put company logos on the cover, and don't crop so a logo becomes the focus (implied endorsement). Commons flags `Restrictions: trademarked`.
- **Licence laundering.** Some Commons and Flickr uploads are someone else's press photo re-uploaded under CC. Red flags: uploader isn't the author, no EXIF, small size, professional studio portrait, "own work" for a celebrity headshot. Reverse-image-search before relying on one (the Karpathy "CC0" file fits this pattern).
- **Wire photos on Commons.** Some PD-tagged files are actually AP/Getty. The same check applies.
- **Resolution.** Many Commons portraits are web-sized. Compute px ÷ 300 for printed inches before choosing, and never upscale with AI to fake detail. KDP warns that artificially raised DPI still prints soft.
- **No AI likenesses.** No generated "photos" of real people, no AI-cleaned faces, no extended backgrounds. Grayscale conversion, crop, levels and dust removal are fine. Record every edit.

### 5.4 Wikimedia Commons API: fetch an image plus licence metadata (tested 2026-10-13)

Set a descriptive User-Agent (Wikimedia's User-Agent policy requires one). Search, then get `imageinfo` with `extmetadata`:

```bash
UA="ai-book-2026/1.0 (https://www.akitaonrails.com/)"

# 1) find candidate files (namespace 6 = File:)
curl -sG -A "$UA" https://commons.wikimedia.org/w/api.php \
  --data-urlencode action=query --data-urlencode list=search \
  --data-urlencode "srsearch=Linus Torvalds" --data-urlencode srnamespace=6 \
  --data-urlencode srlimit=8 --data-urlencode format=json | jq -r '.query.search[].title'

# 2) licence/author/attribution + original URL + a 1200px thumb
curl -sG -A "$UA" https://commons.wikimedia.org/w/api.php \
  --data-urlencode action=query \
  --data-urlencode "titles=File:LinuxCon Europe Linus Torvalds 03.jpg" \
  --data-urlencode prop=imageinfo \
  --data-urlencode "iiprop=url|size|mime|sha1|extmetadata|user|timestamp" \
  --data-urlencode "iiextmetadatafilter=Artist|Credit|LicenseShortName|LicenseUrl|License|UsageTerms|AttributionRequired|Copyrighted|Restrictions|DateTimeOriginal|ImageDescription|ObjectName" \
  --data-urlencode iiurlwidth=1200 --data-urlencode format=json --data-urlencode formatversion=2
```

Trimmed real response:

```json
{
  "query": { "pages": [ {
    "pageid": 36166670,
    "title": "File:LinuxCon Europe Linus Torvalds 03.jpg",
    "imageinfo": [ {
      "timestamp": "2014-10-15T18:18:15Z", "user": "Krd",
      "size": 7421864, "width": 3282, "height": 4922, "mime": "image/jpeg",
      "url": "https://upload.wikimedia.org/wikipedia/commons/5/52/LinuxCon_Europe_Linus_Torvalds_03.jpg?utm_source=…",
      "descriptionurl": "https://commons.wikimedia.org/wiki/File:LinuxCon_Europe_Linus_Torvalds_03.jpg",
      "sha1": "e05465d46343454353b3fed43b17e5b8185762c2",
      "extmetadata": {
        "ImageDescription": { "value": "<a href=\"https://www.wikidata.org/wiki/Q34253\" …>Linus Torvalds</a> speaking at the LinuxCon Europe 2014 in Düsseldorf" },
        "DateTimeOriginal": { "value": "2014-10-15" },
        "Credit":           { "value": "<span class=\"int-own-work\" lang=\"en\">Own work</span>" },
        "Artist":           { "value": "<a href=\"//commons.wikimedia.org/wiki/User:Krd\" …>Krd</a>" },
        "LicenseShortName": { "value": "CC BY-SA 4.0" },
        "UsageTerms":       { "value": "Creative Commons Attribution-Share Alike 4.0" },
        "AttributionRequired": { "value": "true" },
        "LicenseUrl":       { "value": "https://creativecommons.org/licenses/by-sa/4.0" },
        "Copyrighted":      { "value": "True" },
        "Restrictions":     { "value": "" },
        "License":          { "value": "cc-by-sa-4.0" }
      } } ] } ] }
}
```

Notes:
- `Artist` and `Credit` are HTML. Strip the tags for the credit string, but keep the raw value in the record.
- `user` is the last uploader, **not** necessarily the author. Credit `Artist`.
- `Restrictions` is a pipe-separated list (`personality`, `trademarked`, …). It was non-empty for the Hassabis Nobel photos.
- Download `url` (the original) for print and record `sha1` to verify the file later. The `utm_*` query string can be dropped.
- To batch a person's photos, use `generator=search&gsrsearch=…&gsrnamespace=6&prop=imageinfo`. To get the "canonical" portrait, read the person's Wikidata P18 (`https://www.wikidata.org/wiki/Special:EntityData/Q34253.json` → `claims.P18`).
- A `scripts/commons_fetch.rb` that takes a File: title and writes `assets/photos/<id>.{jpg,yml}` with the record below is a natural next step.

---

## 6. Credits / provenance record (YAML)

One file per image, next to the asset (`assets/illustrations/<id>.yml`, `assets/photos/<id>.yml`). The build generates the back-matter credits page and the KDP disclosure checklist from these files.

```yaml
# ---------- AI-generated illustration ----------
id: fig-03-autocomplete
kind: ai_illustration            # ai_illustration | diagram_code | photo | composite
chapters: [3]
editions: [pt, en]
file: assets/illustrations/fig-03-autocomplete.png
sha256: 717bbf80f619b5be893e885c5cbceda7f131c297e155ba9fbf30d271d4809d55
pixels: {width: 2048, height: 1536}
print_size_in: {width: 4.75, height: 3.56}   # → 431 DPI
generation:
  provider: openai               # openai | google | openrouter:<vendor> | hf:<repo>
  endpoint: POST /v1/images/generations
  model: gpt-image-2.5-flare-2026-09-08      # always the pinned snapshot
  date: 2026-10-13T15:40:00-03:00
  style_version: STYLE v1
  prompt: |
    STYLE v1: … A stack of rounded blocks flowing into a network, ending in a speech bubble.
  negative_or_constraints: "no text, no letters, no logos, no real people"
  params: {size: 2048x1536, quality: high, background: opaque, output_format: png, n: 1}
  seed: null                     # not exposed by OpenAI/Gemini; record if the model supports one
  reference_images: [fig-01-cover-motif]
  request_id: gen_…              # OpenAI data[0].generation_id | Gemini responseId
  usage: {input_tokens: 84, output_tokens: 196}
  cost_usd: 0.006
  c2pa_in_original: true
  synthid: false                 # true for Gemini outputs
  selected_from: 4               # drafts generated
post_processing:
  - "labels overlaid as live text (SVG template, labels/fig-03.{pt,en}.yml)"
  - "flattened onto #FBF9F4, sRGB"
human_contribution: "art direction, selection, composition, all labels"
terms:
  provider_terms: https://openai.com/policies/services-agreement/
  output_ownership: "customer owns Output (OpenAI Services Agreement §4.1)"
  copyright_status: "AI-generated portions likely not protectable (US CO Part 2; LDA art. 11)"
kdp_disclosure: ai_generated_image   # ai_generated_image | ai_assisted | none
credit:
  pt: "Ilustração gerada com GPT Image 2.5 (OpenAI) sob direção do autor"
  en: "Illustration generated with GPT Image 2.5 (OpenAI) under the author's direction"

# ---------- Diagram as code ----------
id: fig-05-agent-loop
kind: diagram_code
source: figures/fig-05-agent-loop.d2
labels: figures/fig-05-agent-loop.labels.yml
tool: {name: d2, version: 0.9.0, layout: elk, theme: house-v1}
authored_by: author             # author | author+llm (→ kdp_disclosure: ai_assisted or ai_generated)
kdp_disclosure: none
credit: null

# ---------- Real photo ----------
id: photo-torvalds-linuxcon-2014
kind: photo
subject: [Linus Torvalds]
wikidata: Q34253
event: "LinuxCon Europe 2014, Düsseldorf"
file: assets/photos/photo-torvalds-linuxcon-2014.jpg
source:
  repository: wikimedia_commons  # wikimedia_commons | flickr | gov_pd | press_kit | getty | ap | own
  page_url: https://commons.wikimedia.org/wiki/File:LinuxCon_Europe_Linus_Torvalds_03.jpg
  original_url: https://upload.wikimedia.org/wikipedia/commons/5/52/LinuxCon_Europe_Linus_Torvalds_03.jpg
  original_sha1: e05465d46343454353b3fed43b17e5b8185762c2
  retrieved: 2026-10-13
  title: "LinuxCon Europe Linus Torvalds 03"
  date_taken: 2014-10-15
author: Krd
author_url: https://commons.wikimedia.org/wiki/User:Krd
license:
  short: CC BY-SA 4.0
  url: https://creativecommons.org/licenses/by-sa/4.0/
  attribution_required: true
  share_alike: true
  restrictions: []               # from extmetadata.Restrictions, e.g. [personality, trademarked]
permission_doc: null             # path to press-office email / invoice for licensed photos
modifications: [cropped, grayscale]
adaptation: false                # true → the modified image must itself be released under BY-SA
placement: interior              # interior | cover | marketing
personality_rights_check: "public figure, editorial context, interior only"
credit:
  caption_pt: "Foto: Krd / Wikimedia Commons, CC BY-SA 4.0 (recortada, em tons de cinza)"
  caption_en: "Photo: Krd / Wikimedia Commons, CC BY-SA 4.0 (cropped, grayscale)"
  backmatter: >-
    "LinuxCon Europe Linus Torvalds 03" by Krd,
    https://commons.wikimedia.org/wiki/File:LinuxCon_Europe_Linus_Torvalds_03.jpg,
    CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0/. Cropped and converted to grayscale.
```

---

## Sources

Generated images
- OpenAI pricing (token prices; gpt-image-2.5 Flare/Sunburst, 2, 1.5, 1-mini, 1): https://developers.openai.com/api/docs/pricing
- OpenAI image generation guide (models, parameters, sizes, per-image cost tables, text-rendering caveat, `b64_json`): https://developers.openai.com/api/docs/guides/image-generation
- GPT Image 2.5 launch coverage, 2026-09-08 (secondary; also confirmed by the live `/v1/models` listing with `-2026-09-08` snapshots): https://grida.co/docs/models/gpt-image-2.5 , https://pasqualepillitteri.it/en/news/15233/chatgpt-images-2-5-openai-launch
- OpenAI Services Agreement §4 (Output ownership): https://openai.com/policies/services-agreement/
- Gemini API pricing (Nano Banana 2.1 / 2 / Pro / Flash Lite; 2.5 Flash Image shutdown 2026-10-02): https://ai.google.dev/gemini-api/docs/pricing
- Gemini image generation docs (sizes, models, SynthID, text rendering): https://ai.google.dev/gemini-api/docs/image-generation
- Gemini deprecations (Imagen 4 shutdown 2026-08-17, replacement gemini-3.1-flash-image): https://ai.google.dev/gemini-api/docs/deprecations
- Gemini API Additional Terms (ownership of generated content): https://ai.google.dev/gemini-api/terms
- OpenRouter Terms §5–6 (Model Terms govern output ownership; updated 2026-08-31): https://openrouter.ai/terms
- OpenRouter image API: https://openrouter.ai/docs/guides/overview/multimodal/image-generation
- US Copyright Office, Copyright and AI Part 2 (2025-01-29): https://www.copyright.gov/ai/ , https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf
- Thaler v. Perlmutter cert denied 2026-03-02: https://www.bakerdonelson.com/supreme-court-denies-certiorari-in-thaler-v-perlmutter-ai-cannot-be-an-author-under-the-copyright-act , https://www.jonesday.com/de/insights/2026/03/jones-day-talks-women-in-ip--supreme-court-denies-review-of-thaler-v-perlmutter-ai-authorship-questions-remain
- Lei 9.610/98 (arts. 11, 48, 79): https://www.planalto.gov.br/ccivil_03/leis/l9610.htm
- PL 2338/2023 status (pending in Câmara): https://iabnacional.org.br/wp-content/uploads/2026/07/Indicacao-no-76_2026-PL-2330-2023.pdf , https://teletime.com.br/03/06/2026/panorama-regulatorio-inteligencia-artificial/
- KDP Content Guidelines, AI section: https://kdp.amazon.com/en_US/help/topic/G200672390

Print / e-book specs
- KDP paperback submission guidelines (≥300 DPI, ≤600 DPI recommended): https://kdp.amazon.com/en_US/help/topic/G201857950
- KDP format images (DPI math, artificially raised DPI): https://kdp.amazon.com/en_US/help/topic/G202169030
- Kindle reflowable image guidelines (sRGB, no transparency, 80% width for text images, grayscale e-reader preview): https://kdp.amazon.com/en_US/help/topic/G75V4YX5X8GRGXWV

Diagram tools (latest releases via GitHub API, 2026-10-13)
- D2: https://github.com/terrastruct/d2 · Typst: https://github.com/typst/typst · CeTZ: https://github.com/cetz-package/cetz · fletcher: https://typst.app/universe/package/fletcher · Mermaid CLI: https://github.com/mermaid-js/mermaid-cli · Excalidraw: https://github.com/excalidraw/excalidraw · Graphviz: https://graphviz.org/

Photos
- Commons: Reusing content outside Wikimedia: https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia
- Commons: Credit line: https://commons.wikimedia.org/wiki/Commons:Credit_line
- Commons: Personality rights / identifiable people: https://commons.wikimedia.org/wiki/Commons:Personality_rights , https://commons.wikimedia.org/wiki/Commons:Photographs_of_identifiable_people , https://commons.wikimedia.org/wiki/Template:Personality_rights
- Commons: Freedom of panorama: https://commons.wikimedia.org/wiki/Commons:Freedom_of_panorama
- MediaWiki API imageinfo / extmetadata: https://www.mediawiki.org/wiki/API:Imageinfo
- Wikimedia User-Agent policy: https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy
- CC FAQ (collections vs adaptations; format shifting): https://creativecommons.org/faq/
- CC BY-SA 4.0 legal code (§3 attribution, modification notice, ShareAlike scope): https://creativecommons.org/licenses/by-sa/4.0/legalcode
- 17 U.S.C. §105 (US government works): https://www.law.cornell.edu/uscode/text/17/105
- 17 U.S.C. §120 (architectural works): https://www.law.cornell.edu/uscode/text/17/120
- Código Civil art. 20: https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm
- STJ Súmula 403 and STF ADI 4815 (unauthorised biographies): https://www.stj.jus.br/docs_internet/revista/eletronica/stj-revista-sumulas-2014_38_capSumula403.pdf  ; ADI 4815 (2015, 9–0, Civil Code arts. 20–21 read to not require prior consent; damages remain available): https://www.dizerodireito.com.br/2015/06/para-que-seja-publicada-uma-biografia.html
- Agência Brasil licence history (Commons): https://commons.wikimedia.org/wiki/Template:Agência_Brasil
