package bench;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/** Splits simple (unquoted) CSV lines. */
public final class CsvLine {
    private CsvLine() {
    }

    /**
     * Splits {@code line} at every comma and returns the fields in order. Fields are not trimmed
     * and empty fields, including leading and trailing ones, are preserved, so a line with k
     * commas always yields k + 1 fields. Quoting is not supported.
     *
     * @throws IllegalArgumentException if {@code line} is null
     */
    public static List<String> split(String line) {
        if (line == null) {
            throw new IllegalArgumentException("line is null");
        }
        // Use -1 as the limit to preserve trailing empty strings
        return new ArrayList<>(Arrays.asList(line.split(",", -1)));
    }
}
