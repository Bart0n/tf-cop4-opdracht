import unittest
import os
from coolstuf import checkvalidip
from coolstuf import ports
from coolstuf import log_handler
from coolstuf import database
from coolstuf import tcp_connect
from coolstuf import tcp_syn
from coolstuf import tcp_xmas
from coolstuf import udp
from coolstuf import banner


# Call test_progam.py --buffer to suppress the print statements!
class Tests(unittest.TestCase):
    def test_checkvalidip(self):
        """Checks IP address. Any valid IP returns a True, any non-valid returns a False."""
        # [0] Returns False or True, [1] Returns the error in case of a non-valid IP
        self.assertEqual(
            checkvalidip.check_ip("192.168.1.1")[0],
            True
        )
        self.assertEqual(
            checkvalidip.check_ip("192.168.0.a")[0],
            False
        )

    def test_ports(self):
        """Checks different port ranges, single port, some random ports and a range of ports,
        these should return a nice formatted list of the ports. Any non-valid ports should return a false."""
        self.assertEqual(
            ports.port_format("80-90"),
            [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90]
        )
        self.assertEqual(
            ports.port_format("22,23,25,27"),
            [22, 23, 25, 27]
        )
        self.assertEqual(
            ports.port_format("8080"),
            [8080]
        )
        self.assertFalse(
            ports.port_format("asdf-80")[0],
        )

    def test_writeoutput(self):
        """"Writes output to test.json and test.xml, that should return a True.
        Any non-valid input should return false"""
        # cse = Checked Somewhere Else :)
        self.assertTrue(
            log_handler.write_output("cse", "cse", "cse", "cse", "cse", "cse", "cse", "test_program.json", "json")[0],
        )
        self.assertTrue(
            log_handler.write_output("cse", "cse", "cse", "cse", "cse", "cse", "cse", "test_program.xml", "xml"[0]),
        )
        self.assertFalse(
            log_handler.write_output("cse", "cse", "cse", "cse", "cse", "cse", "cse", "fake insert", "crazy output")[0],
        )

    def test_database(self):
        """"Checks database module"""
        db = database.create_connection("test_program_write.sqlite3")

        # Create database connection
        self.assertIsNotNone(
            database.create_connection("test_program.sqlite3")
        )

        # Create database tables
        self.assertTrue(
            database.create_table(db)
        )

        # Insert data in database
        self.assertIsNotNone(
            database.insert_data(db, "01-01-1990", "8.7.6.5", "tcp-sinterklaas", "0,-1", "1", "2")
        )

        # Close the database before we can remove it
        db.close()
        # Remove database (should return True)
        self.assertTrue(
            database.delete_db("test_program_write.sqlite3")[0]
        )

        # Remove non-existing database (should return False)
        self.assertFalse(
            database.delete_db("fake_test_db.phplite666")[0]
        )

    def test_banner(self):
        """"This should generate the awesome TF-COP4 banner"""
        self.assertIsNotNone(banner.banner())

    def test_tcp_connect_scans(self):
        """"It checks for port 1 on the localhost (127.0.0.1) with the assumption that it is closed.
        Second and third check is port 53 and 478 on Google DNS, if there is no internet, this test will fail!
        """
        # TCP Connect Scan
        self.assertEqual(
            tcp_connect.tcp_connect_scan("127.0.0.1", [1], 1, 0),
            ('[-] Port [1] closed', 0, [1])
        )
        self.assertEqual(
            tcp_connect.tcp_connect_scan("8.8.8.8", [53], 1, 0),
            ('[+] Port [53] open', 1, [53])
        )
        self.assertEqual(
            tcp_connect.tcp_connect_scan("8.8.8.8", [478], 1, 0),
            ('[-] Port [478] closed', 0, [478])
        )

    def test_tcp_syn_scans(self):
        """"It checks for port 1 on the localhost (127.0.0.1) with the assumption that it is closed.
        Second and third check is port 53 and 478 on Google DNS, if there is no internet, this test will fail!
        """
        # TCP SYN Scan
        self.assertEqual(
            tcp_syn.tcp_syn_scan("127.0.0.1", [1], 1, 0),
            ('[-] Port [1] closed', 0, [1])
        )
        self.assertEqual(
            tcp_syn.tcp_syn_scan("8.8.8.8", [53], 1, 0),
            ('[+] Port [53] open', 1, [53])
        )

        self.assertEqual(
            tcp_syn.tcp_syn_scan("8.8.8.8", [478], 1, 0),
            ('[-] Port [478] closed', 0, [478])
        )

    def test_udp_scans(self):
        """"It checks for port 1 on the localhost (127.0.0.1) with the assumption that it is closed.
        Second and third check is port 53 and 478 on Google DNS, if there is no internet, this test will fail!
        """
        # UDP Scan
        self.assertEqual(
            udp.udp_scan("127.0.0.1", [1], 1, 0),
            ('[-] Port [1] closed', 0, [1])
        )
        self.assertEqual(
            udp.udp_scan("8.8.8.8", [53], 1, 0),
            ('[+] Port [53] open or filtered', 1, [53])
        )
        self.assertEqual(
            udp.udp_scan("8.8.8.8", [478], 1, 0),
            ('[+] Port [478] open or filtered', 1, [478])
        )

    def test_xmas_scans(self):
        """"On my tests, not many website reacted with an SYN/ACK or ICMP unreachable to the XMAS scan.
        So we are just testing the localhost on this one.
        """
        # XMAS Scan
        self.assertEqual(
            tcp_xmas.tcp_xmas_scan("127.0.0.1", [1], 1, 0),
            ('[-] Port [1] closed', 0, [1])
        )

    def tearDown(self):
        """Removes the test JSON, XML and Database files that were created during testing"""
        files = ["test_program.json", "test_program.xml", "test_program.sqlite3"]
        for f in files:
            if os.path.isfile(f):
                os.remove(f)


if __name__ == '__main__':
    unittest.main()
