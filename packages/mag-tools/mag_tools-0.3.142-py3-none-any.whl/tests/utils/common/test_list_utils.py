import unittest

from numpy.ma.testutils import assert_equal

from utils.data.list_utils import ListUtils


class TestListUtils(unittest.TestCase):
    def test_split(self):
        # 示例用法
        input_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        n = 3
        result = ListUtils.split(input_list, n)
        print(result)  # 输出: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    def test_split_by_keyword(self):
        lines = [
            "This is test line 1.",
            "This is test line 2.",
            "Keyword",
            "Another test line 1.",
            "Another test line 2.",
            "Keyword",
            "Final test line 1.",
            "Final test line 2."
        ]
        expected_output = [
            ["This is test line 1.",
             "This is test line 2."],
            ["Keyword",
             "Another test line 1.",
             "Another test line 2."],
            ["Keyword",
             "Final test line 1.",
             "Final test line 2."]
        ]
        keyword = "Keyword"

        result = ListUtils.split_by_keyword(lines, keyword)
        self.assertEqual(result, expected_output)

    def test_split_by_keywords(self):
        lines = [
            "apple",
            "apple is red",
            "apple pie is delicious",
            "banana",
            "banana is yellow",
            "banana split is tasty",
            "cherry",
            "cherry is red",
            "date is brown"
        ]
        keywords = ["apple", "banana", "cherry"]

        expected_output = {
            "apple": [
                "apple",
                "apple is red",
                "apple pie is delicious"
            ],
            "banana": [
                "banana",
                "banana is yellow",
                "banana split is tasty"
            ],
            "cherry": [
                "cherry",
                "cherry is red",
                "date is brown"
            ]
        }
        result = ListUtils.split_by_keywords(lines, keywords)
        self.assertEqual(result, expected_output)

        keyword_map = {"apple": (None, None), "banana": (None, None), "cherry": (None, None)}
        result = ListUtils.split_by_boundary(lines, keyword_map)
        self.assertEqual(result, expected_output)

    def test_split_by_empty_line(self):
        lines = [
            "This is test line 1.",
            "This is test line 2.",
            "",
            "Another test line 1.",
            "Another test line 2.",
            "",
            "Final test line 1.",
            "Final test line 2."
        ]
        expected_output = [
            ["This is test line 1.",
             "This is test line 2."],
            ["",
             "Another test line 1.",
             "Another test line 2."],
            ["",
             "Final test line 1.",
             "Final test line 2."]
        ]
        result = ListUtils.split_by_keyword(lines)

        result1 = ListUtils.split_by_keyword(lines, "")
        assert_equal(result1, result)
        self.assertEqual(expected_output, result)

    def test_trim(self):
        # 测试用例 1：起始和结尾都有空行
        lines = [
            "",
            "Line 1",
            "Line 2",
            "",
            "Line 3",
            ""
        ]
        expected_output = [
            "Line 1",
            "Line 2",
            "",
            "Line 3"
        ]
        result = ListUtils.trim(lines)
        self.assertEqual(result, expected_output)

        # 测试用例 2：只有起始有空行
        lines = [
            "",
            "",
            "Line 1",
            "Line 2",
            "Line 3"
        ]
        expected_output = [
            "Line 1",
            "Line 2",
            "Line 3"
        ]
        result = ListUtils.trim(lines)
        self.assertEqual(result, expected_output)

        # 测试用例 3：只有结尾有空行
        lines = [
            "Line 1",
            "Line 2",
            "Line 3",
            "",
            ""
        ]
        expected_output = [
            "Line 1",
            "Line 2",
            "Line 3"
        ]
        result = ListUtils.trim(lines)
        self.assertEqual(result, expected_output)

        # 测试用例 4：没有空行
        lines = [
            "Line 1",
            "Line 2",
            "Line 3"
        ]
        expected_output = [
            "Line 1",
            "Line 2",
            "Line 3"
        ]
        result = ListUtils.trim(lines)
        self.assertEqual(result, expected_output)

        # 测试用例 5：全是空行
        lines = [
            "",
            "",
            ""
        ]
        expected_output = []
        result = ListUtils.trim(lines)
        self.assertEqual(result, expected_output)

    def test_split_by_boundary(self):
        # 示例用法
        data = """MODELTYPE BlackOil
        FIELD

        GRID
        ##################################################
        DIMENS
         5 2 1

        BOX FIPNUM 1 5 1 2 1 1 = 2

        PERMX
        49.29276      162.25308      438.45926      492.32336      791.32867
        704.17102      752.34912      622.96875      542.24493      471.45953

        COPY PERMX  PERMY  1 5 1 2 1 1 
        COPY PERMX  PERMZ  1 5 1 2 1 1

        BOX  PERMZ  1 5 1 2 1 1  '*' 0.01

        PORO
         5*0.087
         5*0.097

        TOPS 10*9000.00

        BOX TOPS   1  1  1 2  1  1  '='  9000.00
        BOX TOPS   2  2  1 2  1  1  '='  9052.90

        DXV
         5*300.0

        DYV
         2*300.0

        DZV
         20

        #GRID END#########################################

        WELL
        ##################################################

        TEMPLATE
        'MARKER' 'I' 'J' 'K1' 'K2' 'OUTLET' 'WI' 'OS' 'SATMAP' 'HX' 'HY' 'HZ' 'REQ' 'SKIN' 'LENGTH' 'RW' 'DEV' 'ROUGH' 'DCJ' 'DCN' 'XNJ' 'YNJ' /
        WELSPECS
        NAME 'INJE1'
        ''  24  25  11  11  NA  NA  SHUT  NA  0  0  0  NA  NA  NA  0.5  NA  NA  NA  1268.16  NA  NA  
        ''  24  25  11  15  NA  NA  OPEN  NA  0  0  DZ  NA  NA  NA  0.5  NA  NA  NA  0  NA  NA  

        NAME 'PROD2'
        ''  5  1  2  2  NA  NA  OPEN  NA  0  0  DZ  NA  0  NA  0.5  0  0  NA  NA  NA  NA  
        ''  5  1  3  3  NA  NA  OPEN  NA  0  0  DZ  NA  0  NA  0.5  0  0  NA  NA  NA  NA  
        ''  5  1  4  4  NA  NA  OPEN  NA  0  0  DZ  NA  0  NA  0.5  0  0  NA  NA  NA  NA 
        #WELL END#########################################

        PROPS
        ##################################################
        SWOF
        #           Sw         Krw       Krow       Pcow(=Po-Pw)
               0.15109           0           1         400
               0.15123           0     0.99997      359.19
               0.15174           0     0.99993      257.92

        #PROPS END########################################

        SOLUTION
        ##################################################

        EQUILPAR
        # Ref_dep    Ref_p    GWC/OWC  GWC_pc/OWC_pc   dh
          9035       3600      9950        0.0         2
        # GOC       GOC_pc
          8800        0.0    
        PBVD
           5000        3600
           9000        3600

        #SOLUTION END######################################

        TUNE
        TSTART  1990-01-01 
        MINDT  0.1  MAXDT  31  DTINC  2.0  DTCUT  0.5  CHECKDX  
        MAXDP  200  MAXDS  0  MAXDC  0  MBEPC  1E-4  MBEAVG  1E-6   
        SOLVER  1034


        RESTART

        RPTSCHED
        BINOUT SEPARATE NETONLY GEOM RPTONLY RSTBIN SOLVD 
        POIL SOIL SEAS SWAT RS NOSTU  TECPLOT 
         /

        RPTSUM
        POIL 1 2 1 /
        POIL AVG Reg 2 /
        """
        keyword_map = {
            "BASE": (None, None),
            "GRID": (
                "##################################################", "#GRID END#########################################"),
            "WELL": (
                "##################################################", "#WELL END#########################################"),
            "PROPS": (
                "##################################################", "#PROPS END########################################"),
            "SOLUTION": ("##################################################",
                         "#SOLUTION END######################################"),
            "TUNE": (None, None)
        }
        lines = data.splitlines()
        lines.insert(0, "BASE")
        _segments = ListUtils.split_by_boundary(lines, keyword_map)

        for segment_name, segment in _segments.items():
            print(f"Segment: {segment_name}")
            for line in segment:
                print(f"    {line}")
            print()


if __name__ == '__main__':
    unittest.main()