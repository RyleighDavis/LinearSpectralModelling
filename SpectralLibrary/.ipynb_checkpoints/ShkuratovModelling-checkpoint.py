import numpy as np

def shkuratov(wave, n, k, S, q=0.7): 
    """This function computes a spectra with the shkuratov radiative 
    transfer equations for the specified inputs. 
    It returns the spectral albedo (reflectance spectra) at the wavelengths 
    input in wave. 
     
    INPUTS: 
        wave: array: array of wavelengths for corresponding n and k values 
        n, k: arrays: arrays of n and k values to be use din shkuratov formula 
        S: number: grain size, in microns 
        q: default 0.7: volume filling fraction (default is 79%) 
         
    OUTPUT: 
        A: array: spectral albedo values for wavelength in wave
    """
    
    #Fresnell coefficient 
    r_o = ((n-1)**2)/((n+1)**2)  
 
    #Reflection Coefficients 
    R_i = 1.04 - (1/(n**2)) 
    R_e = r_o + 0.05 
    R_b = (0.28*n - 0.20)*R_e 
    R_f = R_e-R_b 
    
    #Transmission Coefficients 
    T_e = 1 - R_e 
    T_i = 1 - R_i 
 
    #Tau: optical density 
    tau = (4*np.pi*k*S)/wave 
 
    #Light Scattering Indicatrices
    r_b = R_b + 0.5*T_e*T_i*R_i*np.exp(-2*tau )/(1 - R_i*np.exp(-1*tau)) 
    r_f = R_f + T_e*T_i*np.exp(-1*tau) + 0.5*T_e*T_i*R_i*np.exp(-2*tau )/(1 - R_i*np.exp(-1*tau))
    
    #1D indicatrices 
    rho_b = q*r_b 
    rho_f = q*r_f + (1-q)
    
    #Spectral Albedo 
    return np.array(((1 + rho_b**2 - rho_f**2)/(2*rho_b)) - np.sqrt(((1 + rho_b**2 - rho_f**2)/(2*rho_b))**2 -1))
