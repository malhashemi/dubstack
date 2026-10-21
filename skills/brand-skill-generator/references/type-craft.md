# Type Craft

Typography should make the brand recognizable and its content easy to use. Preserve established faces; build the roles and usage around them. For new typography, choose from the brand's intent and actual reading conditions rather than a fixed list of favorites or banned fonts.

## Select and compare

Translate the desired character into useful visual dimensions:

| Dimension | What to examine |
|---|---|
| Structure | Serif, sans, slab, or mono; construction and historical associations |
| Temperature | Humanist, grotesque, geometric; warmth versus precision |
| Stroke contrast | Expressive contrast versus robust uniformity |
| Proportion | Width, x-height, spacing, and density |
| Terminals and curves | Sharpness, softness, rhythm, distinctive letterforms |
| Case and numerals | Brand-name shape, capitals, figures, technical content |

Treat associations as hypotheses to test with the audience and content. A familiar face can be the right choice; novelty is not a requirement. Add another family when it provides a useful role or contrast, not to satisfy a display/body/mono checklist.

Use real specimens: brand name, representative headline, paragraph, label, numbers, and the languages the brand uses. Compare plausible candidates under similar conditions. Check available weights, glyph coverage, licensing, loading, and how the face relates to the mark before committing.

## Define a system

Use a small, coherent hierarchy with named roles. A modular ratio can help generate a scale, but optical adjustments and different application needs may justify departures. Specify size, weight, leading, and tracking together; hierarchy also comes from spacing, color, and composition.

Separate reading and display needs where useful. Product interfaces may prioritize predictable density, while editorial or campaign work may need a larger or fluid display range. Provide a display token when the brand actually needs it; neither a giant hero nor fixed body sizing is universal.

For web reading, a body size around 1rem and a moderate line length are useful starting points. Inspect the actual font, content, zoom, device, and audience. Use relative units where they support adaptation, preserve zoom, and prevent clipping as text grows.

Check both dark and light use when supported. Perceived weight can change, but weight, tracking, or leading adjustments should follow inspection rather than a mandatory compensation formula. Track capitals only where the typeface and script benefit; Arabic and other joining scripts need script-aware treatment. Test RTL layout and fallback fonts explicitly when relevant.

## Package and verify

Record family names, roles, weights, fallback stacks, and usage rules. Include licensed font files when distribution permits, or document the acquisition/loading dependency and an intentional fallback. Font availability is part of the result, not an assumption.

Put `@font-face` declarations in the token import chain. URLs are relative to that stylesheet: a file in `tokens/` usually reaches kit fonts through `../assets/`. Choose variable or static files and loading behavior from the actual weights, payload, and layout needs.

The brand card supplies non-web sizes and units. Keep its family names and role values consistent with the CSS. Verify that the intended font really loaded before judging the specimen, and inspect hierarchy and sustained reading as well as the display sample.
