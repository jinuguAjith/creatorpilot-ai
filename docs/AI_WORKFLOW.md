# CreatorPilot AI - AI Workflow & Orchestration

**Version:** 1.0  
**Status:** MVP Pipeline  
**Last Updated:** August 2026

---

## 1. AI Generation Pipeline Overview

### High-Level Flow

```
User Input (via Mobile App)
    ↓
Backend API validates & reserves credits
    ↓
Enqueue job to AI Orchestrator
    ↓
Orchestrator processes asynchronously
    ├─ Step 1: Input Moderation
    ├─ Step 2: Campaign Strategy Generation
    ├─ Step 3: Poster Generation
    ├─ Step 4: Video Scene Generation
    ├─ Step 5: Audio Selection
    ├─ Step 6: Voice-Over Generation (if requested)
    ├─ Step 7: Media Composition (FFmpeg)
    └─ Step 8: Output Moderation & Storage
    ↓
Results stored in GCS & metadata in Firestore
    ↓
Mobile app downloads results
```

---

## 2. Detailed Step-by-Step Workflow

### Step 1: Input Moderation

**Purpose:** Filter harmful, abusive, or policy-violating user input

**Implementation:**
```python
class InputModerationStep:
    async def execute(self, campaign_input: CampaignInput) -> ModerationResult:
        """
        Check user input for:
        - Hate speech / discrimination
        - Violence / illegal activity
        - Spam / abuse patterns
        - Profanity
        - URL injection / malicious content
        """
        
        # Option 1: Use Google Perspective API
        score = await self.perspective_api.analyze(campaign_input.text)
        if score > THRESHOLD_REJECT:
            return ModerationResult(passed=False, reason="Inappropriate content")
        
        # Option 2: Use regex + keyword filters
        if self.contains_banned_words(campaign_input.text):
            return ModerationResult(passed=False, reason="Prohibited language")
        
        return ModerationResult(passed=True)
```

**Outcomes:**
- ✅ PASS: Continue to Step 2
- ❌ FAIL: Return error, refund credits, notify user

---

### Step 2: Campaign Strategy Generation

**Purpose:** Generate structured campaign copy and visual direction

**Prompt Template:**
```
You are a professional marketing strategist and copywriter.
Based on the following business input, create a comprehensive campaign strategy.

Business Input:
- Description: {business_description}
- Industry: {industry}
- Target Audience: {target_audience}
- Offer: {offer}
- Location: {location}
- Tone: {tone}

Generate a JSON response with:
{
  "headline": "Main promotional headline (max 10 words)",
  "subheadline": "Supporting line (max 20 words)",
  "social_caption": "Instagram/TikTok caption (max 150 chars)",
  "hashtags": ["#tag1", "#tag2", ...],
  "cta": "Call-to-action button text",
  "visual_direction": "Detailed visual description for designers/AI",
  "color_mood": "Primary color feeling (e.g., warm, cool, luxury)",
  "video_storyboard": [
    {
      "scene_number": 1,
      "scene_name": "Establishing shot",
      "description": "Wide shot of business exterior/entrance",
      "duration_seconds": 4,
      "visual_elements": ["sunlight", "entrance sign", "customers arriving"],
      "suggested_text_overlay": "[Business Name] - Opening Soon"
    },
    ...
  ]
}
```

**Implementation:**
```python
class CampaignStrategyStep:
    async def execute(self, campaign_input: CampaignInput) -> CampaignStrategy:
        prompt = self.build_prompt(campaign_input)
        
        response = await self.gemini_provider.generate_text(
            model="gemini-pro",
            prompt=prompt,
            temperature=0.7,  # Slightly creative
            max_tokens=2000
        )
        
        strategy = json.loads(response)
        return CampaignStrategy(**strategy)
```

**Cost:** ~0.05 USD per call

---

### Step 3: Poster Generation

**Purpose:** Create professional promotional poster image

**Prompt Template:**
```
You are an expert graphic designer using AI image generation.
Create a professional promotional poster based on:

Brand Info:
- Business: {business_name}
- Logo: [provided if available]
- Colors: Primary {color_primary}, Secondary {color_secondary}
- Font style: {font_style}

Poster Content:
- Headline: {headline}
- Subheadline: {subheadline}
- Offer: {offer}
- CTA: {cta}
- Contact: {phone} / {website}
- Location: {location}

Visual Direction: {visual_direction}

Design Requirements:
- Aspect ratio: {aspect_ratio}
- Resolution: 1080x1920px (or equivalent)
- Professional, modern design
- Clear visual hierarchy
- Readable typography
- Brand colors prominently featured
- High contrast for text readability
- Include business logo if provided
- NO spelling errors
- Mobile-optimized composition

Generate a high-quality poster image.
```

