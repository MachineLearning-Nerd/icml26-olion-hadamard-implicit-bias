# Claim 1 output — exact diagonal algorithm toy

This directory records a deliberately narrow check of the sign-after-orthogonalization path in Algorithm 1 of the OLion paper.

The fixture uses a diagonal gradient (3, -2), zero momentum coefficients, learning rate 0.1, gamma 1, zero weight decay, and x0 = (1, -1). The exact diagonal polar factor is Q = (1, -1); entrywise Sign(Q) is unchanged; and the resulting update is x1 = (0.9, -0.9).

The verdict is toy. These values verify the operation order and arithmetic for this special case only. They do not reproduce GPT-2/Llama training, norm figures, or the convergence theorem.

Files:

- results.json: intermediate values and final update.
- summary.json: scoped verdict and boolean checks.
- SHA256SUMS: checksums for the two evidence files.
