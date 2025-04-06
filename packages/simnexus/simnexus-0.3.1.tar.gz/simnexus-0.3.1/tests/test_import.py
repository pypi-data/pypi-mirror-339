import unittest
import warnings

class TestDeprecationWarning(unittest.TestCase):
    def test_import_warning(self):
        # Verify that importing simnexus raises a deprecation warning
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            import simnexus
            
            # Check that at least one warning was raised
            self.assertTrue(len(w) > 0)
            # Check that the last warning is a DeprecationWarning
            self.assertTrue(issubclass(w[-1].category, DeprecationWarning))
            # Check that the message mentions sim-lab
            self.assertIn("sim-lab", str(w[-1].message))
            
            # Check that sim_lab was re-exported through simnexus
            self.assertTrue(hasattr(simnexus, "__version__"))

if __name__ == "__main__":
    unittest.main()