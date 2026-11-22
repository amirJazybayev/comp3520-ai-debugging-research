```java
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
        // Ceiling division: (totalItems + pageSize - 1) / pageSize
        // But we must avoid overflow. Since totalItems is non-negative long and pageSize is positive int,
        // totalItems + pageSize - 1 could overflow if totalItems is near Long.MAX_VALUE.
        // Instead, use: totalItems / pageSize + (totalItems % pageSize == 0 ? 0 : 1)
        long quotient = totalItems / pageSize;
        long remainder = totalItems % pageSize;
        return quotient + (remainder == 0 ? 0 : 1);
    }
}
```