**Implementation:**
```python
class PosterGenerationStep:
    async def execute(self, campaign_strategy: CampaignStrategy, brand_kit: BrandKit) -> ImageArtifact:
        prompt = self.build_poster_prompt(campaign_strategy, brand_kit)
        
        # Generate image via Gemini image generation or similar
        image_bytes = await self.gemini_provider.generate_image(
            prompt=prompt,
            aspect_ratio=campaign_strategy.aspect_ratio,
            quality="high"
        )
        
        # Validate image
        if not self.validate_image(image_bytes):
            raise PosterGenerationError("Generated image failed validation")
        
        # Upload to GCS
        gcs_path = await self.gcs_client.upload(
            bucket="creatorpilot-media",
            file_path=f"gen-{generation_id}/poster.png",
            data=image_bytes
        )
        
        return ImageArtifact(
            type="poster",
            gcs_path=gcs_path,
            size_bytes=len(image_bytes)
        )
```

**Cost:** ~0.5 USD per image

---

### Step 4: Video Scene Generation

**Purpose:** Generate individual video clips for each scene in storyboard

**Process:**
```python
class VideoGenerationStep:
    async def execute(self, campaign_strategy: CampaignStrategy) -> List[VideoClip]:
        video_clips = []
        
        for scene in campaign_strategy.video_storyboard:
            # Build scene-specific prompt
            prompt = f"""
            Generate a professional short video clip for this scene:
            
            Scene: {scene['scene_name']}
            Description: {scene['description']}
            Duration: {scene['duration_seconds']} seconds
            Style: {campaign_strategy.color_mood}, professional
            Industry: {campaign_strategy.industry}
            
            Specifications:
            - Aspect ratio: 9:16 (vertical)
            - Resolution: 1080x1920
            - Frame rate: 30fps
            - Duration: {scene['duration_seconds']}s
            - High quality, cinematic style
            - No text (will be added as overlay)
            - Professional transitions ready
            """
            
            # Generate video via Google Veo or similar
            video_bytes = await self.veo_provider.generate_video(
                prompt=prompt,
                duration_seconds=scene['duration_seconds'],
                aspect_ratio="9:16"
            )
            
            # Upload to GCS
            gcs_path = await self.gcs_client.upload(
                bucket="creatorpilot-media",
                file_path=f"gen-{generation_id}/scene_{scene['scene_number']}.mp4",
                data=video_bytes
            )
            
            clip = VideoClip(
                scene_number=scene['scene_number'],
                gcs_path=gcs_path,
                duration_seconds=scene['duration_seconds']
            )
            video_clips.append(clip)
        
        return video_clips
```

**Cost:** ~2.50 USD per 30-second video (across all scenes)

---

### Step 5: Audio Selection

**Purpose:** Select or generate background music matching campaign mood

**Implementation:**
```python
class AudioSelectionStep:
    async def execute(self, campaign_strategy: CampaignStrategy) -> AudioAsset:
        mood = campaign_strategy.color_mood  # "luxury", "energetic", etc.
        duration = 30  # seconds
        
        # Option 1: Query licensed audio library
        audio_tracks = await self.audio_library.search(
            mood=mood,
            genre="promotional",
            duration_min=duration,
            limit=5
        )
        
        # Select best match (could use ML ranking)
        selected_track = audio_tracks[0]
        
        # Option 2: Generate audio if no good matches
        if not selected_track or selected_track.score < 0.7:
            audio_bytes = await self.text_to_audio.generate(
                description=f"Background music for {mood} promotional video",
                duration=duration
            )
            gcs_path = await self.upload_audio(audio_bytes)
            return AudioAsset(type="generated", gcs_path=gcs_path)
        
        return AudioAsset(type="licensed", gcs_path=selected_track.gcs_path)
```

**Cost:** $0 (using licensed library) or ~0.25 USD (if generated)

---

### Step 6: Voice-Over Generation (Optional)

**Purpose:** Generate AI voice-over reading the campaign caption

