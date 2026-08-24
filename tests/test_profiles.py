from coastprofile.core.profiles import SurveyPoint,build_profile,compare,decimal,main_spatial_group
def test_orientation_and_chainage():
    p=build_profile('P1','2026',[SurveyPoint(0,0,0),SurveyPoint(3,4,5)])
    assert p.points[0].z==5 and p.chainage== (0.0,5.0)
def test_comparison_areas():
    a=build_profile('P','2025',[SurveyPoint(0,0,2),SurveyPoint(10,0,1)])
    b=build_profile('P','2026',[SurveyPoint(0,0,3),SurveyPoint(10,0,2)])
    c=compare(a,b); assert round(c.accretion_area,3)==10 and c.erosion_area==0
def test_decimal_comma(): assert decimal('0,014')==0.014
def test_spatial_outlier():
    keep,out=main_spatial_group([SurveyPoint(0,0,1),SurveyPoint(10,0,0),SurveyPoint(3000,0,0)])
    assert len(keep)==2 and len(out)==1
