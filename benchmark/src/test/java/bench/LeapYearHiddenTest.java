package bench;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class LeapYearHiddenTest {
    @Test
    void centuriesDivisibleBy400AreLeap() {
        assertTrue(LeapYear.isLeap(1600));
        assertTrue(LeapYear.isLeap(2400));
    }

    @Test
    void otherCenturiesAreNotLeap() {
        assertFalse(LeapYear.isLeap(1900));
        assertFalse(LeapYear.isLeap(2100));
    }

    @Test
    void ordinaryYears() {
        assertTrue(LeapYear.isLeap(2024));
        assertFalse(LeapYear.isLeap(2023));
        assertTrue(LeapYear.isLeap(4));
    }

    @Test
    void nonPositiveYearsRejected() {
        assertThrows(IllegalArgumentException.class, () -> LeapYear.isLeap(0));
    }
}
