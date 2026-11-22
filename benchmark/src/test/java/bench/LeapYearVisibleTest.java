package bench;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class LeapYearVisibleTest {
    @Test
    void year2000IsLeap() {
        assertTrue(LeapYear.isLeap(2000));
    }
}
