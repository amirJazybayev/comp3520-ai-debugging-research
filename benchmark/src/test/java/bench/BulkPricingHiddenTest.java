package bench;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class BulkPricingHiddenTest {
    @Test
    void belowThresholdHasNoDiscount() {
        assertEquals(900, BulkPricing.total(100, 9));
        assertEquals(500, BulkPricing.total(100, 5));
    }

    @Test
    void atAndAboveThresholdIsDiscounted() {
        assertEquals(900, BulkPricing.total(100, 10));
        assertEquals(990, BulkPricing.total(100, 11));
    }

    @Test
    void discountRoundsDown() {
        assertEquals(297, BulkPricing.total(33, 10));
        assertEquals(9, BulkPricing.total(1, 10));
    }

    @Test
    void zeroValues() {
        assertEquals(0, BulkPricing.total(0, 50));
        assertEquals(0, BulkPricing.total(100, 0));
    }

    @Test
    void negativeInputsRejected() {
        assertThrows(IllegalArgumentException.class, () -> BulkPricing.total(-1, 3));
        assertThrows(IllegalArgumentException.class, () -> BulkPricing.total(100, -3));
    }
}
