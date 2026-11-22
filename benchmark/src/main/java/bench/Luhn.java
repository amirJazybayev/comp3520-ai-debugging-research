package bench;

/** Luhn (mod 10) checksum used by payment card numbers. */
public final class Luhn {
    private Luhn() {
    }

    /**
     * Returns {@code true} if {@code digits} passes the Luhn check: starting from the rightmost
     * digit (the check digit) and moving left, every second digit is doubled (subtracting 9 if
     * the result exceeds 9), and the sum of all resulting digits must be divisible by 10.
     *
     * @throws IllegalArgumentException if {@code digits} is null, empty, or contains a non-digit
     */
    public static boolean isValid(String digits) {
        if (digits == null || digits.isEmpty()) {
            throw new IllegalArgumentException("no digits");
        }
        int sum = 0;
        int n = digits.length();
        for (int i = 0; i < n; i++) {
            char c = digits.charAt(n - 1 - i);
            if (c < '0' || c > '9') {
                throw new IllegalArgumentException("not a digit: " + c);
            }
            int d = c - '0';
            if (i % 2 == 1) {
                d *= 2;
                if (d > 9) {
                    d -= 9;
                }
            }
            sum += d;
        }
        return sum % 10 == 0;
    }
}
