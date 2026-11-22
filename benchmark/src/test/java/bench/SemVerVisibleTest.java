package bench;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class SemVerVisibleTest {
    @Test
    void minorVersionsCompareNumerically() {
        assertTrue(SemVer.compare("1.10.0", "1.9.0") > 0);
    }
}
