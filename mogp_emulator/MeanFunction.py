import numpy as np
from functools import partial

class MeanFunction(object):
    """
    Base mean function class

    The base class for the mean function implementation includes code for checking inputs and
    implements sum, product, and composition methods to allow more complicated functions to be
    built up from fixed functions and fitting coefficients. Subclasses need to implement the
    following methods:

    * ``get_n_params`` which returns the number of parameters for a given input size. This is
      usually a constant, but can be more complicated (such as the provided ``PolynomialMean``
      class)
    * ``mean_f`` computes the mean function for the provided inputs and parameters
    * ``mean_deriv`` computes the derivative with respect to the parameters
    * ``mean_hessian`` computes the hessian with respect to the parameters
    * ``mean_inputderiv`` computes the derivate with respect to the inputs

    The base class does not have any attributes, but subclasses will usually have some
    attributes that must be set and so are likely to need a ``__init__`` method.
    """

    def _check_inputs(self, x, params):
        """
        Check the shape of the inputs and reshape if needed

        This method checks that the inputs and parameters are consistent for the provided
        mean function. In particular, the following must be met:

        * The inputs ``x`` must be a 2D numpy array, though if it is 1D it is reshaped to add
          a second dimenion of length 1.
        * ``params`` must be a 1D numpy array. If a multi-dimensional array is provided, it
          will be flattened.
        * ``params`` must have a length that is the same as the return value of ``get_n_params``
          when called with the inputs. Note that some mean functions may have different
          numbers of parameters depending on the inputs, so this may not be known in advance.

        :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
        :type x: ndarray
        :param params: Parameters, must be a 1D numpy array (of more than 1D will be flattened)
                       and have the same length as the number of parameters required for the
                       provided input
        :type params: ndarray
        :returns: tuple containing the reshaped ``x`` and ``params`` arrays
        :rtype: tuple containing two ndarrays
        """

        x = np.array(x)
        params = np.array(params).flatten()

        if len(x.shape) == 1:
            x = np.reshape(x, (-1, 1))
        assert len(x.shape) == 2, "inputs must be a 1D or 2D array"

        assert len(params.shape) == 1, "params must be a 1D array"

        assert len(params) == self.get_n_params(x), "bad length for params"

        return x, params

    def get_n_params(self, x):
        """
        Determine the number of parameters

        Returns the number of parameters for the mean function, which possibly depends on x.

        :param x: Input array
        :type x: ndarray
        :returns: number of parameters
        :rtype: int
        """

        raise NotImplementedError("base mean function does not implement a particular function")

    def mean_f(self, x, params):
        """
        Returns value of mean function

        Method to compute the value of the mean function for the inputs and parameters provided.
        Shapes of ``x`` and ``params`` must be consistent based on the return value of the
        ``get_n_params`` method. Returns a numpy array of shape ``(x.shape[0],)`` holding
        the value of the mean function for each input point.

        :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
        :type x: ndarray
        :param params: Parameters, must be a 1D numpy array (of more than 1D will be flattened)
                       and have the same length as the number of parameters required for the
                       provided input
        :type params: ndarray
        :returns: Value of mean function evaluated at all input points, numpy array of shape
                  ``(x.shape[0],)``
        :rtype: ndarray
        """

        raise NotImplementedError("base mean function does not implement a particular function")

    def mean_deriv(self, x, params):
        """
        Returns value of mean function derivative wrt the parameters

        Method to compute the value of the mean function derivative with respect to the
        parameters for the inputs and parameters provided. Shapes of ``x`` and ``params``
        must be consistent based on the return value of the ``get_n_params`` method.
        Returns a numpy array of shape ``(n_params, x.shape[0])`` holding the value of the mean
        function derivative with respect to each parameter (first axis) for each input point
        (second axis).

        :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
        :type x: ndarray
        :param params: Parameters, must be a 1D numpy array (of more than 1D will be flattened)
                       and have the same length as the number of parameters required for the
                       provided input
        :type params: ndarray
        :returns: Value of mean function derivative with respect to the parameters evaluated
                  at all input points, numpy array of shape ``(n_params, x.shape[0])``
        :rtype: ndarray
        """

        raise NotImplementedError("base mean function does not implement a particular function")

    def mean_hessian(self, x, params):
        """
        Returns value of mean function Hessian wrt the parameters

        Method to compute the value of the mean function Hessian with respect to the
        parameters for the inputs and parameters provided. Shapes of ``x`` and ``params``
        must be consistent based on the return value of the ``get_n_params`` method.
        Returns a numpy array of shape ``(n_params, n_params, x.shape[0])`` holding the value
        of the mean function second derivaties with respect to each parameter pair (first twp axes)
        for each input point (last axis).

        :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
        :type x: ndarray
        :param params: Parameters, must be a 1D numpy array (of more than 1D will be flattened)
                       and have the same length as the number of parameters required for the
                       provided input
        :type params: ndarray
        :returns: Value of mean function Hessian with respect to the parameters evaluated
                  at all input points, numpy array of shape ``(n_parmas, n_params, x.shape[0])``
        :rtype: ndarray
        """

        raise NotImplementedError("base mean function does not implement a particular function")

    def mean_inputderiv(self, x, params):
        """
        Returns value of mean function derivative wrt the inputs

        Method to compute the value of the mean function derivative with respect to the
        inputs for the inputs and parameters provided. Shapes of ``x`` and ``params``
        must be consistent based on the return value of the ``get_n_params`` method.
        Returns a numpy array of shape ``(x.shape[1], x.shape[0])`` holding the value of the mean
        function derivative with respect to each input (first axis) for each input point
        (second axis).

        :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
        :type x: ndarray
        :param params: Parameters, must be a 1D numpy array (of more than 1D will be flattened)
                       and have the same length as the number of parameters required for the
                       provided input
        :type params: ndarray
        :returns: Value of mean function derivative with respect to the inputs evaluated
                  at all input points, numpy array of shape ``(x.shape[1], x.shape[0])``
        :rtype: ndarray
        """

        raise NotImplementedError("base mean function does not implement a particular function")

    def __add__(self, other):
        """
        Adds two mean functions

        This method adds two mean functions, returning a ``MeanSum`` object. If the second
        argument is a float or integer, it is converted to a ``ConstantMean`` object. If
        the second argument is neither a subclass of ``MeanFunction`` nor a float/int,
        an exception is raised.

        :param other: Second ``MeanFunction`` (or float/integer) to be added
        :type other: subclass of MeanFunction or float or int
        :returns: ``MeanSum`` instance
        :rtype: MeanSum
        """

        if issubclass(type(other), MeanFunction):
            return MeanSum(self, other)
        elif isinstance(other, (float, int)):
            return MeanSum(self, ConstantMean(other))
        else:
            raise TypeError("other function cannot be added with a MeanFunction")

    def __radd__(self, other):
        """
        Right adds two mean functions

        This method adds two mean functions, returning a ``MeanSum`` object. If the second
        argument is a float or integer, it is converted to a ``ConstantMean`` object. If
        the second argument is neither a subclass of ``MeanFunction`` nor a float/int,
        an exception is raised.

        :param other: Second ``MeanFunction`` (or float/integer) to be added
        :type other: subclass of MeanFunction or float or int
        :returns: ``MeanSum`` instance
        :rtype: MeanSum
        """

        if issubclass(type(other), MeanFunction):
            return MeanSum(other, self)
        elif isinstance(other, (float, int)):
            return MeanSum(ConstantMean(other), self)
        else:
            raise TypeError("other function cannot be added with a MeanFunction")

    def __mul__(self, other):
        """
        Multiplies two mean functions

        This method multiples two mean functions, returning a ``MeanProduct`` object. If
        the second argument is a float or integer, it is converted to a ``ConstantMean``
        object. If the second argument is neither a subclass of ``MeanFunction`` nor a
        float/int, an exception is raised.

        :param other: Second ``MeanFunction`` (or float/integer) to be multiplied
        :type other: subclass of MeanFunction or float or int
        :returns: ``MeanProduct`` instance
        :rtype: MeanProduct
        """

        if issubclass(type(other), MeanFunction):
            return MeanProduct(self, other)
        elif isinstance(other, (float, int)):
            return MeanProduct(self, ConstantMean(other))
        else:
            raise TypeError("other function cannot be multiplied with a MeanFunction")

    def __rmul__(self, other):
        """
        Right multiplies two mean functions

        This method multiples two mean functions, returning a ``MeanProduct`` object. If
        the second argument is a float or integer, it is converted to a ``ConstantMean``
        object. If the second argument is neither a subclass of ``MeanFunction`` nor a
        float/int, an exception is raised.

        :param other: Second ``MeanFunction`` (or float/integer) to be multiplied
        :type other: subclass of MeanFunction or float or int
        :returns: ``MeanProduct`` instance
        :rtype: MeanProduct
        """

        if issubclass(type(other), MeanFunction):
            return MeanProduct(other, self)
        elif isinstance(other, (float, int)):
            return MeanProduct(ConstantMean(other), self)
        else:
            raise TypeError("other function cannot be multipled with a MeanFunction")

    def __call__(self, other):
        """
        Composes two mean functions

        This method multiples two mean functions, returning a ``MeanComposite`` object.
        If the second argument is not a subclass of ``MeanFunction``, an exception is
        raised.

        :param other: Second ``MeanFunction`` to be composed
        :type other: subclass of MeanFunction
        :returns: ``MeanComposite`` instance
        :rtype: MeanComposite
        """

        if issubclass(type(other), MeanFunction):
            return MeanComposite(self, other)
        else:
            raise TypeError("other function cannot be composed with a MeanFunction")

