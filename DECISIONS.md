# Decisions

## Silver quality filter thresholds

These are starting values, not measured cutoffs. I'll check each one against a sample of real documents before trusting it.

- **Length, 200 to 100,000 characters.** Documents under 200 characters are usually stubs or redirects with little usable text. Documents over 100,000 are rare in encyclopedia articles and often lists or tables that behave differently from prose.
- **Non-alphanumeric ratio, at most 0.3.** Prose is mostly letters, digits, and spaces. Menus, code fragments, and garbled text have a high share of symbols. The 0.3 cutoff is a guess that needs a hand review of borderline documents.