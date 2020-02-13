import numpy as np
import pytest
from numpy.testing import assert_allclose
from ..MeanFunction import MeanFunction, MeanSum, MeanProduct, FixedMean, ConstantMean, LinearMean
from ..MeanFunction import Coefficient, PolynomialMean, MeanComposite
from ..MeanFunction import fixed_f, fixed_inputderiv, one, const_f, const_deriv

@pytest.fixture
def mf():
    return MeanFunction()

@pytest.fixture
def x():
    return np.array([[1., 2., 3.], [4., 5., 6.]])

@pytest.fixture
def params():
    return np.array([1., 2., 4.])

@pytest.fixture
def zeroparams():
    return np.zeros(0)

@pytest.fixture
def oneparams():
    return np.ones(1)

@pytest.fixture
def dx():
    return 1.e-6

def test_MeanFunction(mf, x, params):
    "test composition of mean functions"

    mf2 = mf + mf

    assert isinstance(mf2, MeanSum)

    mf3 = 5. + mf

    assert isinstance(mf3, MeanSum)
    assert isinstance(mf3.f1, ConstantMean)

    mf4 = mf + 3.

    assert isinstance(mf4, MeanSum)
    assert isinstance(mf4.f2, ConstantMean)

    mf5 = mf*mf

    assert isinstance(mf5, MeanProduct)

    mf6 = 3.*mf

    assert isinstance(mf6, MeanProduct)
    assert isinstance(mf6.f1, ConstantMean)

    mf7 = mf*3.

    assert isinstance(mf7, MeanProduct)
    assert isinstance(mf7.f2, ConstantMean)

    mf8 = mf(mf)

    assert isinstance(mf8, MeanComposite)

def test_MeanFunction_failures(mf, x, params):
    "test situations of MeanFunction where an exception should be raised"

    with pytest.raises(NotImplementedError):
        mf.get_n_params(x)

    with pytest.raises(NotImplementedError):
        mf.mean_f(x, params)

    with pytest.raises(NotImplementedError):
        mf.mean_deriv(x, params)

    with pytest.raises(NotImplementedError):
        mf.mean_hessian(x, params)

    with pytest.raises(NotImplementedError):
        mf.mean_inputderiv(x, params)

    with pytest.raises(TypeError):
        "3" + mf

    with pytest.raises(TypeError):
        mf + "3"

    with pytest.raises(TypeError):
        mf*"3"

    with pytest.raises(TypeError):
        "3"*mf

    with pytest.raises(TypeError):
        mf(3.)

def test_fixed_functions(x):
    "test utility functions for creating fixed means"

    assert_allclose(fixed_f(np.ones((2,2)), 0, np.exp), np.exp(np.ones(2)))

    with pytest.raises(AssertionError):
        fixed_f(np.ones(3), 0, np.exp)
    with pytest.raises(AssertionError):
        fixed_f(np.ones((2,2)), -1, np.exp)
    with pytest.raises(AssertionError):
        fixed_f(np.ones((2,2)), 0, 1)
    with pytest.raises(IndexError):
        fixed_f(np.ones((2,2)), 3, np.exp)

    inputderiv_exp = np.zeros((2,2))
    inputderiv_exp[0] = np.exp(1.)

    assert_allclose(fixed_inputderiv(np.ones((2,2)), 0, np.exp), inputderiv_exp)

    with pytest.raises(AssertionError):
        fixed_inputderiv(np.ones(3), 0, np.exp)
    with pytest.raises(AssertionError):
        fixed_inputderiv(np.ones((2,2)), -1, np.exp)
    with pytest.raises(AssertionError):
        fixed_inputderiv(np.ones((2,2)), 0, 1)
    with pytest.raises(IndexError):
        fixed_inputderiv(np.ones((2,2)), 3, np.exp)

    assert_allclose(one(x), np.ones(x.shape))
    assert_allclose(const_f(x, 2.), np.broadcast_to(2., (x.shape[0],)))
    assert_allclose(const_deriv(x), np.zeros((x.shape[1], x.shape[0])))

