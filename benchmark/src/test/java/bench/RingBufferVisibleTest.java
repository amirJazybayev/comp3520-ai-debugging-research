package bench;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class RingBufferVisibleTest {
    @Test
    void wrapsAroundAfterRemoval() {
        RingBuffer buffer = new RingBuffer(3);
        buffer.add(1);
        buffer.add(2);
        buffer.add(3);
        assertEquals(1, buffer.remove());
        buffer.add(4);
        assertEquals(2, buffer.remove());
        assertEquals(3, buffer.remove());
        assertEquals(4, buffer.remove());
    }
}
