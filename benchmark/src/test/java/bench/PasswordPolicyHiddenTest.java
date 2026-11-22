package bench;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class PasswordPolicyHiddenTest {
    @Test
    void validPasswords() {
        assertTrue(PasswordPolicy.isValid("Abcdefg1"));
        assertTrue(PasswordPolicy.isValid("1234567X"));
    }

    @Test
    void missingDigitRejected() {
        assertFalse(PasswordPolicy.isValid("ABCDEFGH"));
        assertFalse(PasswordPolicy.isValid("Abcdefgh"));
    }

    @Test
    void missingUppercaseRejected() {
        assertFalse(PasswordPolicy.isValid("abcdefg1"));
    }

    @Test
    void tooShortOrNullRejected() {
        assertFalse(PasswordPolicy.isValid("Abc1"));
        assertFalse(PasswordPolicy.isValid("Abcdef1"));
        assertFalse(PasswordPolicy.isValid(null));
    }
}
