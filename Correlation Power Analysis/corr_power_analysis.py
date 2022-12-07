"""
    *** Correlation Power Analysis ***
        - A side-channel attack -
"""

import numpy as np
import matplotlib.pyplot as plt

# Rijndael S-box
s_box = np.array([0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01,
                  0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d,
                  0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4,
                  0x72, 0xc0, 0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc,
                  0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7,
                  0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2,
                  0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e,
                  0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
                  0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb,
                  0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa, 0xfb,
                  0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c,
                  0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
                  0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c,
                  0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d,
                  0x64, 0x5d, 0x19, 0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a,
                  0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
                  0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3,
                  0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, 0xe7, 0xc8, 0x37, 0x6d,
                  0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a,
                  0xae, 0x08, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6,
                  0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70, 0x3e,
                  0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9,
                  0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9,
                  0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
                  0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99,
                  0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16])


def hamming_weight(X: np.ndarray) -> np.ndarray:
    """Computes the Hamming weight

    Parameters
    ----------
    X : np.ndarray
        A numpy array or matrix of integer elements.

    Returns
    -------
    np.ndarray
        The Hamming weight for each element from X.
    """
    assert X.dtype in [np.int8, np.int16, np.int32, np.int64], \
        "Expected integer values, but provided %s" % X.dtype
    return np.vectorize(lambda x: bin(x).count("1"))(X)


# Load previously generated data
data = np.load("simdata.npy", allow_pickle=True).item()
M, X, K = data["M"].reshape(-1), data["X"].reshape(-1), data["K"].item()

# Get number of leakage points/plaintexts
N = X.shape[0]
print("Size of M:", M.shape)
print("Size of X:", X.shape)
print("K:", K)  # This is supposed to be found by you

# Set possible candidate values from 0-255
target_values = np.arange(256)
nr_values = target_values.shape[0]

# Set Hamming Weight as leakage model for each value in simulated data
lmodel = hamming_weight(target_values)

# Plot first 1000 values of leakage:

plt.figure(figsize=(15, 5))
idx = np.arange(1000)  # x-axis
X1 = X[idx]  # y-axis
plt.plot(idx, X1)
plt.xlabel("Sample index")
plt.ylabel("Leakage")
plt.show()

# Hamming distance for S-box output for the first possible value of the key:
k = 0                                           # The key hypothesis (i.e., the first key)
V = s_box[np.bitwise_xor(target_values[k], M)]  # The output of the S-box, on the first key
L = lmodel[V]                                   # The Hamming Weight model

# Plot leakage hamming weight for S-box output on key = 0:
plt.figure(figsize=(15, 5))
plt.plot(idx, L[idx])
plt.xlabel("Sample index")
plt.ylabel("Hamming weight leakage for k=%d" % k)
plt.show()

# The correlation for this key(k = 0):
c = np.corrcoef(X, L)
c = c[0, 1]
print("Correlation coefficient is: %f\n" % c)

## Find the correct key:

# The correlation for every possible key [0:255]:
cv = np.zeros(nr_values)  # vector with N elements
for k in range(nr_values):
    V = s_box[np.bitwise_xor(target_values[k], M)]  # The output of the S-box, on the key k
    L = lmodel[V]                                   # The Hamming Weight model
    c = np.corrcoef(X, L)
    cv[k] = c[0, 1]


# Plot correlation coefficient for each candidate:

plt.figure(figsize=(15, 5))
idx = np.arange(nr_values)  # x-axis
plt.plot(idx, cv)
plt.xlabel("Target Values")
plt.ylabel("Correlation Values")
plt.show()

## Success Rate of Attack:

n_iter = 50
ntraces = 100  # This should be variable (e.g., 10, 20, 50, ...)
traces = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200]
rng = np.random.default_rng()
key = 208

success_rate = []
for trace in range(len(traces)):
    ntraces = traces[trace]
    isKey = 0
    for i in range(n_iter):
        sel_idx = rng.choice(N, ntraces)
        Mi = M[sel_idx]
        Xi = X[sel_idx]

        # TODO: obtain correlation vector for each selection of traces,
        # then compute success rate
        cv = np.zeros(nr_values)  # vector with N elements
        for k in range(nr_values):
            V = s_box[np.bitwise_xor(target_values[k], Mi)]  # The output of the S-box, on the key k
            L = lmodel[V]                                   # The Hamming Weight model
            c = np.corrcoef(Xi, L)
            cv[k] = c[0, 1]
        max_corr_index= np.where(cv == np.amax(cv))[0][0]  # find the index when the correlation is max
        if max_corr_index == key:
          isKey = isKey + 1
    success_rate.append(isKey/n_iter)

# Plot success rate as a function of number of traces used in attack
plt.figure(figsize=(15, 5))
idx = traces  # x-axis
plt.plot(idx, success_rate)
plt.title("Success Rate of Attack")
plt.xlabel("NTraces")
plt.ylabel("Success Rate")
plt.show()