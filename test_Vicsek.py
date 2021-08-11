import unittest
import VicsekModel
import math

class TestViskeModel(unittest.TestCase):
    def test_randomize_spins(self):
        testModel = VicsekModel.Vicsek(rho = 2)
        equalX = testModel.spins[0].x == testModel.spins[1].x
        equalY = testModel.spins[0].y == testModel.spins[1].y
        equalAngle = testModel.spins[0].angle == testModel.spins[1].angle
        self.assertFalse(equalX or equalY)
        self.assertFalse(testModel.spins[0].angle == 0)

        
        
    def test_randomize_spins_from_base(self):
        spin1 = VicsekModel.VicsekSpins()
        spin2 = VicsekModel.VicsekSpins()
        equalX = spin1.x == spin2.x
        equalY = spin1.y == spin2.y
        equalAngle = spin1.angle == spin2.angle
        self.assertFalse(equalX or equalY)

    def test_spin_movement(self):
        spin = VicsekModel.VicsekSpins(x = 0, y = 0, angle = 0)

        self.assertTrue(spin.x == 0)
        self.assertTrue(spin.y == 0)
        self.assertTrue(spin.angle == 0)

        spin.nextAngle = 1
        spin.Update(.1)

        self.assertTrue(spin.x == 0.1)
        self.assertTrue(spin.y == 0)
        self.assertTrue(spin.angle == 1)

    def test_spin_unitvector(self):
        angleUnitVectorList = ((0, (1,0)),
                               (math.pi/4, (1/math.sqrt(2),1/math.sqrt(2))),
                               (math.pi/2, (0,1)),
                               (math.pi*3/4, (-1/math.sqrt(2),1/math.sqrt(2))),
                               (math.pi, (-1,0)),
                               (math.pi*5/4, (-1/math.sqrt(2),-1/math.sqrt(2))),
                               (math.pi*6/4, (0,-1)),
                               (math.pi*7/4, (1/math.sqrt(2),-1/math.sqrt(2))),
                               (math.pi*2, (1,0)))
                               
                                           
        for pair in angleUnitVectorList:
            spin = VicsekModel.VicsekSpins(angle = pair[0])
            self.assertTrue(math.isclose(spin.UnitVector()[0],pair[1][0],abs_tol = 1e-9)
                            and math.isclose(spin.UnitVector()[1],pair[1][1],abs_tol = 1e-9),
                            'Angle ' + str(pair[0]) + ' returned' + str(spin.UnitVector())
                            + ' Expeceted ' + str(pair[1]))
            
    
if __name__ == '__main__':
    unittest.main()