class MeanSum(MeanFunction):
    """
    Class representing the sum of two mean functions

    This derived class represents the sum of two mean functions, and does the necessary
    bookkeeping needed to compute the required function and derivatives. The code does
    not do any checks to confirm that it makes sense to add these particular mean functions --
    in particular, adding two ``Coefficient`` classes is the same as having a single
    one, but the code will not attempt to simplify this so it is up to the user to get it
    right.

    :iparam f1: first ``MeanFunction`` to be added
    :type f1: subclass of MeanFunction
    :iparam f2: second ``MeanFunction`` to be added
    :type f2: subclass of MeanFunction
    """
    def __init__(self, f1, f2):
        """
        Create a new instance of two added mean functions

        Creates an instance of to added mean functions. Inputs are the two functions
        to be added, which must be subclasses of the base ``MeanFunction`` class.

        :param f1: first ``MeanFunction`` to be added
        :type f1: subclass of MeanFunction
        :param f2: second ``MeanFunction`` to be added
        :type f2: subclass of MeanFunction
        :returns: new ``MeanSum`` instance
        :rtype: MeanSum
        """
        if not issubclass(type(f1), MeanFunction):
            raise TypeError("inputs to MeanSum must be subclasses of MeanFunction")
        if not issubclass(type(f2), MeanFunction):
            raise TypeError("inputs to MeanSum must be subclasses of MeanFunction")

        self.f1 = f1
        self.f2 = f2

    def get_n_params(self, x):
        """
        Determine the number of parameters

        Returns the number of parameters for the mean function, which possibly depends on x.

        :param x: Input array
        :type x: ndarray
        :returns: number of parameters
        :rtype: int
        """
        return self.f1.get_n_params(x) + self.f2.get_n_params(x)

    def mean_f(self, x, params):
        """
        Returns value of mean function

        Method to compute the value of the mean function for the inputs and parameters provided.
        Shapes of ``x`` and ``params`` must be consistent based on the return value of the
        ``get_n_params`` method. Returns a numpy array of shape ``(x.shape[0],)`` holding
        the value of the mean function for each input point.

        For ``MeanSum``, this method applies the sum rule to the results of computing
        the mean for the individual functions.

        :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
        :type x: ndarray
        :param params: Parameters, must be a 1D numpy array (of more than 1D will be flattened)
                       and have the same length as the number of parameters required for the
                       provided input
        :type params: ndarray
        :returns: Value of mean function evaluated at all input points, numpy array of shape
                  ``(x.shape[0],)``
        :rtype: ndarray
        """

        switch = self.f1.get_n_params(x)

        return (self.f1.mean_f(x, params[:switch]) +
                self.f2.mean_f(x, params[switch:]))

    def mean_deriv(self, x, params):
        """
        Returns value of mean function derivative wrt the parameters

        Method to compute the value of the mean function derivative with respect to the
        parameters for the inputs and parameters provided. Shapes of ``x`` and ``params``
        must be consistent based on the return value of the ``get_n_params`` method.
        Returns a numpy array of shape ``(n_params, x.shape[0])`` holding the value of the mean
        function derivative with respect to each parameter (first axis) for each input point
        (second axis).

        For ``MeanSum``, this method applies the sum rule to the results of computing
        the derivative for the individual functions.

        :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
        :type x: ndarray
        :param params: Parameters, must be a 1D numpy array (of more than 1D will be flattened)
                       and have the same length as the number of parameters required for the
                       provided input
        :type params: ndarray
        :returns: Value of mean function derivative with respect to the parameters evaluated
                  at all input points, numpy array of shape ``(n_params, x.shape[0])``
        :rtype: ndarray
        """

        switch = self.f1.get_n_params(x)

        deriv = np.zeros((self.get_n_params(x), x.shape[0]))

        deriv[:switch] = self.f1.mean_deriv(x, params[:switch])
        deriv[switch:] = self.f2.mean_deriv(x, params[switch:])

        return deriv

    def mean_hessian(self, x, params):
        """
        Returns value of mean function Hessian wrt the parameters

        Method to compute the value of the mean function Hessian with respect to the
        parameters for the inputs and parameters provided. Shapes of ``x`` and ``params``
        must be consistent based on the return value of the ``get_n_params`` method.
        Returns a numpy array of shape ``(n_params, n_params, x.shape[0])`` holding the value
        of the mean function second derivaties with respect to each parameter pair (first twp axes)
        for each input point (last axis).

        For ``MeanSum``, this method applies the sum rule to the results of computing
        the Hessian for the individual functions.

        :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
        :type x: ndarray
        :param params: Parameters, must be a 1D numpy array (of more than 1D will be flattened)
                       and have the same length as the number of parameters required for the
                       provided input
        :type params: ndarray
        :returns: Value of mean function Hessian with respect to the parameters evaluated
                  at all input points, numpy array of shape ``(n_parmas, n_params, x.shape[0])``
        :rtype: ndarray
        """

        switch = self.f1.get_n_params(x)

        hess = np.zeros((self.get_n_params(x), self.get_n_params(x), x.shape[0]))

        hess[:switch, :switch] = self.f1.mean_hessian(x, params[:switch])
        hess[switch:, switch:] = self.f2.mean_hessian(x, params[switch:])

        return hess

    def mean_inputderiv(self, x, params):
        """
        Returns value of mean function derivative wrt the inputs

        Method to compute the value of the mean function derivative with respect to the
        inputs for the inputs and parameters provided. Shapes of ``x`` and ``params``
        must be consistent based on the return value of the ``get_n_params`` method.
        Returns a numpy array of shape ``(x.shape[1], x.shape[0])`` holding the value of the mean
        function derivative with respect to each input (first axis) for each input point
        (second axis).

        For ``MeanSum``, this method applies the sum rule to the results of computing
        the derivative for the individual functions.

        :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
        :type x: ndarray
        :param params: Parameters, must be a 1D numpy array (of more than 1D will be flattened)
                       and have the same length as the number of parameters required for the
                       provided input
        :type params: ndarray
        :returns: Value of mean function derivative with respect to the inputs evaluated
                  at all input points, numpy array of shape ``(x.shape[1], x.shape[0])``
        :rtype: ndarray
        """

        switch = self.f1.get_n_params(x)

        return (self.f1.mean_inputderiv(x, params[:switch]) +
                self.f2.mean_inputderiv(x, params[switch:]))