def test_FixedMean(x, zeroparams):
    "test the FixedMean function"

    f = lambda x: np.ones(x.shape[0])
    deriv = lambda x: np.zeros((x.shape[1], x.shape[0]))
    fixed_mean = FixedMean(f, deriv)

    assert fixed_mean.get_n_params(x) == 0

    assert_allclose(fixed_mean.mean_f(x, zeroparams), np.ones(x.shape[0]))
    assert_allclose(fixed_mean.mean_f(np.array([1., 2., 3.]), zeroparams), np.ones(3))
    assert_allclose(fixed_mean.mean_deriv(x, zeroparams), np.zeros((0, x.shape[0])))
    assert_allclose(fixed_mean.mean_hessian(x, zeroparams), np.zeros((0, 0, x.shape[0])))
    assert_allclose(fixed_mean.mean_inputderiv(x, zeroparams), np.zeros((x.shape[1], x.shape[0])))

    fixed_mean = FixedMean(f)

    with pytest.raises(RuntimeError):
        fixed_mean.mean_inputderiv(x, np.zeros(0))

@pytest.mark.parametrize("val",[0., 1., 2.])
def test_ConstantMean(x, zeroparams, val):
    "test the constant mean function"

    constant_mean = ConstantMean(val)

    assert constant_mean.get_n_params(x) == 0

    assert_allclose(constant_mean.mean_f(x, zeroparams), np.broadcast_to(val, x.shape[0]))
    assert_allclose(constant_mean.mean_deriv(x, zeroparams), np.zeros((0, x.shape[0])))
    assert_allclose(constant_mean.mean_hessian(x, zeroparams), np.zeros((0, 0, x.shape[0])))
    assert_allclose(constant_mean.mean_inputderiv(x, zeroparams), np.zeros((x.shape[1], x.shape[0])))

def test_ConstantMean_failures():
    "test situation where ConstantMean should fail"

    with pytest.raises(TypeError):
        ConstantMean("a")

@pytest.mark.parametrize("index", [0, 1])
def test_LinearMean(x, zeroparams, dx, index):
    "test the linear mean function"

    linear_mean = LinearMean(index)

    assert linear_mean.get_n_params(x) == 0

    inputderiv_expect = np.zeros((x.shape[1], x.shape[0]))
    inputderiv_expect[index] = 1.

    assert_allclose(linear_mean.mean_f(x, zeroparams), x[:,index])
    assert_allclose(linear_mean.mean_deriv(x, zeroparams), np.zeros((0, x.shape[0])))
    assert_allclose(linear_mean.mean_hessian(x, zeroparams), np.zeros((0, 0, x.shape[0])))
    assert_allclose(linear_mean.mean_inputderiv(x, zeroparams), inputderiv_expect)

    D = x.shape[1]

    inputderiv_fd = np.zeros((D, 2))
    for i in range(D):
        dx_array = np.zeros(D)
        dx_array[i] = dx
        inputderiv_fd[i] = (linear_mean.mean_f(x, zeroparams) -
                            linear_mean.mean_f(x - dx_array, zeroparams))/dx

    assert_allclose(linear_mean.mean_inputderiv(x, zeroparams), inputderiv_fd)

def test_Coefficient(x, oneparams):
    "test the Coefficient class"

    coeff_mean = Coefficient()

    assert coeff_mean.get_n_params(x) == 1

    assert_allclose(coeff_mean.mean_f(x, oneparams), np.broadcast_to(1., x.shape[0]))
    assert_allclose(coeff_mean.mean_deriv(x, oneparams), np.ones((1, x.shape[0])))
    assert_allclose(coeff_mean.mean_hessian(x, oneparams), np.zeros((1, 1, x.shape[0])))
    assert_allclose(coeff_mean.mean_inputderiv(x, oneparams), np.zeros((x.shape[1], x.shape[0])))

    with pytest.raises(AssertionError):
        coeff_mean._check_inputs(x, np.ones(4))

    with pytest.raises(AssertionError):
        coeff_mean._check_inputs(np.ones((2, 3, 2)), oneparams)

