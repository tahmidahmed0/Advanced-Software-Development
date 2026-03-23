import unittest
from models.lease import Lease
from models.payment import Payment

class TestPaymentLogic(unittest.TestCase):
    def test_early_exit_penalty(self):
        lease = Lease(None, 1, 1, "2026-01-01", "2026-12-31", 1000, 1200)
        self.assertEqual(lease.calculate_early_exit_penalty(), 60.0)

    def test_payment_is_late(self):
        payment = Payment(None, 1, 1, 1200, "2026-03-01", None, "Pending")
        self.assertTrue(payment.is_late("2026-03-10"))

if __name__ == "__main__":
    unittest.main()