class MeanProduct(MeanFunction):
    """
    Class representing the product of two mean functions

    This derived class represents the product of two mean functions, and does the necessary
    bookkeeping needed to compute the required function and derivatives. The code does
    not do any checks to confirm that it makes sense to multiply these particular mean functions --
    in particular, multiplying two ``Coefficient`` classes is the same as having a single
    one, but the code will not attempt to simplify this so it is up to the user to get it
    right.

    :iparam f1: first ``MeanFunction`` to be multiplied
    :type f1: subclass of MeanFunction
    :iparam f2: second ``MeanFunction`` to be multiplied
    :type f2: subclass of MeanFunction
    """
    def __init__(self, f1, f2):
        """
        Create a new instance of two mulitplied mean functions

        Creates an instance of to multiplied mean functions. Inputs are the two functions
        to be multiplied, which must be subclasses of the base ``MeanFunction`` class.

        :param f1: first ``MeanFunction`` to be multiplied
        :type f1: subclass of MeanFunction
        :param f2: second ``MeanFunction`` to be multiplied
        :type f2: subclass of MeanFunction
        :returns: new ``MeanProduct`` instance
        :rtype: MeanProduct
        """

        if not issubclass(type(f1), MeanFunction):
            raise TypeError("inputs to MeanProduct must be subclasses of MeanFunction")
        if not issubclass(type(f2), MeanFunction):
            raise TypeError("inputs to MeanProduct must be subclasses of MeanFunction")

        self.f1 = f1
        self.f2 = f2

    def get_n_params(self, x):
        """
        Determine the number of parameters

        Returns the number of parameters for the mean function, which possibly depends on x.

        :param x: Input array
        :type x: ndarray
        :returns: number of parameters
        :rtype: int
        """
        return self.f1.get_n_params(x) + self.f2.get_n_params(x)

    def mean_f(self, x, params):
        """
        Returns value of mean function

        Method to compute the value of the mean function for the inputs and parameters provided.
        Shapes of ``x`` and ``params`` must be consistent based on the return value of the
        ``get_n_params`` method. Returns a numpy array of shape ``(x.shape[0],)`` holding
        the value of the mean function for each input point.

        For ``MeanProduct``, this method applies the product rule to the results of computing
        the mean for the individual functions.

        :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
        :type x: ndarray
        :param params: Parameters, must be a 1D numpy array (of more than 1D will be flattened)
                       and have the same length as the number of parameters required for the
                       provided input
        :type params: ndarray
        :returns: Value of mean function evaluated at all input points, numpy array of shape
                  ``(x.shape[0],)``
        :rtype: ndarray
        """

        switch = self.f1.get_n_params(x)

        return (self.f1.mean_f(x, params[:switch])*
                self.f2.mean_f(x, params[switch:]))

    def mean_deriv(self, x, params):
        """
        Returns value of mean function derivative wrt the parameters

        Method to compute the value of the mean function derivative with respect to the
        parameters for the inputs and parameters provided. Shapes of ``x`` and ``params``
        must be consistent based on the return value of the ``get_n_params`` method.
        Returns a numpy array of shape ``(n_params, x.shape[0])`` holding the value of the mean
        function derivative with respect to each parameter (first axis) for each input point
        (second axis).

        For ``MeanProduct``, this method applies the product rule to the results of computing
        the derivative for the individual functions.

        :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
        :type x: ndarray
        :param params: Parameters, must be a 1D numpy array (of more than 1D will be flattened)
                       and have the same length as the number of parameters required for the
                       provided input
        :type params: ndarray
        :returns: Value of mean function derivative with respect to the parameters evaluated
                  at all input points, numpy array of shape ``(n_params, x.shape[0])``
        :rtype: ndarray
        """

        switch = self.f1.get_n_params(x)

        deriv = np.zeros((self.get_n_params(x), x.shape[0]))

        deriv[:switch] = (self.f1.mean_deriv(x, params[:switch])*
                          self.f2.mean_f(x, params[switch:]))

        deriv[switch:] = (self.f1.mean_f(x, params[:switch])*
                          self.f2.mean_deriv(x, params[switch:]))

        return deriv

    def mean_hessian(self, x, params):
        """
        Returns value of mean function Hessian wrt the parameters

        Method to compute the value of the mean function Hessian with respect to the
        parameters for the inputs and parameters provided. Shapes of ``x`` and ``params``
        must be consistent based on the return value of the ``get_n_params`` method.
        Returns a numpy array of shape ``(n_params, n_params, x.shape[0])`` holding the value
        of the mean function second derivaties with respect to each parameter pair (first twp axes)
        for each input point (last axis).

        For ``MeanProduct``, this method applies the product rule to the results of computing
        the Hessian for the individual functions.

        :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
        :type x: ndarray
        :param params: Parameters, must be a 1D numpy array (of more than 1D will be flattened)
                       and have the same length as the number of parameters required for the
                       provided input
        :type params: ndarray
        :returns: Value of mean function Hessian with respect to the parameters evaluated
                  at all input points, numpy array of shape ``(n_parmas, n_params, x.shape[0])``
        :rtype: ndarray
        """

        switch = self.f1.get_n_params(x)

        hess = np.zeros((self.get_n_params(x), self.get_n_params(x), x.shape[0]))

        hess[:switch, :switch] = (self.f1.mean_hessian(x, params[:switch])*
                                  self.f2.mean_f(x, params[switch:]))
        hess[:switch, switch:, :] = (self.f1.mean_deriv(x, params[:switch])[:,np.newaxis,:]*
                                     self.f2.mean_deriv(x, params[switch:])[np.newaxis,:,:])
        hess[switch:, :switch, :] = np.transpose(hess[:switch, switch:, :], (1, 0, 2))
        hess[switch:, switch:] = (self.f1.mean_f(x, params[:switch])*
                                  self.f2.mean_hessian(x, params[switch:]))

        return hess


    def mean_inputderiv(self, x, params):
        """
        Returns value of mean function derivative wrt the inputs

        Method to compute the value of the mean function derivative with respect to the
        inputs for the inputs and parameters provided. Shapes of ``x`` and ``params``
        must be consistent based on the return value of the ``get_n_params`` method.
        Returns a numpy array of shape ``(x.shape[1], x.shape[0])`` holding the value of the mean
        function derivative with respect to each input (first axis) for each input point
        (second axis).

        For ``MeanProduct``, this method applies the product rule to the results of computing
        the derivative for the individual functions.

        :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
        :type x: ndarray
        :param params: Parameters, must be a 1D numpy array (of more than 1D will be flattened)
                       and have the same length as the number of parameters required for the
                       provided input
        :type params: ndarray
        :returns: Value of mean function derivative with respect to the inputs evaluated
                  at all input points, numpy array of shape ``(x.shape[1], x.shape[0])``
        :rtype: ndarray
        """

        switch = self.f1.get_n_params(x)

        return (self.f1.mean_inputderiv(x, params[:switch])*
                self.f2.mean_f(x, params[switch:]) +
                self.f1.mean_f(x, params[:switch])*
                self.f2.mean_inputderiv(x, params[switch:]))

