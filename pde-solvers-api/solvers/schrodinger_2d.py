import numpy as np
from scipy.sparse import diags, kron, eye
from scipy.sparse.linalg import eigsh
from scipy.sparse import csr_matrix

def solve_2d_schrodinger(R, N, V_func=None):
    """
    Решает 2D уравнение Шрёдингера в круговой полости
    R - радиус полости
    N - число точек по каждому направлению
    V_func - функция потенциала V(x,y) (по умолчанию 0 внутри полости)
    """
    h = 2*R/(N-1)
    x = np.linspace(-R, R, N)
    y = np.linspace(-R, R, N)
    X, Y = np.meshgrid(x, y)
    
    # Маска для круговой области
    r = np.sqrt(X**2 + Y**2)
    mask = (r <= R).flatten()
    
    # Кинетический оператор (2D лапласиан)
    diag = np.ones(N)
    off_diag = np.ones(N-1)
    T = diags([-off_diag, 2*diag, -off_diag], [-1, 0, 1])/(h**2)
    I = eye(N)
    H = -0.5*(kron(T, I) + kron(I, T))
    
    # Применяем граничные условия (ψ=0 при r>R)
    H = H.tocsr()[mask,:][:,mask]
    
    # Находим первые 5 собственных состояний
    E, psi = eigsh(H, k=5, which='SA')
    
    # Восстанавливаем полные 2D волновые функции
    psi_2d = []
    for i in range(psi.shape[1]):
        full_psi = np.zeros(N*N)
        full_psi[mask] = psi[:,i]
        psi_2d.append(full_psi.reshape(N,N))
    
    return E, psi_2d, X, Y
