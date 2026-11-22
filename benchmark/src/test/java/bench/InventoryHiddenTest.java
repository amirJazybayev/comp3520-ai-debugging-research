package bench;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.NoSuchElementException;
import java.util.Set;
import org.junit.jupiter.api.Test;

class InventoryHiddenTest {
    @Test
    void failedRemovalLeavesStockUnchanged() {
        Inventory inventory = new Inventory();
        inventory.add("APPLE", 5);
        assertThrows(IllegalStateException.class, () -> inventory.remove("APPLE", 6));
        assertEquals(5, inventory.quantity("APPLE"));
        assertEquals(Set.of("APPLE"), inventory.skus());
    }

    @Test
    void removingAllUnitsDelistsSku() {
        Inventory inventory = new Inventory();
        inventory.add("APPLE", 3);
        inventory.add("PEAR", 1);
        inventory.remove("APPLE", 3);
        assertEquals(0, inventory.quantity("APPLE"));
        assertEquals(Set.of("PEAR"), inventory.skus());
    }

    @Test
    void partialRemoval() {
        Inventory inventory = new Inventory();
        inventory.add("APPLE", 3);
        inventory.add("APPLE", 2);
        inventory.remove("APPLE", 4);
        assertEquals(1, inventory.quantity("APPLE"));
    }

    @Test
    void invalidRemovals() {
        Inventory inventory = new Inventory();
        inventory.add("APPLE", 3);
        assertThrows(NoSuchElementException.class, () -> inventory.remove("KIWI", 1));
        assertThrows(IllegalArgumentException.class, () -> inventory.remove("APPLE", 0));
    }
}