class MeanComposite(MeanFunction):
    """
    Class representing the composition of two mean functions

    This derived class represents the composition of two mean functions, and does the necessary
    bookkeeping needed to compute the required function and derivatives. The code does
    not do any checks to confirm that it makes sense to compose these particular mean
    functions -- in particular, applying a ``Coefficient`` class to another function will
    simply wipe out the second function. This will not raise an error, but the code will not
    attempt to alert the user to this so it is up to the user to get it right.

    Because the Hessian computation requires mixed partials that are not normally implemented
    in the ``MeanFunction`` class, the Hessian computation is not currently implemented.
    If you require Hessian computation for a composite mean function, you must implement
    it yourself.

    :iparam f1: first ``MeanFunction`` to be applied to the second
    :type f1: subclass of MeanFunction
    :iparam f2: second ``MeanFunction`` to be composed as the input to the first
    :type f2: subclass of MeanFunction
    """
    def __init__(self, f1, f2):
        """
        Create a new instance of two composed mean functions

        Creates an instance of to composed mean functions. Inputs are the two functions
        to be composed (``f1(f2)``), which must be subclasses of the base ``MeanFunction``
        class.

        :param f1: first ``MeanFunction`` to be applied to the second
        :type f1: subclass of MeanFunction
        :param f2: second ``MeanFunction`` to be composed as the input to the first
        :type f2: subclass of MeanFunction
        :returns: new ``MeanComposite`` instance
        :rtype: MeanComposite
        """
        if not issubclass(type(f1), MeanFunction):
            raise TypeError("inputs to MeanComposite must be subclasses of MeanFunction")
        if not issubclass(type(f2), MeanFunction):
            raise TypeError("inputs to MeanComposite must be subclasses of MeanFunction")

        self.f1 = f1
        self.f2 = f2

    def get_n_params(self, x):
        """
        Determine the number of parameters

        Returns the number of parameters for the mean function, which possibly depends on x.

        :param x: Input array
        :type x: ndarray
        :returns: number of parameters
        :rtype: int
        """
        return self.f1.get_n_params(np.zeros((x.shape[0], 1))) + self.f2.get_n_params(x)

    def mean_f(self, x, params):
        """
        Returns value of mean function

        Method to compute the value of the mean function for the inputs and parameters provided.
        Shapes of ``x`` and ``params`` must be consistent based on the return value of the
        ``get_n_params`` method. Returns a numpy array of shape ``(x.shape[0],)`` holding
        the value of the mean function for each input point.

        For ``MeanComposite``, this method applies the output of the second function as
        input to the first function.

        :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
        :type x: ndarray
        :param params: Parameters, must be a 1D numpy array (of more than 1D will be flattened)
                       and have the same length as the number of parameters required for the
                       provided input
        :type params: ndarray
        :returns: Value of mean function evaluated at all input points, numpy array of shape
                  ``(x.shape[0],)``
        :rtype: ndarray
        """

        switch = self.f1.get_n_params(x)

        return self.f1.mean_f(np.reshape(self.f2.mean_f(x, params[switch:]), (-1, 1)),
                              params[:switch])

    def mean_deriv(self, x, params):
        """
        Returns value of mean function derivative wrt the parameters

        Method to compute the value of the mean function derivative with respect to the
        parameters for the inputs and parameters provided. Shapes of ``x`` and ``params``
        must be consistent based on the return value of the ``get_n_params`` method.
        Returns a numpy array of shape ``(n_params, x.shape[0])`` holding the value of the mean
        function derivative with respect to each parameter (first axis) for each input point
        (second axis).

        For ``MeanComposite``, this method applies the chain rule to the results of computing
        the derivative for the individual functions.

        :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
        :type x: ndarray
        :param params: Parameters, must be a 1D numpy array (of more than 1D will be flattened)
                       and have the same length as the number of parameters required for the
                       provided input
        :type params: ndarray
        :returns: Value of mean function derivative with respect to the parameters evaluated
                  at all input points, numpy array of shape ``(n_params, x.shape[0])``
        :rtype: ndarray
        """

        switch = self.f1.get_n_params(x)

        deriv = np.zeros((self.get_n_params(x), x.shape[0]))

        f2 = np.reshape(self.f2.mean_f(x, params[switch:]), (-1, 1))

        deriv[:switch] = self.f1.mean_deriv(f2, params[:switch])

        deriv[switch:] = (self.f1.mean_inputderiv(f2, params[:switch])*
                          self.f2.mean_deriv(x, params[switch:]))

        return deriv

    def mean_inputderiv(self, x, params):
        """
        Returns value of mean function derivative wrt the inputs

        Method to compute the value of the mean function derivative with respect to the
        inputs for the inputs and parameters provided. Shapes of ``x`` and ``params``
        must be consistent based on the return value of the ``get_n_params`` method.
        Returns a numpy array of shape ``(x.shape[1], x.shape[0])`` holding the value of the mean
        function derivative with respect to each input (first axis) for each input point
        (second axis).

        For ``MeanComposite``, this method applies the chain rule to the results of computing
        the derivative for the individual functions.

        :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
        :type x: ndarray
        :param params: Parameters, must be a 1D numpy array (of more than 1D will be flattened)
                       and have the same length as the number of parameters required for the
                       provided input
        :type params: ndarray
        :returns: Value of mean function derivative with respect to the inputs evaluated
                  at all input points, numpy array of shape ``(x.shape[1], x.shape[0])``
        :rtype: ndarray
        """

        switch = self.f1.get_n_params(x)

        return (self.f1.mean_inputderiv(np.reshape(self.f2.mean_f(x, params[switch:]), (-1, 1)),
                                        params[:switch])*
                self.f2.mean_inputderiv(x, params[switch:]))

