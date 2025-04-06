import unittest

import numpy as np

from pwlfit.grid import Grid
from pwlfit.fit import fitFixedKnotsContinuous, fitPrunedKnotsDiscontinuous, fitPrunedKnotsContinuous
from pwlfit.util import generate_data


class TestPrunedKnotsContinuous(unittest.TestCase):

    def test(self):
        D = generate_data(ndata=1000, ngrid=50, nknots=10, noise=0.05, missing_frac=0.05)
        # Interpolate the true model to each grid point
        yknots = np.interp(D.grid.xgrid, D.xknots, D.yknots)
        # Fit using all possible knots and verify that they are pruned to the correct subset
        fit = fitPrunedKnotsContinuous(D.ydata, D.ivar, D.grid, yknots, mu=2, fit=True)
        self.assertTrue(np.array_equal(D.iknots, fit.iknots))
        # Check that the fitted values are within the expected range
        self.assertTrue((np.mean(fit.chisq) > 0.9) and (np.mean(fit.chisq) < 1.1))

    def testLog(self):
        D = generate_data(
            5000, 20, 5, noise=0.05, missing_frac=0.05, xlo=0.1, xhi=10, transform='log')
        yknots = np.interp(D.grid.sgrid, D.grid.sgrid[D.iknots], D.yknots)
        # Fit using all possible knots and verify that they are pruned to the correct subset
        fit = fitPrunedKnotsContinuous(D.ydata, D.ivar, D.grid, yknots, mu=2, fit=True)
        self.assertTrue(np.array_equal(D.iknots, fit.iknots))
        # Check that the fitted values are within the expected range
        self.assertTrue((np.mean(fit.chisq) > 0.9) and (np.mean(fit.chisq) < 1.1))

    def testWithIKnots(self):
        D = generate_data(ndata=1000, ngrid=50, nknots=10, noise=0.05, missing_frac=0.05)
        # Fit using the true iknots
        fit = fitPrunedKnotsContinuous(
            D.ydata, D.ivar, D.grid, D.yknots, iknots=D.iknots, mu=2, fit=True)
        self.assertTrue(np.array_equal(fit.iknots, D.iknots))
        # Check that the fitted values are within the expected range
        self.assertTrue((np.mean(fit.chisq) > 0.9) and (np.mean(fit.chisq) < 1.1))


class TestPrunedKnotsDiscontinuous(unittest.TestCase):

    def testContinuous(self):
        D = generate_data(ndata=1000, ngrid=50, nknots=10, noise=0.05, missing_frac=0.05)
        # Fit using all possible knots and verify that they are pruned to the correct subset
        fit = fitPrunedKnotsDiscontinuous(D.ydata, D.ivar, D.grid, mu=2, fit=True)
        self.assertTrue(np.array_equal(D.iknots, fit.iknots))
        # Check that the fitted values are within the expected range
        self.assertTrue((np.mean(fit.chisq) > 0.9) and (np.mean(fit.chisq) < 1.1))

    def testContinuousLog(self):
        D = generate_data(ndata=1000, ngrid=50, nknots=10, noise=0.05, missing_frac=0.05)
        # Fit using all possible knots and verify that they are pruned to the correct subset
        fit = fitPrunedKnotsDiscontinuous(D.ydata, D.ivar, D.grid, mu=2, fit=True)
        self.assertTrue(np.array_equal(D.iknots, fit.iknots))
        # Check that the fitted values are within the expected range
        self.assertTrue((np.mean(fit.chisq) > 0.9) and (np.mean(fit.chisq) < 1.1))

    def testDiscontinuous(self):
        D = generate_data(ndata=500, ngrid=50, nknots=8, noise=0.05, missing_frac=0.05, continuous=False)
        # Fit using all possible knots and verify that they are pruned to the correct subset
        fit = fitPrunedKnotsDiscontinuous(D.ydata, D.ivar, D.grid, mu=2, fit=True)
        self.assertTrue(np.array_equal(D.iknots, fit.iknots))
        # Check that the fitted values are within the expected range
        self.assertTrue((np.mean(fit.chisq) > 0.9) and (np.mean(fit.chisq) < 1.1))

    def testWithIKnots(self):
        D = generate_data(ndata=1000, ngrid=50, nknots=10, noise=0.05, missing_frac=0.05)
        # Fit using the true knots
        fit = fitPrunedKnotsDiscontinuous(D.ydata, D.ivar, D.grid, iknots=D.iknots, mu=2, fit=True)
        self.assertTrue(np.array_equal(D.iknots, D.iknots))
        # Check that the fitted values are within the expected range
        self.assertTrue((np.mean(fit.chisq) > 0.9) and (np.mean(fit.chisq) < 1.1))


