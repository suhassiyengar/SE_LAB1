# Lab 4: VibeCoding – Lava Escape Repair Lab

**Student:** Suhas S Iyengar  
**Student ID:** PES1UG24AM291  
**Course:** Software Engineering Lab (SETAPESU26)  
**Date:** October 6, 2026  
**Assigned Repository:** `52_lava-escape`  
**Target Submission:** `se_lab1/lab4`  

---

## 📋 Deliverables Summary

| Deliverable | Description | File Path | Status |
|---|---|---|---|
| **Before Gameplay Video** | 10-second gameplay video showing the original underside collision snapping bug | `lab4/before_recording.mp4` | ✅ Completed |
| **After Gameplay Video** | 10-second gameplay video showing all bug fixes & 3 features working | `lab4/after_recording.mp4` | ✅ Completed |
| **Updated Codebase** | Python source files implementing all mechanics cleanly | `lab4/game/`, `lab4/main.py` | ✅ Completed |
| **Chat & Prompt Log** | Full PDF and Markdown transcript of prompts, rationale, and commit logs | `lab4/Lab4_VibeCoding_Chat_History.pdf` | ✅ Completed |

---

## 📌 Commit Log (Individual Commits per Task)

1. **Task 1 Commit (`1bc1a42`)**: `Task 1: Fix platform underside collision snapping bug`
2. **Task 2 Commit (`9f4aefc`)**: `Task 2: Implement crumbling platform hazards`
3. **Task 3 Commit (`95446d9`)**: `Task 3: Implement high-velocity spring platforms`
4. **Task 4 Commit (`f15f119`)**: `Task 4: Implement rising danger HUD and periodic lava burst surges`

---

## 🚀 Step-by-Step VibeCoding Prompt Log

### Step 1: Initial Run & Before Gameplay Recording
- **Prompt:** Launch original game to test mechanics and record before video.
- **Bug Diagnosed:** In `game/player.py`, `self.rect.bottom <= p.bottom + 10` snapped the player to `p.top` even when ascending or with apex below the top surface.
- **Video Recorded:** `before_recording.mp4` (10 seconds).

---

### Step 2: Task 1 – Fix Platform Underside Collision Snapping Bug
- **Prompt:**
  > *"Fix the platform collision snapping bug in game/player.py. Ensure that when jumping from underneath, the player does not snap to the platform top unless they have strictly cleared the upper edge."*
- **Solution:**
  - Preserved previous bottom position before moving: `prev_bottom = self.rect.bottom`.
  - Added strict check: `prev_bottom <= plat_rect.top + 4` and descending motion `vel_y >= 0`.
- **Validation:** Automated unit test verified jumping from underneath passes cleanly through; falling from above grounds securely on platform surface.
- **Commit:** `1bc1a42`.

---

### Step 3: Task 2 – Implement Crumbling Platform Hazards
- **Prompt:**
  > *"Implement crumbling platform hazards in game/world.py. Add an OOP Platform class where crumbling platforms begin shaking and collapse into falling debris after being stepped on, forcing constant upward mobility."*
- **Solution:**
  - Implemented `Platform(pygame.Rect)` with state: `kind="crumbling"`, `crumble_timer=50`, `shake_offset_x`, `debris`.
  - When player lands, `stepped_on = True`. The platform shakes with increasing jitter, crack lines appear, and after 50 frames collapses into 14 falling rubble particles (`is_broken = True`).
  - Player falls through cleanly once collapsed.
- **Validation:** Automated unit test verified `stepped_on` trigger, crumbling timer countdown, break flag, and player falling through.
- **Commit:** `9f4aefc`.

---

### Step 4: Task 3 – Implement High-Velocity Spring Platforms
- **Prompt:**
  > *"Implement high-velocity spring platforms. Add distinct green spring platforms that launch the player with bonus vertical velocity (e.g. -20 vs standard -13) with a bounce animation and launch sparkle particles."*
- **Solution:**
  - Added `kind="spring"` with emerald-green body, metallic base, and chevron graphics.
  - Landing on spring automatically triggers `trigger_spring()`: propels player upward with `vel_y = -20` (reaching >360px vertical height), compresses spring pad for 12 frames, and sprays launch sparkles.
- **Validation:** Unit test verified instant velocity change to `-20`, bounce timer activation, and particle emission.
- **Commit:** `95446d9`.

---

### Step 5: Task 4 – Implement Rising Danger HUD & Periodic Lava Burst Surges
- **Prompt:**
  > *"Implement a Rising Danger HUD & periodic Lava Burst Surges in game_engine.py and world.py. Track lava speed with a color-coded danger gauge and trigger timed lava surges with warning banners and fire burst particles."*
- **Solution:**
  - Implemented 540-frame cycle (~9s at 60 FPS):
    - Normal ascent (0-380 frames)
    - Warning phase (380-450 frames): flashing amber alert banner `! LAVA SURGE WARNING !`
    - Surge active phase (450-540 frames): lava speed multiplied by 2.6x, flashing red banner `>>> LAVA SURGE ACTIVE! <<<`, and burst fire sparks shooting up from the waves.
  - Enhanced `draw_lava`: dynamic wave amplitude (14px), speed (0.22), glowing crest lines, and ambient radiant heat glow.
  - Danger Meter HUD: Displays real-time speed (`{speed:.1f}x`), danger status (`LOW`, `MED`, `HIGH`, `SURGE BURST!`), and color-shifting gauge.
- **Validation:** 60-frame simulation verified warning banner at frame 385, active surge boost at frame 460, and zero-error drawing.
- **Commit:** `f15f119`.

---

### Step 6: Post-Changes & 'After' Gameplay Video
- **Recording Captured:** `after_recording.mp4` (10 seconds) demonstrating clean jumping, collapsing fragile platforms, high-velocity spring launches, and lava burst surge with the Danger HUD.
