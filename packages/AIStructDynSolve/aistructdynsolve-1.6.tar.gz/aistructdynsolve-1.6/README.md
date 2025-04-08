<meta http-equiv="Content-Type" content="text/html; charset=utf-8">

# AIStructDynSolve

AIStructDynSolve is an artificial intelligence (AI) powered framework designed to solve both forward and inverse problems in structural dynamics. 
It leverages advanced artificial intelligence methods—particularly physics-informed neural networks (PINNs) and their extensions—to model, predict, and analyze dynamic structural responses under various loading scenarios, such as seismic excitations.

### The framework solves the following ODE of MDOF:

M\*U_dotdot+C\*U_dot+K*U=Pt

- Initial Conditions:
- U(t=0)=InitialU
- U_dot(t=0)=InitialU_dot

### The framework aims to:
- Accurately simulate time-dependent structural behavior (forward problems).
- Identify structural parameters or input forces from measured responses (inverse problems).
- Incorporate domain knowledge and physical laws for improved generalization and interpretability.
- Address challenges in multi-frequency, multi-scale dynamics, especially in earthquake engineering applications.

### Author:
- **Ke Du**  
  Email: duke@iem.ac.cn

### Date:
- 2023/12/26

