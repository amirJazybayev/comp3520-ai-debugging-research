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
        if (text == null || text.isEmpty()) {
            return 0;
        }
        return text.split("\\s+").length;
    }
}
