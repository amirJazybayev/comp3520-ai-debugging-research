package bench;

import static org.junit.jupiter.api.Assertions.assertFalse;

import org.junit.jupiter.api.Test;

class PasswordPolicyVisibleTest {
    @Test
    void passwordWithoutUppercaseIsRejected() {
        assertFalse(PasswordPolicy.isValid("abcdefgh1"));
    }
}
