package bench;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class RateLimiterVisibleTest {
    @Test
    void allowanceIsRestoredInNextWindow() {
        RateLimiter limiter = new RateLimiter(2, 1000);
        assertTrue(limiter.tryAcquire(0));
        assertTrue(limiter.tryAcquire(1));
        assertFalse(limiter.tryAcquire(2));
        assertTrue(limiter.tryAcquire(1000));
    }
}
