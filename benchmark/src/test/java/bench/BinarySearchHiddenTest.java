package bench;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class BinarySearchHiddenTest {
    private static final int[] DATA = {2, 4, 6, 8, 10, 12};

    @Test
    void findsEveryElement() {
        for (int i = 0; i < DATA.length; i++) {
            assertEquals(i, BinarySearch.indexOf(DATA, DATA[i]));
        }
    }

    @Test
    void singleElementArray() {
        assertEquals(0, BinarySearch.indexOf(new int[] {5}, 5));
        assertEquals(-1, BinarySearch.indexOf(new int[] {5}, 6));
    }

    @Test
    void missingKeys() {
        assertEquals(-1, BinarySearch.indexOf(DATA, 1));
        assertEquals(-1, BinarySearch.indexOf(DATA, 7));
        assertEquals(-1, BinarySearch.indexOf(DATA, 13));
        assertEquals(-1, BinarySearch.indexOf(new int[0], 1));
    }

    @Test
    void nullRejected() {
        assertThrows(IllegalArgumentException.class, () -> BinarySearch.indexOf(null, 1));
    }
}
