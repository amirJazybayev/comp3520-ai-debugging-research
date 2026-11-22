package bench;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class SemVerHiddenTest {
    @Test
    void equalVersions() {
        assertEquals(0, SemVer.compare("1.2.3", "1.2.3"));
        assertEquals(0, SemVer.compare("1.2", "1.2.0"));
        assertEquals(0, SemVer.compare("2", "2.0.0"));
    }

    @Test
    void numericOrdering() {
        assertTrue(SemVer.compare("2.0.0", "10.0.0") < 0);
        assertTrue(SemVer.compare("2.0.0", "1.99.99") > 0);
        assertTrue(SemVer.compare("0.0.1", "0.1") < 0);
        assertTrue(SemVer.compare("1.0.10", "1.0.9") > 0);
    }

    @Test
    void invalidVersionsRejected() {
        assertThrows(IllegalArgumentException.class, () -> SemVer.compare("1.x", "1.0"));
        assertThrows(IllegalArgumentException.class, () -> SemVer.compare("", "1.0"));
        assertThrows(IllegalArgumentException.class, () -> SemVer.compare("1.0", null));
        assertThrows(IllegalArgumentException.class, () -> SemVer.compare("1.2.3.4", "1.0"));
    }
}
