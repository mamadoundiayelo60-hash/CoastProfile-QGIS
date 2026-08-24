import unittest

from coastprofile.core.profiles import (
    SurveyPoint,
    build_profile,
    compare,
    decimal,
    main_spatial_group,
    profile_identifier,
    natural_sort_key,
)


class ProfileEngineTests(unittest.TestCase):
    def test_orientation_and_chainage(self):
        profile=build_profile('P1','2026',[SurveyPoint(0,0,0),SurveyPoint(3,4,5)])
        self.assertEqual(profile.points[0].z,5)
        self.assertEqual(profile.chainage,(0.0,5.0))

    def test_comparison_areas(self):
        first=build_profile('P','2025',[SurveyPoint(0,0,2),SurveyPoint(10,0,1)])
        second=build_profile('P','2026',[SurveyPoint(0,0,3),SurveyPoint(10,0,2)])
        result=compare(first,second)
        self.assertEqual(round(result.accretion_area,3),10)
        self.assertEqual(result.erosion_area,0)

    def test_comparison_erosion_and_common_length(self):
        first=build_profile('P','2025',[SurveyPoint(0,0,3),SurveyPoint(10,0,2)])
        second=build_profile('P','2027',[SurveyPoint(0,0,2),SurveyPoint(20,0,1)])
        result=compare(first,second)
        self.assertEqual(result.chainage[-1],10)
        self.assertEqual(round(result.erosion_area,3),7.5)
        self.assertEqual(result.accretion_area,0)
        self.assertEqual(round(result.net_area,3),-7.5)

    def test_decimal_comma(self):
        self.assertEqual(decimal('0,014'),0.014)

    def test_spatial_outlier(self):
        kept,rejected=main_spatial_group([SurveyPoint(0,0,1),SurveyPoint(10,0,0),SurveyPoint(3000,0,0)])
        self.assertEqual(len(kept),2)
        self.assertEqual(len(rejected),1)

    def test_identifiers_are_never_remapped(self):
        self.assertEqual(profile_identifier(0),'0')
        self.assertEqual(profile_identifier('TR-17'),'TR-17')
        self.assertIsNone(profile_identifier('  '))

    def test_natural_identifier_sort(self):
        values=['10','2','1','P11','P3']
        self.assertEqual(sorted(values,key=natural_sort_key),['1','2','10','P3','P11'])


if __name__ == '__main__':
    unittest.main()