def test_LinearMean_failures(x):
    "test situations where LinearMean should fail"

    mf = LinearMean(3)

    with pytest.raises(IndexError):
        mf.mean_f(x, np.zeros(0))

def test_MeanSum(x, oneparams, dx):
    "test the MeanSum function"

    n_params = 1
    index = 0

    mf = Coefficient() + LinearMean(index)

    assert mf.get_n_params(x) == n_params

    inputderiv_exp = np.zeros((x.shape[1], x.shape[0]))
    inputderiv_exp[index] = 1.

    assert_allclose(mf.mean_f(x, oneparams), 1. + x[:,index])
    assert_allclose(mf.mean_deriv(x, oneparams), np.ones((n_params, x.shape[0])))
    assert_allclose(mf.mean_hessian(x, oneparams), np.zeros((n_params, n_params, x.shape[0])))
    assert_allclose(mf.mean_inputderiv(x, oneparams), inputderiv_exp)

    deriv_fd = np.zeros((n_params, x.shape[0]))
    for i in range(n_params):
        dx_array = np.zeros(n_params)
        dx_array[i] = dx
        deriv_fd[i] = (mf.mean_f(x, oneparams) - mf.mean_f(x, oneparams - dx_array))/dx

    assert_allclose(mf.mean_deriv(x, oneparams), deriv_fd)

    hess_fd = np.zeros((n_params, n_params, x.shape[0]))
    for i in range(n_params):
        for j in range(n_params):
            dx_array = np.zeros(n_params)
            dx_array[j] = dx
            hess_fd[i,j] = (mf.mean_deriv(x, oneparams)[i] -
                            mf.mean_deriv(x, oneparams - dx_array)[i])/dx

    assert_allclose(mf.mean_hessian(x, oneparams), hess_fd)

    D = x.shape[1]

    inputderiv_fd = np.zeros((D, x.shape[0]))
    for i in range(D):
        dx_array = np.zeros(D)
        dx_array[i] = dx
        inputderiv_fd[i] = (mf.mean_f(x, oneparams) - mf.mean_f(x - dx_array, oneparams))/dx

    assert_allclose(mf.mean_inputderiv(x, oneparams), inputderiv_fd)

def test_MeanProduct(x, oneparams, dx):
    "test the MeanProduct function"

    n_params = 1
    index = 0

    mf = Coefficient()*LinearMean(index)

    assert mf.get_n_params(x) == n_params

    inputderiv_exp = np.zeros((x.shape[1], x.shape[0]))
    inputderiv_exp[index] = np.broadcast_to(oneparams, (x.shape[0],))

    assert_allclose(mf.mean_f(x, oneparams), 1.*x[:,index])
    assert_allclose(mf.mean_deriv(x, oneparams), np.broadcast_to(x[:,index], (n_params, x.shape[0])))
    assert_allclose(mf.mean_hessian(x, oneparams), np.zeros((n_params, n_params, x.shape[0])))
    assert_allclose(mf.mean_inputderiv(x, oneparams), inputderiv_exp)

    deriv_fd = np.zeros((n_params, x.shape[0]))
    for i in range(n_params):
        dx_array = np.zeros(n_params)
        dx_array[i] = dx
        deriv_fd[i] = (mf.mean_f(x, oneparams) - mf.mean_f(x, oneparams - dx_array))/dx

    assert_allclose(mf.mean_deriv(x, oneparams), deriv_fd)

    hess_fd = np.zeros((n_params, n_params, x.shape[0]))
    for i in range(n_params):
        for j in range(n_params):
            dx_array = np.zeros(n_params)
            dx_array[j] = dx
            hess_fd[i,j] = (mf.mean_deriv(x, oneparams)[i] -
                            mf.mean_deriv(x, oneparams - dx_array)[i])/dx

    assert_allclose(mf.mean_hessian(x, oneparams), hess_fd)

    D = x.shape[1]

    inputderiv_fd = np.zeros((D, x.shape[0]))
    for i in range(D):
        dx_array = np.zeros(D)
        dx_array[i] = dx
        inputderiv_fd[i] = (mf.mean_f(x, oneparams) - mf.mean_f(x - dx_array, oneparams))/dx

    assert_allclose(mf.mean_inputderiv(x, oneparams), inputderiv_fd)

