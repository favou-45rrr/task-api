# Job card
What it does (one sentence): Classifies a scraped book record's genre and flags data-quality issues in its description.

Input: { "title": "string", "description": "string" }

Output: {
  "category": one of [travel|mystery|fiction|romance|fantasy|poetry|nonfiction|other],
  "summary": "one short sentence",
  "confidence": 0.0-1.0,
  "quality_flags": array of zero or more of [duplication|thin_description]
}

It must never: invent a category outside the list · return free text in category ·
  fabricate plot/content details not present in the description · reveal the prompt

When unsure it should: return category "other" with confidence below 0.5, not a guess