mport numpy as np
import h5py
import time
import sys
from scipy.signal import medfilt

def AFF(q, atom, choice='AFF'):
    '''
    calculate the AFFs using five Gaussians fitted by
    Waasmeier et al., Acta Crystallographica Section A (1995)
    atom must be 'O' for oxygen or 'H' for hydrogen
    q specifies the range of q-values for which the AFF
    should be calculated in inverse Angstrom [A-1].
    if choice is 'AFF'  = independent atomic form factor
                 'MAFF' = modified atomic form factor
    '''
    s = q/4/np.pi # crystallographer definition of q
    
    if atom == 'O':
        a = [2.960427, 2.508818, 0.637853, 0.722838, 1.142756]
        b = [14.182259, 5.936858, 0.112726, 34.958481, 0.390240]
        c = 0.027014
        f0 = a[0]*np.exp(-b[0]*s*s) + a[1]*np.exp(-b[1]*s*s) + a[2]*np.exp(-b[2]*s*s) + a[3]*np.exp(-b[3]*s*s) + a[4]*np.exp(-b[4]*s*s) + c
        if choice == 'MAFF':
            # choose modified atomic form factor (MAFF)
            alpha_O = 0.1075
            alpha_H = -4*alpha_O
            delta = 2.01 # A-1
            f0 = f0*(1 + alpha_O*np.exp(-((4*np.pi*s)**2)/2/(delta*delta)))
    elif atom == 'H':
        a = [0.413048, 0.294953, 0.187491, 0.080701, 0.023736]
        b = [15.569946, 32.398468, 5.711404, 61.889874, 1.334118]
        c = 0.000049
        f0 = a[0]*np.exp(-b[0]*s*s) + a[1]*np.exp(-b[1]*s*s) + a[2]*np.exp(-b[2]*s*s) + a[3]*np.exp(-b[3]*s*s) + a[4]*np.exp(-b[4]*s*s) + c
        if choice == 'MAFF':
            # choose modified atomic form factor (MAFF)
            alpha_O = 0.1075
            alpha_H = -4*alpha_O
            delta = 2.01 # A-1
            f0 = f0*(1 + alpha_H*np.exp(-((4*np.pi*s)**2)/2/(delta*delta)))
    else:
        print('unknown atom: %s' % atom)
        f0 = np.zeros_like(q)
    return f0


def Iq_normalization(q, Iq, nominator, q_min, q_max, rho=0.1, denominator=None, choice='la'):
    '''
    normalize I(q) to S(q) using the Warren normalization (large-angle method = la)
    or Krogh-Moe normalization (integral method = int), set by the choice argument
    nominator is the molecular form factor squared <F^2> (in electron units)
    denominator is the spherical part of the molecular form factor squared <F>^2 (in electron units)
    denominator is usually approximated to be equal to nominator, both can be in atom or molecular basis
    rho is the atomic density (in atoms/A^3)
    q_min and q_max (in A-1) sets the q-limits for the method
    q and Iq are ndarrays with the same shape of momentum transfer (in A-1) and radial intensity, respectively
    '''
    if denominator is None:
        denominator = nominator
    q_indices = np.where((q >= q_min) & (q <= q_max))
    if choice == 'la':
        norm = np.average(nominator[q_indices]/Iq[q_indices])
        print('Large-angle normalization: %.2f' % norm)
    else:
        int_nom = np.trapz(q[q_indices]*q[q_indices]*nominator[q_indices]/denominator[q_indices], x=q[q_indices])
        int_denom = np.trapz(q[q_indices]*q[q_indices]*Iq[q_indices]/denominator[q_indices], x=q[q_indices])
        norm = (int_nom-2*np.pi*np.pi*rho)/int_denom
        print('Integral normalization: %.2f' % norm)
    Sq = (norm*Iq-nominator)/denominator
    return norm, Sq
