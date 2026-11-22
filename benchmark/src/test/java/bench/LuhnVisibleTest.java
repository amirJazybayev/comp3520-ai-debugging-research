package bench;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class LuhnVisibleTest {
    @Test
    void validSixteenDigitNumber() {
        assertTrue(Luhn.isValid("4111111111111111"));
    }
}