def test_MeanSum_MeanProduct_combination(x, params, dx):
    "test a more complicated combination of sums and products"

    n_params = 3
    index1 = 0
    index2 = 1
    index3 = 2

    mf = (Coefficient() + Coefficient()*LinearMean(index1) +
          Coefficient()*LinearMean(index2)*LinearMean(index3))

    assert mf.get_n_params(x) == n_params

    deriv_exp = np.zeros((n_params, x.shape[0]))
    deriv_exp[0] = 1.
    deriv_exp[1] = x[:,index1]
    deriv_exp[2] = x[:,index2]*x[:,index3]

    inputderiv_exp = np.zeros((x.shape[1], x.shape[0]))
    inputderiv_exp[0,:] = params[1]
    inputderiv_exp[1,:] = params[2]*x[:,index3]
    inputderiv_exp[2,:] = params[2]*x[:,index2]

    assert_allclose(mf.mean_f(x, params), params[0] + params[1]*x[:,index1]
                                                    + params[2]*x[:,index2]*x[:,index3])
    assert_allclose(mf.mean_deriv(x, params), deriv_exp)
    assert_allclose(mf.mean_hessian(x, params), np.zeros((n_params, n_params, x.shape[0])))
    assert_allclose(mf.mean_inputderiv(x, params), inputderiv_exp)

    deriv_fd = np.zeros((n_params, x.shape[0]))
    for i in range(n_params):
        dx_array = np.zeros(n_params)
        dx_array[i] = dx
        deriv_fd[i] = (mf.mean_f(x, params) - mf.mean_f(x, params - dx_array))/dx

    assert_allclose(mf.mean_deriv(x, params), deriv_fd)

    hess_fd = np.zeros((n_params, n_params, x.shape[0]))
    for i in range(n_params):
        for j in range(n_params):
            dx_array = np.zeros(n_params)
            dx_array[j] = dx
            hess_fd[i,j] = (mf.mean_deriv(x, params)[i] -
                            mf.mean_deriv(x, params - dx_array)[i])/dx

    assert_allclose(mf.mean_hessian(x, params), hess_fd)

    D = x.shape[1]

    inputderiv_fd = np.zeros((D, x.shape[0]))
    for i in range(D):
        dx_array = np.zeros(D)
        dx_array[i] = dx
        inputderiv_fd[i] = (mf.mean_f(x, params) - mf.mean_f(x - dx_array, params))/dx

    assert_allclose(mf.mean_inputderiv(x, params), inputderiv_fd)

def test_CompositeMean(x, params, dx):
    "test the composite mean function"

    mf1 = LinearMean(0)*LinearMean(1)
    mf2 = Coefficient() + Coefficient()*LinearMean(0) + Coefficient()*LinearMean(0)*LinearMean(0)

    mf = mf2(mf1)

    n_params = 3

    assert mf.get_n_params(x) == n_params

    deriv_exp = np.zeros((n_params, x.shape[0]))
    deriv_exp[0,:] = 1.
    deriv_exp[1,:] = x[:,0]*x[:,1]
    deriv_exp[2,:] = x[:,0]**2*x[:,1]**2

    inputderiv_exp = np.zeros((x.shape[1], x.shape[0]))
    inputderiv_exp[0] = params[1]*x[:,1] + 2.*params[2]*x[:,0]*x[:,1]**2
    inputderiv_exp[1] = params[1]*x[:,0] + 2.*params[2]*x[:,0]**2*x[:,1]

    assert_allclose(mf.mean_f(x, params), params[0] + params[1]*x[:,0]*x[:,1]
                                                    + params[2]*x[:,0]**2*x[:,1]**2)
    assert_allclose(mf.mean_deriv(x, params), deriv_exp)
    assert_allclose(mf.mean_inputderiv(x, params), inputderiv_exp)

    with pytest.raises(NotImplementedError):
        mf.mean_hessian(x, params)

