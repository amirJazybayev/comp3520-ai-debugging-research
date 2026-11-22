package bench;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.junit.jupiter.api.Test;

class StatisticsHiddenTest {
    @Test
    void evenCountAveragesMiddleValues() {
        assertEquals(2.5, Statistics.median(Arrays.asList(4, 1, 3, 2)), 1e-9);
    }

    @Test
    void singleValue() {
        assertEquals(7.0, Statistics.median(List.of(7)), 1e-9);
    }

    @Test
    void inputIsNotModified() {
        List<Integer> input = new ArrayList<>(Arrays.asList(5, 3, 9, 1));
        Statistics.median(input);
        assertEquals(Arrays.asList(5, 3, 9, 1), input);
    }

    @Test
    void unmodifiableInputIsAccepted() {
        assertEquals(3.0, Statistics.median(List.of(5, 1, 3)), 1e-9);
    }

    @Test
    void largeValuesDoNotOverflow() {
        assertEquals(Integer.MAX_VALUE, Statistics.median(List.of(Integer.MAX_VALUE, Integer.MAX_VALUE)), 1e-9);
    }

    @Test
    void emptyOrNullRejected() {
        assertThrows(IllegalArgumentException.class, () -> Statistics.median(List.of()));
        assertThrows(IllegalArgumentException.class, () -> Statistics.median(null));
    }
}