**Implementation:**
```python
class VoiceOverGenerationStep:
    async def execute(self, campaign_strategy: CampaignStrategy, language: str) -> AudioAsset:
        if not campaign_strategy.include_voiceover:
            return None
        
        text = campaign_strategy.social_caption
        
        # Use Google Cloud TTS
        voice_bytes = await self.tts_provider.synthesize(
            text=text,
            language_code=language,  # "en-IN", "te-IN", etc.
            voice_name="Neural2-C",
            pitch=0,
            speaking_rate=1.0
        )
        
        # Upload to GCS
        gcs_path = await self.gcs_client.upload(
            bucket="creatorpilot-media",
            file_path=f"gen-{generation_id}/voiceover.mp3",
            data=voice_bytes
        )
        
        return AudioAsset(type="voiceover", gcs_path=gcs_path, language=language)
```

**Cost:** ~0.10 USD per 1000 characters

---

### Step 7: Media Composition (FFmpeg)

**Purpose:** Combine video scenes, audio, voice-over, text overlays into final MP4

**Implementation:**
```python
class MediaCompositionStep:
    async def execute(
        self,
        video_clips: List[VideoClip],
        audio: AudioAsset,
        voiceover: Optional[AudioAsset],
        campaign_strategy: CampaignStrategy,
        brand_kit: BrandKit
    ) -> VideoArtifact:
        
        # 1. Download all assets from GCS
        assets = await self.download_assets(video_clips, audio, voiceover)
        
        # 2. Build FFmpeg command
        ffmpeg_cmd = self.build_ffmpeg_command(
            video_clips=video_clips,
            audio=audio,
            voiceover=voiceover,
            campaign_strategy=campaign_strategy,
            brand_kit=brand_kit
        )
        
        """
        Example FFmpeg workflow:
        
        1. Concatenate video scenes with transitions
        ffmpeg -f concat -safe 0 -i filelist.txt -vf "transition=fade:d=0.5" output.mp4
        
        2. Mix audio tracks (background + voice-over)
        ffmpeg -i video.mp4 -i background.mp3 -i voiceover.mp3 \
            -filter_complex "[1:a][2:a]amerge=inputs=2[a]" \
            -map 0:v -map "[a]" -c:a aac output.mp4
        
        3. Add text overlays (headline, CTA, hashtags)
        ffmpeg -i video.mp4 \
            -vf "drawtext=...headline..., drawtext=...cta..." \
            output.mp4
        
        4. Add logo watermark/branding
        ffmpeg -i video.mp4 -i logo.png \
            -filter_complex "overlay=10:10" \
            output.mp4
        
        5. Final encoding and optimization
        ffmpeg -i composed.mp4 -c:v libx264 -preset medium -crf 23 \
            -c:a aac -b:a 128k -vf scale=1080:1920 final.mp4
        """
        
        # 3. Execute FFmpeg
        output_path = "/tmp/final_video.mp4"
        result = await self.execute_ffmpeg(ffmpeg_cmd, output_path)
        
        if result.return_code != 0:
            raise CompositionError(f"FFmpeg failed: {result.stderr}")
        
        # 4. Validate output
        if not self.validate_video(output_path):
            raise CompositionError("Generated video failed validation")
        
        # 5. Upload to GCS
        with open(output_path, 'rb') as f:
            gcs_path = await self.gcs_client.upload(
                bucket="creatorpilot-media",
                file_path=f"gen-{generation_id}/video.mp4",
                data=f.read()
            )
        
        return VideoArtifact(
            type="video",
            gcs_path=gcs_path,
            duration_seconds=30,
            dimensions="1080x1920",
            fps=30
        )
```

**Cost:** ~0.10 USD (compute + storage)

---

### Step 8: Output Moderation & Storage

**Purpose:** Validate generated content and store metadata

**Implementation:**
```python
class OutputModerationStep:
    async def execute(self, poster: ImageArtifact, video: VideoArtifact) -> bool:
        """
        Check generated content for:
        - NSFW content in images/video
        - Quality issues
        - Copyright flags
        - Compliance with policies
        """
        
        # Scan poster
        poster_safe = await self.safety_checker.check_image(poster.gcs_path)
        if not poster_safe:
            raise OutputModerationError("Poster flagged as unsafe")
        
        # Scan video frames (sample first/middle/last frames)
        video_safe = await self.safety_checker.check_video(video.gcs_path)
        if not video_safe:
            raise OutputModerationError("Video flagged as unsafe")
        
        # All checks passed
        return True
```

