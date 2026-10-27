# READY-TO-PASTE FORM ANSWERS — team blackbox (Indie track)

Champion idea: **Ustad** — film a job once, it becomes a self-teaching SOP with checkpoints,
a trainee quiz and expert approval (street-food stall chains first, every trade next).
Full spec: `CHAMPION_V2.md`. Replace the two [FILL] items before submitting; everything
else is paste-ready. Honesty rule: only claim infra you actually build (the 8-day plan builds all of it).

---

## FORM 1 — Modal Credits (Google Form)

| Field | Paste this |
|---|---|
| Full name | `nabidnur abrar` |
| Email you applied with on Cerebral Valley | `nurnabid754@gmail.com` |
| Team name | `team blackbox` |
| Teammate emails | `nurnabid754@gmail.com` |
| Track | **Indie** |
| Project one-liner (What are you building and how will you use Modal?) | `Ustad turns a one-time phone filming of any work task into a step-by-step illustrated SOP with checkpoints, a trainee quiz and an expert-approval loop — built for hands-on businesses like street-food stall chains. We will use Modal sandboxes as isolated, reproducible workers for our video pipeline (frame extraction, batching and pre/post-processing around the Meta Model API calls), and Modal endpoints to serve self-hosted open-weight Muse Glimmer so the trainee mode keeps working offline and at the edge. Estimated compute: $50-100 across the hacking window.` |
| GitHub profile or repo link | `https://github.com/Hisernberg` (profile) — repo: `https://github.com/Hisernberg/meta-ai-hackathon-2026` |
| Modal workspace name | [FILL] — create a free account at modal.com first; recommended workspace name: `team-blackbox` |
| Email on your Modal account | `nurnabid754@gmail.com` (use the same email so the team matches) |
| What will you use Modal for? | Check: **Inference on open-weight models via Endpoints** + **Sandboxes**. (Optionally add Other: "video-processing pipeline workers") |
| Estimated compute you need | **$50-100** |
| Acknowledgement | Check the box |

---

## FORM 2 — Baseten Credits (Google Form)

| Field | Paste this |
|---|---|
| Full name | `Nabidnur abrar` |
| Email you applied with on Cerebral Valley | `nurnabid754@gmail.com` |
| Team name | `team-blackbox` |
| All Teammate emails | `nurnabid754@gmail.com` |
| Track | **Indie** |
| Project one-liner (What are you building and how will you use Baseten?) | `Ustad converts one-time filmed demonstrations of work tasks into structured, illustrated SOPs with trainee quizzes for hands-on businesses (street-food stall chains first). We will use Baseten to serve Muse Spark Open (open weights) for the high-volume text steps — structuring step lists, generating checkpoint quizzes and nightly batch re-processing of newly filmed tasks — where frontier-API cost per token would not scale, with 2M TPM headroom absorbing our batch bursts.` |
| GitHub profile or repo link | `https://github.com/Hisernberg` (repo: `https://github.com/Hisernberg/meta-ai-hackathon-2026`) |
| Expected request volume | **Heavy (agents, batch)** — nightly batch re-processing of filmed tasks + multi-step agent loops per video |
| Acknowledgement | Check the box |

---

## FORM 3 — Final Project Submission (Cerebral Valley)

