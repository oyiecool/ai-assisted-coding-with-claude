# count_words — Chapter 15, section 15.7, and scenario 12

The learner's word counter that returned 0 for every file, and the fix
found by tracing the loop by hand.

**Try it first.** Read `count_words_buggy` and trace it on a two-line file
whose last line is empty. What is `words` after the loop? Where is `count`
set? Then read `count_words`.

```bash
pytest examples/ch15-count-words
```

The last test shows the buggy version failing the two cases the tutor asked
for: a file whose last line is empty, and a file with several lines.
