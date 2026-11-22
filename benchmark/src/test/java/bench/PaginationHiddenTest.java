package bench;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class PaginationHiddenTest {
    @Test
    void exactMultiples() {
        assertEquals(2, Pagination.pageCount(10, 5));
        assertEquals(5, Pagination.pageCount(5, 1));
    }

    @Test
    void smallCounts() {
        assertEquals(0, Pagination.pageCount(0, 5));
        assertEquals(1, Pagination.pageCount(1, 5));
        assertEquals(1, Pagination.pageCount(4, 5));
    }

    @Test
    void noOverflowForHugeTotals() {
        assertEquals(4611686018427387904L, Pagination.pageCount(Long.MAX_VALUE, 2));
        assertEquals(Long.MAX_VALUE, Pagination.pageCount(Long.MAX_VALUE, 1));
    }

    @Test
    void invalidArgumentsRejected() {
        assertThrows(IllegalArgumentException.class, () -> Pagination.pageCount(10, 0));
        assertThrows(IllegalArgumentException.class, () -> Pagination.pageCount(-1, 5));
    }
}
