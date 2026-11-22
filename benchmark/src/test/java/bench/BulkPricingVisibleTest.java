package bench;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class BulkPricingVisibleTest {
    @Test
    void tenItemsGetTheBulkDiscount() {
        assertEquals(900, BulkPricing.total(100, 10));
    }
}
