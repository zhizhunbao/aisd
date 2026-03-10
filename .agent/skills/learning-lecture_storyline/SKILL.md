---
name: learning-lecture_storyline
description: Reorganize lecture slides into a coherent storyline narrative for deeper understanding. Use when (1) user asks to create a "鏁呬簨绾? or "storyline" from slides, (2) user wants to understand the logical progression of a lecture, (3) user mentions reorganizing or restructuring lecture content for better comprehension.
---

# Learning Lecture Storyline

## Objectives

Transform fragmented lecture slides into a **coherent narrative story** that reveals the logical progression of ideas, making technical concepts easier to understand by showing _why_ each new concept was needed (problem 鈫?motivation 鈫?solution 鈫?new problem 鈫?...).

## Core Philosophy

> **Slides tell you WHAT to learn. A storyline tells you WHY each idea exists.**

Traditional slides present topics in blocks (A, B, C, D). A storyline connects them causally:

- A has a problem 鈫?which motivates B
- B improves on A but still has a flaw 鈫?which motivates C
- C solves B's flaw but introduces a new challenge 鈫?which motivates D

This "鎵撴€崌绾? (boss-fight progression) structure maps naturally to how technology evolves.

> 鈿狅笍 **Cross-cutting Rule:** Follow the **Source Citation & Proof Rule** (`learning-source_citation` SKILL.md). Key technical claims must cite textbook sources; formulas embedded in the storyline must reference their derivation (e.g., "璇﹁ tutorial 搂N").
> 鈿狅笍 **閫氱敤瑙勫垯锛?* 閬靛畧**鏉ユ簮寮曡瘉涓庤瘉鏄庤鍒?*锛坄learning-source_citation` SKILL.md锛夈€傚叧閿妧鏈杩伴』娉ㄦ槑鏁欑涔︽潵婧愶紝宓屽叆鐨勫叕寮忛』鎸囧悜鎺ㄥ鍑哄锛堝"璇﹁ tutorial 搂N"锛夈€?

## Instructions

### Phase 1: Extract & Analyze Source Material

1. **Read the PDF/slides** using `dev-pdf_processing` or PyMuPDF (`fitz`).
2. **Check for existing notes**: Look for `*_slides.md` or `*_notes.md` in the same `notes/` directory 鈥?these contain valuable Chinese annotations.
3. **Identify the overarching question**: What central problem is the entire lecture trying to solve? (e.g., "How to predict the next word?")
4. **Map the technology evolution chain**: List each approach in order and identify:
   - What problem it solves
   - What new problem it introduces (its limitation)
   - How it transitions to the next approach

### Phase 2: Design the Storyline Structure

Use this **standard narrative template**:

```markdown
# Lecture N 鏁呬簨绾匡細[涓€鍙ヨ瘽涓婚]

