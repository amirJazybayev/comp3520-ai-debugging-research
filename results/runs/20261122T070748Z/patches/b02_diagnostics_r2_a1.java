package bench;

/** Helpers for paginating result lists. */
public final class Pagination {
    private Pagination() {
    }

    /**
     * Returns the number of pages needed to show {@code totalItems} items with at most
     * {@code pageSize} items per page. Zero items need zero pages. Must work for every
     * non-negative {@code long} value without arithmetic overflow.
     *
     * @throws IllegalArgumentException if {@code totalItems} is negative or {@code pageSize} is not positive
     */
    public static long pageCount(long totalItems, int pageSize) {
        if (totalItems < 0 || pageSize <= 0) {
            throw new IllegalArgumentException("invalid arguments");
        }
        return (totalItems + pageSize - 1) / pageSize;
    }
}
