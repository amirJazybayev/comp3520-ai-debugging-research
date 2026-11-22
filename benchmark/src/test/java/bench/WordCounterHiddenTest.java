package bench;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class WordCounterHiddenTest {
    @Test
    void emptyInputs() {
        assertEquals(0, WordCounter.count(null));
        assertEquals(0, WordCounter.count(""));
        assertEquals(0, WordCounter.count("    "));
        assertEquals(0, WordCounter.count("\t\n"));
    }

    @Test
    void mixedWhitespace() {
        assertEquals(3, WordCounter.count("a\tb\nc"));
        assertEquals(2, WordCounter.count(" one two"));
    }

    @Test
    void simpleSentences() {
        assertEquals(1, WordCounter.count("one"));
        assertEquals(4, WordCounter.count("the quick brown fox"));
    }
}