> **Source:** `[filename].pdf`
> **鏍稿績涓婚锛?* [鐢ㄤ竴鍙ラ€氫織鐨勮瘽姒傛嫭鏁磋鍦ㄨВ鍐充粈涔堥棶棰榏
> **鏁呬簨绾匡細** [鐢ㄤ竴涓瘮鍠绘鎷繘鍖栬繃绋媇

---

## 馃幀 搴忓箷锛氭垜浠瑙ｅ喅浠€涔堥棶棰橈紵

[瀹氫箟鏍稿績闂锛岀粰鍑虹洿瑙備緥瀛愶紝璇存槑涓轰粈涔堥噸瑕乚

## 馃摎 绗竴绔狅細[鏁板/鐞嗚鍩虹]

[涓哄悗缁柟妗堥摵鍨繀瑕佺殑鐭ヨ瘑]

## 馃М 绗簩绔狅細鏂规涓€鈥斺€擺鍚嶇О]锛堚潓 澶辫触/閮ㄥ垎鎴愬姛锛?

[浠嬬粛鏂规 鈫?灞曠ず鏁堟灉 鈫?鏆撮湶鑷村懡闂 鈫?馃攽 鏁呬簨杞姌鐐筣

## 馃 绗笁绔狅細鏂规浜屸€斺€擺鍚嶇О]锛堚殸锔?鏈夌己闄凤級

[鐢变笂涓€绔犵殑闂寮曞嚭 鈫?浠嬬粛鏂规 鈫?鏆撮湶鏂伴棶棰?鈫?馃攽 鏁呬簨杞姌鐐筣

## 馃彴 绗洓绔狅細鏂规涓夆€斺€擺鍚嶇О]锛堚渽 瑙ｅ喅锛侊級

[鐢变笂涓€绔犵殑闂寮曞嚭 鈫?浠嬬粛鏂规 鈫?瑙ｉ噴涓轰粈涔堣兘瑙ｅ喅鍓嶉潰鐨勯棶棰榏

## 馃搹 [璇勪及/搴旂敤绔犺妭]锛堝閫傜敤锛?

## 馃椇锔?鍏ㄥ眬鍥為【锛氭妧鏈紨杩涜矾绾垮浘

[ASCII 璺嚎鍥?+ 瀵规瘮琛ㄦ牸]

## 馃帗 鑰冭瘯/澶嶄範閲嶇偣妫€鏌ユ竻鍗?

[Checklist 褰㈠紡]
```

### Phase 3: Write Each Chapter

For each chapter, follow these writing guidelines:

#### 3.1 Chapter Opening 鈥?Motivation First

姣忕珷寮€澶?*蹇呴』**鍥炵瓟锛?涓轰粈涔堟垜浠渶瑕佽繖涓紵" 浠庝笂涓€绔犵殑鉂岄棶棰樿嚜鐒跺紩鍑恒€?

```markdown
> 馃攽 **鏁呬簨杞姌鐐癸細** [涓婁竴涓柟妗圿鐨刐鍏蜂綋闂]浣垮緱鎴戜滑涓嶅緱涓嶅鎵炬柊鏂规硶 鈫?[鏂版柟妗圿鐧诲満锛?
```

#### 3.2 Concept Explanation 鈥?鍥涘眰閫掕繘娉?

瀵规瘡涓牳蹇冩蹇碉紝鎸変互涓嬪洓灞傞€掕繘瑙ｉ噴锛?

| 灞傛                | 鍐呭                 | 绀轰緥                            |
| ------------------- | -------------------- | ------------------------------- |
| **鈶?涓€鍙ヨ瘽瀹氫箟**    | 鐢ㄦ渶閫氫織鐨勮瑷€       | "RNN = 涓€涓缁忓厓 + 涓€鏍瑰洖蹇嗙嚎" |
| **鈶?鍏紡/鍘熺悊**     | 绮剧‘鐨勬暟瀛︽弿杩?      | `h鈧?= W鈧撀穢鈧?+ W鈧暵穐鈧溾倠鈧?+ b`      |
| **鈶?鍏蜂綋渚嬪瓙**      | 鐢ㄨ绋嬩腑鐨勪緥瀛愯蛋涓€閬?| "the students opened their..."  |
| **鈶?绫绘瘮/璁板繂鎶€宸?* | 鐢熸椿鍖栨瘮鍠?          | "h鈧?灏卞儚涓嶆柇鏇存柊鐨勭瑪璁?         |

#### 3.3 Transitions 鈥?Problem 鈫?Solution Arc

姣忕珷缁撳熬**蹇呴』**鍖呭惈涓€涓け璐?闂灞曠ず锛岀敤鏉ユ棤缂濊繃娓″埌涓嬩竴绔狅細

```markdown
### X.N 鉂?[鏂规鍚峕鐨勮嚧鍛介棶棰樷€斺€擺闂鍚峕

[鐢ㄥ叿浣撲緥瀛愬睍绀哄け璐ュ満鏅痌

> 馃攽 **鏁呬簨杞姌鐐癸細** [闂鎬荤粨] 鈫?鎴戜滑闇€瑕?[涓嬩竴涓柟妗堢殑鏍稿績鑳藉姏]锛?
```

#### 3.4 Comparisons 鈥?Use Tables

鍦ㄦ柊鏂规寮曞叆鍚庯紝鐢ㄥ姣旇〃鏍兼竻鏅板睍绀鸿繘姝ワ細

```markdown
| 缁村害   | 鏃ф柟妗?| 鏂版柟妗? |
| ------ | :----: | :-----: |
| 鑳藉姏1  |   鉂?  |   鉁?   |
| 鑳藉姏2  |   鉂?  |   鉁?   |
| 鏂伴棶棰?|  N/A   | 鈿狅笍 鎻忚堪 |
```

### Phase 4: Write the Global Review

#### 4.1 ASCII Evolution Roadmap

蹇呴』鍖呭惈涓€涓?ASCII 鑹烘湳璺嚎鍥撅紝灞曠ず瀹屾暣鎶€鏈紨杩涢摼锛?

```markdown
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?鎶€鏈紨杩涜矾绾垮浘 鈹?
鈹?鈹?
鈹?鏂规1 鈹?
鈹?鉁?浼樼偣 鈹?
鈹?鉂?鑷村懡闂 鈹?
鈹?鈹?鈹?
鈹?鈻?鈹?
鈹?鏂规2 鈹?
鈹?鉁?瑙ｅ喅浜嗘柟妗?鐨勯棶棰?鈹?
鈹?鉂?鏂扮殑鑷村懡闂 鈹?
鈹?鈹?鈹?
鈹?鈻?鈹?
鈹?鏂规3 鈹?
鈹?鉁?瑙ｅ喅浜嗘柟妗?鐨勯棶棰?鈹?
鈹?鈹?鈹?
鈹?鈻?鈹?
鈹?涓嬩竴绔欙細... 鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
```

#### 4.2 Transition Summary Table

```markdown
| 浠?鈫?鍒?| 瑙ｅ喅浜嗕粈涔堟牳蹇冮棶棰橈紵 |
| ------- | -------------------- |
| A 鈫?B   | [涓€鍙ヨ瘽]             |
| B 鈫?C   | [涓€鍙ヨ瘽]             |
```

#### 4.3 Review Checklist

鐢?`- [ ]` 鏍煎紡鍒楀嚭鎵€鏈夐渶瑕佹帉鎻＄殑鑰冪偣锛屽搴斿悇绔犳牳蹇冨唴瀹广€?

### Phase 5: Quality Checks

鍦ㄥ畬鎴愭晠浜嬬嚎鍚庯紝鎵ц浠ヤ笅妫€鏌ワ細

- [ ] **鍥犳灉瀹屾暣鎬?*: 姣忎釜鏂版柟妗堢殑寮曞叆閮芥湁鏄庣‘鐨?鍥犱负鍓嶉潰鐨勬柟妗堟湁X闂"鐨勫姩鏈?
- [ ] **闆惰烦璺冨師鍒?*: 娌℃湁绐佺劧鍐掑嚭鏉ョ殑姒傚康鈥斺€旀瘡涓湳璇湪浣跨敤鍓嶉兘宸茶В閲?
- [ ] **渚嬪瓙涓€鑷存€?*: 灏介噺鍏ㄧ瘒浣跨敤鍚屼竴涓疮绌夸緥瀛愶紙濡?"the students opened their..."锛?
- [ ] **鍏紡瑕嗙洊**: 鎵€鏈夊叧閿叕寮忛兘鏈?涓€鍙ヨ瘽鐩磋 + 鏁板琛ㄨ揪 + 渚嬪瓙"涓夊眰瑙ｉ噴
- [ ] **杞姌鏍囪**: 姣忎釜绔犺妭杩囨浮澶勯兘鏈?`馃攽 鏁呬簨杞姌鐐筦 鏍囪
- [ ] **璺嚎鍥?*: 鏂囨湯鍖呭惈瀹屾暣鐨?ASCII 鎶€鏈紨杩涜矾绾垮浘
- [ ] **澶嶄範娓呭崟**: 鏂囨湯鍖呭惈 checklist 鏍煎紡鐨勮€冭瘯瑕佺偣

## Formatting Rules

### Language

- **涓讳綋璇█**: 涓枃
- **鏈澶勭悊**: 棣栨鍑虹幇鏃剁敤 "涓枃 (English)" 鏍煎紡锛屼箣鍚庡彲鍙敤涓嫳鏂囦换涓€
- **鍏紡**: 鐢?code block 鎴?inline code 灞曠ず锛岀‘淇濆彲璇绘€?
- **Emoji**: 绔犺妭鏍囬浣跨敤 emoji 澧炲姞瑙嗚鍖哄垎锛堭煄煋氿煣煣狆煆梆煋忦煑猴笍馃帗锛?

### Structure

- 鐢?`---` 鍒嗛殧绗﹂殧寮€涓昏绔犺妭
- 姣忕珷鍐呯敤 `###` 绾у埆鏍囬鍒掑垎灏忚妭
- 瀵规瘮鐢ㄨ〃鏍硷紝娴佺▼鐢ㄤ唬鐮佸潡缂╄繘锛岄噸鐐圭敤鍔犵矖
- 绫绘瘮鍜岃蹇嗘妧宸х敤 `> 馃挕` blockquote 楂樹寒

### Naming Convention

- 杈撳嚭鏂囦欢鍚? `[topic_key]_storyline.md`
- 瀛樻斁浣嶇疆: `courses/[course]/notes/`

## Output File Structure

```text
courses/[course]/
鈹溾攢鈹€ slides/
鈹?  鈹斺攢鈹€ [topic].pdf                      # Source slides
鈹斺攢鈹€ notes/
    鈹溾攢鈹€ [topic_key]_slides.md                # Raw extraction (if exists)
    鈹溾攢鈹€ [topic_key]_notes.md                 # Detailed notes (if exists)
    鈹斺攢鈹€ [topic_key]_storyline.md             # 猸?This skill's output
```

## Example Reference

See `courses/nlp/notes/lecture5_storyline.md` for a complete example that transforms a 63-page NLP lecture (covering N-gram 鈫?FFNN 鈫?RNN 鈫?LSTM) into a coherent storyline narrative.

