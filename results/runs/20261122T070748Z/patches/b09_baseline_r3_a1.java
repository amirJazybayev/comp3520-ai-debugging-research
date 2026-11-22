package bench;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.Set;
import java.util.TreeSet;

/** Tracks stock levels per SKU. */
public final class Inventory {
    private final Map<String, Integer> stock = new HashMap<>();

    /**
     * Adds {@code qty} units of {@code sku}.
     *
     * @throws IllegalArgumentException if {@code sku} is null or {@code qty} is not positive
     */
    public void add(String sku, int qty) {
        if (sku == null || qty <= 0) {
            throw new IllegalArgumentException("invalid arguments");
        }
        stock.merge(sku, qty, Integer::sum);
    }

    /**
     * Removes {@code qty} units of {@code sku}. When the stock of a SKU reaches zero it is no
     * longer listed by {@link #skus()}.
     *
     * @throws IllegalArgumentException if {@code qty} is not positive
     * @throws NoSuchElementException if {@code sku} is not stocked
     * @throws IllegalStateException if fewer than {@code qty} units are in stock; the stock is
     *     left unchanged in that case
     */
    public void remove(String sku, int qty) {
        if (qty <= 0) {
            throw new IllegalArgumentException("qty must be positive");
        }
        Integer current = stock.get(sku);
        if (current == null) {
            throw new NoSuchElementException(sku);
        }
        if (current < qty) {
            throw new IllegalStateException("insufficient stock");
        }
        if (current == qty) {
            stock.remove(sku);
        } else {
            stock.put(sku, current - qty);
        }
    }

    /** Returns the units in stock for {@code sku}, or 0 if it is not stocked. */
    public int quantity(String sku) {
        return stock.getOrDefault(sku, 0);
    }

    /** Returns the stocked SKUs in ascending order. */
    public Set<String> skus() {
        return Collections.unmodifiableSet(new TreeSet<>(stock.keySet()));
    }
}
