from printable_object import PrintableObject

"""
File Generated by Lisp2Python Translator
"""

class Strategy(PrintableObject):

    def __init__(self, **entries):

        """
        Constructs a new Strategy object.

        name          -- string
        sort_key      -- string
        keywords      -- list of symbols
        synonyms      -- list of symbols
        isa           -- list of symbols
        isa_depth     -- string for padding printing.
        instances     -- list of strategies
        polarity      -- intrinsic position for this version of the strategy
        quote         -- real quotation
        notes         -- list of remarks
        rank          -- selection order for this strategy
        test          -- predicate for testing applicability of this strategy [text]
        test_code     -- predicate code
        preamble      -- preamble English generation procedure
        protocol      -- procedure for generating transcript comments
        example       -- code to execute to test this strategy
        no_second_try -- flag -- don't execute this strategy at deep analysis

        return        -- returns nothing
        """
        self.name = None
        self.sort_key = None
        self.keywords = []
        self.synonyms = []
        self.isa = []
        self.isa_depth = None
        self.instances = []
        self.polarity = None
        self.quote = None
        self.notes = []
        self.rank = None
        self.test = None
        self.test_code = None
        self.preamble = None
        self.protocol = None
        self.example = None
        self.no_second_try = None
        self.__dict__.update(entries)
