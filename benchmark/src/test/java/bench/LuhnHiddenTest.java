package bench;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class LuhnHiddenTest {
    @Test
    void validNumbersOfBothParities() {
        assertTrue(Luhn.isValid("79927398713"));
        assertTrue(Luhn.isValid("1234567812345670"));
        assertTrue(Luhn.isValid("18"));
        assertTrue(Luhn.isValid("0"));
    }

    @Test
    void invalidNumbers() {
        assertFalse(Luhn.isValid("79927398710"));
        assertFalse(Luhn.isValid("4111111111111112"));
        assertFalse(Luhn.isValid("19"));
    }

    @Test
    void malformedInputRejected() {
        assertThrows(IllegalArgumentException.class, () -> Luhn.isValid(null));
        assertThrows(IllegalArgumentException.class, () -> Luhn.isValid(""));
        assertThrows(IllegalArgumentException.class, () -> Luhn.isValid("12a4"));
    }
}
