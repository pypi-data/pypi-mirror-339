"""
Created on 22 Feb 2023

Test suite validating that the object instances resulting from the annotation parsing 
are compliant with their VODML class definitions

@author: laurentmichel
"""

import os
import unittest
from mivot_validator.utils.session import Session
from mivot_validator.utils.xml_utils import XmlUtils
from mivot_validator.utils.dict_utils import DictUtils

from mivot_validator.instance_checking.instance_checker import (
    InstanceChecker,
    CheckFailedException,
)
from mivot_validator.instance_checking.xml_interpreter.exceptions import (
    MappingException,
)

mapping_sample = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
vodml_sample = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "../mivot_validator/",
    "instance_checking/",
    "vodml/",
)


class TestInstCheck(unittest.TestCase):
    def testOK(self):
        files = os.listdir(mapping_sample)
        for sample_file in files:
            if sample_file.startswith("instcheck_") and "_ok_3" in sample_file:
                print(f"testing {sample_file}")
                session = Session()
                session.install_local_vodml("mango")
                file_path = os.path.join(mapping_sample, sample_file)
                instance = XmlUtils.xmltree_from_file(file_path)
                status = InstanceChecker.check_instance_validity(
                    instance.getroot(), session
                )
                session.close()
                self.assertTrue(status)


if __name__ == "__main__":
    unittest.main()