class FixedMean(MeanFunction):
    """
    Class representing a fixed mean function with no parameters

    Class representing a mean function with a fixed function (and optional derivative)
    and no fitting parameters. The user must provide these functions when initializing
    the instance.

    :iparam f: fixed mean function, must be callable and take a single argument (the inputs)
    :type f: function
    :iparam deriv: fixed derivative function (optional if no derivatives are needed), must
                   be callable and take a single argument (the inputs)
    :type deriv: function or None
    """
    def __init__(self, f, deriv=None):
        """
        Initialize a class instance representing a fixed mean function with no parameters

        Create a class instance representing a mean function with a fixed function
        (and optional derivative) and no fitting parameters. The user must provide these
        functions, though the derivative is optional. The code will check that the provided
        arguments are callable, but will not confirm that the inputs and outputs are the
        correct type/shape.

        :param f: fixed mean function, must be callable and take a single argument (the inputs)
        :type f: function
        :param deriv: fixed derivative function (optional if no derivatives are needed), must
                       be callable and take a single argument (the inputs)
        :type deriv: function or None
        :returns: new ``FixedMean`` instance
        :rtype: FixedMean
        """
        assert callable(f), "fixed mean function must be a callable function"
        if not deriv is None:
            assert callable(deriv), "mean function derivative must be a callable function"

        self.f = f
        self.deriv = deriv

    def get_n_params(self, x):
        """
        Determine the number of parameters

        Returns the number of parameters for the mean function, which possibly depends on x.
        For a ``FixedMean`` class, this is zero.

        :param x: Input array
        :type x: ndarray
        :returns: number of parameters
        :rtype: int
        """
        return 0

    def mean_f(self, x, params):
        """
        Returns value of mean function

        Method to compute the value of the mean function for the inputs and parameters provided.
        Shapes of ``x`` and ``params`` must be consistent based on the return value of the
        ``get_n_params`` method. For ``FixedMean`` classes, there are no parameters so the
        ``params`` argument should be an array of length zero. Returns a numpy array of shape
        ``(x.shape[0],)`` holding the value of the mean function for each input point.

        :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
        :type x: ndarray
        :param params: Parameters, must be a 1D numpy array (of more than 1D will be flattened)
                       and have the same length as the number of parameters required for the
                       provided input (zero in this case)
        :type params: ndarray
        :returns: Value of mean function evaluated at all input points, numpy array of shape
                  ``(x.shape[0],)``
        :rtype: ndarray
        """

        x, params = self._check_inputs(x, params)

        return self.f(x)

    def mean_deriv(self, x, params):
        """
        Returns value of mean function derivative wrt the parameters

        Method to compute the value of the mean function derivative with respect to the
        parameters for the inputs and parameters provided. Shapes of ``x`` and ``params``
        must be consistent based on the return value of the ``get_n_params`` method.
        For ``FixedMean`` classes, there are no parameters so the ``params`` argument
        should be an array of length zero. Returns a numpy array of shape
        ``(n_params, x.shape[0])`` holding the value of the mean function derivative with
        respect to each parameter (first axis) for each input point (second axis). Since
        fixed means have no parameters, this will just be an array of zeros.

        :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
        :type x: ndarray
        :param params: Parameters, must be a 1D numpy array (of more than 1D will be flattened)
                       and have the same length as the number of parameters required for the
                       provided input
        :type params: ndarray
        :returns: Value of mean function derivative with respect to the parameters evaluated
                  at all input points, numpy array of shape ``(n_params, x.shape[0])``
        :rtype: ndarray
        """

        x, params = self._check_inputs(x, params)

        return np.zeros((self.get_n_params(x), x.shape[0]))

    def mean_hessian(self, x, params):
        """
        Returns value of mean function Hessian wrt the parameters

        Method to compute the value of the mean function Hessian with respect to the
        parameters for the inputs and parameters provided. Shapes of ``x`` and ``params``
        must be consistent based on the return value of the ``get_n_params`` method.
        For ``FixedMean`` classes, there are no parameters so the ``params`` argument
        should be an array of length zero. Returns a numpy array of shape
        ``(n_params, n_params, x.shape[0])`` holding the value of the mean function
        second derivaties with respect to each parameter pair (first twp axes) for each
        input point (last axis). Since fixed means have no parameters, this will just
        be an array of zeros.

        :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
        :type x: ndarray
        :param params: Parameters, must be a 1D numpy array (of more than 1D will be flattened)
                       and have the same length as the number of parameters required for the
                       provided input
        :type params: ndarray
        :returns: Value of mean function Hessian with respect to the parameters evaluated
                  at all input points, numpy array of shape ``(n_parmas, n_params, x.shape[0])``
        :rtype: ndarray
        """

        x, params = self._check_inputs(x, params)

        return np.zeros((self.get_n_params(x), self.get_n_params(x), x.shape[0]))

    def mean_inputderiv(self, x, params):
        """
        Returns value of mean function derivative wrt the inputs

        Method to compute the value of the mean function derivative with respect to the
        inputs for the inputs and parameters provided. Shapes of ``x`` and ``params``
        must be consistent based on the return value of the ``get_n_params`` method.
        For ``FixedMean`` classes, there are no parameters so the ``params`` argument
        should be an array of length zero. Returns a numpy array of shape
        ``(x.shape[1], x.shape[0])`` holding the value of the mean function derivative
        with respect to each input (first axis) for each input point (second axis).

        :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
        :type x: ndarray
        :param params: Parameters, must be a 1D numpy array (of more than 1D will be flattened)
                       and have the same length as the number of parameters required for the
                       provided input
        :type params: ndarray
        :returns: Value of mean function derivative with respect to the inputs evaluated
                  at all input points, numpy array of shape ``(x.shape[1], x.shape[0])``
        :rtype: ndarray
        """

        x, params = self._check_inputs(x, params)

        if self.deriv is None:
            raise RuntimeError("Derivative function was not provided with this FixedMean")
        else:
            return self.deriv(x)

