package bench;

import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class InventoryVisibleTest {
    @Test
    void removingMoreThanStockedFails() {
        Inventory inventory = new Inventory();
        inventory.add("APPLE", 5);
        assertThrows(IllegalStateException.class, () -> inventory.remove("APPLE", 7));
    }
}
