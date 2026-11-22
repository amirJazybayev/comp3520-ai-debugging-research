package bench;

/** Converts between Fahrenheit and Celsius. */
public final class TemperatureConverter {
    private static final double ABSOLUTE_ZERO_F = -459.67;

    private TemperatureConverter() {
    }

    /**
     * Converts degrees Fahrenheit to degrees Celsius.
     *
     * @throws IllegalArgumentException if {@code fahrenheit} is below absolute zero (-459.67 F)
     */
    public static double fahrenheitToCelsius(double fahrenheit) {
        if (fahrenheit < ABSOLUTE_ZERO_F) {
            throw new IllegalArgumentException("below absolute zero");
        }
        return (fahrenheit - 32) * 5 / 9.0;
    }

    /** Converts degrees Celsius to degrees Fahrenheit. */
    public static double celsiusToFahrenheit(double celsius) {
        return celsius * 9 / 5 + 32;
    }
}
