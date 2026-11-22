package bench;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.junit.jupiter.api.Test;

class CsvLineVisibleTest {
    @Test
    void trailingEmptyFieldIsKept() {
        assertEquals(List.of("a", "b", ""), CsvLine.split("a,b,"));
    }
}