def fixed_f(x, index, f):
    """
    Dummy function to index into x and apply a function

    Usage is intended to be with a fixed mean function, where an index and specific mean
    function are meant to be bound using partial before setting it as the ``f`` attribute of
    ``FixedMean``

    :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
    :type x: ndarray
    :param index: integer index to be applied to the second axis of ``x``, used to select
                  a particular input variable. Must be non-negative and less than the
                  length of the second axis of the inputs.
    :type index: int
    :param f: fixed mean function, must be callable and take a single argument (the inputs)
    :type f: function
    :returns: Value of mean function evaluated at all input points, numpy array of shape
              ``(x.shape[0],)``
    :rtype: ndarray
    """
    assert callable(f), "fixed mean function must be callable"
    assert index >= 0, "provided index cannot be negative"
    assert x.ndim == 2, "x must have 2 dimensions"

    try:
        val = f(x[:,index])
    except IndexError:
        raise IndexError("provided mean function index is out of range")

    return val

def fixed_inputderiv(x, index, deriv):
    """
    Dummy function to index into x and apply a derivative function

    Usage is intended to be with a fixed mean function, where an index and specific derivative
    function are meant to be bound using partial before setting it as the ``deriv`` attribute of
    ``FixedMean``

    :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
    :type x: ndarray
    :param index: integer index to be applied to the second axis of ``x``, used to select
                  a particular input variable. Must be non-negative and less than the
                  length of the second axis of the inputs.
    :type index: int
    :param deriv: fixed derivative function, must be callable and take a single argument (the inputs)
    :type deriv: function
    :returns: Value of mean derivative evaluated at all input points, numpy array of shape
              ``(x.shape[1], x.shape[0])``
    :rtype: ndarray
    """
    assert callable(deriv), "fixed mean function derivative must be callable"
    assert index >= 0, "provided index cannot be negative"
    assert x.ndim == 2, "x must have 2 dimensions"

    try:
        out = np.zeros((x.shape[1], x.shape[0]))
        out[index, :] = deriv(np.transpose(x[:, index]))
    except IndexError:
        raise IndexError("provided mean function index is out of range")

    return out