**Cost:** ~0.05 USD per check

---

## 3. Error Handling & Retries

### Retry Strategy

```python
class RetryPolicy:
    """
    Define retry behavior per step
    """
    
    RETRY_POLICIES = {
        "input_moderation": {"max_retries": 0},  # Fail fast
        "campaign_strategy": {"max_retries": 2, "backoff": "exponential"},
        "poster_generation": {"max_retries": 3, "backoff": "exponential"},
        "video_generation": {"max_retries": 2, "backoff": "exponential"},
        "audio_selection": {"max_retries": 1, "backoff": "linear"},
        "voiceover_generation": {"max_retries": 2, "backoff": "exponential"},
        "media_composition": {"max_retries": 2, "backoff": "exponential"},
        "output_moderation": {"max_retries": 1, "backoff": "linear"},
    }
    
    async def execute_with_retry(self, step_name: str, fn, *args, **kwargs):
        policy = self.RETRY_POLICIES[step_name]
        max_retries = policy["max_retries"]
        
        for attempt in range(max_retries + 1):
            try:
                return await fn(*args, **kwargs)
            except Exception as e:
                if attempt >= max_retries:
                    raise  # Final attempt failed
                
                wait_time = self.calculate_backoff(
                    attempt,
                    policy["backoff"]
                )
                logger.warning(f"Retry {step_name} attempt {attempt+1} in {wait_time}s")
                await asyncio.sleep(wait_time)
```

### Fallback Strategies

| Step | Fallback |
|------|----------|
| Poster Gen Fails | Return template-based design |
| Video Gen Fails | Return image slideshow (3-5 images with transitions) |
| Audio Not Found | Use default royalty-free background music |
| Voice-Over Fails | Skip voice, continue with video + music |

---

## 4. Cost Estimation

### Per-Generation Cost Breakdown

```
Typical 30-second campaign generation:

Gemini API calls (text + image gen):    $0.55
  - Campaign strategy:                   $0.05
  - Poster generation:                   $0.50

Google Veo (video generation):          $2.50
  - Scene generation (4 scenes × 7.5s):  $2.50

TTS (voice-over):                       $0.10
  - Synthesize caption text:             $0.10

FFmpeg (composition):                   $0.10
  - CPU compute, temporary storage:      $0.10

Moderation checks:                      $0.05
  - Image/video safety scanning:         $0.05

GCS Storage (30 days):                  $0.20
  - Poster (2.5 MB):                     $0.001
  - Video (125 MB):                      $0.199

═════════════════════════════════════════════
TOTAL ESTIMATED COST:                   $3.50 USD
═════════════════════════════════════════════

Credits charged to user:
- Poster:          100 credits
- Video (30s):     500 credits  
- Caption:         25 credits
- Voice-over:      100 credits
═════════════════════════════════════════════
Total:             725 credits

Assume: 725 credits = $2.90 revenue
Margin: $2.90 - $3.50 = -$0.60 (loss on this transaction)

⚠️ This means we need:
1. Optimize AI provider costs
2. Charge more per output
3. Offer discounts for bulk subscriptions
```

---

## 5. Monitoring & Observability

### Key Metrics

```python
metrics = {
    "generation_latency_ms": histogram,
    "step_latency_ms": histogram (per step),
    "success_rate_percent": gauge,
    "failure_rate_by_step": gauge,
    "ai_cost_per_generation_usd": gauge,
    "retry_count_distribution": histogram,
    "generation_queue_size": gauge,
    "active_generations_count": gauge,
    "provider_latency_ms": histogram (per provider),
}
```

### Logging

```python
# Every step logs structured JSON
logger.info({
    "event": "step_completed",
    "generation_id": generation_id,
    "step": "poster_generation",
    "status": "COMPLETED",
    "duration_ms": 8000,
    "retry_count": 0,
    "ai_provider": "gemini-pro-vision",
    "cost_usd": 0.50,
    "timestamp": datetime.utcnow().isoformat()
})
```

---

## Document Status

**PHASE 0 STATUS: AI WORKFLOW DOCUMENTED**

- ✅ Generation pipeline detailed
- ✅ Step-by-step implementation specified
- ✅ Prompts and techniques documented
- ✅ Error handling & retry logic defined
- ✅ Cost estimation provided
- ✅ Monitoring strategy outlined
- ⏳ Ready for security documentation

---

**Next:** SECURITY.md - Security implementation, authentication, authorization, and compliance.