| Field | Paste this |
|---|---|
| Team Name | `team blackbox` |
| Team Members | `navi12` (Nabid Nur) — as registered |
| Track | **Indie** |
| Which problem statement | **Build for Your World** |
| Most Viral Track — X post link | [FILL] — post the demo clip on X during submission week and paste the link (optional bonus track; recommended: the "quiz catches the skipped step" 15s clip) |
| Project Description | `Ustad — the job that teaches itself. In every street-food stall chain, the real recipe lives in one expert's hands: new hires learn by shadowing for weeks, quality drifts stall by stall, and when the expert quits, the chain re-learns from customer complaints. Ustad fixes this with one habit: film the task once. Our pipeline turns that single phone video into a living, checkable procedure — Muse Spark 1.3 segments the take into timestamped steps, Muse Voice Transcribe aligns the narrated know-how, SAM 3.1 isolates the key object in every step, and Muse Image renders clean step cards and "spot the mistake" trainee scenes. The expert approves the draft with one tap — that signature makes it the standard. Trainees then learn from the SOP as a tap-through quiz on a shared phone, earning a readiness score instead of breaking real things; a self-hosted Muse Glimmer path keeps training alive with zero connectivity. Film it once, and everyone becomes the master's second pair of hands.` |
| Public GitHub Repository | `https://github.com/Hisernberg/meta-ai-hackathon-2026` — **[ACTION: flip the repo to Public before submitting]** (Settings → General → Danger Zone → Change visibility) |
| 3-Minute Demo Video | [FILL] — YouTube link; shoot Day 7, upload Day 8; beat sheet in `CHAMPION_V2.md` §6 |
| Describe your use of Meta products to build the submitted project | `Meta's Model API is the engine of every Ustad loop: muse-spark-1.3 performs video understanding to segment a filmed task into timestamped steps and outputs structured step JSON; muse-voice-transcribe-1.0 transcribes and diarizes the expert's Bengali narration (streaming, $0.18/hr) and aligns each sentence to its step; sam-3.1 segments the key tool or ingredient in each step's keyframe from a text prompt; muse-image-1.0 renders clean illustrated step cards and generates the deliberately-wrong "spot the mistake" scenes for trainee quizzes; and muse-glimmer (open weights) is self-hosted so trainee mode works offline on shared phones. We also process videos through Modal sandbox workers and batch text steps on Baseten using Muse Spark Open.` |
| Why are Meta's models important to your solution? | `Ustad is only possible because one API covers the whole multimodal chain a work procedure is made of — video, speech, segmentation and image generation — with token/image pricing a solo builder's credits can absorb. Spark's long video understanding turns a messy 5-minute film into structured steps; SAM 3.1's text-prompted segmentation is what makes step cards readable to someone who has never done the job; and the open-weight models (Glimmer, Spark Open) let the training path run offline on a $100 laptop and in batch on Baseten — exactly the reality of the stalls and workshops Ustad is built for. No single-model API could produce the illustrated, checkable, multilingual artifact that makes a filmed task teach itself.` |
| Provide feedback from your experience using Meta products | `The Model API's OpenAI-compatible surface made integration fast, and the multimodal breadth (video understanding + SAM 3.1 + Voice Transcribe + anchored image editing behind one key) is the standout — our entire pipeline is four calls. Voice Transcribe's diarization at $0.18/hr is exceptional value. Friction points: video-understanding latency on longer takes needed a chunking strategy, and streaming tool-calling took a couple of iterations to stabilize under parallel step extraction. Overall the credit program made a multimodal pipeline viable for a solo indie build.` |
| Provide feedback from your experience using partner technologies (Fireworks, Modal, Baseten) | `Modal's sandboxes were the cleanest way to isolate our ffmpeg/video-processing workers — reproducible environments without local setup pain. Baseten's open-weight serving for Muse Spark Open handled our nightly batch re-processing with predictable throughput, and the 2M TPM headroom removed rate-limit anxiety during batch bursts. We did not need Fireworks for this build but the option of a second open-weight host would be our first stop at scale.` |

---

### Submission-week action list (in order)

1. Build per plan (Day 2-7) — keep the repo's commit history honest and frequent.
2. Day 7: shoot the 3-minute demo (beat sheet: `CHAMPION_V2.md` §6); edit to 3:00 max.
3. Day 8 morning: flip GitHub repo **public**; upload video to YouTube (unlisted is fine unless rules say public); post the X clip for Most Viral.
4. Submit the Cerebral Valley form; paste answers above with the two [FILL] items.
5. Deadline safety: submission is due **Nov 5, 8:00 AM Dhaka time** (Nov 4, 9:00 PM ET) — target **Nov 4, ~9:00 PM Dhaka** to keep a 12-hour buffer.
6. Submit Modal + Baseten credit forms ASAP (selection is use-case based, not first-come) — the one-liners above are ready.
