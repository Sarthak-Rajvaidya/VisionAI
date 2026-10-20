Current existing soln 

Seeing AI, Envision, Google Lookout, Be My Eyes
Be My Eyes, for instance, now runs its smart assistant integrated with GPT-4 to power its virtual assistant features, which means it needs a live internet connection to work well. 

one Envision AI user reviewing the app said the recognition quality was excellent but they hoped for full offline recognition, since the current performance still depends on connectivity.

Lookout launched only for Google's Pixel devices in the US initially, and general availability across budget Android phones (which is what most users in India actually own) has been slow.

Almost all of them are English-first; regional-language OCR/TTS support (Hindi, Marathi, etc.) is thin to nonexistent.->Main problem :-


1. Fully offline, on-device pipeline (strongest, most "engineering" angle)
Run a quantized YOLOv8-nano/tiny model + an on-device OCR engine (Google ML Kit Text Recognition or PaddleOCR mobile) + Android's built-in offline TTS — no server calls at all. This directly answers the exact complaint real users have, and it's a genuinely measurable, demoable claim: "works with airplane mode on." It's also very reviewable — you can show latency numbers and say "zero cloud dependency, zero data cost, works in low-connectivity areas," which lands well with a panel.
2. Regional language support
Most competitors are built for the US/global English market. Build OCR + TTS output in Hindi/Marathi (or whichever language fits your context) alongside English. This is a strong, low-effort differentiator for an Indian academic project — evaluators respond well to localization because it's an obvious, real gap nobody big is solving well.

3. Priority-based, spatial audio feedback (the UX differentiator)
Instead of announcing everything the camera sees in order, rank detections by relevance — an obstacle directly in your path gets announced immediately and loudly; a poster on a wall gets lower priority or is skipped. Add basic left/right stereo panning so "chair on your left" actually sounds like it's on your left. This is genuinely different from most apps, which just read out a flat list of detected objects — and it's very demoable live.

4. Optimize explicitly for low-end/budget devices
Bonus differentiator, almost free to claim if you're already doing #1: benchmark your app specifically on a ₹10–15k Android phone and report FPS/latency there, not on a flagship. Most competing apps are effectively built and tested on high-end hardware. "Runs smoothly on affordable phones" is a real, citable design goal that directly serves your stated population (affordable AI-powered assistance — which is already in your problem statement).


