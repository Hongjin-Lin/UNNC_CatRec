# Product Brief — CatRec (喵友圈圈)

---

## A · Problem Statement

Students and staff at UNNC who feed and care for stray cats face a persistent identification problem: the campus cat community is large (50+ individuals at UNNC alone), cats look similar to untrained eyes, and there is no shared, accessible record of which cat is which. When a cat is injured, ill, or missing, caretakers cannot quickly identify it by name or locate its health records (TNR status, personality, usual location). New community members who want to help have no way to learn which cats have already been neutered, making duplicate TNR procedures a real risk. Without a reliable identification system, care coordination is fragmented, word-of-mouth dependent, and inaccessible to anyone new to the campus.

---

## B · Solution

CatRec is a mobile app (UniApp, targeting WeChat Mini Program and H5) with three core capabilities:

**1. AI-powered cat identification**
The user photographs a cat on campus. The app uploads the image to a backend running a fine-tuned DINOv2 vision model (AvitoTech animal identification weights). The model computes a 384-dimensional embedding, compares it against a pre-built vector database of all registered campus cats, and returns the top-3 most likely matches with confidence scores. The user taps a result to open that cat's full profile.

**2. Cat registry with rich profiles**
Each cat has a profile showing name, usual location, personality traits, TNR status, and a photo album sourced from a shared campus photo library. Users can browse the full registry, search by name, and view an interactive campus map showing where each cat is typically found.

**3. Cat registration**
Authorised administrators can add new cats via the app: upload a photo, fill in basic info, and submit. The backend embeds the new photo and adds it to the identification vector database.

The three features directly address the problem: identification replaces guesswork, profiles replace fragmented word-of-mouth records, and the registry ensures TNR status is visible to anyone.

---

## C · Target Users

**Primary user:** University students and campus staff (non-expert, casual animal lovers) at Chinese university campuses with a semi-managed stray cat population, who interact with campus cats at least a few times per week and want to know the cats by name or check their health status.

**Usage scenario:**

A first-year student notices an orange cat near the library that she has never seen before. She opens CatRec, taps the camera icon on the Identify tab, and photographs the cat. Within 3 seconds the app returns: "蛋黄 — 92% confidence. Location: Library entrance. TNR: ✅ Done. Personality: Friendly, food-motivated." She now knows the cat's name, knows it has been neutered, and can find it again using the campus map. She did not need to ask anyone or join any WeChat group.

---

## D · Core Value Proposition

**One-sentence value proposition:**

For university students who encounter campus stray cats daily, CatRec identifies any cat by photo in seconds and surfaces its full care record, so that anyone — including newcomers — can participate in campus cat welfare without relying on institutional memory or WeChat group knowledge.

**Brief explanation:**

Existing approaches rely entirely on social knowledge: long-time students remember cats by face, information lives in WeChat group chats, and TNR records are maintained in spreadsheets that most people never see. CatRec makes this knowledge persistent, searchable, and accessible through a single photo. The AI identification layer is what lowers the barrier from "you need to already know the cats" to "anyone with a phone can contribute."

---

## E · AI & Technical Approach

**AI / model type(s) used:**
- Vision encoder: DINOv2-small (Facebook), fine-tuned on animal identification by AvitoTech (`AvitoTech/DINO-v2-small-for-animal-identification`)
- Similarity search: cosine similarity over pre-computed L2-normalised embedding vectors (numpy dot product, no vector DB dependency)

**Role of AI in the product:**

The model converts a user-submitted photo into a 384-dimensional feature vector capturing the cat's visual identity (coat pattern, facial structure, body shape). This vector is compared against a library of per-cat embeddings, each built by averaging embeddings across multiple reference photos of that individual cat. The top-3 closest matches by cosine similarity are returned, filtered by a confidence threshold of 0.70 to suppress false positives.

**Why AI is the right approach here:**

Rule-based approaches (colour tagging, manual photo lookup) do not scale beyond ~10 cats and fail entirely for users who are new to the campus. Individual cat identification from unconstrained photos is a fine-grained visual recognition task — the same class ("orange tabby") must be split into 10+ distinct individuals based on subtle texture and marking differences. This requires a deep vision model trained on animal features, not generic image search or metadata matching.

---

## F · Key Assumptions

**Assumption 1:**
We assume that 2–6 clear reference photos per cat are sufficient to build a robust identification embedding, because DINOv2's averaged embedding generalises well across lighting and angle variation. This has been partially validated: identification works reliably for cats with 3+ distinct reference images, but accuracy degrades for cats with only 1 reference photo (e.g., 二胖, 小茉莉).

**Assumption 2:**
We assume that campus cat caretakers will maintain the photo library and register new cats via the admin interface, keeping the vector database current. This has not been validated — the app currently depends on a manual `build_embeddings.py` script being re-run after each new cat is added, which creates an operational dependency on a technical administrator.

**Assumption 3:**
We assume that a 0.70 cosine similarity threshold correctly separates true matches from look-alike cats (e.g., multiple orange tabbies on the same campus). This threshold was set empirically and has not been tested against a held-out dataset of deliberately similar-looking cats.

---

## G · Differentiation

**Current alternatives or common approaches:**

Most campus cat communities in China manage cat identity entirely through WeChat groups: photos are shared, long-time members identify cats verbally, and TNR records are kept in pinned spreadsheet links. Some campuses use physical ear tags or collar numbers, which require physical proximity to read and are often removed or lost.

**What makes our approach different:**

CatRec is the only approach in this context that makes identification available to users with zero prior knowledge of the cat population. The key trade-off is coverage vs. setup cost: the app requires an initial investment in building the photo library and embedding database, but once built, any new community member can identify any registered cat instantly without asking anyone. It also centralises TNR status, location, and personality data in one place that is accessible from a phone rather than buried in a chat history.
