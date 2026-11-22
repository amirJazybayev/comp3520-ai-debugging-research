package bench;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class TemperatureConverterHiddenTest {
    @Test
    void knownPoints() {
        assertEquals(0.0, TemperatureConverter.fahrenheitToCelsius(32), 1e-9);
        assertEquals(-40.0, TemperatureConverter.fahrenheitToCelsius(-40), 1e-9);
        assertEquals(37.0, TemperatureConverter.fahrenheitToCelsius(98.6), 1e-9);
    }

    @Test
    void roundTrip() {
        for (double c = -50; c <= 150; c += 12.5) {
            assertEquals(c, TemperatureConverter.fahrenheitToCelsius(TemperatureConverter.celsiusToFahrenheit(c)), 1e-9);
        }
    }

    @Test
    void reverseConversionUnchanged() {
        assertEquals(212.0, TemperatureConverter.celsiusToFahrenheit(100), 1e-9);
    }

    @Test
    void belowAbsoluteZeroRejected() {
        assertThrows(IllegalArgumentException.class, () -> TemperatureConverter.fahrenheitToCelsius(-500));
    }
}
