package bench;

/** Compares dotted numeric version strings such as "1.10.2". */
public final class SemVer {
    private SemVer() {
    }

    /**
     * Compares versions of the form {@code MAJOR[.MINOR[.PATCH]]} numerically, component by
     * component. Missing components count as 0, so "1.2" equals "1.2.0". Returns a negative
     * number, zero, or a positive number as {@code a} is lower than, equal to, or higher than
     * {@code b}.
     *
     * @throws IllegalArgumentException if either version is null, empty, has more than three
     *     components, or has a component that is not a non-negative integer
     */
    public static int compare(String a, String b) {
        int[] pa = parse(a);
        int[] pb = parse(b);
        for (int i = 0; i < 3; i++) {
            if (pa[i] < pb[i]) {
                return -1;
            }
            if (pa[i] > pb[i]) {
                return 1;
            }
        }
        return 0;
    }

    private static int[] parse(String version) {
        if (version == null || version.isEmpty()) {
            throw new IllegalArgumentException("empty version");
        }
        String[] parts = version.split("\\.", -1);
        if (parts.length > 3) {
            throw new IllegalArgumentException("too many components: " + version);
        }
        int[] result = new int[3];
        for (int i = 0; i < parts.length; i++) {
            if (!parts[i].matches("\\d+")) {
                throw new IllegalArgumentException("bad component: " + version);
            }
            result[i] = Integer.parseInt(parts[i]);
        }
        return result;
    }
}
