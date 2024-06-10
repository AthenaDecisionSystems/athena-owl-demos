package xom.utilities;

import static org.junit.jupiter.api.Assertions.*;

import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;

import org.junit.jupiter.api.Test;

class DateUtilsTest {

	@Test
	void test() {
		Calendar startCal = new GregorianCalendar(2024,3,5);
		Date startDate = startCal.getTime();

		Calendar endCal = new GregorianCalendar(2024,3,7);
		Date endDate = endCal.getTime();
		
		long duration = DateUtils.daysBetween(startDate, endDate);
		assertEquals(2, duration);
	}

}
