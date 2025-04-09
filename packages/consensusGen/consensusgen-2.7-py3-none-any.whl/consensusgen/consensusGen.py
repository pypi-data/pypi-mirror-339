# -*- coding: utf-8 -*-
"""
Created on Wed May 29 08:43:09 2024

@author: romain.coulon
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def cosine_similarity(seq1, seq2):
    
    freq1 = Counter(seq1)
    freq2 = Counter(seq2)
    # Get the set of all unique genes
    genes = set(freq1.keys()).union(set(freq2.keys()))
    
    # Create frequency vectors
    vec1 = [freq1.get(gene, 0) for gene in genes]
    vec2 = [freq2.get(gene, 0) for gene in genes]
    # Calculate dot product
    dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
    
    # Calculate magnitudes
    magnitude1 = np.sqrt(sum(v1 ** 2 for v1 in vec1))
    magnitude2 = np.sqrt(sum(v2 ** 2 for v2 in vec2))
    
    if not magnitude1 or not magnitude2:
        return 0.0
    
    # Calculate cosine similarity
    return dot_product / (magnitude1 * magnitude2)

def DoE(x,u,x_ref,ux_ref,*,w=[],uw=[],k=2):
    """This function aims to calculate Degrees of equivalence.
    
    References: 
        [Accred Qual Assur (2008)13:83-89, Metrologia 52(2015)S200]
        https://link.springer.com/article/10.1007/s00769-007-0330-1
        https://iopscience.iop.org/article/10.1088/0026-1394/52/3/S200/pdf
    
    :param x: Sample of values
    :type x: array of floats
    :param u: Sample of standard uncertainties related to the values
    :type u: array of floats
    :param x_ref: Estimation of the reference value
    :type x_ref: float
    :param ux_ref: Estimation of uncertainty of the reference value
    :type ux_ref: float
    
    :param w: (Optional) Weights associated to each data point.
    :type w: array of floats
    :param uw: (Optional) Standard uncertainty associated to weights of each data point.
    :type uw: array of floats
    :param k: (Optional) Coverage factor (set by default equal to 2)
    :type k: float    
    
    :param d: Estimation of the degrees of equivalence
    :type d: array of floats
    :param ud: Estimation of the uncertainties related to the degrees of equivalence
    :type ud: array of floats    
    :param dr: Estimation of the relative degrees of equivalence
    :type dr: array of floats
    :param udr: Estimation of the uncertainties related to the relative degrees of equivalence
    :type udr: array of floats  
    
    :return y: d, ud, dr, udr
    :rtype y: tuple
    """
    
    x = np.asarray(x) # format input data
    u = np.asarray(u) # format input data
    w = np.asarray(w) # format input data
    uw = np.asarray(uw) # format input data
    d = x - x_ref  # euclidian distance from the reference value
    cov = np.empty(len(x))
    for i in range(len(x)):
        cov[i]=sum(x**2*uw[i]**2)
    u2d=(1 - 2*w)*u**2 + ux_ref**2 + cov # variance associated with DE (the weight factor is available)
    ud=k*u2d**0.5     # enlarged standard deviation associated with DoE
    dr=d/x_ref        # relative DoE
    udr=ud/x_ref      # relative u(DoE)
    return d, ud, dr, udr

def displayResult(X, u, result, *, lab=False):
    """
    Display the result of the genetic algorithm consensusGen()

    Parameters
    ----------
    X : list of floats
        Measurement values.
    u : list of floats
        Standard uncertainties of measurement values.
    result : list
        Output of consensusGen().
    lab : list, optional
        List of the participants. The default is False.

    Returns
    -------
    None.
    """
    mu_vec, u_mu_vec, g0pop, gLpop, w, u_w, pops, F = result
    mu=mu_vec[-1]; u_mu=u_mu_vec[-1]
    nX = len(X)
    d, ud, dr, udr = DoE(X,u,mu,u_mu,w=w,uw=u_w)
    MAD=np.median(abs(d)) # median of absolute value of degrees of equivalence
    x=d/MAD            # x-coordinates
    y=ud/MAD           # y-coordinates
    
    
    if not lab:
        lab = np.linspace(1, nX, nX)-1
        labstr = [str(int(x)) for x in lab]
    else:
        labstr = lab
    
    print(f"The consensus value is {mu:.4g} ± {u_mu:.2g} (k=1)")
    print("The degrees of equivalence are:")
    for il, lL in enumerate(labstr):
        print(f"\t {lL}: {d[il]:.2g} ± {ud[il]:.2g} (k=2)")
    
    # Data plot
    plt.figure("Data")
    plt.clf()
    # plt.title("Data points and the reference value")
    plt.errorbar(labstr, X, yerr=u, fmt='ok', capsize=3, ecolor='k', label=r"$x_i$")
    plt.plot(lab, np.ones(nX) * mu, "-r", label=r"$\hat{\mu}$")
    plt.plot(lab, np.ones(nX) * (mu + u_mu), "--r", label=r"$\hat{\mu} + u(\hat{\mu})$")
    plt.plot(lab, np.ones(nX) * (mu - u_mu), "--r", label=r"$\hat{\mu} - u(\hat{\mu})$")
    plt.ylabel(r'value', fontsize=12)
    plt.xlabel(r'$L$', fontsize=12)
    plt.legend()

    # plt.figure("Convergence")
    # plt.clf()
    # plt.title("Convergence of the reference value")
    # plt.errorbar(np.arange(0,len(mu_vec),1), mu_vec, yerr=u_mu_vec, fmt='ok', capsize=3, ecolor='k', label=r"$\hat{\mu}$")
    # plt.ylabel(r'Generation', fontsize=12)
    # plt.xlabel(r'Reference value', fontsize=12)
    # plt.legend()

    # Data plot
    plt.figure("DoE")
    plt.clf()
    # plt.title("Degrees of equivalence")
    plt.errorbar(labstr, d, yerr=ud, fmt='ok', capsize=3, ecolor='k')
    plt.plot(lab, np.zeros(nX), "-r")
    plt.ylabel(r'$D_i$', fontsize=12)
    plt.xlabel(r'$L$', fontsize=12)

    # Data plot
    plt.figure("rDoE")
    plt.clf()
    # plt.title("Relative degrees of equivalence")
    plt.errorbar(labstr, dr, yerr=udr, fmt='ok', capsize=3, ecolor='k')
    plt.plot(lab, np.zeros(nX), "-r")
    plt.ylabel(r'$D_{i}/\mu$', fontsize=12)
    plt.xlabel(r'$L$', fontsize=12)

    # Weights plot
    plt.figure("Weights")
    plt.clf()
    # plt.title("Weights of the data in the reference value")
    plt.bar(labstr, w, yerr=u_w, capsize=5)
    plt.ylabel(r'$w_i$', fontsize=12)
    plt.xlabel(r'$L$', fontsize=12)
    # plt.legend()

    # Distributions plot
    plt.figure("Distributions")
    plt.clf()
    plt.hist(g0pop, bins=100, edgecolor='none', density=True, label='Linear Pooling')
    plt.hist(gLpop, bins=100, edgecolor='none', alpha=0.7, density=True, label='Genetic Algorithm')
    plt.ylabel(r'$p(y_i)$', fontsize=12)
    plt.xlabel(r'$y_i$', fontsize=12)
    plt.legend()

    # Show plots
    plt.show()

    # PomPlot
    plt.figure("PomPlot")
    plt.clf()
    # plt.title("PomPlot")
    # plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
    # plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True
    fig, ax = plt.subplots() # create of subplot object
    ax.plot(x,y,'ok')
    # define the frame
    plt.ylim(1.1*max(y),0)
    plt.xlim(1.1*min(x),1.1*max(x))
    # print axes title
    ax.set_title(r'$D_{i}$/med($D$)', fontsize=14)
    ax.set_ylabel(r'$u(D_{i})$/med($D$)', fontsize=14)
    # draw the lignes
    x0=np.arange(-9,9,1)
    y0=np.arange(-9,9,1)
    plt.plot(x0,y0,'-g',label=r'$\zeta=1$')
    plt.plot(x0,-y0,'-g')
    plt.plot(x0,y0/2,'-b',label=r'$\zeta=2$')
    plt.plot(x0,-y0/2,'-b')
    plt.plot(x0,y0/3,'-r',label=r'$\zeta=3$')
    plt.plot(x0,-y0/3,'-r')
    for i,g in enumerate(labstr):
        plt.text(x[i]+0.1,y[i]+0.1,g)
    plt.legend() # display the legend

    # Show plots
    plt.show()
    
    plt.figure(r"$\mu$ value vs $t$")
    plt.clf()
    # plt.title(r"$\mu$ vs $t$")
    plt.errorbar(np.arange(0,len(mu_vec),1), result[0], yerr=u_mu_vec, fmt='ok', capsize=3, ecolor='k')
    plt.ylabel(r'$\mu$', fontsize=12)
    plt.xlabel(r'$t$', fontsize=12)

    plt.figure(r"$Z$ vs $t$")
    plt.clf()
    # plt.title(r"$Z$ vs $t$")
    plt.plot(np.arange(0,len(result[0]),1), pops, 'ok')
    # plt.plot(lab, np.zeros(nX), "-r")
    plt.ylabel(r'$Z$', fontsize=12)
    plt.xlabel(r'$t$', fontsize=12)
    
    plt.figure(r"$F$ vs $t$")
    plt.clf()
    # plt.title(r"$Z$ vs $t$")
    plt.plot(np.arange(0,len(result[0]),1), F, 'ok')
    # plt.plot(lab, np.zeros(nX), "-r")
    plt.ylabel(r'$F$', fontsize=12)
    plt.xlabel(r'$t$', fontsize=12)
    
    
    

def consensusGen(X, u, *, ng=1, ni=100000, threshold=0.98, model="normal", df=10):
    """
    Calculate a reference value using an evolutionary algorithm.
    See: Romain Coulon and Steven Judge 2021 Metrologia 58 065007
    https://doi.org/10.1088/1681-7575/ac31c0

    Parameters
    ----------
    X : list of floats
        Measurement values.
    u : list of floats
        Standard uncertainties of measurement values.
    ng : int, optional
        Number of generations (Default = 1). Set ng=0 for Linear Pool estimation.
    ni : int, optional
        Number of individuals in the whole population (Default = 10000).
    threshold : float, optional
        Threshold on the cosine similarity (Default = 1).
    model : string, optional
        Define the statistical model. "normal" for Normal distribution and "t" for shifted Student's t-distribution (Default = "normal").
    df : integer, optional
        Degree of freedom applied with the shifted Student's t-distribution (Default = 10). 

    Returns
    -------
    ref_val : float
        Reference value.
    unc_ref_val : float
        Standard uncertainty of the reference value.
    phen00 : list of floats
        Linear Pool distribution.
    phen1 : list of floats
        Filtered distribution.
    weights : list of floats
        Weights associated with laboratories.
    unc_weights : list of floats
        Standard uncertainties of the weight
    popSize0 : list of integers
        Population sizes as a function of the selection step
    """
    
    def initialize_population(X, u, m, ni_per_group):
        """Initialize the population based on normal distribution."""
        if model=="normal":
            q = np.array([np.random.normal(X[i], u[i], ni_per_group) for i in range(m)])
        elif model=="t":
            q = np.array([X[i]+u[i]*np.random.standard_t(df=df, size=ni_per_group) for i in range(m)])
        else:
            print("undefined model")
        return q.ravel(), q
    
    def create_genomes(m, ni_per_group):
        """Assign initial genomes to each individual."""
        return [chr(65+i) for i in range(m) for _ in range(ni_per_group)]
    
    def evolutionary_step(phen0, gen0, threshold, popSize0):
        """Run an evolution step and generate new population."""
        phen1, gen1, fi = [], [], [] ; F=0
        for i in range(popSize0-1):
            fi.append(1-cosine_similarity(gen0[i], gen0[i+1]))
            if fi[-1] > threshold:
                F+=fi[-1]
                r = np.random.rand()
                phen1.append(r * phen0[i] + (1 - r) * phen0[i+1])
                gen1.append(gen0[i] + gen0[i+1])
        
        return phen1, gen1, F/len(gen1), np.mean(fi)

    def calculate_weights(gen1, m):
        """Calculate the weights based on the occurrence of each gene."""
        listgen = "".join(gen1)
        weights_dic = Counter(listgen)
        w = [weights_dic.get(chr(65+i),0) / len(listgen) for i in range(m)]
        unc_w = [np.sqrt(weights_dic.get(chr(65+i),0)) / len(listgen) for i in range(m)]
        return w, unc_w
            
    # Initialization
    m = len(X)
    ni_per_group = ni // m
    generations = range(ng)
    
    ref_val = np.empty(ng+1)
    unc_ref_val = np.empty(ng+1)
    
    phen0, q = initialize_population(X, u, m, ni_per_group)
    phen00 = phen0.copy()
    popSize0 = [len(phen0)]
    
    gen0 = create_genomes(m, ni_per_group)
    
    paired_vectors = list(zip(phen0, gen0))
    sorted_pairs = sorted(paired_vectors, key=lambda pair: pair[0])
    phen0, gen0 = zip(*sorted_pairs)
    phen0 = list(phen0)
    gen0 = list(gen0)
    
    ref_val[0] = np.mean(phen0)
    unc_ref_val[0] = np.std(phen0) / np.sqrt(m)
    Ff = []
    for t in generations:
        phen1, gen1, F , F0= evolutionary_step(phen0, gen0, threshold, popSize0[-1])
        if t==0:
            Ff.append(F0)
        Ff.append(F)
        popSize0.append(len(phen1))
        rateSibling = popSize0[-1] / popSize0[0]
        print(f"The sibling rate at generation {t+1} is {100 * rateSibling:.2f}% (size: {popSize0[-1]}).")

        ref_val[t+1] = np.mean(phen1)
        unc_ref_val[t+1] = (np.std(phen1) / np.sqrt(m)) * np.sqrt(popSize0[0] / popSize0[-1])
        
        weights, unc_weights = np.asarray(calculate_weights(gen1, m))
        phen0 = phen1
        gen0 = gen1

    return ref_val, unc_ref_val, phen00, phen1, weights, unc_weights, popSize0, Ff

# Example usage (replace with actual function call and data):
# l = ["A", "B", "C", "D", "E", "F", "G"]
# x = [10.1, 11, 14, 10, 10.5, 9.8, 5.1]
# u = [1,    1, 1,  2, 1,    1.5, 3]

# l = ["A", "B", "C","D", "E"]
# x = [11, 12, 13, 12, 17]
# u = [2, 2, 2, 2, 1]

# N=10
# l = [chr(65+x) for x in range(N)]
# x = np.random.normal(loc=10, scale=0.5, size=N)
# x[0]=14
# x[1]=15
# u = np.ones(N)*1
# result = consensusGen(x, u, ng=2, ni=100000, threshold=0.01, model="normal", df=20)
# print(result[0], result[1])



# displayResult(x, u, result, lab=l)

