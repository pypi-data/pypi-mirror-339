import unittest
from WordToNumber import word_to_num

class TestWordToNumExtended(unittest.TestCase):
    """Extended test cases for word_to_num function."""
    
    def test_alternative_wording(self):
        """Test alternative ways to express numbers."""
        self.assertEqual(word_to_num("a hundred"), 100)
        self.assertEqual(word_to_num("a thousand"), 1000)
        self.assertEqual(word_to_num("half a million"), 500000)
        self.assertEqual(word_to_num("a dozen"), 12)
        self.assertEqual(word_to_num("three score"), 60)
        self.assertEqual(word_to_num("four score and seven"), 87)
        self.assertEqual(word_to_num("one hundred and one"), 101)
        self.assertEqual(word_to_num("one thousand and one"), 1001)
    
    def test_ordinal_numbers(self):
        """Test ordinal number words."""
        self.assertEqual(word_to_num("first"), 1)
        self.assertEqual(word_to_num("twenty second"), 22)
        self.assertEqual(word_to_num("ninety ninth"), 99)
        self.assertEqual(word_to_num("one hundredth"), 100)
        self.assertEqual(word_to_num("three hundred and forty fifth"), 345)
        self.assertEqual(word_to_num("one thousandth"), 1000)
        self.assertEqual(word_to_num("millionth"), 1000000)
    
    def test_negative_numbers(self):
        """Test negative number words."""
        self.assertEqual(word_to_num("negative one"), -1)
        self.assertEqual(word_to_num("minus twenty"), -20)
        self.assertEqual(word_to_num("negative one hundred and fifty"), -150)
        self.assertEqual(word_to_num("minus one thousand"), -1000)
        self.assertEqual(word_to_num("negative one lakh"), -100000)
        self.assertEqual(word_to_num("negative point five"), -0.5)
        self.assertEqual(word_to_num("minus one point two five"), -1.25)
    
    def test_fraction_words(self):
        """Test fraction words."""
        self.assertEqual(word_to_num("half"), 0.5)
        self.assertEqual(word_to_num("one third"), 1/3)
        self.assertEqual(word_to_num("three quarters"), 0.75)
        self.assertEqual(word_to_num("two and a half"), 2.5)
        self.assertEqual(word_to_num("one and three quarters"), 1.75)
        self.assertEqual(word_to_num("five and a third"), 5 + 1/3)
    
    def test_case_insensitivity(self):
        """Test case insensitivity."""
        self.assertEqual(word_to_num("ONE"), 1)
        self.assertEqual(word_to_num("Twenty"), 20)
        self.assertEqual(word_to_num("One Hundred"), 100)
        self.assertEqual(word_to_num("ONE MILLION"), 1000000)
        self.assertEqual(word_to_num("One Lakh"), 100000)
    
    def test_mixed_number_systems(self):
        """Test handling of ambiguous or mixed number systems."""
        # These should fail with ValueError
        with self.assertRaises(ValueError):
            word_to_num("one billion lakh")
        
        with self.assertRaises(ValueError):
            word_to_num("one crore million")
        
        with self.assertRaises(ValueError):
            word_to_num("one arba billion")
    
    def test_extremely_large_numbers(self):
        """Test extremely large numbers."""
        self.assertEqual(word_to_num("one trillion"), 1000000000000)
        self.assertEqual(word_to_num("one quadrillion"), 1000000000000000)
        self.assertEqual(word_to_num("one quintillion"), 1000000000000000000)
        # Indian system large numbers
        self.assertEqual(word_to_num("one arab"), 1000000000)  # Alternative for arba
        self.assertEqual(word_to_num("one kharab"), 100000000000)
        self.assertEqual(word_to_num("one neel"), 10000000000000)
        self.assertEqual(word_to_num("one padma"), 1000000000000000)
        self.assertEqual(word_to_num("one shankh"), 100000000000000000)
    
    def test_complex_decimal_cases(self):
        """Test complex decimal cases."""
        self.assertEqual(word_to_num("twenty three point four five six seven"), 23.4567)
        self.assertEqual(word_to_num("point zero zero one"), 0.001)
        self.assertEqual(word_to_num("zero point zero zero one"), 0.001)
        self.assertEqual(word_to_num("one million point zero zero one"), 1000000.001)
        self.assertEqual(word_to_num("one crore point zero zero zero one"), 10000000.0001)
    
    def test_number_with_text(self):
        """Test numbers embedded in text."""
        # If the library is expected to handle this
        self.assertEqual(word_to_num("The answer is twenty one"), 21)
        self.assertEqual(word_to_num("Please give me one hundred dollars"), 100)
        self.assertEqual(word_to_num("It costs two thousand five hundred rupees"), 2500)
    
    def test_unusual_formatting(self):
        """Test unusual formatting and spacing."""
        self.assertEqual(word_to_num("twenty-five-thousand"), 25000)
        self.assertEqual(word_to_num("one_million"), 1000000)
        self.assertEqual(word_to_num("twenty\nfive"), 25)
        self.assertEqual(word_to_num("one,hundred,thousand"), 100000)
    
    def test_multiple_decimal_points(self):
        """Test handling of multiple decimal points."""
        with self.assertRaises(ValueError):
            word_to_num("one point two point three")
        
        with self.assertRaises(ValueError):
            word_to_num("point one point two")
    
    def test_invalid_position_words(self):
        """Test invalid position of words."""
        with self.assertRaises(ValueError):
            word_to_num("hundred one")  # Incorrect order
        
        with self.assertRaises(ValueError):
            word_to_num("thousand hundred")  # Missing number before hundred
        
        with self.assertRaises(ValueError):
            word_to_num("million one")  # Incorrect order
    
    def test_indian_system_variations(self):
        """Test variations in Indian number system terminology."""
        self.assertEqual(word_to_num("one lac twenty five thousand"), 125000)
        self.assertEqual(word_to_num("twenty five lakhs"), 2500000)
        self.assertEqual(word_to_num("two crores fifty lakhs"), 25000000)
        self.assertEqual(word_to_num("five arab twenty five crore"), 5250000000)
    
    def test_american_british_variations(self):
        """Test American and British number variations."""
        self.assertEqual(word_to_num("one billion"), 1000000000)  # American billion
        self.assertEqual(word_to_num("one thousand million"), 1000000000)  # Traditional British billion
        self.assertEqual(word_to_num("one milliard"), 1000000000)  # European alternative
    
    def test_hybrid_expressions(self):
        """Test hybrid numerical expressions."""
        self.assertEqual(word_to_num("two dozen"), 24)
        self.assertEqual(word_to_num("three score and ten"), 70)
        self.assertEqual(word_to_num("a quarter of a hundred"), 25)
        self.assertEqual(word_to_num("half a thousand"), 500)
    
    def test_number_word_repetition(self):
        """Test repetition of number words."""
        with self.assertRaises(ValueError):
            word_to_num("one one")
        
        with self.assertRaises(ValueError):
            word_to_num("twenty twenty")
        
        with self.assertRaises(ValueError):
            word_to_num("hundred hundred")
    
    def test_edge_cases_zero(self):
        """Test edge cases with zero."""
        self.assertEqual(word_to_num("zero point zero"), 0.0)
        self.assertEqual(word_to_num("zero zero zero"), 0)
        self.assertEqual(word_to_num("one hundred and zero"), 100)
        self.assertEqual(word_to_num("zero hundred"), 0)
        self.assertEqual(word_to_num("zero million"), 0)
    
    def test_scientific_notation_words(self):
        """Test words expressing scientific notation."""
        self.assertEqual(word_to_num("ten to the power of six"), 1000000)
        self.assertEqual(word_to_num("ten raised to three"), 1000)
        self.assertEqual(word_to_num("ten to the ninth"), 1000000000)
    
    def test_number_names(self):
        """Test specific number names."""
        self.assertEqual(word_to_num("googol"), 10**100)
        self.assertEqual(word_to_num("centillion"), 10**303)
        self.assertEqual(word_to_num("vigintillion"), 10**63)
    
    def test_malformed_input(self):
        """Test malformed input."""
        with self.assertRaises(ValueError):
            word_to_num(None)
        
        with self.assertRaises(ValueError):
            word_to_num(123.45)
        
        with self.assertRaises(ValueError):
            word_to_num([1, 2, 3])
        
        with self.assertRaises(ValueError):
            word_to_num({"one": 1})
    
    def test_input_with_symbols(self):
        """Test input with symbols."""
        with self.assertRaises(ValueError):
            word_to_num("one+two")
        
        with self.assertRaises(ValueError):
            word_to_num("twenty*thirty")
        
        # These might be valid depending on implementation
        self.assertEqual(word_to_num("20 + 30"), 50)
        self.assertEqual(word_to_num("one hundred - fifty"), 50)
    
    def test_combined_international_systems(self):
        """Test combined international number systems if supported."""
        # Below might be valid or invalid depending on implementation
        # Testing if implementation can handle 'lakh crore' format
        self.assertEqual(word_to_num("one lakh crore"), 10000000000000)

if __name__ == "__main__":
    unittest.main()