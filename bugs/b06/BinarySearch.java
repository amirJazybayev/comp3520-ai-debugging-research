package bench;

/** Searching in sorted arrays. */
public final class BinarySearch {
    private BinarySearch() {
    }

    /**
     * Returns an index of {@code key} in the ascending-sorted array {@code sorted}, or -1 if the
     * key is not present.
     *
     * @throws IllegalArgumentException if {@code sorted} is null
     */
    public static int indexOf(int[] sorted, int key) {
        if (sorted == null) {
            throw new IllegalArgumentException("array is null");
        }
        int low = 0;
        int high = sorted.length - 1;
        while (low < high) {
            int mid = (low + high) >>> 1;
            if (sorted[mid] < key) {
                low = mid + 1;
            } else if (sorted[mid] > key) {
                high = mid - 1;
            } else {
                return mid;
            }
        }
        return -1;
    }
}
