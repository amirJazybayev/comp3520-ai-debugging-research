package bench;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class TemperatureConverterVisibleTest {
    @Test
    void boilingPoint() {
        assertEquals(100.0, TemperatureConverter.fahrenheitToCelsius(212), 1e-9);
    }
}
