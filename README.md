# Language Detector

This algorithm is an implementation made by José Angel Daza, based on the paper ["N-Gram-Based Text Categorization"](https://www.let.rug.nl/~vannoord/TextCat/textcat.pdf) by William B. Cavnar and John M. Trenkle (1994).

The script currently works only in Python3. To **run the script** just execute:
```javascript
python3 Main.py
```

This will automatically look for all the samples defined in LANGUAGE_SAMPLES inside the script, it will split the samples into Training and Testing, and run the test in a verbose way. Finally, it will ask the user if he/she wants to perform custom testings with the constructed models. Since training and testing are randomly chosen, each time the script is run the model will be slightly different, but the overall results are quite similar. Currently, the package includes: English, French, German, and Spanish.


**To avoid verbose output** you can disable Testing module, by changing the flag in *line 153*:

    TEST_ENABLED = False.

This will result in the training sample to be 100% of each language sample.


**Configuration Parameters** are inside the script *(lines 153 to 156)*. They can be tuned as desired, but the default values are supposed to be optimal. The parameters are:

1. TEST_ENABLED: defaults to True. Randomly splits each language sample into 80% training set and 20% testing set.

2. TOP_NGRAMS: defaults to 400. Is the limit of Top-N n-grams that will be used to evaluate distances. The rest of the n-grams are deprecated, since only the upper part of the n-gram frequency is useful for language detection purposes.

3. DEFAULT_PENALTY: defaults to 250. Is the "distance" assigned to any n-gram from a test string that is not present in the language profile of a language.

4. LANGUAGE_SAMPLES: contains the list of available modeled languages. It currently contains only 4 languages, for testing purposes, but any could be added to the list. Language samples are small, but enough to give decent results. Of course, **performance could be improved with bigger language samples**).
