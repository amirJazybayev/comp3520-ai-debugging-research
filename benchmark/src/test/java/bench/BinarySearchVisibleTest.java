package bench;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class BinarySearchVisibleTest {
    @Test
    void findsLastElement() {
        assertEquals(3, BinarySearch.indexOf(new int[] {1, 3, 5, 7}, 7));
    }
}
