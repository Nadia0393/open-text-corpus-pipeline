# Decisions

## Silver quality filter thresholds

These are starting values, not measured cutoffs. I'll check each one against a sample of real documents before trusting it.

- **Length, 200 to 100,000 characters.** Documents under 200 characters are usually stubs or redirects with little usable text. Documents over 100,000 are rare in encyclopedia articles and often lists or tables that behave differently from prose.
- **Non-alphanumeric ratio, at most 0.3.** Prose is mostly letters, digits, and spaces. Menus, code fragments, and garbled text have a high share of symbols. The 0.3 cutoff is a guess that needs a hand review of borderline documents.
- **Repeated trigram fraction, at most 0.2.** A starting guess. Short texts under three words count as having no repeats, so the length filter handles them.

## Exact dedup

- Dedup hashes normalized text, not raw text, so whitespace and encoding variants count as duplicates.
- The kept row is the lowest `doc_id`, so reruns keep the same copy.
- Null text is dropped before dedup, since nulls would collapse into one row.