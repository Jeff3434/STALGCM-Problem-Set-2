# Regex Used

These are the regex replacements used in the notebook for the cleaned output files.

1. `re.sub(r'\s+([.,;:!?])', r'\1', text)`
   - Removes spaces before punctuation marks like `.`, `,`, `;`, `:`, `!`, and `?`.

2. `re.sub(r'\(\s+', '(', text)`
   - Removes extra spaces right after an opening parenthesis.

3. `re.sub(r'\s+\)', ')', text)`
   - Removes extra spaces right before a closing parenthesis.
