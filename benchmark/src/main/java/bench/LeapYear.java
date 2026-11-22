package bench;

/** Gregorian calendar helpers. */
public final class LeapYear {
    private LeapYear() {
    }

    /**
     * Returns {@code true} if {@code year} is a leap year in the Gregorian calendar: divisible by 4,
     * except years divisible by 100, which are leap years only if also divisible by 400.
     *
     * @throws IllegalArgumentException if {@code year} is less than 1
     */
    public static boolean isLeap(int year) {
        if (year < 1) {
            throw new IllegalArgumentException("year must be positive");
        }
        return (year % 4 == 0 && year % 100 != 0) || year % 400 == 0;
    }
}
