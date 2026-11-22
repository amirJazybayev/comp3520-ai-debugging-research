package bench;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class WordCounterVisibleTest {
    @Test
    void repeatedSpacesBetweenWords() {
        assertEquals(2, WordCounter.count("  hello   world "));
    }
}
