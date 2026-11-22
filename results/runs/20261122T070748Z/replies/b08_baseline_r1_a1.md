```java
package bench;

/** Validates user passwords against the account policy. */
public final class PasswordPolicy {
    private PasswordPolicy() {
    }

    /**
     * Returns {@code true} if {@code password} is non-null, at least 8 characters long, and
     * contains at least one digit and at least one uppercase letter.
     */
    public static boolean isValid(String password) {
        if (password == null || password.length() < 8) {
            return false;
        }
        boolean hasDigit = false;
        boolean hasUpper = false;
        for (char c : password.toCharArray()) {
            if (Character.isDigit(c)) {
                hasDigit = true;
            }
            if (Character.isUpperCase(c)) {
                hasUpper = true;
            }
        }
        return hasDigit && hasUpper;
    }
}
```