Problem Set 2: Text Cleaning

Tasks
Using Wikipedia articles and their associated references as the source of data, each group shall complete the following tasks:

1. Retrieval. Retrieve the target Wikipedia articles and their associated references using any appropriate method, such as copy-and-paste, downloading the source file, or using a software application.
   - 2016 Philippine Presidential Election: https://en.wikipedia.org/wiki/2016_Philippine_presidential_election
   - 2022 Philippine Presidential Election: https://en.wikipedia.org/wiki/2022_Philippine_presidential_election
2. Pre-processing. Remove document tags, unnecessary spaces, table text, formatting artifacts, and other unrelated keywords, symbols, or noise from the data. An example is shown below.

| Before                                  | After       |
| :-------------------------------------- | :---------- |
| 1. <indig>Kumain kami [edit][1]</indig> | Kumain kami |

3. Segmentation. Properly segment the text into sentences. An example is provided below.

| Before                                        | After                                            |
| :-------------------------------------------- | :----------------------------------------------- |
| Phrase 1: Phrase 2. Sentence 3.<br>Sentence 4 | Phrase 1: Phrase 2.<br>Sentence 3.<br>Sentence 4 |

4. Documentation. Document the entire process to ensure that each step can be replicated. The documentation must include the data source, the method used to retrieve the data, and a detailed description of the cleaning and segmentation procedures (in a separate XLSX file). Any use of AI tools or other external sources must be properly acknowledged, including the prompts used and the corresponding outputs.

| Step |  Search  | Replace | Mode / Remarks |        Explanation         |
| :--: | :------: | :-----: | :------------: | :------------------------: |
|  1   |    ^+    | <empty> |     Reg Ex     | Remove spaces at the start |
|  2   | \r\n\r\n |  \r\n   |    Extended    |  Remove unnecessary lines  |

AI Usage (disregard this part for now)
Provide a declaration of AI usage (per person)

1. AI tool(s) used
2. Describe briefly how you used the AI tool(s) in the completion of this assignment. Examples include idea generation, grammar checking, paraphrasing, summarizing references, formatting help, etc.
3. Extent of Use:
   a. Minimal – used only for grammar/spell check.
   b. Moderate – used for inspiration, then reworded significantly.
   c. Extensive – relied heavily on AI to generate portions of the work, with minimal changes.
4. In 2–3 sentences, reflect on how the use of AI contributed to your learning. If no AI was used, reflect on why you chose not to.
5. Prompts used and outputs.

Additional Notes

- We will be using Beautiful Soup for web scraping.
- The text within all references must be collected, as long as the site is accessible. Otherwise, the reference can be skipped.