class TestFixedKnotsContinuous(unittest.TestCase):

    def setUp(self):
        self.D = generate_data(ndata=1000, ngrid=50, nknots=10, noise=0.05, missing_frac=0.05)

    def testFullRange(self):
        iknots = self.D.iknots
        ndata = self.D.grid.breaks[iknots[-1]] - self.D.grid.breaks[iknots[0]]
        fit = fitFixedKnotsContinuous(self.D.ydata, self.D.ivar, self.D.grid, iknots, fit=True)
        # Check that the fit results are of the expected shape
        self.assertTrue(np.array_equal(fit.iknots, iknots))
        self.assertEqual(fit.xknots.shape, (len(iknots),))
        self.assertEqual(fit.y1knots.shape, (len(iknots) - 1,))
        self.assertEqual(fit.y2knots.shape, (len(iknots) - 1,))
        self.assertTrue(np.array_equal(fit.y1knots[1:], fit.y2knots[:-1]))
        self.assertEqual(fit.xfit.shape, (ndata,))
        self.assertEqual(fit.yfit.shape, (ndata,))
        self.assertEqual(fit.chisq.shape, (ndata,))
        # Check that the fitted values are within the expected range
        self.assertTrue((np.mean(fit.chisq) > 0.9) and (np.mean(fit.chisq) < 1.1))

    def testFitResultAsDict(self):
        fit = fitFixedKnotsContinuous(self.D.ydata, self.D.ivar, self.D.grid, iknots=self.D.iknots)
        fit_dict = fit.asdict(precision=2)
        self.assertEqual(fit_dict["iknots"], self.D.iknots.tolist())
        self.assertEqual(
            fit_dict["yknots"],
            [0.66, 0.78, 0.03, -0.5, 0.63, -0.57, 0.48, 0.26, 0.86, -0.53])

    def testPartialRange(self):
        iknots = self.D.iknots[2:-1]
        ndata = self.D.grid.breaks[iknots[-1]] - self.D.grid.breaks[iknots[0]]
        fit = fitFixedKnotsContinuous(self.D.ydata, self.D.ivar, self.D.grid, iknots, fit=True)
        # Check that the fit results are of the expected shape
        self.assertTrue(np.array_equal(fit.iknots, iknots))
        self.assertEqual(fit.xknots.shape, (len(iknots),))
        self.assertEqual(fit.y1knots.shape, (len(iknots) - 1,))
        self.assertEqual(fit.y2knots.shape, (len(iknots) - 1,))
        self.assertTrue(np.array_equal(fit.y1knots[1:], fit.y2knots[:-1]))
        self.assertEqual(fit.xfit.shape, (ndata,))
        self.assertEqual(fit.yfit.shape, (ndata,))
        self.assertEqual(fit.chisq.shape, (ndata,))
        # Check that the fitted values are within the expected range
        self.assertTrue((np.mean(fit.chisq) > 0.9) and (np.mean(fit.chisq) < 1.1))

    def testSubRange(self):
        iknots = self.D.iknots[2::2]
        ndata = self.D.grid.breaks[iknots[-1]] - self.D.grid.breaks[iknots[0]]
        fit = fitFixedKnotsContinuous(self.D.ydata, self.D.ivar, self.D.grid, iknots, fit=True)
        # Check that the fit results are of the expected shape
        self.assertTrue(np.array_equal(fit.iknots, iknots))
        self.assertEqual(fit.xknots.shape, (len(iknots),))
        self.assertEqual(fit.y1knots.shape, (len(iknots) - 1,))
        self.assertEqual(fit.y2knots.shape, (len(iknots) - 1,))
        self.assertTrue(np.array_equal(fit.y1knots[1:], fit.y2knots[:-1]))
        self.assertEqual(fit.xfit.shape, (ndata,))
        self.assertEqual(fit.yfit.shape, (ndata,))
        self.assertEqual(fit.chisq.shape, (ndata,))
        # Check that the fitted values are within the expected range
        self.assertTrue(np.mean(fit.chisq) > 10)

    def testZeroIvar(self):
        ivar = np.zeros_like(self.D.ivar)
        with self.assertRaises(ValueError):
            fitFixedKnotsContinuous(self.D.ydata, ivar, self.D.grid, self.D.iknots, fit=True)

    def testLog(self):
        D = generate_data(ndata=1000, ngrid=50, nknots=10, noise=0.05, missing_frac=0.05)
        fit = fitFixedKnotsContinuous(D.ydata, D.ivar, D.grid, D.iknots, fit=True)
        self.assertTrue(np.array_equal(D.iknots, fit.iknots))
        # Check that the fitted values are within the expected range
        self.assertTrue((np.mean(fit.chisq) > 0.9) and (np.mean(fit.chisq) < 1.1))

    def testWithXGrid(self):
        grid = Grid(self.D.xdata, xgrid=self.D.xknots)
        fit = fitFixedKnotsContinuous(self.D.ydata, self.D.ivar, grid, fit=True)
        # Check that the fitted values are within the expected range
        self.assertTrue((np.mean(fit.chisq) > 0.9) and (np.mean(fit.chisq) < 1.1))

    def testWithDefaultIKnots(self):
        fit = fitFixedKnotsContinuous(self.D.ydata, self.D.ivar, self.D.grid, fit=True)


if __name__ == '__main__':
    unittest.main()
