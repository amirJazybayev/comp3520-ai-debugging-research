package bench;

/** Fixed-window rate limiter. */
public final class RateLimiter {
    private final int maxRequests;
    private final long windowMillis;
    private boolean started;
    private long windowStart;
    private int count;

    /**
     * Allows at most {@code maxRequests} requests per window of {@code windowMillis} milliseconds.
     *
     * @throws IllegalArgumentException if either argument is not positive
     */
    public RateLimiter(int maxRequests, long windowMillis) {
        if (maxRequests <= 0 || windowMillis <= 0) {
            throw new IllegalArgumentException("limits must be positive");
        }
        this.maxRequests = maxRequests;
        this.windowMillis = windowMillis;
    }

    /**
     * Returns {@code true} if a request at time {@code nowMillis} is allowed. The first request
     * starts a window covering {@code [start, start + windowMillis)}; a request at or after the
     * end of the current window starts a new window with a fresh allowance. Timestamps passed to
     * successive calls never decrease.
     */
    public boolean tryAcquire(long nowMillis) {
        if (!started || nowMillis - windowStart >= windowMillis) {
            started = true;
            windowStart = nowMillis;
            count = 0;
        }
        if (count < maxRequests) {
            count++;
            return true;
        }
        return false;
    }
}
