package bench;

/** Small string helpers. */
public final class TextUtils {
    private TextUtils() {
    }

    /**
     * Returns {@code true} if {@code s} is {@code null}, empty, or contains only whitespace
     * characters as defined by {@link Character#isWhitespace(char)}.
     */
    public static boolean isBlank(String s) {
        if (s == null) {
            return true;
        }
        return s.trim().isEmpty();
    }
}