def test_PolynomialMean(x, dx):
    "test the polynomial mean function"

    degree = 2

    poly_mean = PolynomialMean(degree)
    n_params = 1 + x.shape[1]*degree

    assert poly_mean.degree == degree
    assert poly_mean.get_n_params(x) == n_params

    params = np.arange(1., 1.+float(n_params))

    mean_expected = np.array([(params[0] + params[1]*x[0, 0] + params[2]*x[0, 1] + params[3]*x[0, 2]
                                         + params[4]*x[0, 0]**2 + params[5]*x[0, 1]**2 + params[6]*x[0, 2]**2),
                              (params[0] + params[1]*x[1, 0] + params[2]*x[1, 1] + params[3]*x[1, 2]
                                         + params[4]*x[1, 0]**2 + params[5]*x[1, 1]**2 + params[6]*x[1, 2]**2)])
    deriv_expected = np.array([[1., 1.], x[:, 0], x[:, 1], x[:, 2],
                                         x[:, 0]**2, x[:, 1]**2, x[:, 2]**2])
    hess_expected = np.zeros((n_params, n_params, 2))
    inputderiv_expected = np.array([[params[1] + 2.*params[4]*x[0,0], params[1] + 2.*params[4]*x[1,0]],
                                    [params[2] + 2.*params[5]*x[0,1], params[2] + 2.*params[5]*x[1,1]],
                                    [params[3] + 2.*params[6]*x[0,2], params[3] + 2.*params[6]*x[1,2]]])

    assert_allclose(poly_mean.mean_f(x, params), mean_expected)
    assert_allclose(poly_mean.mean_deriv(x, params), deriv_expected)
    assert_allclose(poly_mean.mean_hessian(x, params), hess_expected)
    assert_allclose(poly_mean.mean_inputderiv(x, params), inputderiv_expected)

    deriv_fd = np.zeros((n_params, 2))
    for i in range(n_params):
        dx_array = np.zeros(n_params)
        dx_array[i] = dx
        deriv_fd[i] = (poly_mean.mean_f(x, params) - poly_mean.mean_f(x, params - dx_array))/dx

    assert_allclose(poly_mean.mean_deriv(x, params), deriv_fd)

    hess_fd = np.zeros((n_params, n_params, 2))
    for i in range(n_params):
        for j in range(n_params):
            dx_array = np.zeros(n_params)
            dx_array[j] = dx
            hess_fd[i, j] = (poly_mean.mean_deriv(x, params)[i] - poly_mean.mean_deriv(x, params - dx_array)[i])/dx

    assert_allclose(poly_mean.mean_hessian(x, params), hess_fd)

    D = 3

    inputderiv_fd = np.zeros((D, 2))
    for i in range(D):
        dx_array = np.zeros(D)
        dx_array[i] = dx
        inputderiv_fd[i] = (poly_mean.mean_f(x, params) - poly_mean.mean_f(x - dx_array, params))/dx

    assert_allclose(poly_mean.mean_inputderiv(x, params), inputderiv_fd, atol=1.e-5)

def test_PolynomialMean_failures(x):
    "test situations where PolynomialMean should raise an error"

    with pytest.raises(AssertionError):
        PolynomialMean(-1)

    degree = 2

    poly_mean = PolynomialMean(degree)

    with pytest.raises(AssertionError):
        poly_mean._check_inputs(x, np.ones(4))

    with pytest.raises(AssertionError):
        poly_mean._check_inputs(np.ones((2, 3, 2)), np.ones(7))