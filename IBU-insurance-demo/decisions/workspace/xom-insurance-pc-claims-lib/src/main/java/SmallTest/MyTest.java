package SmallTest;

import java.util.Calendar;
import java.util.GregorianCalendar;

import com.athena.insurance.claims.datamodel.Client;
import com.athena.insurance.claims.datamodel.enums.ChannelType;

public class MyTest {

	public static void main(String[] args) {
		
		Calendar dateOfBirth_cal = new GregorianCalendar(2001, 2, 11);
		Calendar firstContractDate_cal = new GregorianCalendar(2021, 2, 23);
		Client client = new Client("Joe", "Smith", dateOfBirth_cal.getTime(), firstContractDate_cal.getTime(), 70, 1200.0, ChannelType.email);
		
		
		System.out.println(client.getFirstName() + " was born on " + client.getDateOfBirth());

	}

}
