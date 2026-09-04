# Part C Memo

## Assumptions

- Launch window is 3 weeks.
- Available training budget is 1x A100 for 2 weeks.
- Human review budget is 10 hours per week and only for Hindi plus Kannada.
- No external API budget is available.

## Arithmetic

Assume a 0.5B-class quantized rewriter and 1,000 seed intents across six languages: 6,000 synthetic pairs. At 100 target tokens per pair, that is approximately 600,000 target tokens. Reserve two 4-8 hour A100 runs plus evaluation inside the two-week GPU window. Review 400 held-out Hindi/Kannada outputs at three minutes each: `400 * 3 / 60 = 20` reviewer-hours, exactly the two-week review budget. Prompt-only has the lowest compute cost but consumes iteration and review time without producing a reusable artifact. Full SFT has the largest rollback and validation scope. The rewriter best fits the constrained budget.

## Success metric and threshold

Use blinded native review for Hindi and Kannada. Launch only if both languages reach at least `4.0/5` mean casualness, semantic adequacy is at least `95%` on 400 reviewed outputs, and p95 end-to-end latency increases by no more than `15%` over the base path.

## Kill criterion and timing

Kill the rewriter after the second training/evaluation iteration, no later than the end of week 2, if either language is below `3.5/5` casualness, semantic adequacy is below `90%`, or latency exceeds the `15%` ceiling. Ship the best prompt-only configuration rather than compressing an unvalidated model into the week-3 launch.

## Day-1 experiment

Create a 100-intent mini-eval across six languages. Compare the current prompt, a prompt-only casual variant, and a small rewriter applied after the same base-model outputs. Blind the Hindi/Kannada samples, measure casualness, semantic adequacy, and latency, and proceed to the 6,000-pair synthetic run only if prompt-only does not meet the target without violating the quality and latency constraints.

## Recommendation

Choose the small rewriter model path, starting with Hindi and Kannada only, because it is the only option that matches the reviewer bottleneck, stays within the GPU budget, avoids ongoing API cost, and still offers a credible path to better style consistency than prompt-only before launch.
