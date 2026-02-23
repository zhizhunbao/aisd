"""
Naive Bayes Calculation Verification for Lab 4 Step 14
Student Number: 041107730
"""
import numpy as np

# Dataset
male_data = np.array([
    [6.0, 75, 9.0],
    [5.92, 80, 9.5],
    [5.58, 85, 10.0],
    [5.92, 90, 11.0]
])
female_data = np.array([
    [5.2, 55, 7.0],
    [5.5, 60, 8.0],
    [5.45, 65, 8.5],
    [5.6, 70, 9.0]
])

# Test person (from student number 041107730)
test_person = np.array([5.0, 80, 5.0])

print("=" * 60)
print("Step 14: Naive Bayes Classification")
print("=" * 60)

# Step 1: Prior probabilities
print("\n--- Step 1: Prior Probabilities ---")
p_male = 4/8
p_female = 4/8
print(f"P(M) = 4/8 = {p_male}")
print(f"P(F) = 4/8 = {p_female}")

# Step 2: Mean
print("\n--- Step 2: Mean by Class ---")
male_mean = male_data.mean(axis=0)
female_mean = female_data.mean(axis=0)
print(f"Male Mean:   H={male_mean[0]:.4f}, W={male_mean[1]:.4f}, FS={male_mean[2]:.4f}")
print(f"Female Mean: H={female_mean[0]:.4f}, W={female_mean[1]:.4f}, FS={female_mean[2]:.4f}")

# Step 3: Sample Variance (ddof=1)
print("\n--- Step 3: Sample Variance (n-1) ---")
male_var = male_data.var(axis=0, ddof=1)
female_var = female_data.var(axis=0, ddof=1)
print(f"Male Var:   H={male_var[0]:.6f}, W={male_var[1]:.4f}, FS={male_var[2]:.6f}")
print(f"Female Var: H={female_var[0]:.6f}, W={female_var[1]:.4f}, FS={female_var[2]:.6f}")

# Step 4: Covariance Matrix (sample, ddof=1)
print("\n--- Step 4: Covariance Matrix ---")
male_cov = np.cov(male_data.T, ddof=1)
female_cov = np.cov(female_data.T, ddof=1)

print("\nMale Covariance Matrix:")
print("         Height      Weight     FootSize")
labels = ['Height  ', 'Weight  ', 'FootSize']
for i, label in enumerate(labels):
    print(f"  {label} [{male_cov[i,0]:10.4f}  {male_cov[i,1]:10.4f}  {male_cov[i,2]:10.4f}]")

print("\nFemale Covariance Matrix:")
print("         Height      Weight     FootSize")
for i, label in enumerate(labels):
    print(f"  {label} [{female_cov[i,0]:10.4f}  {female_cov[i,1]:10.4f}  {female_cov[i,2]:10.4f}]")

# Detailed covariance calculation (for hand-writing reference)
print("\n--- Detailed Covariance Calculations (Male) ---")
features = ['H', 'W', 'FS']
for i in range(3):
    for j in range(i, 3):
        terms = []
        for k in range(4):
            term = (male_data[k, i] - male_mean[i]) * (male_data[k, j] - male_mean[j])
            terms.append(term)
        total = sum(terms)
        cov_val = total / 3
        print(f"Cov({features[i]},{features[j]}) = [{' + '.join([f'{t:.4f}' for t in terms])}] / 3 = {total:.4f}/3 = {cov_val:.4f}")

print("\n--- Detailed Covariance Calculations (Female) ---")
for i in range(3):
    for j in range(i, 3):
        terms = []
        for k in range(4):
            term = (female_data[k, i] - female_mean[i]) * (female_data[k, j] - female_mean[j])
            terms.append(term)
        total = sum(terms)
        cov_val = total / 3
        print(f"Cov({features[i]},{features[j]}) = [{' + '.join([f'{t:.4f}' for t in terms])}] / 3 = {total:.4f}/3 = {cov_val:.4f}")

