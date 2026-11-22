package bench;

/** Counts words in free text. */
public final class WordCounter {
    private WordCounter() {
    }

    /**
     * Returns the number of words in {@code text}, where a word is a maximal run of characters
     * that are not whitespace according to {@link Character#isWhitespace(char)}. A null text has
     * zero words.
     */
    public static int count(String text) {
        if (text == null) {
            return 0;
        }
        int words = 0;
        boolean inWord = false;
        for (int i = 0; i < text.length(); i++) {
            boolean space = Character.isWhitespace(text.charAt(i));
            if (!space && !inWord) {
                words++;
            }
            inWord = !space;
        }
        return words;
    }
}
