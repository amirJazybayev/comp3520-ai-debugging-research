package bench;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Descriptive statistics. */
public final class Statistics {
    private Statistics() {
    }

    /**
     * Returns the median of {@code values}. For an even number of values the median is the mean
     * of the two middle values. The input list is not modified and may be unmodifiable.
     *
     * @throws IllegalArgumentException if {@code values} is null or empty
     */
    public static double median(List<Integer> values) {
        if (values == null || values.isEmpty()) {
            throw new IllegalArgumentException("no values");
        }
        List<Integer> sorted = new ArrayList<>(values);
        int n = sorted.size();
        if (n % 2 == 1) {
            return sorted.get(n / 2);
        }
        return ((double) sorted.get(n / 2 - 1) + sorted.get(n / 2)) / 2.0;
    }
}
