package bench;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.Arrays;
import org.junit.jupiter.api.Test;

class StatisticsVisibleTest {
    @Test
    void medianOfUnsortedOddList() {
        assertEquals(2.0, Statistics.median(Arrays.asList(3, 1, 2)), 1e-9);
    }
}
