package bench;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class TextUtilsHiddenTest {
    @Test
    void emptyAndWhitespaceAreBlank() {
        assertTrue(TextUtils.isBlank(null));
        assertTrue(TextUtils.isBlank(""));
        assertTrue(TextUtils.isBlank("   "));
        assertTrue(TextUtils.isBlank("\t\n\r"));
    }

    @Test
    void unicodeWhitespaceIsBlank() {
        assertTrue(TextUtils.isBlank("  "));
    }

    @Test
    void textIsNotBlank() {
        assertFalse(TextUtils.isBlank("a"));
        assertFalse(TextUtils.isBlank("  x  "));
    }
}
