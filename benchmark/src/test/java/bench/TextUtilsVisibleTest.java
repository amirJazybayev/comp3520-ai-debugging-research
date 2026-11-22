package bench;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class TextUtilsVisibleTest {
    @Test
    void nullIsBlank() {
        assertTrue(TextUtils.isBlank(null));
    }
}
