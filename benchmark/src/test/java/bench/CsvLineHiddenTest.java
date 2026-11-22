package bench;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;
import org.junit.jupiter.api.Test;

class CsvLineHiddenTest {
    @Test
    void onlyCommas() {
        assertEquals(List.of("", "", ""), CsvLine.split(",,"));
    }

    @Test
    void emptyLineIsOneEmptyField() {
        assertEquals(List.of(""), CsvLine.split(""));
    }

    @Test
    void innerAndLeadingEmptyFields() {
        assertEquals(List.of("a", "", "b"), CsvLine.split("a,,b"));
        assertEquals(List.of("", "x"), CsvLine.split(",x"));
    }

    @Test
    void whitespaceIsPreserved() {
        assertEquals(List.of(" a ", " b "), CsvLine.split(" a , b "));
    }

    @Test
    void nullRejected() {
        assertThrows(IllegalArgumentException.class, () -> CsvLine.split(null));
    }
}