def one(x):
    """
    Function to return an array of ones with the same shape as the input

    Function to return a numpy array of ones with the same shape as the input. Used in
    linear mean functions to evaluate derivatives.

    :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
    :type x: ndarray
    :returns: Numpy array of ones with the same shape as x
    :rtype: ndarray
    """
    return np.ones(x.shape)

def const_f(x, val):
    """
    Function to return an array of a constant value

    Function to return a numpy array of a constant value with the correct shape for a given
    input. Used in constant mean functions to evaluate the function.

    :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
    :type x: ndarray
    :param val: value of output, must be a float
    :type val: float
    :returns: Numpy array of ``val`` with shape ``(x.shape[0],)``
    :rtype: ndarray
    """
    assert x.ndim == 2, "x must have 2 dimensions"

    return np.broadcast_to(val, x.shape[0])

def const_deriv(x):
    """
    Function to return an array of zeros with the transposed shape of the inputs

    Function to return a numpy array of zeros with the shape that is transpose of the
    shape of the input. Used in constant mean functions to evaluate the derivative.

    :param x: Inputs, must be a 1D or 2D numpy array (if 1D a second dimension will be added)
    :type x: ndarray
    :returns: Numpy array of zeros with shape ``(x.shape[1], x.shape[0])``
    :rtype: ndarray
    """
    assert x.ndim == 2, "x must have 2 dimensions"

    return np.zeros((x.shape[1], x.shape[0]))

