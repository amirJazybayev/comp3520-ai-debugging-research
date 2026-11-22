```java
package bench;

import java.util.NoSuchElementException;

/** A fixed-capacity first-in-first-out queue of ints backed by a circular array. */
public final class RingBuffer {
    private final int[] items;
    private int head;
    private int size;

    /** @throws IllegalArgumentException if {@code capacity} is not positive */
    public RingBuffer(int capacity) {
        if (capacity <= 0) {
            throw new IllegalArgumentException("capacity must be positive");
        }
        items = new int[capacity];
    }

    /**
     * Appends {@code value} at the tail.
     *
     * @throws IllegalStateException if the buffer is full
     */
    public void add(int value) {
        if (size == items.length) {
            throw new IllegalStateException("buffer full");
        }
        int tail = (head + size) % items.length;
        items[tail] = value;
        size++;
    }

    /**
     * Removes and returns the oldest value.
     *
     * @throws NoSuchElementException if the buffer is empty
     */
    public int remove() {
        if (size == 0) {
            throw new NoSuchElementException("buffer empty");
        }
        int value = items[head];
        head = (head + 1) % items.length;
        size--;
        return value;
    }

    /** Returns the number of stored values. */
    public int size() {
        return size;
    }
}
```