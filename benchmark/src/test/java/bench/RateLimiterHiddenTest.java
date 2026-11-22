package bench;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class RateLimiterHiddenTest {
    @Test
    void windowBoundaryIsExclusive() {
        RateLimiter limiter = new RateLimiter(1, 1000);
        assertTrue(limiter.tryAcquire(500));
        assertFalse(limiter.tryAcquire(1499));
        assertTrue(limiter.tryAcquire(1500));
    }

    @Test
    void fullAllowanceInEveryWindow() {
        RateLimiter limiter = new RateLimiter(3, 100);
        for (int window = 0; window < 5; window++) {
            long t = window * 100L;
            assertTrue(limiter.tryAcquire(t));
            assertTrue(limiter.tryAcquire(t + 1));
            assertTrue(limiter.tryAcquire(t + 2));
            assertFalse(limiter.tryAcquire(t + 3));
        }
    }

    @Test
    void newWindowStartsAtFirstRequestAfterExpiry() {
        RateLimiter limiter = new RateLimiter(1, 100);
        assertTrue(limiter.tryAcquire(0));
        assertTrue(limiter.tryAcquire(250));
        assertFalse(limiter.tryAcquire(349));
        assertTrue(limiter.tryAcquire(350));
    }

    @Test
    void invalidLimitsRejected() {
        assertThrows(IllegalArgumentException.class, () -> new RateLimiter(0, 100));
        assertThrows(IllegalArgumentException.class, () -> new RateLimiter(1, 0));
    }
}
