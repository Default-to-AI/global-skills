# Product Strategy Frameworks — Quick Reference Card

---

## One-Liner Invocations

| Need | Skill | Prompt Template |
|------|-------|-----------------|
| Positioning | blue-ocean-strategy | "Build a Strategy Canvas of our top 6 competitors, then apply the Four Actions Framework to find a blue ocean move." |
| Customer needs | jobs-to-be-done | "Help me uncover the real Job to Be Done for our product. Who are the hiring managers and what competing 'hires' should I worry about?" |
| GTM (B2B SaaS) | crossing-the-chasm | "Are we ready for pragmatist buyers? Map our product against the whole product model and identify a beachhead segment." |
| Brand messaging | storybrand-messaging | "Walk me through the full StoryBrand brand script: hero, problem, guide, plan, CTA, success vs. failure." |
| Outbound sales | predictable-revenue | "Design a Cold Calling 2.0 outbound process: ideal customer profile, 3-email sequence, lead qualification, and pipeline math." |
| Experiments | lean-startup | "Build a Build-Measure-Learn experiment card and a 5-day sprint plan to go from sketches to testable prototype." |
| Retention | hooked-ux | "Diagnose onboarding drop-off using B=MAP. Then map each step to the Hook Model cycle." |
| CRO audit | cro-methodology + influence-psychology | "Run a full CRO audit: top 5 visitor objections, missing persuasion assets, and which of Cialdini's 7 principles are absent." |
| Negotiation | negotiation | "Write responses to our top 3 objections using tactical empathy: labels, calibrated questions, and 'That's right' moments." |
| Team incentives | drive-motivation | "Create a Vision/Traction Organizer with our 10-year target, 3-year picture, and 1-year plan. Then audit our incentive structure for Autonomy-Mastery-Purpose." |
| Operations | traction-eos | "Create a Vision/Traction Organizer with our 10-year target, 3-year picture, and 1-year plan." |
| Sprint process | design-sprint | "Build a Build-Measure-Learn experiment card and a 5-day sprint plan to go from sketches to testable prototype." |
| UI design | refactoring-ui + top-design | "Design a homepage that would score on Awwwards: type system, hero composition, scroll reveals, and micro-interactions." |
| Typography | web-typography | "Audit our typography for readability. Then apply Refactoring UI hierarchy principles and deliver updated CSS." |
| Usability | ux-heuristics + design-everyday-things | "Apply Nielsen's 10 heuristics and Norman's framework to audit our dashboard. Rate each violation 0-4 severity." |
| iOS compliance | ios-hig-design | "Check our iOS app against HIG: navigation patterns, 44pt touch targets, Dynamic Island, and safe areas." |
| Quiz funnels | scorecard-marketing | "Design a complete scorecard funnel: quiz title, 12 questions, scoring logic, and 3 result tiers with tailored CTAs." |
| Memorable comms | made-to-stick | "Score our pitch on the SUCCESs checklist. Rewrite it so the core message passes the Commander's Intent test." |

---

## Install Order (Dependency-Aware)

```bash
# 1. Core strategy (no deps)
jobs-to-be-done
blue-ocean-strategy
crossing-the-chasm

# 2. Messaging & sales (use core strategy outputs)
storybrand-messaging
predictable-revenue

# 3. Experiment & growth (use messaging outputs)
lean-startup
design-sprint
hooked-ux

# 4. Operations & team
traction-eos
drive-motivation

# 5. Design / specialized (standalone)
refactoring-ui
web-typography
ux-heuristics
design-everyday-things
ios-hig-design
top-design
scorecard-marketing
made-to-stick
cro-methodology
influence-psychology
negotiation
```

---

## Verification Checklist

After installing each skill:
- [ ] `hermes skills list | grep <skill-name>` shows it
- [ ] `"Use <skill-name> skill to analyze our product"` produces structured framework output (not generic advice)
- [ ] References load: skill has `references/` dir with book frameworks/templates