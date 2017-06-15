# 1D Differential Equation solver
Any given order 1D equation can be solver for user specific time domain and initial condition. Homegenous or non-homogenous, using state-space approach.

## Define equation
Equation has to satisfy critearia of declaration explained in example of single mass damped pendulum.

    def eq(derivative,t):
        return 1 / J * (M0*np.sin(b*t ) - c * derivative[1] - k * derivative[0])
    
## Define case
    case = ODEsolver(eq)

## Define time domain
    case.setTimeDomain(0,10,0.0001)

## Define initial conditions
    initData = [0.0, 0.0]
    case.setInitalConditions(initData)

## Run solver
    case.derive()

## Access solution
    solution = case.solution

## Draw results in given time domain
    case.izris()
