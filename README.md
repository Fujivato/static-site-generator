# Python Static Content Generator

## v1.0.0
Version 1 of the Static site generator is the output from following the course content on boot.dev. Some deliberate decisions were made to omit functionality from the markdown to html generation process whilst completing the project; namely:

- Converting square brackets to `<input type="checkbox" />` fields
- Supporting nested `<ul />`, `<ol />` and `<li />` elements
- Adding `<p>` tags around text elements

## Future Updates

1. Add support for nested lists
2. Convert square brackets to input elements
3. Adding logic to determine which free text elements to wrap in `<p>` tags
4. Additional Unit Test coverage
5. Improve logic for converting markdown into blocks