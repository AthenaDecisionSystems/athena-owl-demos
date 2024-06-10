package com.athena.insurance.claims.datamodel;

import com.athena.insurance.claims.datamodel.enums.ChannelType;
import org.junit.jupiter.api.Test;

import java.util.Calendar;
import java.util.GregorianCalendar;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class ClientTest {

    @Test
    void testCreateClient() {
        Calendar dateOfBirth_cal = new GregorianCalendar(2003,10,31);
        Calendar firstContractDate_cal = new GregorianCalendar(2023,11,10);

        Client client = new Client("Joe", "Smith", dateOfBirth_cal.getTime(), firstContractDate_cal.getTime(), 60, 450.0, ChannelType.email);
        assertEquals("Joe", client.getFirstName());
    }
}
