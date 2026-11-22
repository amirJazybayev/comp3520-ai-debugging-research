package bench;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class PaginationVisibleTest {
    @Test
    void partialLastPageCountsAsAPage() {
        assertEquals(3, Pagination.pageCount(11, 5));
    }
}
