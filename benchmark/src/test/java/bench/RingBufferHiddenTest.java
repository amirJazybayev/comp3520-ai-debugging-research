package bench;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.NoSuchElementException;
import org.junit.jupiter.api.Test;

class RingBufferHiddenTest {
    @Test
    void manyWrapCyclesKeepFifoOrder() {
        RingBuffer buffer = new RingBuffer(2);
        for (int i = 0; i < 20; i++) {
            buffer.add(i);
            buffer.add(i + 100);
            assertEquals(i, buffer.remove());
            assertEquals(i + 100, buffer.remove());
        }
        assertEquals(0, buffer.size());
    }

    @Test
    void sizeTracksContents() {
        RingBuffer buffer = new RingBuffer(3);
        buffer.add(7);
        buffer.add(8);
        assertEquals(2, buffer.size());
        buffer.remove();
        assertEquals(1, buffer.size());
    }

    @Test
    void fullBufferRejectsAdd() {
        RingBuffer buffer = new RingBuffer(1);
        buffer.add(1);
        assertThrows(IllegalStateException.class, () -> buffer.add(2));
    }

    @Test
    void emptyBufferRejectsRemove() {
        RingBuffer buffer = new RingBuffer(2);
        assertThrows(NoSuchElementException.class, buffer::remove);
    }

    @Test
    void invalidCapacityRejected() {
        assertThrows(IllegalArgumentException.class, () -> new RingBuffer(0));
    }
}