class ConstantMean(FixedMean):
    """
    Class representing a constant fixed mean function

    Subclass of ``FixedMean`` where the function is a constant, with the value
    provided when ``ConstantMean`` is initialized. Uses utility functions to bind the
    value to the ``fixed_f`` function and sets that as the ``f`` attribute.

    :iparam f: fixed mean function, must be callable and take a single argument (the inputs)
    :type f: function
    :iparam deriv: fixed derivative function (optional if no derivatives are needed), must
                   be callable and take a single argument (the inputs)
    :type deriv: function
    """
    def __init__(self, val):
        """
        Initialize a new ConstantMean

        Create a new ``ConstantMean`` instance with the given constant value.

        :param val: Constant mean function value, must be a float or an integer
        :type val: float or int
        :returns: new ``ConstantMean`` instance
        :rtype: ConstantMean
        """
        if not isinstance(val, (float, int)):
            raise TypeError("val must be a float or an integer")
        self.f = partial(const_f, val=val)
        self.deriv = const_deriv

class LinearMean(FixedMean):
    """
    Class representing a linear fixed mean function

    Subclass of ``FixedMean`` where the function is a linear function. By default the
    function is linear in the first input dimension, though any non-negative integer index
    can be provided to control which input is used in the linear function. Uses utility
    functions to bind the correct function to the ``fixed_f`` function and sets that as
    the ``f`` attribute and similar with the ``fixed_deriv`` utility function and the
    ``deriv`` attribute.

    :iparam f: fixed mean function, must be callable and take a single argument (the inputs)
    :type f: function
    :iparam deriv: fixed derivative function, must be callable and take a single argument
                   (the inputs)
    :type deriv: function
    """
    def __init__(self, index=0):
        """
        Initialize a new LinearMean

        Create a new ``LinearMean`` instance with the given index value. This index is used
        to select the dimension of the input for evaluating the function.

        :param index: integer index to be applied to the second axis of ``x``, used to select
                      a particular input variable. Must be non-negative and less than the
                      length of the second axis of the inputs.
        :type index: int
        :returns: new ``LinearMean`` instance
        :rtype: LinearMean
        """
        self.f = partial(fixed_f, index=index, f=np.array)
        self.deriv = partial(fixed_inputderiv, index=index, deriv=one)

class Coefficient(MeanFunction):
    "class representing a single parameter fitting coefficient"
    def get_n_params(self, x):
        return 1

    def mean_f(self, x, params):

        x, params = self._check_inputs(x, params)

        return np.broadcast_to([params[0]], x.shape[0])

    def mean_deriv(self, x, params):

        x, params = self._check_inputs(x, params)

        return np.ones((self.get_n_params(x), x.shape[0]))

    def mean_hessian(self, x, params):

        x, params = self._check_inputs(x, params)

        return np.zeros((self.get_n_params(x), self.get_n_params(x), x.shape[0]))

    def mean_inputderiv(self, x, params):

        x, params = self._check_inputs(x, params)

        return np.zeros((x.shape[1], x.shape[0]))

class PolynomialMean(MeanFunction):
    "mean function where every input dimension is fit to a fixed degree polynomial"
    def __init__(self, degree):
        assert int(degree) >= 0., "degree must be a positive integer"

        self.degree = int(degree)

    def get_n_params(self, x):
        return x.shape[1]*self.degree + 1

    def mean_f(self, x, params):
        x, params = self._check_inputs(x, params)

        n_params = self.get_n_params(x)

        indices = np.arange(0, n_params - 1) % x.shape[1]
        expon = np.arange(0, n_params - 1) // x.shape[1] + 1

        output = params[0] + np.sum(params[1:]*x[:, indices]**expon, axis = 1)

        return output

    def mean_deriv(self, x, params):

        x, params = self._check_inputs(x, params)

        n_params = self.get_n_params(x)

        deriv = np.zeros((n_params, x.shape[0]))
        deriv[0] = np.ones(x.shape[0])

        indices = np.arange(0, n_params - 1) % x.shape[1]
        expon = np.arange(0, n_params - 1) // x.shape[1] + 1

        deriv[1:,:] = np.transpose(x[:, indices]**expon)

        return deriv

    def mean_hessian(self, x, params):

        x, params = self._check_inputs(x, params)

        n_params = self.get_n_params(x)

        hess = np.zeros((n_params, n_params, x.shape[0]))

        return hess

    def mean_inputderiv(self, x, params):
        x, params = self._check_inputs(x, params)

        expon = np.reshape(np.arange(0, x.shape[0]*x.shape[1]*self.degree)//x.shape[1]//self.degree,
                           (self.degree, x.shape[0]*x.shape[1]))
        x_indices = np.reshape(np.arange(0, x.shape[0]*x.shape[1]*self.degree) % (x.shape[0]*x.shape[1]),
                               (self.degree, x.shape[0]*x.shape[1]))
        param_indices = np.reshape(np.arange(0, x.shape[0]*x.shape[1]*self.degree) % x.shape[1],
                                   (self.degree, x.shape[0]*x.shape[1])) + expon*x.shape[1]
        param_indices = np.reshape(param_indices, (self.degree, x.shape[0]*x.shape[1]))

        output = np.sum((expon + 1.)*params[1:][param_indices]*x.flatten()[x_indices]**expon, axis=0)

        return np.transpose(np.reshape(output, (x.shape[0], x.shape[1])))