# Step 5: Gaussian PDF
print("\n--- Step 5: Gaussian PDF P(x|class) ---")
print(f"\nTest Person: H={test_person[0]}, W={test_person[1]}, FS={test_person[2]}")

def gaussian_pdf(x, mean, var):
    coeff = 1 / np.sqrt(2 * np.pi * var)
    exponent = -(x - mean)**2 / (2 * var)
    return coeff * np.exp(exponent), coeff, exponent

print("\nFor Male:")
p_h_m, coeff, exp_val = gaussian_pdf(test_person[0], male_mean[0], male_var[0])
print(f"  P(H=5.0|M): mu={male_mean[0]:.4f}, var={male_var[0]:.6f}")
print(f"    1/sqrt(2*pi*{male_var[0]:.4f}) = {coeff:.4f}")
print(f"    exp(-({test_person[0]}-{male_mean[0]:.4f})^2 / (2*{male_var[0]:.4f})) = exp({exp_val:.4f}) = {np.exp(exp_val):.6e}")
print(f"    P(H=5.0|M) = {p_h_m:.6e}")

p_w_m, coeff, exp_val = gaussian_pdf(test_person[1], male_mean[1], male_var[1])
print(f"  P(W=80|M): mu={male_mean[1]:.4f}, var={male_var[1]:.4f}")
print(f"    P(W=80|M) = {p_w_m:.6e}")

p_fs_m, coeff, exp_val = gaussian_pdf(test_person[2], male_mean[2], male_var[2])
print(f"  P(FS=5.0|M): mu={male_mean[2]:.4f}, var={male_var[2]:.6f}")
print(f"    P(FS=5.0|M) = {p_fs_m:.6e}")

print("\nFor Female:")
p_h_f, coeff, exp_val = gaussian_pdf(test_person[0], female_mean[0], female_var[0])
print(f"  P(H=5.0|F): mu={female_mean[0]:.4f}, var={female_var[0]:.6f}")
print(f"    P(H=5.0|F) = {p_h_f:.6e}")

p_w_f, coeff, exp_val = gaussian_pdf(test_person[1], female_mean[1], female_var[1])
print(f"  P(W=80|F): mu={female_mean[1]:.4f}, var={female_var[1]:.4f}")
print(f"    P(W=80|F) = {p_w_f:.6e}")

p_fs_f, coeff, exp_val = gaussian_pdf(test_person[2], female_mean[2], female_var[2])
print(f"  P(FS=5.0|F): mu={female_mean[2]:.4f}, var={female_var[2]:.6f}")
print(f"    P(FS=5.0|F) = {p_fs_f:.6e}")

# Step 6: Posterior (unnormalized)
print("\n--- Step 6: Posterior Probabilities ---")
posterior_m = p_male * p_h_m * p_w_m * p_fs_m
posterior_f = p_female * p_h_f * p_w_f * p_fs_f

print(f"P(M|X) ∝ P(M) × P(H|M) × P(W|M) × P(FS|M)")
print(f"       = {p_male} × {p_h_m:.4e} × {p_w_m:.4e} × {p_fs_m:.4e}")
print(f"       = {posterior_m:.4e}")

print(f"P(F|X) ∝ P(F) × P(H|F) × P(W|F) × P(FS|F)")
print(f"       = {p_female} × {p_h_f:.4e} × {p_w_f:.4e} × {p_fs_f:.4e}")
print(f"       = {posterior_f:.4e}")

# Normalized
total_post = posterior_m + posterior_f
print(f"\nNormalized:")
print(f"P(M|X) = {posterior_m/total_post:.6e}")
print(f"P(F|X) = {posterior_f/total_post:.6e}")

print(f"\n{'='*60}")
if posterior_f > posterior_m:
    print(f"CONCLUSION: Classified as FEMALE (F)")
    print(f"P(F|X) / P(M|X) = {posterior_f/posterior_m:.0f}x more likely Female")
else:
    print(f"CONCLUSION: Classified as MALE (M)")
print(f"{'='*60}")
