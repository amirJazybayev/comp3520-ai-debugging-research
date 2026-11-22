package bench;

/** Computes order totals with a bulk discount. */
public final class BulkPricing {
    private BulkPricing() {
    }

    /**
     * Returns the total price in cents for {@code quantity} items costing {@code unitCents} each.
     * Orders of 10 or more items receive a 10% discount; the discounted total is rounded down
     * to a whole cent.
     *
     * @throws IllegalArgumentException if {@code unitCents} or {@code quantity} is negative
     */
    public static long total(long unitCents, int quantity) {
        if (unitCents < 0 || quantity < 0) {
            throw new IllegalArgumentException("inputs must be non-negative");
        }
        long gross = unitCents * quantity;
        if (quantity >= 10) {
            return gross * 90 / 100;
        }
        return gross;
    }
}
