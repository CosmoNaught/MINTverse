# MINTverse house style

The model is the [malariasimulation vignettes](https://mrc-ide.github.io/malariasimulation/).
Write the way that package's authors write. `misc/prosecheck.py` enforces the mechanical half of
what follows and fails the build on any violation.

## Punctuation

- **No em-dashes.** The malariasimulation corpus contains none. Parentheses do the aside work.
- **No semicolons in prose.**
- **No colons in the middle of a sentence.** A colon at the end of a line, introducing a code
  block or a list, is fine.
- En-dashes only inside numeric ranges in tables (`0–1`).
- No rhetorical questions.

## Rhythm

Front-load every paragraph. The first sentence states the whole point and the rest of the
paragraph elaborates it. Never open on a short pronouncement that the paragraph then explains.

> Bad: "The emulator runs from an EIR. The first stage inverts whatever you have, a measured
> prevalence or an HBR, into the EIR that would sustain it."
>
> Good: "MINTverse runs in two stages because the emulator takes an EIR and a user almost never
> has one. The first stage inverts whatever has been measured, a parasite prevalence or a human
> biting rate, into the EIR that would sustain it in the setting it was measured in."

Default to long, clause-stacked expository sentences, punctuated occasionally by a short flat
declarative. Mean around 16 words with high variance. A page of same-length sentences reads as
machine-written, and `prosecheck.py` measures exactly this.

No aphorisms. No metaphor. No mystery-then-reveal ("That approach is wrong." / "It is also a
surprising one."). No verbless fragments.

## Headings

Bare nouns or bare imperatives. `Parameterisation`, `Simulation`, `Visualisation`, `Batching`,
`Run a scenario`, `A note on itn_use`. Seven words at most.

Not `Truth against emulator`, not `The pickle boundary`, not `What dn0 does not capture`, not
`Domain limits {#where-validity-is-decided}`.

## Tone

- "We" for the walkthrough, "the user" for a capability in the abstract. Contractions are fine.
- Chain sections with "First, ... Next, ... Having established X, we can now Y."
- Every warning is "Note that ...". Every pointer is "Please see ...".
- Assume the reader knows malaria. Do not assume they know the API, and walk it argument by
  argument.
- British spelling. Parameterise, visualise, modelled, behaviour, colour, summarising.

## Describing output

Tell the reader what to notice, then explain the mechanism with "This is because...". Contrast
with "X, while Y". **Name the plot colours in the prose.**

> "The red line runs above the white one while the green line stays on it, because `estimint`
> estimated an EIR of 12.5 against a true 11.8."

## This is not a buying guide

The packages compute trajectories. They do not tell anyone which net to purchase. Do not write
`Which net to buy`, `Ranking on endline cases`, `Product choice`, "a district has a fixed
budget", "the policy question is", "worth the extra cost per net". Report what the curves do and
stop. Prevalence trajectories first, then clinical cases, then cases averted.

## Vocabulary to avoid

The excess vocabulary of LLM-assisted writing, from Kobak et al., *Delving into LLM-assisted
writing in biomedical publications through excess vocabulary* (Science Advances, 2025), and
Liang et al. (ICML 2024). `prosecheck.py` carries the full list.

delve, underscore, showcase, intricate, meticulous, commendable, pivotal, realm, tapestry,
testament, nuanced, boasts, leverage, seamless, crucial, comprehensive, landscape, multifaceted,
groundbreaking, transformative, paramount, compelling, unlock, streamline, myriad, plethora,
holistic, paradigm, synergy, facilitate, interplay, elevate, harness, unveil, illuminate,
foster, moreover, furthermore, additionally, ultimately, importantly, notably, utilise.

And the phrases: "it is worth noting", "in conclusion", "shed light on", "at its core",
"in essence", "deep dive", "not just a", "more than just".

## Every output is in a box

`styles/theme.scss` boxes every executed-cell output. A `​```text` fence is a transcript and is
labelled "Output". A fence that is a diagram rather than a result is tagged
`​```{.text .diagram}` so it keeps the panel but loses the label.
